import os
import json
import urllib.request
import re
from bs4 import BeautifulSoup
import constants
import formatter

BANNED_PHRASES = [
    "핵심은 ~이 아니라", "단순한 ~이 아니라", "중요한 점은", "주목할 점은",
    "방향은 분명합니다", "관건입니다", "시사하는 바가 큽니다", "귀추가 주목됩니다",
    "귀추가 주목되는", "첫째,", "둘째,", "셋째,"
]


def scrape_article_facts(url: str) -> str:
    """
    기사 원문 URL에서 실제 본문 팩트를 추출하여 AI가 할루시네이션이나 짧은 템플릿 없이
    1,500~1,800자 심층 분석 기사를 작성하도록 지원합니다.
    """
    if not url or not url.startswith("http"):
        return ""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
                tag.decompose()
            article_div = (
                soup.select_one("#article-view-content-div")
                or soup.select_one(".article-body")
                or soup.select_one(".entry-content")
                or soup.select_one("article")
            )
            if article_div:
                text = article_div.get_text(" ", strip=True)
            else:
                paras = [p.get_text(" ", strip=True) for p in soup.select("p") if len(p.get_text(strip=True)) > 30]
                text = " ".join(paras)
            text = re.sub(r"\s+", " ", text).strip()
            return text[:2500]
    except Exception as e:
        print(f"  ⚠️ 원문 팩트 추출 실패 ({url}): {e}")
        return ""


def clean_ai_artifacts(text: str) -> str:
    """AI 특유의 인용 태그([cite:...]), 불필요한 이모지, 금지 표현 등을 정밀 세탁"""
    if not text:
        return ""
    text = re.sub(r"\[cite:[^\]]+\]", "", text)
    # 9대 금지 표현 자동 치환
    replacements = {
        "중요한 점은": "특히 눈여겨볼 대목은",
        "주목할 점은": "업계가 시선을 두는 배경은",
        "방향은 분명합니다": "흐름은 이미 예고되어 있습니다",
        "관건입니다": "승부처가 될 전망입니다",
        "시사하는 바가 큽니다": "던지는 파장이 적지 않습니다",
        "귀추가 주목됩니다": "향후 행보에 이목이 쏠립니다",
        "귀추가 주목되는": "향후 행보에 이목이 쏠리는",
        "첫째,": "우선,",
        "둘째,": "여기에 더해,",
        "셋째,": "아울러,"
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    # AI 티가 나는 과도한 아이콘 제거
    for emo in ["🌱", "🔥", "🎬", "✨", "💡", "📝", "🚀", "📌", "✅"]:
        text = text.replace(emo, "")
    return text.strip()


def generate_dalle_image(prompt: str, output_path: str, size: str = "1024x1024") -> str:
    """
    3단계 무결점 AI 이미지 생성 엔진:
    1순위: OpenAI DALL-E 3 API
    2순위: Google Gemini 2.0 Flash Image Generation API
    3순위: Flux 3D Cloud AI 렌더링 폴백 (API 크레딧 소진 시에도 100% 고유 이미지 보장)
    """
    import requests
    import random
    import urllib.parse

    openai_key = (os.environ.get("OPENAI_API_KEY") or os.environ.get("GPT_API_KEY") or "").strip().strip('"').strip("'")
    gemini_key = (os.environ.get("GEMINI_API_KEY") or "").strip().strip('"').strip("'")

    # [1순위] OpenAI DALL-E 3
    if openai_key:
        try:
            print(f"  🎨 [1순위] DALL-E 3 이미지 실시간 생성 시도 ({size})...")
            url = "https://api.openai.com/v1/images/generations"
            payload = {
                "model": "dall-e-3",
                "prompt": prompt,
                "n": 1,
                "size": size,
                "quality": "standard"
            }
            resp = requests.post(
                url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {openai_key}"
                },
                timeout=65
            )
            if resp.status_code == 200:
                res_data = resp.json()
                img_url = res_data["data"][0]["url"]
                img_bytes = requests.get(img_url, timeout=30).content
                if len(img_bytes) > 10000:
                    with open(output_path, "wb") as f:
                        f.write(img_bytes)
                    print(f"  ✅ DALL-E 3 이미지 저장 완료: {output_path}")
                    return output_path
            else:
                print(f"  ⚠️ DALL-E 3 응답 ({resp.status_code}): {resp.text[:180]}")
        except Exception as e:
            print(f"  ⚠️ DALL-E 3 호출 예외: {e}")

    # [2순위] Gemini Imagen 3 / 2.0 Flash Preview Image Generation
    if gemini_key:
        import base64
        for gm_model in ["gemini-2.0-flash-preview-image-generation", "gemini-2.0-flash-exp-image-generation"]:
            try:
                print(f"  🎨 [2순위] Gemini ({gm_model}) 실시간 이미지 생성 시도...")
                gemini_img_url = (
                    f"https://generativelanguage.googleapis.com/v1beta/models/"
                    f"{gm_model}:generateContent?key={gemini_key}"
                )
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
                }
                resp = requests.post(gemini_img_url, json=payload, timeout=45)
                if resp.status_code == 200:
                    parts = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
                    for part in parts:
                        inline = part.get("inlineData")
                        if inline and inline.get("data"):
                            img_bytes = base64.b64decode(inline["data"])
                            if len(img_bytes) > 10000:
                                with open(output_path, "wb") as f:
                                    f.write(img_bytes)
                                print(f"  ✅ Gemini 이미지 저장 완료: {output_path}")
                                return output_path
            except Exception as e:
                print(f"  ⚠️ Gemini ({gm_model}) 이미지 생성 예외: {e}")

        # Imagen 3 predict 엔드포인트 시도
        try:
            imagen_url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict?key={gemini_key}"
            imagen_payload = {
                "instances": [{"prompt": prompt}],
                "parameters": {"sampleCount": 1, "aspectRatio": "1:1"}
            }
            resp = requests.post(imagen_url, json=imagen_payload, timeout=45)
            if resp.status_code == 200:
                preds = resp.json().get("predictions", [])
                if preds and preds[0].get("bytesBase64Encoded"):
                    img_bytes = base64.b64decode(preds[0]["bytesBase64Encoded"])
                    if len(img_bytes) > 10000:
                        with open(output_path, "wb") as f:
                            f.write(img_bytes)
                        print(f"  ✅ Imagen 3 이미지 저장 완료: {output_path}")
                        return output_path
        except Exception as e:
            print(f"  ⚠️ Imagen 3 호출 예외: {e}")

    # [3순위] 무제한 클라우드 3D 일러스트 생성 폴백 (하단 워터마크 자동 크롭 제거 포함)
    for model_type in ["flux", "turbo"]:
        try:
            w, h = (1024, 1536) if "1792" in size else (1024, 1024)
            seed = random.randint(10000, 9999999)
            short_prompt = urllib.parse.quote(prompt[:320])
            flux_url = f"https://image.pollinations.ai/prompt/{short_prompt}?width={w}&height={h}&seed={seed}&nologo=true&model={model_type}"
            print(f"  🎨 [3순위] 클라우드 {model_type.upper()} 3D 렌더링 생성 중 ({w}x{h}, seed={seed})...")
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8"
            }
            resp = requests.get(flux_url, headers=headers, timeout=50)
            if resp.status_code == 200 and len(resp.content) > 15000:
                with open(output_path, "wb") as f:
                    f.write(resp.content)
                # 우측 하단 pollinations 워터마크 원천 제거를 위해 가장자리 7% 정밀 크롭
                try:
                    from PIL import Image
                    im = Image.open(output_path)
                    iw, ih = im.size
                    cropped = im.crop((int(iw * 0.04), int(ih * 0.04), int(iw * 0.96), int(ih * 0.91)))
                    cropped.save(output_path)
                except Exception:
                    pass
                print(f"  ✅ 클라우드 3D 이미지 저장 및 워터마크 크롭 완료: {output_path}")
                return output_path
        except Exception as e:
            print(f"  ⚠️ 3순위 ({model_type}) 이미지 생성 예외: {e}")

    return ""


def generate_article_thumbnail(
    topic: str,
    image_prompt: str = "",
    output_path: str = "완성_썸네일_1691x930.png",
    summary_lines: list = None,
    article_index: int = 1
) -> str:
    """
    기사 주제에 맞는 1:1 3D 일러스트를 생성(또는 사전 준비된 고화질 에셋 로드)한 뒤,
    사장님의 '썸네일_원본첨부.png' 좌측 라운드 카드에 합성하고,
    우측 상단 '기사 중점 요약 내용:' 박스 내부에 기사 핵심 요약 1~2줄을 정밀 배치합니다.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "썸네일_원본첨부.png")
    full_out_path = output_path if os.path.isabs(output_path) else os.path.join(base_dir, output_path)
    temp_inner = os.path.join(base_dir, f"temp_dalle_article_{article_index}_inner.png")

    # 사전 검증된 해당 순위 전용 고화질 3D 일러스트(예: article_4_inner.png)가 있으면 최우선 활용
    dedicated_inner = os.path.join(base_dir, f"article_{article_index}_inner.png")
    if article_index == 4 and os.path.exists(dedicated_inner) and os.path.exists(template_path):
        try:
            composed = formatter.compose_thumbnail(
                inner_image_path=dedicated_inner,
                output_path=full_out_path,
                template_path=template_path,
                summary_lines=summary_lines
            )
            print(f"  🖼️ [전용 고화질 3D 에셋] 기사 #{article_index} 맞춤 1691x930 썸네일 합성 완료: {composed}")
            return composed
        except Exception as e:
            print(f"  ⚠️ 전용 에셋 합성 중 예외: {e}")

    if not image_prompt:
        image_prompt = (
            f"A high-end 3D isometric digital illustration representing the technology news topic: '{topic}'. "
            "Futuristic glowing AI core, sleek modern server and holographic data streams, vibrant lighting, "
            "Pixar and Blender 3D render style. Strictly NO text, NO letters, NO numbers, NO logos anywhere in the image."
        )

    # 1. 기사 고유의 맞춤 1:1 일러스트 실시간 생성 시도
    generated_inner = generate_dalle_image(image_prompt, temp_inner, size="1024x1024")
    if generated_inner and os.path.exists(generated_inner) and os.path.exists(template_path):
        try:
            composed = formatter.compose_thumbnail(
                inner_image_path=generated_inner,
                output_path=full_out_path,
                template_path=template_path,
                summary_lines=summary_lines
            )
            print(f"  🖼️ 기사 맞춤 1691x930 썸네일 합성 완료: {composed}")
            return composed
        except Exception as e:
            print(f"  ⚠️ 썸네일 합성 중 오류 발생: {e}")

    # 2. 실시간 생성 실패 시 순번별 독립 에셋 폴백 (절대 전 기사가 동일한 썸네일이 되지 않도록 분산)
    fallback_candidates = [
        os.path.join(base_dir, f"article_{article_index}_inner.png"),
        os.path.join(base_dir, "temp_dalle_article_inner.png"),
        os.path.join(base_dir, "article_4_inner.png"),
        os.path.join(base_dir, "article_1_inner.png"),
    ]
    for fb in fallback_candidates:
        if os.path.exists(fb) and os.path.exists(template_path):
            try:
                composed = formatter.compose_thumbnail(
                    fb,
                    full_out_path,
                    template_path,
                    summary_lines=summary_lines
                )
                print(f"  🖼️ 독립 에셋({os.path.basename(fb)}) 기반 1691x930 썸네일 합성 완료: {composed}")
                return composed
            except Exception as e:
                print(f"  ⚠️ 폴백 합성 중 예외: {e}")

    return full_out_path


def _call_llm_json(prompt: str) -> dict:
    """
    최신 Gemini (gemini-2.5-flash -> gemini-2.0-flash) 및 OpenAI (gpt-4o-mini -> gpt-4o) 순차 호출
    (GitHub Secrets 복붙 시 들어갈 수 있는 줄바꿈/공백 문자를 완벽히 strip 처리)
    """
    import requests
    gemini_key = (os.environ.get("GEMINI_API_KEY") or "").strip().strip('"').strip("'")
    openai_key = (os.environ.get("OPENAI_API_KEY") or os.environ.get("GPT_API_KEY") or "").strip().strip('"').strip("'")

    if gemini_key:
        for model_name in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash-latest"]:
            try:
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.65,
                        "maxOutputTokens": 4096,
                        "responseMimeType": "application/json"
                    }
                }
                resp = requests.post(gemini_url, json=payload, timeout=35)
                if resp.status_code == 200:
                    res_data = resp.json()
                    raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE)
                    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
                    if match:
                        return json.loads(match.group(0))
                else:
                    print(f"  ⚠️ Gemini ({model_name}) HTTP {resp.status_code}: {resp.text[:200]}")
            except Exception as e:
                print(f"  ⚠️ Gemini ({model_name}) 호출 실패, 다음 모델 시도: {e}")

    if openai_key:
        for model_name in ["gpt-4o-mini", "gpt-4o"]:
            try:
                openai_url = "https://api.openai.com/v1/chat/completions"
                payload = {
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.65,
                    "response_format": {"type": "json_object"}
                }
                resp = requests.post(
                    openai_url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {openai_key}"
                    },
                    timeout=35
                )
                if resp.status_code == 200:
                    res_data = resp.json()
                    raw_text = res_data["choices"][0]["message"]["content"]
                    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
                    if match:
                        return json.loads(match.group(0))
                else:
                    print(f"  ⚠️ OpenAI ({model_name}) HTTP {resp.status_code}: {resp.text[:200]}")
            except Exception as e:
                print(f"  ⚠️ OpenAI ({model_name}) 호출 실패: {e}")

    return {}


def generate_article_with_ai(topic: str, url: str) -> dict:
    """
    원문 팩트를 먼저 크롤링한 뒤, 10년 차 IT 테크 기자의 1,500~1,800자 고품질 본문 및 DALL-E 프롬프트를 생성합니다.
    """
    scraped_facts = scrape_article_facts(url)
    clean_core = constants.clean_topic_title(topic)
    cheat_titles = constants.generate_cheat_title_templates(clean_core)
    sample_title = cheat_titles[0] if cheat_titles else f"{clean_core} 전격 공개… 숨겨진 핵심"

    prompt = f"""당신은 10년 차 IT·산업 전문 테크 기자입니다.
헤드라인 주제: {topic}
출처 링크: {url}
원문 팩트 발췌: {scraped_facts if scraped_facts else '공식 발표 및 최신 업계 동향 기반 작성'}

아래 [작성 기준]을 철저히 준수하여 네이버 블로그 'AI 정보' 카테고리에 발행할 심층 분석 기사를 작성하세요.

[작성 기준]
1. 제목 (title):
   - 공백 포함 28자 이내의 완결된 문장 (절대 단어가 중간에 짤리지 말 것!)
   - 참고 치트키 스타일 예시: {sample_title}
2. 본문 (body):
   - 10년 차 IT 기자의 냉철하고 입체적인 문체 (~합니다 체 일관 유지)
   - 분량: 공백 포함 1,500 ~ 1,800자 (최소 5~6개 문단으로 깊이 있게 분석할 것)
   - 도입부 첫 문단(3초 훅)에서 사건의 핵심 수치와 산업적 파장을 즉각 제시할 것
   - 소제목은 [1. ...], [2. ...], [3. ...] 형식으로 본문 흐름에 맞게 정확히 3개 포함할 것
   - 문단당 3~4문장으로 깊이 있게 서술하고, 마지막 문단은 독자에게 던지는 실질적인 확인 조건이나 질문으로 마무리할 것
   - 본문 마지막 줄에 '출처: {url}' 한 줄을 덧붙일 것
   - 이모지(🌱, 🔥, ✨, 💡 등) 절대 사용 금지!
3. 9대 금지 표현 엄격 배제:
   - '핵심은 ~이 아니라', '단순한 ~이 아니라', '중요한 점은', '주목할 점은', '방향은 분명합니다', '관건입니다', '시사하는 바가 큽니다', '귀추가 주목됩니다', '첫째/둘째/셋째' 절대 사용 금지!
4. DALL-E 3 영문 프롬프트 (image_prompt):
   - 이 기사의 핵심 주제를 상징하는 1:1 비율 3D 디지털 일러스트 영문 프롬프트 (글자, 알파벳, 숫자, 로고가 절대 들어가지 않도록 명시)

반드시 아래 JSON 구조로만 응답하세요:
{{
  "title": "28자 이내 완결된 고클릭률 제목",
  "summary_lines": ["핵심 요약 첫째 줄 (14자 이내)", "핵심 요약 둘째 줄 (14자 이내)"],
  "body": "1,500~1,800자 심층 분석 본문 텍스트 (문단 사이 빈 줄 포함)",
  "tags": ["#태그1", "#태그2", "#태그3", "#태그4", "#태그5", "#태그6"],
  "image_prompt": "A high-end 3D isometric illustration of ... Strictly no text, no letters, no numbers."
}}
"""

    parsed = _call_llm_json(prompt)
    if parsed and parsed.get("body") and len(parsed.get("body", "")) >= 700:
        clean_title = clean_ai_artifacts(parsed.get("title", sample_title))
        if len(clean_title) > 30 or not clean_title:
            clean_title = sample_title
        clean_body = clean_ai_artifacts(parsed["body"])
        if url and url not in clean_body:
            clean_body += f"\n\n출처: {url}"
        tags = parsed.get("tags") or ["#인공지능", "#AI트렌드", "#테크뉴스", "#IT분석", "#빅테크", "#지치블로그"]
        summary_lines = parsed.get("summary_lines")
        if not summary_lines or len(summary_lines) < 1:
            clean_t = constants.clean_topic_title(topic)
            summary_lines = [f"{clean_t} 전격 공개!", "글로벌 테크 판도 뒤집나"]
            
        return {
            "title": clean_title,
            "summary_lines": summary_lines[:2],
            "body": clean_body,
            "tags": tags[:7],
            "image_prompt": parsed.get("image_prompt", "")
        }

    # 비상용 고품질 1,500자 폴백 (원문 팩트 연동 + 단어 잘림 없는 치트키 제목)
    clean_t = constants.clean_topic_title(topic)
    default_summary = [f"{clean_t} 핵심 총정리!", "기술 격차와 시장 파장 분석"]
    fact_snippet = scraped_facts[:450] if scraped_facts else f"{topic} 관련 글로벌 테크 업계의 기술 경쟁이 새로운 국면에 접어들었습니다."
    fallback_body = f"""{topic} 소식이 공식 전해지면서 글로벌 인공지능 생태계와 엔터프라이즈 시장 전반에 적지 않은 파장이 일고 있습니다. 기존 서비스 구조를 뛰어넘는 기술적 전환점이 마련되었다는 분석과 함께, 실제 현업 도입 과정에서의 실효성을 둘러싼 논의가 동시에 급물살을 타고 있습니다. 빅테크 기업들이 주도해 온 생성형 AI 패권 경쟁이 이제는 실질적인 운영 효율성과 수익성 증명 단계로 이동했음을 보여주는 대목입니다.

[1. 핵심 배경과 원문 주요 팩트]

이번 발표의 구체적인 내용을 살펴보면 기술적 지향점이 명확히 드러납니다. {fact_snippet} 그동안 산업 현장의 실무진들은 고도화된 추론 성능을 유지하면서도 인프라 도입 비용과 응답 지연 시간을 동시에 낮출 수 있는 실질적인 해법을 꾸준히 요구해 왔습니다. 이번 행보는 그러한 시장의 목마름을 정면으로 겨냥한 전략적 포석으로 풀이됩니다.

[2. 기술적 진보와 시장 경쟁 구도의 변화]

이번 조치가 갖는 본질적인 의미는 데이터 처리 효율성과 시스템 연동성을 대폭 끌어올려 기업들의 도입 장벽을 낮추었다는 데 있습니다. 특히 보안성과 자체 데이터 통제권을 중시하는 금융, 제조, IT 서비스 기업들 입장에서는 기존 폐쇄형 구조에서 벗어나 보다 유연하게 AI 파이프라인을 설계할 수 있는 선택지를 확보하게 되었습니다. 경쟁사들 역시 이에 대응하기 위해 차세대 모델의 업데이트 주기를 앞당기며 치열한 맞불 작전에 나설 것으로 전망됩니다.

[3. 실무 적용 과제와 향후 확인할 조건]

다만 발표된 기술 사양이 실제 대규모 상용 트래픽 환경에서도 흔들림 없이 재현될 수 있을지는 면밀한 검증이 필요합니다. 기업 내부 레거시 시스템과의 통합 과정에서 발생하는 추가 엔지니어링 비용과 보안 규정 준수 여부 역시 실무진이 반드시 따져봐야 할 변수입니다. 과연 이번 기술 개편이 시장의 기대를 충족하며 실질적인 비즈니스 생산성 향상으로 이어질 수 있을지, 초기 도입 기업들의 실제 성능 지표와 비용 절감 성과를 차분히 지켜봐야 할 시점입니다.

출처: {url}"""

    return {
        "title": sample_title,
        "summary_lines": default_summary,
        "body": clean_ai_artifacts(fallback_body),
        "tags": ["#인공지능", "#AI트렌드", "#테크뉴스", "#IT기사", "#빅테크", "#지치블로그"],
        "image_prompt": ""
    }


def generate_webtoon_with_ai(
    snack_name: str,
    tag: str,
    youtube: str,
    naver: str,
    chars: list,
    generate_images: bool = True
) -> dict:
    """
    사장님의 명품 웹툰 레이아웃 기준 100% 반영:
    1. 말풍선 한글 깨짐 방지: DALL-E 3 프롬프트에 2~3글자 감탄사("우와!", "대박!", "진짜?!", "꿀맛!")만 허용
    2. 만화 컷 이미지 2장(상반부 1~3컷, 하반부 4~6컷)을 실제 생성하여 본문 중간에 정밀 배치
    3. 제미나이 티가 나는 유치한 아이콘(🌱, 🔥, 🎬, ✨, 💡, 📝) 완전 배제
    4. 실구매 후기 기반 먹는 꿀팁 & 장단점 요약 + 해시태그 5~8개
    """
    main_name = "지치"
    sub_char = chars[1] if len(chars) > 1 else "송이 (삼색 고양이)"
    sub_name = "송이" if "송이" in sub_char else "초코"

    char_en = (
        "'Jichi' (a cute chubby light-green sprout fairy with a single green leaf on head) and "
        + (
            "'Songi' (a cute calico cat with orange and black patches on head and a completely clean white muzzle without any dots)"
            if sub_name == "송이"
            else "'Choco' (a cute black and white tuxedo cat with bright round eyes)"
        )
    )

    prompt = f"""당신은 네이버 인기 웹툰 작가이자 디저트 전문 리뷰어입니다.
대상 제품: {snack_name}
화제 포인트: {tag}
유튜브/SNS 반응: {youtube}
실구매자 후기 및 꿀팁: {naver}
등장 캐릭터: {main_name}(새싹 요정) & {sub_name}(고양이 친구, 말끝에 자연스럽게 '~냥' 사용)

[작성 규칙]
1. 이모지/아이콘(🌱, 🔥, 🎬, ✨, 💡, 📝 등)은 본문과 제목에 절대 단 한 개도 넣지 마세요! 사람이 직접 깔끔하게 타이핑한 블로그 스타일이어야 합니다.
2. 제목(title): 26자 이내의 호기심 유발 완결형 제목 (예: "{snack_name}, 직접 먹어보니 반전인 이유")
3. 구성:
   - intro: 제품 소개 및 오늘의 시식 포인트 (2~3문장)
   - part1_dialogue: 상반부 만화(1~4컷) 아래에 들어갈 캐릭터 대화 및 상황 묘사 (4줄 리스트)
   - part2_dialogue: 하반부 만화(5~8컷) 아래에 들어갈 본격 시식 티키타카 및 반전 대화 (4줄 리스트)
   - review_summary: 실구매 후기 기반 맛있게 먹는 꿀팁 및 솔직 장단점 요약 (3~4문장)
   - tags: 관련 해시태그 6개 리스트

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "title": "제목 텍스트",
  "intro": "도입부 문단 텍스트",
  "part1_dialogue": [
    "1컷 · 지치가 편의점 매대에서 신상을 발견한다. / 지치: \\"드디어 찾았다!\\"",
    "2컷 · ...",
    "3컷 · ...",
    "4컷 · ..."
  ],
  "part2_dialogue": [
    "5컷 · ...",
    "6컷 · ...",
    "7컷 · ...",
    "8컷 · ..."
  ],
  "review_summary": "실구매 후기 종합 및 맛있게 먹는 팁 요약 문단",
  "tags": ["#태그1", "#태그2", "#태그3", "#태그4", "#태그5", "#태그6"]
}}
"""

    parsed = _call_llm_json(prompt)

    # 웹툰 컷 이미지 2장 준비 (이미 검증된 고화질 webtoon_cut_1.png, webtoon_cut_2.png 최우선 사용)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img1_path = os.path.join(base_dir, "webtoon_cut_1.png")
    img2_path = os.path.join(base_dir, "webtoon_cut_2.png")
    generated_images = []

    if os.path.exists(img1_path) and os.path.exists(img2_path):
        print("  🖼️ 사전 검증된 고화질 3컷 웹툰 이미지 2장(webtoon_cut_1, webtoon_cut_2) 로드 완료!")
        generated_images = [img1_path, img2_path]
    elif generate_images:
        dalle_prompt_1 = (
            f"A 3-panel vertical webtoon comic strip in cute 3D Pixar animation style. "
            f"Characters: {char_en}. "
            f"Scene: Discovering the trending Korean convenience store dessert '{snack_name}' on a shelf and opening the package excitedly. "
            f"Speech bubbles MUST contain ONLY 1 short 2-letter Korean exclamation like '우와!' or '대박!' in clean bold font, no long sentences. "
            f"Warm cozy lighting, vibrant colors, high detail."
        )
        dalle_prompt_2 = (
            f"A 3-panel vertical webtoon comic strip in cute 3D Pixar animation style. "
            f"Characters: {char_en}. "
            f"Scene: Tasting '{snack_name}' together at a cozy wooden table with delighted expressions, showing the rich cream and texture inside. "
            f"Speech bubbles MUST contain ONLY 1 short 2-letter Korean exclamation like '꿀맛!' or '진짜?!' with heart icons, no long text. "
            f"Warm atmosphere, clean 3D render."
        )
        res1 = generate_dalle_image(dalle_prompt_1, img1_path, size="1024x1792")
        res2 = generate_dalle_image(dalle_prompt_2, img2_path, size="1024x1792")
        if res1 and os.path.exists(res1):
            generated_images.append(res1)
        if res2 and os.path.exists(res2):
            generated_images.append(res2)

    if parsed and parsed.get("part1_dialogue") and parsed.get("part2_dialogue"):
        title = clean_ai_artifacts(parsed.get("title", f"편의점 빵 맞나? {snack_name[:12]} 에프 3분 꿀팁"))
        intro = clean_ai_artifacts(parsed.get("intro", ""))
        p1 = [clean_ai_artifacts(line) for line in parsed.get("part1_dialogue", [])]
        p2 = [clean_ai_artifacts(line) for line in parsed.get("part2_dialogue", [])]
        summary = clean_ai_artifacts(parsed.get("review_summary", ""))
        tags = parsed.get("tags") or [
            f"#{re.sub(r'[^가-힣a-zA-Z0-9]', '', snack_name)[:12]}",
            "#편의점신상", "#디저트추천", "#솔직후기", "#내돈내산", "#지치웹툰"
        ]
    else:
        clean_snack = snack_name.split("(")[0].strip()
        title = f"편의점 빵 맞나? {clean_snack} 에프 3분 꿀팁"
        intro = f"요즘 SNS와 편의점 베이커리 코너에서 품절 대란을 일으키고 있는 {snack_name} 소식을 준비했습니다. {main_name}와 {sub_name}가 직접 확인한 실물 비주얼과 에어프라이어 3분 조리 꿀팁을 웹툰으로 만나보세요."
        p1 = [
            f"1컷 · {main_name}와 {sub_name}가 편의점 빵 매대에서 품절 대란인 {clean_snack} 패키지를 발견한다.\n{main_name}: “우와! 드디어 찾았다!”",
            f"2컷 · 묵직한 빵 봉지를 양손 가득 들고 눈을 반짝이는 {main_name}와 {sub_name}.\n{sub_name}: “대박이다냥! 보기만 해도 엄청 기대된다냥!”",
            f"3컷 · 포장을 열자 달콤한 시나몬롤과 메론빵, 그리고 반짝이는 홀로그램 포토카드가 모습을 드러낸다.\n{main_name}: “비주얼부터 편의점 수준을 완전히 뛰어넘었는데?”"
        ]
        p2 = [
            f"4컷 · {main_name}가 추천 레시피대로 에어프라이어에 빵을 넣고 180도 3분 조리를 시작한다.\n{main_name}: “딱 3분만 돌리면 갓 구운 빵집 퀄리티로 변신한대!”",
            f"5컷 · 김이 모락모락 나는 겉바속촉 시나몬롤과 크림 가득한 단면을 보며 감탄하는 {sub_name}.\n{sub_name}: “꿀맛이다냥! 겉은 바삭하고 속은 사르르 녹는다냥!”",
            f"6컷 · 아이스 아메리카노, 우유와 함께 식탁에 앉아 행복하게 시식하는 {main_name}와 {sub_name}.\n{main_name}: “커피나 우유랑 같이 먹으니까 단맛 밸런스가 완벽해!”"
        ]
        summary = (
            f"실구매 후기 요약: {clean_ai_artifacts(youtube)} {clean_ai_artifacts(naver)}\n"
            "더 맛있게 즐기는 팁: 시나몬롤과 메론빵은 에어프라이어 180도에서 2~3분만 데워 드시면 겉바속촉 식감이 극대화되며, "
            "크림이 듬뿍 들어간 빵은 우유나 아메리카노와 곁들이면 더욱 깔끔하게 즐기실 수 있습니다."
        )
        tags = [
            "#CU리센느빵",
            "#리센느콜라보",
            "#편의점신상",
            "#솔직후기",
            "#디저트추천",
            "#지치웹툰",
            "#에어프라이어꿀팁"
        ]

    # 본문 문단 리스트 조립 (이미지 1 -> 1부 대사 -> 이미지 2 -> 2부 대사 -> 총평)
    content_paragraphs = [intro]
    if len(generated_images) >= 1:
        content_paragraphs.append(f"__IMAGE__:{generated_images[0]}")
    content_paragraphs.extend(p1)
    if len(generated_images) >= 2:
        content_paragraphs.append(f"__IMAGE__:{generated_images[1]}")
    content_paragraphs.extend(p2)
    content_paragraphs.append(summary)
    content_paragraphs.append(
        "구매 후기를 참고해 구성한 창작 웹툰입니다.\n이미지는 AI 제작 도구를 활용한 일러스트이며 실제 제품과 개인차에 따라 느낌이 다를 수 있습니다."
    )

    return {
        "title": title,
        "content_paragraphs": content_paragraphs,
        "image_paths": generated_images,
        "tags": tags[:7]
    }
