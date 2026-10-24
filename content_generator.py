import os
import sys
import json
import urllib.request
import re
from bs4 import BeautifulSoup
import constants
import formatter

# Windows 콘솔 인코딩 안전화
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BANNED_PHRASES = [
    "직접 써보니", "충격 반전", "진짜 충격",
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
    """AI 특유의 인용 태그([cite:...]), 불필요한 이모지, 과장된 느낌표(!), 금지 표현 등을 정밀 세탁"""
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
    
    # [대표님 엄격 지시] 제미니 티가 나는 모든 이모지/아이콘 영구 완전 박멸
    for emo in ["🌱", "🔥", "🎬", "✨", "💡", "📝", "🚀", "📌", "✅", "☕", "🥐", "🍰", "🍭", "🎵", "❤️", "❗", "‼️"]:
        text = text.replace(emo, "")
    
    # 소제목([ ... ]) 내부의 AI 특유의 촌스러운 느낌표(!) 자동 제거: 예: [팩트 체크!] -> [팩트 체크]
    text = re.sub(r'\[([^\]]*?)!+([^\]]*?)\]', r'[\1\2]', text)
    
    return text.strip()


def load_character_memory() -> dict:
    """블로그 공식 캐릭터 소개글 기반 영구 캐릭터 메모리(character_memory.json) 로드"""
    mem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "characters", "character_memory.json")
    if os.path.exists(mem_path):
        try:
            with open(mem_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"  ⚠️ 캐릭터 메모리 로드 경고: {e}")
    return {}


def generate_dalle_image(prompt: str, output_path: str, size: str = "1024x1024", reference_images: list = None) -> str:
    """
    [지치 컴퍼니 엄격 규정] 100% OpenAI DALL-E 3 단독 잠금(Lock) 이미지 생성 엔진
    - 사장님 특별 지시: Gemini 및 타 엔진 절대 개입 금지 (가로채기/새치기 영구 박멸)
    - OpenAI DALL-E 3 실시간 호출 실패 시 즉시 빈 문자열("")을 반환하여 코리티(QA)가 발행을 즉시 중지할 수 있도록 보장
    """
    import requests

    openai_key = (os.environ.get("OPENAI_API_KEY") or os.environ.get("GPT_API_KEY") or "").strip().strip('"').strip("'")

    if not openai_key:
        print("  🚨 [코리티 보안 경고] OPENAI_API_KEY / GPT_API_KEY 환경변수가 누락되었습니다!")
        print("  🛑 [발행 중지 프로토콜] 제미니 등 타사 엔진 우회는 엄격히 차단되며, 즉시 생성을 중단합니다.")
        return ""

    # 캐릭터 메모리에서 공식 시각 DNA 및 송이 얼굴 무점(NO dots on face) 절대 제약조건 자동 보강
    char_mem = load_character_memory()
    if char_mem and ("Jichi" in prompt or "지치" in prompt or "Songi" in prompt or "송이" in prompt):
        jichi_dna = char_mem.get("characters", {}).get("jichi", {}).get("visual_dna", "")
        songi_dna = char_mem.get("characters", {}).get("songi", {}).get("visual_dna", "")
        dna_suffix = (
            f"\n[OFFICIAL CHARACTER MEMORY LOCK]\n"
            f"- Jichi: {jichi_dna}\n"
            f"- Songi: {songi_dna}\n"
            f"- HARD CONSTRAINT FOR SONGI: Never draw any dots, moles, spots, or beauty marks anywhere on or around Songi's white face, nose, cheeks, mouth, or forehead."
        )
        if "[OFFICIAL CHARACTER MEMORY LOCK]" not in prompt:
            prompt = prompt + dna_suffix

    # [OpenAI DALL-E 3 단독 호출]
    try:
        print(f"  🎨 [코자이너] OpenAI DALL-E 3 고화질 렌더링 호출 중... ({size})")
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
            timeout=70
        )
        if resp.status_code == 200:
            res_data = resp.json()
            img_url = res_data["data"][0]["url"]
            img_bytes = requests.get(img_url, timeout=35).content
            if len(img_bytes) > 10000:
                with open(output_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  ✅ [ENGINE VERIFIED: OpenAI DALL-E 3] 이미지 저장 완료: {output_path}")
                return output_path
            else:
                print(f"  ⚠️ DALL-E 3 응답 이미지 바이트 부족 ({len(img_bytes)} bytes)")
        else:
            print(f"  ⚠️ DALL-E 3 API 응답 실패 ({resp.status_code}): {resp.text[:200]}")
    except Exception as e:
        print(f"  ⚠️ DALL-E 3 호출 중 예외 발생: {e}")

    # 사장님 엄명: DALL-E 3 실패 시 타사 엔진(Gemini, Imagen, Flux 등)으로 임의 폴백하지 않고 즉시 실패 반환
    print("  🚨 [코자이너 & 코리티] OpenAI DALL-E 3 생성 실패! 타 엔진 개입을 차단하고 생성을 중단합니다.")
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

    # 주제별 맞춤 프롬프트 테마 다양화 (고정된 큐브/서버룸 탈피)
    if not image_prompt:
        clean_kw = constants.clean_topic_title(topic)
        themes = [
            f"A vibrant high-end 3D digital illustration of a futuristic robotic hand interacting with floating luminous neural network elements representing '{clean_kw}'. Clean pastel studio lighting, Blender 3D render style.",
            f"A modern 3D conceptual workspace with floating holographic charts, dynamic digital data streams, and glowing creative light beams representing '{clean_kw}'. Warm ambient lighting, Pixar style.",
            f"An elegant 3D futuristic tech monument and dynamic glowing energy waves symbolizing cutting-edge innovation for '{clean_kw}'. Cinematic soft lighting, minimal clean background.",
            f"A high-tech 3D laboratory scene with sleek transparent glass interfaces, floating crystal data nodes, and vibrant ambient colors representing '{clean_kw}'. Depth of field, Blender 3D style."
        ]
        chosen_theme = themes[article_index % len(themes)]
        image_prompt = (
            f"{chosen_theme} Strictly NO text, NO letters, NO numbers, NO watermarks, NO logos anywhere in the image."
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
    sample_title = cheat_titles[0] if cheat_titles else f"{clean_core} 전격 공개! 핵심 분석"

    prompt = f"""당신은 10년 차 IT·산업 전문 테크 기자입니다.
헤드라인 주제: {topic}
핵심 키워드: {clean_core}
출처 링크: {url}
원문 팩트 발췌: {scraped_facts if scraped_facts else '공식 발표 및 최신 업계 동향 기반 작성'}

아래 [작성 기준]을 철저히 준수하여 네이버 블로그 'AI 정보' 카테고리에 발행할 심층 분석 기사를 작성하세요.

[작성 기준]
1. 제목 (title):
   - 공백 포함 22~28자 이내의 완결되고 세련된 한국어 문장 (절대 단어가 중간에 짤리지 말 것!)
   - ⚠️ 절대 금지: '직접 써보니', '충격 반전' 같은 낚시성 문구는 실제 체험한 내용이 아니므로 절대 쓰지 말 것!
   - 기술 기사의 본질에 맞게 '공식 발표', '핵심 기술 분석', '글로벌 테크 판도', '실무 체크포인트' 등 신뢰도 높은 전문 어휘를 사용할 것
   - 참고 가능한 제목 스타일 후보(그대로 베끼지 말고 기사 팩트에 맞게 응용):
     * {cheat_titles[0]}
     * {cheat_titles[1] if len(cheat_titles) > 1 else clean_core + ' 공식 발표! 기술 분석'}
     * {cheat_titles[2] if len(cheat_titles) > 2 else clean_core + ' 테크 업계가 주목하는 이유'}
2. 본문 (body):
   - 10년 차 IT 기자의 냉철하고 입체적인 문체 (~합니다 체 일관 유지)
   - 분량: 공백 포함 1,500 ~ 1,800자 (최소 5~6개 문단으로 깊이 있게 분석할 것)
   - 도입부 첫 문단(3초 훅)에서 사건의 핵심 수치와 산업적 파장을 즉각 제시할 것
   - [공식 자료 기반 설명]과 [실제 직접 경험/후기] 명확히 구분:
     * 본문 상단 소제목에 반드시 "[공식 보도자료 및 기술 문서 기반 분석]"임을 명시하여 신뢰도를 극대화할 것!
   - 소제목은 [1. 공식 발표 핵심 사양과 배경], [2. 기술적 진보와 시장 경쟁 구도], [3. 실무 도입 시 한계와 관전 포인트] 형식으로 본문 흐름에 맞게 정확히 3개 포함할 것
   - [가독성 강조 서식]: 각 문단에서 가장 중요한 핵심 결론, 핵심 수치, 또는 충격적인 팩트 1~2개 어절을 반드시 **굵은 글씨** 마크다운(**볼드**)으로 감싸서 강조할 것!
   - 문단당 3~4문장으로 깊이 있게 서술할 것
   - [필수 요건: 기자의 구체적 심층 분석 1~2줄 추가]:
     * 본문 마무리 직전에 '💡 [지치 블로그 테크 전문 분석]' 섹션을 두고, 단순 요약이 아닌 업계에 미칠 파장이나 실무자가 취해야 할 전략에 대한 1~2줄의 날카롭고 구체적인 자체 분석 의견을 반드시 작성할 것!
   - 본문 마지막 줄에 '공식 출처: {url}' 한 줄을 덧붙일 것
   - 이모지(🌱, 🔥, ✨, 💡 등 본문 내용 중 남발) 절대 사용 금지!
3. 12대 금지 표현 엄격 배제:
   - '직접 써보니', '충격 반전', '진짜 충격' 절대 사용 금지!
   - '핵심은 ~이 아니라', '단순한 ~이 아니라', '중요한 점은', '주목할 점은', '방향은 분명합니다', '관건입니다', '시사하는 바가 큽니다', '귀추가 주목됩니다', '첫째/둘째/셋째' 절대 사용 금지!
4. 섬네일 요약 카피 (summary_lines):
   - 첫째 줄: 기사의 핵심 팩트 1줄 (12자 이내, 예: "앤트그룹 AI 8종 공개" 또는 "메타 주가 7% 급락")
   - 둘째 줄: 향후 파장이나 관전 포인트 1줄 (13자 이내, 예: "빅테크 판도 흔드나" 또는 "현금 적자 리스크 비상")
   - 절대 '핵심 총정리!', '기술 격차와 시장 파장 분석' 같은 판에 박힌 멘트 금지!
5. 3D 일러스트 프롬프트 (image_prompt):
   - 기사 내용에 어울리는 구체적인 3D 콘셉트 영문 프롬프트 (단순한 파란색 큐브 형태 절대 금지, 다채로운 조명과 오브젝트 활용)
   - Strictly no text, no letters, no numbers, no logos.

반드시 아래 JSON 구조로만 응답하세요:
{{
  "title": "22~28자 완결된 기사 맞춤형 고클릭률 제목",
  "summary_lines": ["기사 핵심 팩트 (12자 이내)", "산업 파장/전망 (13자 이내)"],
  "body": "1,500~1,800자 심층 분석 본문 텍스트 (문단 사이 빈 줄 포함)",
  "tags": ["#태그1", "#태그2", "#태그3", "#태그4", "#태그5", "#태그6"],
  "image_prompt": "A modern 3D illustration of ... Strictly no text, no letters, no numbers."
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
        
        # 공감 & 이웃추가 전환율 극대화 CTA 마무리 문구 추가
        cta_text = "\n\n오늘 분석이 도움 되셨다면 공감(❤️)과 이웃 추가 부탁드립니다! 지치 블로그가 매일 아침 가장 빠르고 정확한 글로벌 테크 트렌드를 배달해 드립니다."
        if "공감(❤️)" not in clean_body:
            clean_body += cta_text

        tags = parsed.get("tags") or ["#인공지능", "#AI트렌드", "#테크뉴스", "#IT분석", "#빅테크", "#지치블로그"]
        summary_lines = parsed.get("summary_lines")
        if not summary_lines or len(summary_lines) < 2 or "시장 파장 분석" in "".join(summary_lines):
            clean_t = constants.clean_topic_title(topic)
            summary_lines = [f"{clean_t} 전격 공개!", "글로벌 테크 판도 뒤집나"]
            
        return {
            "title": clean_title,
            "summary_lines": summary_lines[:2],
            "body": clean_body,
            "tags": tags[:7],
            "image_prompt": parsed.get("image_prompt", "")
        }

    # 비상용 고품질 1,500자 폴백 (원문 팩트 연동 + 단어 잘림 없는 전문 제목)
    clean_t = constants.clean_topic_title(topic)
    fallback_title = cheat_titles[0] if cheat_titles else f"{clean_t} 공식 발표! 핵심 기술 분석"
    default_summary = [f"{clean_t} 공식 발표", "글로벌 테크 판도 변화"]
    fact_snippet = scraped_facts[:450] if scraped_facts else f"{topic} 관련 글로벌 테크 기업의 공식 기술 문서 및 보도자료를 기반으로 분석한 최신 동향입니다."
    fallback_body = f"""{topic} 소식이 공식 전해지면서 글로벌 인공지능 생태계와 엔터프라이즈 시장 전반에 적지 않은 파장이 일고 있습니다. 기존 서비스 구조를 뛰어넘는 기술적 전환점이 마련되었다는 분석과 함께, 실제 현업 도입 과정에서의 실효성을 둘러싼 논의가 동시에 급물살을 타고 있습니다. 빅테크 기업들이 주도해 온 생성형 AI 패권 경쟁이 이제는 실질적인 운영 효율성과 수익성 증명 단계로 이동했음을 보여주는 대목입니다.

[1. 공식 발표 핵심 사양과 배경]

이번 발표의 구체적인 내용을 살펴보면 기술적 지향점이 명확히 드러납니다. (※ 본 내용은 공식 보도자료 및 기술 백서 기반의 자료 분석입니다.) {fact_snippet} 그동안 산업 현장의 실무진들은 고도화된 추론 성능을 유지하면서도 인프라 도입 비용과 응답 지연 시간을 동시에 낮출 수 있는 실질적인 해법을 꾸준히 요구해 왔습니다. 이번 행보는 그러한 시장의 목마름을 정면으로 겨냥한 전략적 포석으로 풀이됩니다.

[2. 기술적 진보와 시장 경쟁 구도]

이번 조치가 갖는 본질적인 의미는 데이터 처리 효율성과 시스템 연동성을 대폭 끌어올려 기업들의 도입 장벽을 낮추었다는 데 있습니다. 특히 보안성과 자체 데이터 통제권을 중시하는 금융, 제조, IT 서비스 기업들 입장에서는 기존 폐쇄형 구조에서 벗어나 보다 유연하게 AI 파이프라인을 설계할 수 있는 선택지를 확보하게 되었습니다. 경쟁사들 역시 이에 대응하기 위해 차세대 모델의 업데이트 주기를 앞당기며 치열한 맞불 작전에 나설 것으로 전망됩니다.

[3. 실무 도입 시 한계와 관전 포인트]

다만 발표된 기술 사양이 실제 대규모 상용 트래픽 환경에서도 흔들림 없이 재현될 수 있을지는 면밀한 검증이 필요합니다. 기업 내부 레거시 시스템과의 통합 과정에서 발생하는 추가 엔지니어링 비용과 보안 규정 준수 여부 역시 실무진이 반드시 따져봐야 할 변수입니다. 과연 이번 기술 개편이 시장의 기대를 충족하며 실질적인 비즈니스 생산성 향상으로 이어질 수 있을지, 초기 도입 기업들의 실제 성능 지표와 비용 절감 성과를 차분히 지켜봐야 할 시점입니다.

[지치 블로그 테크 전문 분석]
단순 사양 경쟁을 넘어 '실제 현업 인프라 비용 대비 실효성'을 확보했는지가 이번 기술의 최대 승부처입니다. 실무진은 벤치마크 점수에만 의존하지 말고 소규모 PoC(개념 검증)를 거쳐 자사 워크플로우에 최적화하는 전략이 요구됩니다.

공식 출처: {url}"""

    return {
        "title": fallback_title,
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
