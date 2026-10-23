import random

def generate_ai_news_prompt(topic: str, url: str, key_facts: str = "") -> str:
    """루틴 3: AI 뉴스 원고 작성용 프롬프트"""
    return f"""[지치 블로그: AI 기사 작성 요청]
주제: {topic}
참고 출처: {url}
참고 팩트: {key_facts}

[필수 작성 기준]
1. 문체 및 분량:
   - 10년 차 IT·산업 기자 문체 (합니다체 또는 한다체 중 하나로 일관성 유지)
   - 공백 제외 1,500 ~ 1,800자 분량
   - 문단당 2~5문장으로 의미 단위 구성
   - 소제목은 0~2개만 자연스럽게 사용 (반복 소제목 금지)
   - 같은 종결어미 3회 이상 연속 금지
   - 접속사 시작 문장은 문단당 최대 1회
   - 직접 인용은 기사당 최대 2문장
   - 마지막은 교훈·상투적 조언이 아니라 '남은 질문이나 확인할 조건'으로 마무리

2. 도입부 3초 훅 (Hook):
   - 첫 문단에서 사건과 핵심 반전을 바로 제시하여 독자 이탈 방지

3. 사실 검증 및 신뢰도 철칙 (네이버 우수 블로거 선정 기준 준수):
   - 모델명, 가격, 출시일, 성능 수치는 공식 발표 기준
   - 확인되지 않은 기능이나 주관적 느낌을 체험한 것처럼 날조 금지
   - 실제 사용·체험하지 않은 경우 '직접 써보니', '충격 반전' 등 과장 낚시성 표현 절대 금지!
   - [공식 자료 기반 설명]과 [실제 직접 경험/후기]를 명확한 구분 표시로 분리 작성할 것
   - 글 말미에는 공식 출처와 함께 10년 차 IT 기자의 날카롭고 구체적인 독자 분석(1~2줄)을 반드시 포함할 것
   - 기업 주장과 독립 검증 성과 구분

4. 절대 금지 표현:
   - '직접 써보니', '충격 반전', '진짜 충격' (실제 사용 후기가 아닐 때 제목/본문 사용 절대 금지)
   - '핵심은 ~이 아니라', '단순한 ~이 아니라', '중요한 점은', '주목할 점은'
   - '방향은 분명합니다', '관건입니다', '시사하는 바가 큽니다', '귀추가 주목됩니다'
   - '첫째·둘째·셋째' 식의 단순 나열 금지

5. 출력 형식:
   [추천 제목 3종] (28자 이내로 완결된 문장! 비밀 치트키인 상황반전/자극호기심/타겟공감 키워드를 문맥에 맞게 다채롭게 활용하세요. 문장 중간이 뚝 잘리지 않도록 완전한 문장으로 마무리할 것)
   [본문 텍스트] (가운데 정렬 감안, 1,500~1,800자)
   [태그 5개] (#키워드 형식으로 정확히 5개)
   [DALL-E 3 영문 이미지 프롬프트] (글자/숫자/로고 절대 없는 1:1 고품질 3D 일러스트 프롬프트 1문장)
"""

def generate_webtoon_script_prompt(snack_name: str, reviews: str, prop_twist: str, selected_chars: list) -> str:
    """사장님의 정확한 네이버 블로그 웹툰 포스팅 레이아웃에 100% 맞춘 통합 프롬프트"""
    chars_str = ", ".join(selected_chars)
    
    char_desc_list = []
    for c in selected_chars:
        if "지치" in c:
            char_desc_list.append("'Jichi' (cute chubby light-green sprout fairy)")
        elif "송이" in c:
            char_desc_list.append("'Songi' (cute calico cat, clean white muzzle without any dots)")
        elif "초코" in c:
            char_desc_list.append("'Choco' (cute black and white tuxedo cat)")
        elif "로봇" in c:
            char_desc_list.append("'AI Robot' (cute white and cyan mini assistant robot)")
    if not char_desc_list:
        char_desc_list = ["'Jichi' (sprout fairy)", "'Songi' (calico cat, clean face)"]
    chars_joined_en = " and ".join(char_desc_list)

    return f"""[지치 블로그: AI 웹툰 자동화 포스팅 완벽 패키지]
대상 제품: {snack_name}
실구매 후기 정보: {reviews}
소품 반전 아이템: {prop_twist}
등장 캐릭터: {chars_str} (주인공 '지치' 중심의 활기찬 대화)

[블로그 작성 구조 및 규칙 - 반드시 아래 양식 그대로 작성해 주세요!]

1. [추천 제목 3종]
   - 25자 내외 완결된 문장, 호기심 유발형 제목 3개 추천

2. [네이버 블로그 본문 레이아웃]
   [이미지 1 삽입 위치 (3~4컷 상반부 만화)]
   
   [이미지 1 상세 대화 내용]
   - 컷 1~3의 생생한 캐릭터별 대화 텍스트 작성 (티키타카 대화)
   - 소품 반전({prop_twist})이 등장하는 위트 있는 내용
   
   ---
   [이미지 2 삽입 위치 (3~4컷 하반부 만화)]
   
   [이미지 2 상세 대화 내용]
   - 컷 4~6의 캐릭터별 대화 텍스트 작성 (실제 후기 비교 및 솔직한 반응)
   
   ---
   [마무리: 실구매 후기 기반 맛있게 먹는 꿀팁 & 장단점 요약]
   - 후기에서 확인된 가장 맛있게 먹는 추천 방법 (예: 시럽 1펌프 줄이기, 얼먹, 에어프라이어 굽기 등)
   - 실제 구매자들이 느낀 솔직한 장점과 단점 요약 정리
   
   ---
   [해시태그 (5~8개)]
   - #{snack_name.replace(' ', '')} 포함 정확히 5~8개 해시태그

3. [DALL-E 3 전용 영문 이미지 프롬프트 2장]
   ⭐ 한글 깨짐 방지 철칙: 말풍선 안에는 절대 긴 문장을 넣지 말고, "우와!", "대박!", "진짜?!", "꿀맛!" 등 딱 2~3글자의 짧고 단순한 감탄 단어 또는 이모티콘만 들어가도록 영문 지정할 것!
   
   - 이미지 1 (컷 1~3): 3-panel vertical webtoon comic strip, 3D Pixar animation style. Characters strictly follow reference: {chars_joined_en}. Scene accurately depicts discovery of '{snack_name}' and '{prop_twist}' at a store. Speech bubbles contain ONLY very short 2-3 letter Korean words like '우와!', '대박!', '진짜?!' with emotion icons. Vibrant cozy lighting, clean 3D render --ar 2:3
   - 이미지 2 (컷 4~6): 3-panel vertical webtoon comic strip, 3D Pixar animation style. Same characters: {chars_joined_en}. Scene accurately depicts reviewing and tasting '{snack_name}' around a cozy wooden table. Speech bubbles contain ONLY short Korean exclamations like '꿀맛!', '대박!' with hearts/stars. High detail, warm atmosphere --ar 2:3

4. [발행 전 필수 검증 체크리스트]
   - 이미지 내 말풍선 한글 글자가 깨지거나 뭉개지지 않았는지 육안 확인 필수 (깨짐 발생 시 짧은 단어로 1회 재생성 또는 본문 텍스트로 보완 후 안전 발행할 것!)
"""
