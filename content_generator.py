import os
import sys
import json
import urllib.request
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

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
    [지치 컴퍼니 표준] Google Gemini Image 생성 기본 엔진 (사장님 특명 반영)
    - 불안정한 GPT/DALL-E 대신 Google Gemini Image를 기본 엔진으로 채택합니다.
    - 실패 시 순번별 고유 독립 3D 에셋(article_1~3_inner.png)으로 안전 매핑됩니다.
    """
    import requests
    import json
    import base64

    gemini_key = (os.environ.get("GEMINI_API_KEY") or "").strip().strip('"').strip("'")
    if not gemini_key:
        print("  ⚠️ GEMINI_API_KEY 미설정: 로컬 전용 3D 에셋으로 자동 연결합니다.")
        return ""

    # 캐릭터 메모리에서 공식 시각 DNA 및 송이 얼굴 무점 절대 제약조건 자동 보강
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

    # [1단계: Google Gemini Image 모델 순차 호출]
    image_models = [
        "gemini-2.5-flash-image",
        "gemini-3.1-flash-image",
        "gemini-3.1-flash-lite-image",
        "gemini-3-pro-image"
    ]

    for model_name in image_models:
        try:
            print(f"  🎨 [코자이너] Google Gemini Image ({model_name}) 렌더링 호출 중...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
            }
            resp = requests.post(url, json=payload, timeout=40)
            if resp.status_code == 200:
                data = resp.json()
                for cand in data.get("candidates", []):
                    for part in cand.get("content", {}).get("parts", []):
                        inline = part.get("inlineData")
                        if inline and inline.get("data"):
                            img_bytes = base64.b64decode(inline["data"])
                            if len(img_bytes) > 5000:
                                with open(output_path, "wb") as f:
                                    f.write(img_bytes)
                                print(f"  ✅ [ENGINE VERIFIED: Google Gemini Image] 이미지 저장 완료: {output_path}")
                                return output_path
            else:
                print(f"  ⚠️ Gemini ({model_name}) 응답: HTTP {resp.status_code}")
        except Exception as e:
            print(f"  ⚠️ Gemini ({model_name}) 예외 발생: {e}")

    print("  🚨 [코자이너] Gemini Image 실시간 쿼터 초과 또는 응답 지연 -> 순번별 고유 독립 에셋으로 자동 분기")
    return ""


# [지치 컴퍼니 표준 별칭] 제미나이 이미지 생성 엔진 기본 연결
generate_gemini_image = generate_dalle_image


def generate_article_thumbnail(
    topic: str,
    image_prompt: str = "",
    output_path: str = "완성_썸네일_1691x930.png",
    summary_lines: list = None,
    article_index: int = 1
) -> str:
    """
    기사 주제에 맞는 1:1 3D 일러스트를 Google Gemini Image 기본 엔진으로 생성한 뒤,
    사장님의 '썸네일_원본첨부.png' 좌측 라운드 카드에 합성하고,
    우측 상단 '기사 중점 요약 내용:' 박스 내부에 기사 핵심 요약 1~2줄을 정밀 배치합니다.
    (만약 Gemini 호출 지연/할당량 초과 시 기사 번호별 전용 고화질 3D 에셋으로 1:1 자동 분기)
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "썸네일_원본첨부.png")
    full_out_path = output_path if os.path.isabs(output_path) else os.path.join(base_dir, output_path)
    temp_inner = os.path.join(base_dir, f"temp_gemini_article_{article_index}_inner.png")

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

    # 1. Google Gemini Image 기본 엔진 실시간 생성 시도 (사장님 특명)
    print(f"  🎨 [기사 #{article_index} 기본 엔진] Google Gemini Image 맞춤 일러스트 생성 시도...")
    generated_inner = generate_dalle_image(image_prompt, temp_inner, size="1024x1024")
    if generated_inner and os.path.exists(generated_inner) and os.path.exists(template_path):
        try:
            composed = formatter.compose_thumbnail(
                inner_image_path=generated_inner,
                output_path=full_out_path,
                template_path=template_path,
                summary_lines=summary_lines
            )
            print(f"  🖼️ [Google Gemini Image 생성 성공] 기사 #{article_index} 맞춤 1691x930 썸네일 합성 완료: {composed}")
            return composed
        except Exception as e:
            print(f"  ⚠️ 썸네일 합성 중 오류 발생: {e}")

    # 2. 실시간 생성 미응답/할당량 초과 시: 워터마크나 중복 에셋(파란 소용돌이/지구본) 대신
    #    기사 주제 해시 기반 다이내믹 3D 글래스모피즘 일러스트를 실시간 생성하여 100% 고유 이미지 보장!
    print(f"  🔄 [안전 보장] Gemini 실시간 미응답 -> 기사 #{article_index} 맞춤형 다이내믹 3D 테크 일러스트 즉시 생성")
    try:
        dyn_inner = formatter.generate_dynamic_tech_illustration(topic, temp_inner, article_index=article_index)
        if dyn_inner and os.path.exists(dyn_inner) and os.path.exists(template_path):
            composed = formatter.compose_thumbnail(
                inner_image_path=dyn_inner,
                output_path=full_out_path,
                template_path=template_path,
                summary_lines=summary_lines
            )
            print(f"  🖼️ [다이내믹 3D 테크 아트워크] 중복 없는 1691x930 썸네일 합성 완료: {composed}")
            return composed
    except Exception as dyn_err:
        print(f"  ⚠️ 다이내믹 일러스트 합성 중 예외: {dyn_err}")

    dedicated_inner = os.path.join(base_dir, f"article_{article_index}_inner.png")
    fallback_candidates = [
        os.path.join(base_dir, "article_4_inner.png"),
        dedicated_inner,
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
                print(f"  🖼️ [폴백 에셋({os.path.basename(fb)})] 1691x930 썸네일 합성 완료: {composed}")
                return composed
            except Exception as e:
                print(f"  ⚠️ 폴백 합성 중 예외: {e}")

    return full_out_path


def _call_llm_json(prompt: str) -> dict:
    """
    최신 Gemini 3.8 Flash High 우선 호출 (gemini-3.8-flash -> gemini-3.7-flash -> gemini-3.5-flash -> gemini-2.5-flash)
    및 OpenAI (gpt-4o-mini -> gpt-4o) 순차 호출
    """
    import requests
    gemini_key = (os.environ.get("GEMINI_API_KEY") or "").strip().strip('"').strip("'")
    openai_key = (os.environ.get("OPENAI_API_KEY") or os.environ.get("GPT_API_KEY") or "").strip().strip('"').strip("'")

    if gemini_key:
        for model_name in ["gemini-3.6-flash", "gemini-3-flash-preview", "gemini-3.1-flash-lite", "gemini-3.8-flash"]:
            try:
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.65,
                        "maxOutputTokens": 8192,
                        "responseMimeType": "application/json"
                    }
                }
                resp = requests.post(gemini_url, json=payload, timeout=45)
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


def generate_article_with_ai(topic: str, url: str, article_index: int = 1) -> dict:
    """
    [ACE ETF급 매거진 에디토리얼 AI 기사 생성 엔진 (6대 대수술 완결판)]
    1. 상단 2줄 형광펜 훅 카피([HOOK]) + [핵심 3줄 요약] 박스([SUMMARY_BOX]) 전진 배치
    2. 판박이 소제목 폐지 -> 기사 맞춤형 버티컬 바 소제목 3종([SUB]▎ ...[/SUB])
    3. 본문 중간 고해상도 인포그래픽 비교표 카드(__IMAGE__:infographic_card.png) 자동 렌더링 및 삽입
    4. 섹션 전환부 독자 질문형 따옴표 인용구([QUOTE]“ ... ”[/QUOTE]) 배치
    5. 파스텔 형광펜 음영([HL_SKY], [HL_YELLOW]) 및 네이비 블루([BLUE]) 핵심 문장 하이라이팅
    6. 수미상관 엔딩 슬로건 및 다이어트된 연관 분석 링크 1건 연결
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scraped_facts = scrape_article_facts(url)
    clean_core = constants.clean_topic_title(topic)
    cheat_titles = constants.generate_cheat_title_templates(clean_core)
    sample_title = cheat_titles[0] if cheat_titles else f"{clean_core} 전격 공개! 핵심 분석"

    prompt = f"""당신은 10년 차 IT·산업 전문 테크 에디터이자 리서치 애널리스트입니다.
헤드라인 주제: {topic}
핵심 키워드: {clean_core}
출처 링크: {url}
원문 팩트 발췌: {scraped_facts if scraped_facts else '공식 발표 및 최신 업계 동향 기반 작성'}

아래 [매거진 에디토리얼 작성 기준]을 철저히 준수하여 네이버 블로그 'AI 정보' 카테고리에 발행할 최고급 매거진형 심층 분석 기사를 JSON으로 작성하세요.

[매거진 에디토리얼 작성 기준]
1. 제목 (title):
   - 공백 포함 22~28자 이내의 완결되고 세련된 한국어 문장 (단어 중간 잘림 절대 금지)
   - 금지어: '직접 써보니', '충격 반전', '진짜 충격' 절대 사용 금지
2. 상단 훅 카피 (hook_lines):
   - 대표 이미지 바로 아래에 들어갈 강렬한 2줄 헤드 카피 (각 줄 22~30자 내외)
3. 상단 3줄 핵심 요약 박스 (summary_3points):
   - 바쁜 독자가 3초 만에 핵심을 파악할 수 있는 3가지 요약 문장 (핵심 팩트 / 배경 원인 / 실무 파장)
4. 맞춤형 소제목 3개와 본문 섹션 (sections):
   - ⚠️ 경고: '공식 발표 핵심 사양과 개념 및 뜻' 같은 기계적인 고정 소제목 절대 사용 금지!
   - 반드시 이번 기사 내용(기업명, 기술명, 핵심 수치, 갈등 구도 등)이 살아있는 매력적이고 구체적인 소제목 3개를 새로 지을 것!
     (예: "7조 원대 로봇 빅딜은 왜 중국의 벽에 부딪혔나", "140억 활성 매개변수로 추론 비용을 꺾은 비결", "글로벌 공급망 재편 속 국내 기업이 챙겨야 할 실무 변수")
   - 각 섹션 본문(paragraphs)은 2개 문단(문단당 3~4문장)으로 깊이 있게 작성하여 전체 본문이 1,500~1,800자가 되도록 할 것 (~합니다 체 일관 유지).
   - ⭐ [PC·모바일 동시 최적화 1:2 배수 문장 길이 규격 (필수 준수)]:
     * 모든 문장은 마침표(.)가 끝날 때마다 줄바꿈되어 출력됩니다.
     * PC에서는 1문장=1줄로 시원하게 들어오고, 모바일(가로폭 22자)에서는 어중간한 꼬리 줄 없이 딱 2줄(또는 1줄)로 떨어지도록, 모든 개별 문장의 길이(공백 포함, 태그 제외)를 반드시 `38~44자`(모바일 2줄 꽉 차는 길이) 또는 `19~22자`(단문)로 맞춰 작성할 것!
     * 절대 `25~34자`(모바일 둘째 줄에 5~8자만 남는 톱니바퀴 구간)나 `46자 이상`(PC 1줄을 초과하는 장문)으로 문장을 쓰지 말고, 문장이 길어지면 접속사(`~하며,`, `~하고,`) 대신 마침표(`.`)로 깔끔하게 끊어 두 문장으로 나눌 것!
   - 각 문단에서 가장 핵심이 되는 구절이나 문장 1곳에는 `[BLUE]핵심 구절[/BLUE]` 또는 `[HL_SKY]형광펜 강조 문장[/HL_SKY]`, `[HL_YELLOW]핵심 수치 강조[/HL_YELLOW]` 태그를 자연스럽게 입혀 가독성을 극대화할 것! (주의: `[BLUE]` 태그 바깥이나 안쪽에 `**` 기호를 중복해서 붙이지 말 것!)
   - 어려운 전문 용어는 괄호나 쉬운 비유로 친절히 풀어 쓸 것.
5. 중간 질문형 인용구 (pull_quote):
   - 2번째 섹션과 3번째 섹션 사이에 독자의 스크롤 집중력을 깨우는 1줄 질문 문장 (예: "그렇다면 이번 아키텍처 전환이 실제 기업 현업과 비용 구조에는 어떤 변화를 가져올까요?")
6. 본문 중간 삽입용 인포그래픽 비교표 데이터 (infographic):
   - 기사의 핵심 수치와 구조를 한눈에 보여주는 비교표 데이터:
     * card_title: 표 상단 제목 (예: "{clean_core} 핵심 지표 및 시장 파장 비교")
     * metric_label: 배지 라벨 (8자 이내, 예: "핵심 관전 지표")
     * metric_main: 핵심 수치/변화 요약 1줄 (28자 이내)
     * metric_sub: 부연 설명 1줄 (38자 이내)
     * table_headers: ["핵심 구분", "주요 팩트 및 기술·시장 수치", "산업 및 실무 파장"]
     * table_rows: 정확히 3개 행, 각 행은 ["구분명(8자 이내)", "구체적 팩트와 수치 설명(35~50자)", "시장/실무 파장 핵심 요약(25~40자)"]
7. 지치 블로그 테크 전문 분석 (expert_analysis):
   - 실무진과 투자자가 취해야 할 전략적 판단 기준을 2~3문장으로 날카롭게 제시 ('실제 현업 도입 시 제가 활용하고 있는 기준을 바탕으로' 자연스럽게 1회 연결)
8. 엔딩 2줄 슬로건 (ending_slogan):
   - 글을 마무리하는 여운 있는 2줄 요약 슬로건
9. 금지 표현 엄격 배제:
   - '중요한 점은', '주목할 점은', '방향은 분명합니다', '관건입니다', '시사하는 바가 큽니다', '귀추가 주목됩니다', '첫째/둘째/셋째', 이모지(🌱, 🔥 등) 절대 사용 금지!

반드시 아래 JSON 구조로만 응답하세요:
{{
  "title": "22~28자 완결된 기사 맞춤형 제목",
  "summary_lines": ["썸네일 첫줄 (12자 이내)", "썸네일 둘째줄 (13자 이내)"],
  "hook_lines": ["상단 훅 카피 첫째 줄", "상단 훅 카피 둘째 줄"],
  "summary_3points": [
    "핵심 팩트: 구체적 수치와 핵심 사건 요약",
    "배경 원인: 기술적·산업적 전환 배경 요약",
    "실무 파장: 업계 및 실무진이 주목할 핵심 영향"
  ],
  "sections": [
    {{
      "subheading": "기사 맞춤형 구체적 소제목 1",
      "paragraphs": ["첫 번째 문단 (3~4문장, [BLUE]...[/BLUE] 또는 **볼드** 포함)", "두 번째 문단 (3~4문장, [HL_SKY]...[/HL_SKY] 포함)"]
    }},
    {{
      "subheading": "기사 맞춤형 구체적 소제목 2",
      "paragraphs": ["세 번째 문단 (3~4문장, [BLUE]...[/BLUE] 포함)", "네 번째 문단 (3~4문장, [HL_YELLOW]...[/HL_YELLOW] 포함)"]
    }},
    {{
      "subheading": "기사 맞춤형 구체적 소제목 3",
      "paragraphs": ["다섯 번째 문단 (3~4문장, 실무진이 알아야 할 핵심 팩트를 정확하게 안내해 드리면 포함)", "여섯 번째 문단 (3~4문장, [BLUE]...[/BLUE] 포함)"]
    }}
  ],
  "pull_quote": "독자의 호기심을 자극하는 중간 브릿지 질문 한 문장?",
  "infographic": {{
    "card_title": "{clean_core} 핵심 분석 및 산업 파장 비교",
    "metric_label": "핵심 관전 지표",
    "metric_main": "기사의 가장 중요한 수치/변화 1줄 요약",
    "metric_sub": "해당 수치가 갖는 산업적 의미 1줄 요약",
    "table_headers": ["핵심 구분", "주요 발표 팩트 및 수치", "산업 및 실무 파장"],
    "table_rows": [
      ["핵심 사양/배경", "구체적인 수치와 팩트 설명", "시장 및 경쟁사 파장"],
      ["기술/사업 구조", "기존 대비 달라진 핵심 메커니즘", "비용 절감 및 효율화 효과"],
      ["리스크/체크점", "규제·한계점 또는 선결 과제", "현업 도입 시 필수 점검 사항"]
    ]
  }},
  "expert_analysis": "실제 현업 도입 시 제가 활용하고 있는 기준을 바탕으로 분석한 2~3문장 결론",
  "ending_slogan": ["마무리 슬로건 첫째 줄", "마무리 슬로건 둘째 줄"],
  "tags": ["#태그1", "#태그2", "#태그3", "#태그4", "#태그5", "#태그6"],
  "image_prompt": "A vibrant 3D illustration of ... Strictly no text, no letters, no numbers."
}}
"""

    parsed = _call_llm_json(prompt)
    import history_checker
    best1_block = history_checker.build_best3_tech_links_block("jcjung1401", exclude_title=topic, max_links=1)

    if parsed and parsed.get("sections") and isinstance(parsed.get("sections"), list):
        clean_title = clean_ai_artifacts(parsed.get("title", sample_title))
        if len(clean_title) > 30 or not clean_title:
            clean_title = sample_title

        hook_lines = [clean_ai_artifacts(x) for x in (parsed.get("hook_lines") or []) if x]
        if len(hook_lines) < 2:
            hook_lines = [
                f"글로벌 테크 업계를 뒤흔든 {clean_core} 핵심 이슈!",
                "단순 기술 경쟁을 넘어 실제 수익성과 산업 판도를 가르는 분수령"
            ]

        summary_3points = [clean_ai_artifacts(x) for x in (parsed.get("summary_3points") or []) if x]
        if len(summary_3points) < 3:
            summary_3points = [
                f"핵심 팩트: {clean_core} 공식 발표로 글로벌 시장 판도 변화 가속",
                "배경 원인: 차세대 아키텍처 전환 및 비용 효율성 극대화 경쟁",
                "실무 파장: 엔터프라이즈 도입 시 기술 실효성과 규제 리스크 동시 점검 필수"
            ]

        # 본문 중간 인포그래픽 비교표 카드 이미지 렌더링
        info_data = parsed.get("infographic") or {}
        infographic_filename = f"infographic_card_{article_index}.png"
        infographic_path = os.path.join(base_dir, infographic_filename)
        try:
            formatter.generate_infographic_table_card(
                card_title=clean_ai_artifacts(info_data.get("card_title") or f"{clean_core} 핵심 분석 및 시장 파장 비교"),
                metric_banner={
                    "label": clean_ai_artifacts(info_data.get("metric_label") or "핵심 관전 지표"),
                    "main_value": clean_ai_artifacts(info_data.get("metric_main") or f"{clean_core} 핵심 패러다임 전환"),
                    "sub_value": clean_ai_artifacts(info_data.get("metric_sub") or "기술 효율성 극대화 및 글로벌 시장 재편 가속화")
                },
                table_headers=info_data.get("table_headers") or ["핵심 구분", "주요 발표 팩트 및 수치", "산업 및 실무 파장"],
                table_rows=info_data.get("table_rows") or [],
                output_path=infographic_path
            )
            print(f"  📊 [코자이너] 본문 중간 삽입용 매거진 인포그래픽 비교표 카드 생성 완료: {infographic_path}")
        except Exception as info_err:
            print(f"  ⚠️ 인포그래픽 카드 생성 중 예외: {info_err}")

        # 매거진 에디토리얼 본문 블록 조립
        blocks = []

        # 1. 상단 훅 카피 ([HOOK])
        blocks.append(f"[HOOK]**{hook_lines[0]}**\n[HL_SKY]**{hook_lines[1]}**[/HL_SKY][/HOOK]")

        # 2. 상단 [핵심 3줄 요약] 박스 ([SUMMARY_BOX])
        s_lines = ["[BLUE]**[핵심 3줄 요약]**[/BLUE]"]
        for pt in summary_3points[:3]:
            clean_pt = re.sub(r"^[•▪▸\-*]\s*", "", pt).strip()
            s_lines.append(f"▸ {clean_pt}")
        blocks.append("[SUMMARY_BOX]" + "\n".join(s_lines) + "[/SUMMARY_BOX]")

        # 3. 섹션 1, 2, 3 및 중간 인포그래픽 + 따옴표 인용구 징검다리 배치
        sections = parsed.get("sections", [])
        pull_quote = clean_ai_artifacts(parsed.get("pull_quote") or f"그렇다면 이번 {clean_core} 이슈가 실제 현업과 시장에는 어떤 변수가 될까요?")

        for s_idx, sec in enumerate(sections[:3]):
            sub_txt = clean_ai_artifacts(sec.get("subheading", f"핵심 관전 포인트 {s_idx+1}"))
            sub_txt = re.sub(r"^(?:\d+[\.\)]\s*|[▎|]\s*)+", "", sub_txt).strip()
            blocks.append(f"[SUB]▎ {sub_txt}[/SUB]")

            for p_txt in (sec.get("paragraphs") or []):
                cleaned_p = clean_ai_artifacts(p_txt)
                if cleaned_p:
                    blocks.append(cleaned_p)

            # 섹션 1 직후: 본문 중간 인포그래픽 비교표 이미지 삽입!
            if s_idx == 0 and os.path.exists(infographic_path):
                blocks.append(f"__IMAGE__:{infographic_path}")

            # 섹션 2 직후: 중앙 따옴표 질문 인용구([QUOTE]) 삽입!
            if s_idx == 1 and pull_quote:
                clean_q = pull_quote.strip('“”"\' ')
                blocks.append(f"[QUOTE]“ {clean_q} ”[/QUOTE]")

        # 4. 지치 블로그 테크 전문 분석
        expert_txt = clean_ai_artifacts(
            parsed.get("expert_analysis")
            or "실제 현업 도입 시 제가 활용하고 있는 기준을 바탕으로 볼 때, 단순 벤치마크 수치보다 자사 워크플로우와의 호환성 및 규제 리스크를 선제적으로 검증하는 전략이 필수적입니다."
        )
        blocks.append("[SUB]▎ 지치 블로그 테크 전문 분석[/SUB]")
        blocks.append(expert_txt)

        # 5. 수미상관 엔딩 슬로건 ([HOOK])
        ending_slogan = [clean_ai_artifacts(x) for x in (parsed.get("ending_slogan") or []) if x]
        if len(ending_slogan) >= 2:
            blocks.append(f"[HOOK]**{ending_slogan[0]}**\n[HL_SKY]**{ending_slogan[1]}**[/HL_SKY][/HOOK]")

        # 6. 공식 출처 + 연관 분석 1건 + 공감 CTA
        if url:
            blocks.append(f"공식 출처:\n\n{url}")
        blocks.append(best1_block)
        blocks.append(
            "소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n"
            "오늘 전해드린 테크 분석이 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다.\n"
            "지치 블로그가 매일 가장 빠르고 정확한 글로벌 테크 동향을 전달해 드리겠습니다."
        )

        clean_body = "\n\n".join(blocks)
        tags = parsed.get("tags") or ["#인공지능", "#AI트렌드", "#테크뉴스", "#IT분석", "#빅테크", "#지치블로그"]
        summary_lines = parsed.get("summary_lines")
        if not summary_lines or len(summary_lines) < 2 or "시장 파장 분석" in "".join(summary_lines):
            summary_lines = [f"{clean_core} 전격 공개!", "글로벌 테크 판도 뒤집나"]

        return {
            "title": clean_title,
            "summary_lines": summary_lines[:2],
            "body": clean_body,
            "tags": tags[:7],
            "image_prompt": parsed.get("image_prompt", ""),
            "infographic_path": infographic_path if os.path.exists(infographic_path) else ""
        }

    # 비상용 고품질 매거진 폴백
    clean_t = constants.clean_topic_title(topic)
    fallback_title = cheat_titles[0] if cheat_titles else f"{clean_t} 공식 발표! 핵심 기술 분석"
    default_summary = [f"{clean_t} 공식 발표", "글로벌 테크 판도 변화"]
    fact_snippet = scraped_facts[:450] if scraped_facts else f"{topic} 관련 글로벌 테크 기업의 공식 기술 문서 및 보도자료를 기반으로 분석한 최신 동향입니다."

    infographic_path = os.path.join(base_dir, f"infographic_card_{article_index}.png")
    try:
        formatter.generate_infographic_table_card(
            card_title=f"{clean_t} 핵심 사양 및 산업 파장 비교",
            metric_banner={
                "label": "핵심 관전 지표",
                "main_value": f"{clean_t} 기술 전환 및 시장 재편",
                "sub_value": "운영 효율성 극대화 vs 현업 도입 실효성 검증"
            },
            table_headers=["핵심 구분", "주요 발표 팩트 및 사양", "산업 및 실무 파장"],
            table_rows=[
                ["핵심 발표", f"{clean_t} 관련 차세대 전략 및 기술 스펙 공개", "글로벌 빅테크 주도권 경쟁 가속화"],
                ["효율성 변화", "데이터 처리 및 시스템 연동 효율 대폭 개선", "엔터프라이즈 AI 도입 장벽 완화"],
                ["실무 체크점", "기존 레거시 인프라 통합 및 보안 규정 변수", "도입 전 소규모 개념 검증(PoC) 필수"]
            ],
            output_path=infographic_path
        )
    except Exception:
        pass

    fallback_body = f"""[HOOK]**글로벌 인공지능 시장의 시선이 집중된 {clean_t} 핵심 발표!**
[HL_SKY]**단순 스펙 경쟁을 넘어 실질적 운영 효율과 수익성을 증명하는 전환점**[/HL_SKY][/HOOK]

[SUMMARY_BOX][BLUE]**[핵심 3줄 요약]**[/BLUE]
▸ 핵심 팩트: {topic} 공식 발표로 엔터프라이즈 및 글로벌 테크 생태계 파장 확산
▸ 배경 원인: 고비용 추론 구조를 탈피하고 실질적인 시스템 연동성과 수익성 확보 추진
▸ 실무 파장: 기업 현업 도입 시 레거시 호환성 및 보안·규제 리스크 사전 검증 필수[/SUMMARY_BOX]

[SUB]▎ {clean_t} 전격 부상, 무엇이 달라졌나[/SUB]

결론부터 말씀드리면 {topic} 소식이 공식 전해지면서 글로벌 인공지능 생태계와 엔터프라이즈 시장 전반에 적지 않은 파장이 일고 있습니다. [BLUE]기존 서비스 구조를 뛰어넘는 기술적 전환점이 마련되었다는 분석과 함께, 실제 현업 도입 과정에서의 실효성을 둘러싼 논의가 동시에 급물살을 타고 있습니다.[/BLUE] 빅테크 기업들이 주도해 온 생성형 AI 패권 경쟁이 이제는 실질적인 운영 효율성과 수익성 증명 단계로 이동했음을 보여주는 대목입니다.

이번 발표의 구체적인 내용을 살펴보면 기술적 지향점이 명확히 드러납니다. (※ 본 내용은 공식 보도자료 및 기술 백서 기반의 자료 분석입니다.) {fact_snippet} [HL_SKY]그동안 산업 현장의 실무진들은 고도화된 추론 성능을 유지하면서도 인프라 도입 비용과 응답 지연 시간을 동시에 낮출 수 있는 실질적인 해법을 꾸준히 요구해 왔습니다.[/HL_SKY]

__IMAGE__:{infographic_path}

[SUB]▎ 데이터 효율성 혁신과 글로벌 빅테크 경쟁 구도[/SUB]

이번 조치가 갖는 본질적인 의미는 데이터 처리 효율성과 시스템 연동성을 대폭 끌어올려 기업들의 도입 장벽을 낮추었다는 데 있습니다. 특히 보안성과 자체 데이터 통제권을 중시하는 금융, 제조, IT 서비스 기업들 입장에서는 [HL_YELLOW]기존 폐쇄형 구조에서 벗어나 보다 유연하게 AI 파이프라인을 설계할 수 있는 선택지를 확보하게 되었습니다.[/HL_YELLOW]

경쟁사들 역시 이에 대응하기 위해 차세대 모델의 업데이트 주기를 앞당기며 치열한 맞불 작전에 나설 것으로 전망됩니다. 실무진이 알아야 할 핵심 팩트를 정확하게 안내해 드리면, 독자적인 생태계 구축보다 기업 고객의 실질적인 총소유비용(TCO)을 얼마나 절감해 주는지가 시장 점유율을 가르는 핵심 지표로 자리 잡고 있습니다.

[QUOTE]“ 그렇다면 발표된 기술 사양이 실제 기업 현업 환경에서도 그대로 재현될 수 있을까요? ”[/QUOTE]

[SUB]▎ 현업 도입 시 리스크와 실무진 핵심 체크포인트[/SUB]

다만 발표된 기술 사양이 실제 대규모 상용 트래픽 환경에서도 흔들림 없이 재현될 수 있을지는 면밀한 검증이 필요합니다. [BLUE]기업 내부 레거시 시스템과의 통합 과정에서 발생하는 추가 엔지니어링 비용과 보안 규정 준수 여부 역시 실무진이 반드시 따져봐야 할 변수입니다.[/BLUE] 과연 이번 기술 개편이 시장의 기대를 충족하며 실질적인 비즈니스 생산성 향상으로 이어질 수 있을지, 초기 도입 기업들의 실제 성능 지표와 비용 절감 성과를 차분히 지켜봐야 할 시점입니다.

[SUB]▎ 지치 블로그 테크 전문 분석[/SUB]

단순 사양 경쟁을 넘어 '실제 현업 인프라 비용 대비 실효성'을 확보했는지가 이번 기술의 최대 승부처입니다. 실제 현업 도입 시 제가 활용하고 있는 기준을 바탕으로 볼 때, 실무진은 벤치마크 점수에만 의존하지 말고 소규모 PoC(개념 검증)를 거쳐 자사 워크플로우에 최적화하는 전략이 요구됩니다.

공식 출처:

{url}

{best1_block}

소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.
오늘 전해드린 테크 분석이 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다.
지치 블로그가 매일 가장 날카롭고 신속한 글로벌 테크 동향을 전달해 드리겠습니다."""

    return {
        "title": fallback_title,
        "summary_lines": default_summary,
        "body": clean_ai_artifacts(fallback_body),
        "tags": ["#인공지능", "#AI트렌드", "#테크뉴스", "#IT기사", "#빅테크", "#지치블로그"],
        "image_prompt": "",
        "infographic_path": infographic_path if os.path.exists(infographic_path) else ""
    }


def generate_webtoon_with_ai(
    snack_name: str,
    tag: str,
    youtube: str,
    naver: str,
    chars: list,
    real_photos: list = None
) -> dict:
    """
    [지치 컴퍼니 정규 웹툰 엔진 (사장님 3대 특명 반영)]
    1. 코자이너는 AI 기사일 때만 제미니로 이미지를 생성합니다.
       - 웹툰에서는 API 이미지 생성을 절대 호출하지 않습니다!
    2. 웹툰에서는 코서치가 찾아온 실물 사진을 바탕으로, 코디터가 6~8컷의 시놉시스를 작성합니다.
    3. 코자이너는 코디터의 6~8컷 시놉시스를 기반으로 3D 픽사 스타일 '명령 프롬프트'만 나타냅니다.
    4. 소제목 번호매김 금지 및 스마트에디터 dot(•) 표시 원천 금지 규정을 100% 준수합니다.
    """
    main_name = "지치"
    sub_char = chars[1] if len(chars) > 1 else "송이 (삼색 고양이)"
    sub_name = "송이" if "송이" in sub_char else "초코"

    char_en = (
        "'Jichi' (a cute chubby light-green sprout fairy with two fresh green leaves on head, heart-shaped face mask) and "
        + (
            "'Songi' (a cute chubby calico cat with spotless white fur on face, absolutely NO dots/moles/freckles, black left ear patch, orange right ear patch)"
            if sub_name == "송이"
            else "'Choco' (a cute black and white tuxedo cat with bright round eyes)"
        )
    )

    prompt = f"""당신은 네이버 인기 웹툰 작가이자 디저트 전문 에디터(코디터)입니다.
대상 제품: {snack_name}
화제 포인트: {tag}
유튜브/SNS 반응: {youtube}
실구매자 후기 및 꿀팁: {naver}
등장 캐릭터: {main_name}(새싹 요정) & {sub_name}(고양이 친구, 말끝에 자연스럽게 '~냥' 사용)

[사장님 엄격 말투 및 문체 규칙 7대 원칙]
1. 문장 끝은 '~했어요', '~더라고요', '~같아요', '~인 것 같아요'처럼 부드러운 구어체로 쓰세요.
   - '~확인됐습니다', '~평가했습니다', '~판단됩니다', '~알려드립니다' 같은 딱딱한 보고서체/신문기사체는 절대 쓰지 마세요.
2. 한 문장은 짧게 쓰세요. 접속사나 쉼표로 길게 이어붙이지 말고 두 문장으로 나누세요.
3. 아래 AI 특유의 표현은 절대 쓰지 마세요:
   - 금지: '공통으로 확인됐다', '극찬했다', '높은 가격대', '다소 부담스럽다', '~에 대해 알아보겠습니다', '결론적으로', '종합하면', '~라고 할 수 있습니다'
   - 대체: '둘 다 이 얘기는 똑같이 하더라고요', '진짜 맛있다고 난리였어요', '가격이 좀 세긴 해요' 처럼 친근한 일상 표현으로 바꾸세요.
4. 숫자나 가격은 느낌을 같이 말해주세요. (예: "하나에 5,900원이라 솔직히 좀 비싸죠")
5. 가끔 독자에게 말을 걸어주세요. (예: "궁금하시죠?", "저라면 한 번쯤은 사 먹어볼 것 같아요")
6. 감탄이나 솔직한 한마디를 한두 군데 넣으세요. 단, 이모티콘이나 느낌표(!)는 남발하지 마세요.
7. 장점만 늘어놓지 말고 아쉬운 점도 편하게 솔직하게 한마디 해주세요.

[면책 문구 규칙]
- 맨 아래 안내 문구는 딱딱한 고지문이 아니라 블로거가 덧붙이는 한마디처럼 쓰세요:
  "참고로 이 웹툰은 구매 후기를 보고 상상해서 그린 창작이에요. 제가 직접 먹어본 건 아니니까, 맛은 사람마다 다를 수 있다는 점 감안해주세요."

[소제목 및 리스트 서식 규칙]
1. [소제목 번호매김 절대 금지]: 소제목에 숫자를 붙이지 마세요.
2. [스마트에디터 dot 및 번호 리스트 트리거 금지]: 문단이나 줄 시작에 대시(-), 불릿(*, •), 숫자(1. 2. 3.)를 절대 붙이지 마세요.
3. 8컷의 정통 시놉시스(1컷~8컷 대화 및 상황)를 작성하세요.

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "title": "{snack_name}, [반전 한마디]!",
  "synopsis_cuts": [
    {{"cut_number": 1, "action": "지치가 편의점에서 신상을 발견한다.", "dialogue": "{main_name}: 오늘은 ...?"}},
    {{"cut_number": 2, "action": "...", "dialogue": "{sub_name}: ...다냥!"}},
    {{"cut_number": 3, "action": "...", "dialogue": "..."}},
    {{"cut_number": 4, "action": "...", "dialogue": "..."}},
    {{"cut_number": 5, "action": "...", "dialogue": "..."}},
    {{"cut_number": 6, "action": "...", "dialogue": "..."}},
    {{"cut_number": 7, "action": "...", "dialogue": "..."}},
    {{"cut_number": 8, "action": "...", "dialogue": "..."}}
  ],
  "review_chat": "둘 다 이 얘기는 똑같이 하더라고요. 겉은 쫀득하고 속 크림은 진한데, 하나에 5,900원이라 솔직히 가격이 좀 세긴 해요. 그래도 궁금하시죠? 저라면 한 번쯤은 사 먹어볼 것 같아요.",
  "disclaimer": "참고로 이 웹툰은 구매 후기를 보고 상상해서 그린 창작이에요. 제가 직접 먹어본 건 아니니까, 맛은 사람마다 다를 수 있다는 점 감안해주세요.",
  "tags": ["#태그1", "#태그2", "#태그3", "#태그4", "#태그5"]
}}
"""

    parsed = _call_llm_json(prompt)

    # 코서치가 찾아온 실물 사진 로드 (API 이미지 생성 절대 호출 안 함)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    photos = real_photos or []
    if not photos:
        candidates = [
            os.path.join(base_dir, "pistachio_shelf.png"),
            os.path.join(base_dir, "pistachio_package.png"),
            os.path.join(base_dir, "pistachio_cross_section.png"),
        ]
        photos = [p for p in candidates if os.path.exists(p)]

    synopsis_cuts = parsed.get("synopsis_cuts", []) if parsed else []
    prompts_list = [c.get("designer_prompt", "") for c in synopsis_cuts if isinstance(c, dict)]

    clean_snack = snack_name.split("(")[0].strip()
    if parsed and synopsis_cuts:
        title = clean_ai_artifacts(parsed.get("title", f"{clean_snack}, 떡인 줄 알았는데?"))
        review_chat = clean_ai_artifacts(parsed.get("review_chat", ""))
        disclaimer = clean_ai_artifacts(parsed.get("disclaimer", "참고로 이 웹툰은 구매 후기를 보고 상상해서 그린 창작이에요. 제가 직접 먹어본 건 아니니까, 맛은 사람마다 다를 수 있다는 점 감안해주세요."))
        tags = parsed.get("tags") or [
            f"#{re.sub(r'[^가-힣a-zA-Z0-9]', '', snack_name)[:12]}",
            "#편의점신상", "#디저트추천", "#솔직후기", "#내돈내산", "#지치웹툰"
        ]
    else:
        title = f"{clean_snack}, 떡인 줄 알았는데?"
        synopsis_cuts = [
            {"cut_number": 1, "action": f"편의점 냉장 매대에서 올리브색 상자를 발견한 {main_name}.", "dialogue": f"{main_name}: “성수동에서 줄 서던 한정선이 편의점에?”"},
            {"cut_number": 2, "action": f"{sub_name}가 가격표를 보고 눈이 휘둥그레진다.", "dialogue": f"{sub_name}: “5,900원?! 편의점 떡 중에 제일 비싸다냥!”"},
            {"cut_number": 3, "action": f"{main_name}가 전통 한지 느낌의 단아한 상자를 조심스레 연다.", "dialogue": f"{main_name}: “포장부터 고급 한과 느낌이 물씬 나네!”"},
            {"cut_number": 4, "action": f"반으로 가른 찹쌀떡 속에 묵직한 연두색 원물 크림이 드러난다.", "dialogue": f"{sub_name}: “우와! 속에 든 피스타치오 크림이 완전 빵빵하다냥!”"},
            {"cut_number": 5, "action": f"{main_name}가 크림 속에 콕콕 박힌 통 분태를 유심히 들여다본다.", "dialogue": f"{main_name}: “초록색 색소가 아니라 진짜 통 피스타치오를 갈아 넣었어!”"},
            {"cut_number": 6, "action": f"{sub_name}가 냉동실 문을 열며 포크를 챙겨 온다.", "dialogue": f"{sub_name}: “딱 10분만 살짝 얼려 먹으면 젤라또 같다냥!”"},
            {"cut_number": 7, "action": f"겉은 쫀득하고 속은 시원한 찹쌀떡을 베어 문 {sub_name}의 볼이 빵빵해진다.", "dialogue": f"{sub_name}: “겉은 찰떡인데 속은 완전 고급 젤라또 케이크다냥!”"},
            {"cut_number": 8, "action": f"{main_name}가 빈 접시를 보며 활짝 웃는다.", "dialogue": f"{main_name}: “비싸다고 투덜대더니 순식간에 다 먹었네!”"}
        ]
        review_chat = "구매 후기를 찾아봤더니 둘 다 이 얘기는 똑같이 하더라고요. 떡피는 얇고 쫀득한데 속 크림은 피스타치오 맛이 엄청 진하대요. 다만 하나에 5,900원이라 솔직히 가격이 좀 세긴 해요. 궁금하시죠? 저라면 한 번쯤은 사 먹어볼 것 같아요."
        disclaimer = "참고로 이 웹툰은 구매 후기를 보고 상상해서 그린 창작이에요. 제가 직접 먹어본 건 아니니까, 맛은 사람마다 다를 수 있다는 점 감안해주세요."
        tags = [
            f"#{re.sub(r'[^가-힣a-zA-Z0-9]', '', clean_snack)[:12]}",
            "#편의점신상",
            "#디저트추천",
            "#솔직후기",
            "#내돈내산",
            "#지치웹툰"
        ]

    # 본문 문단 구성: 2026-10-30 사장님 & 친누나 600+ 조회수 황금 레이아웃 100% 적용
    # [절대 원칙 1] 4컷 웹툰 이후 나오는 긴 텍스트 대화(1컷~8컷 대본) 전면 삭제! (방문객에게 빠르게 신상 핵심 전달)
    # [절대 원칙 2] 코자이너 웹툰 말풍선은 5글자 이내 초심플 한글 키워드만 삽입!
    # [절대 원칙 3] 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 적용!
    # [절대 원칙 4] 프롬프트 바로 아래 '코자이너 컷별 실사 이미지 배치 가이드' 의무화!
    # [절대 원칙 5] 3·3·3 태그 황금 공식 (인물 3개 + 브랜드 3개 + 제품 3개)
    content_paragraphs = []

    # 1. 친근한 오프닝 인사 및 신상 화제성 소개
    intro_p = f"""안녕하세요, 지치 블로그를 찾아주신 여러분!
귀여운 새싹 요정 지치와 호기심 대장 고양이 송이입니다!
최근 SNS와 편의점 디저트 코너에서 품절 대란을 일으키고 있는 화제의 신상,
**{snack_name}**를 지치와 송이가 발 빠르게 만나보았습니다!"""
    content_paragraphs.append(intro_p)

    # 2. 코자이너 1컷~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 신상 출시 공식 포스터 또는 스마트폰 뉴스 기사 캡처 실사\n"
        "- 2번컷 참조 사진: 편의점 앱 재고 조회 화면 또는 출동 준비 사진\n"
        "- 3번컷 참조 사진: 방문할 편의점 매장 외관 및 네온 간판 실사\n"
        "- 4번컷 참조 사진: 편의점 매대 진열 사진 및 제품 포장지(패키지) 정면 실물 사진"
    )

    # 3. 코자이너 5컷~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 포장지 개봉 후 빵/디저트 겉면 실물 사진 (크기/색감 대조)\n"
        "- 6번컷 참조 사진: 제품을 반으로 갈라 크림이 흘러나오는 리얼 단면 실사 (핵심!)\n"
        "- 7번컷 참조 사진: 한 입 베어 문 크림/토핑 레이어 확대 실사\n"
        "- 8번컷 참조 사진: 엔딩 컷 및 추천 음료(아아, 흰 우유) 페어링 세팅 실사"
    )

    # 실사 사진 컷 연결
    if photos and len(photos) >= 1:
        content_paragraphs.append(f"__IMAGE__:{photos[0]}")
    content_paragraphs.append(guide_cut1_4)

    if photos and len(photos) >= 2:
        content_paragraphs.append(f"__IMAGE__:{photos[1]}")
    content_paragraphs.append(guide_cut5_8)

    # 4. [친누나표 팩트 체크 & Tasty Tip! 황금 포맷 - 4대 독립 블록 구성 (구분선 없이 바로 제품명 시작)]
    block_info = f"제품명 : {clean_snack}\n가격 : 매장 판매가 기준 (편의점/매장 확인)\n매장 : 전국 편의점 및 공식 오프라인 매장"
    block_flavor = f"핵심 플레이버 : {tag}\n달콤하고 부드러운 크림과 풍미 가득한 베이스 조합"
    block_feature = "특징 및 식감: 뻔한 단맛 아님!\n원물의 진한 풍미와 크림의 황금밸런스\n입안 가득 퍼지는 쫀득하고 부드러운 식감이 완전 좋아요"
    block_tip = "Tasty Tip!\n얼죽아 사람들과 딱인 아아와 함께!\n난 커피가 싫다! 우유나 홍차러버이신 분들은\n고소한 흰 우유나 얼그레이와 좋아요"
    content_paragraphs.extend([block_info, block_flavor, block_feature, block_tip])

    # 5. 엔딩 공감 및 소통 멘트
    cta_p = "오늘 전해드린 편의점 신상 리뷰가 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다! 지치와 송이가 매일 가장 핫한 편의점 신상과 최신 트렌드를 전달해 드리겠습니다."
    content_paragraphs.append(cta_p)

    return {
        "title": title,
        "content_paragraphs": content_paragraphs,
        "synopsis_cuts": synopsis_cuts,
        "designer_prompts": prompts_list,
        "image_paths": photos,
        "tags": tags[:7]
    }
