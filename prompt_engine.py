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

def select_webtoon_characters(series_type: str = "snack") -> list:
    """
    [지치컴퍼니 캐릭터 편성 3대 황금 원칙]
    1. 리센느 시리즈: 지치 + 송이 고정
    2. AI 테크 연동 기사: 지치 + 초코 + AI로봇 고정
    3. 일반 편의점 신상: 지치 무조건 필수 포함 + (송이, 초코, AI로봇 중 자유/랜덤)
    """
    if series_type == "rescene":
        return ["지치 (새싹 요정)", "송이 (삼색 고양이)"]
    elif series_type == "ai_tech":
        return ["지치 (새싹 요정)", "초코 (턱시도 고양이)", "AI로봇 (미니 어시스턴트)"]
    else:
        # 일반 편의점 스낵: 지치 무조건 포함 + 1~2명 랜덤 편성
        possible_partners = [
            ["송이 (삼색 고양이)"],
            ["초코 (턱시도 고양이)"],
            ["초코 (턱시도 고양이)", "AI로봇 (미니 어시스턴트)"],
            ["송이 (삼색 고양이)", "AI로봇 (미니 어시스턴트)"]
        ]
        chosen = random.choice(possible_partners)
        return ["지치 (새싹 요정)"] + chosen


def generate_webtoon_script_prompt(snack_name: str, reviews: str, prop_twist: str, selected_chars: list) -> str:
    """사장님의 네이버 블로그 공인 황금 표준 규격 (이미지+4컷 대사 x 2회 교차) 100% 반영 프롬프트"""
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
        char_desc_list = ["'Jichi' (sprout fairy)", "'Choco' (tuxedo cat)", "'AI Robot' (mini robot)"]
    chars_joined_en = " and ".join(char_desc_list)

    return f"""[지치 블로그: 웹툰 황금 표준 패키지 작성 요청]
대상 제품: {snack_name}
실구매 후기 정보: {reviews}
핵심 반전 및 먹방 꿀팁: {prop_twist}
등장 캐릭터: {chars_str}

[필수 블로그 작성 구조 - 사장님 공인 10단계 황금 레이아웃 철저 준수]

1. [추천 제목 3종] (24~28자 이내 완결된 호기심+팩트형 문장)

2. [네이버 블로그 본문 레이아웃]
   [이미지 1 삽입 위치 (1, 2, 3, 4번 4컷 분할 만화)]
   
   1컷 · [상황 묘사]
   캐릭터: “[대사]”
   
   2컷 · [상황 묘사]
   캐릭터: “[대사]”
   
   3컷 · [상황 묘사]
   캐릭터: “[대사]”
   
   4컷 · [상황 묘사]
   캐릭터: “[대사]”
   
   ----------------------------------------
   [이미지 2 삽입 위치 (5, 6, 7, 8번 4컷 분할 만화)]
   
   5컷 · [상황 묘사]
   캐릭터: “[대사]”
   
   6컷 · [상황 묘사]
   캐릭터: “[대사]”
   
   7컷 · [상황 묘사]
   캐릭터: “[대사]”
   
   8컷 · [상황 묘사]
   캐릭터: “[대사]”
   
   ----------------------------------------
   [지치와 친구들의 실구매 후기 팩트 체크]
   1. 크기와 가격 대비 만족도:
   [모바일 16~18자 호흡 설명]
   
   2. 반전의 식감과 퀄리티:
   [모바일 16~18자 호흡 설명]
   
   3. 200% 맛있게 먹는 특급 조합:
   [모바일 16~18자 호흡 설명]
   
   ----------------------------------------
   [안내 및 제작 정보]
   본 포스팅은 공식 보도와 독립 구매 후기를 바탕으로 재구성한 지치컴퍼니의 순수 창작 웹툰입니다.
   등장인물의 행동과 대사는 각색된 연출이며, 직접 구매·시식한 후기가 아닙니다.
   게시된 이미지는 AI로 생성한 3D 연출 이미지이며 실제 제품 사진이 아니므로, 개인에 따라 맛과 식감의 차이가 있을 수 있습니다.
   
   ----------------------------------------
   [참고 출처]
   공식 기사 및 블로그 실구매 후기 URL
   
   ----------------------------------------
   [해시태그]
   #{snack_name.replace(' ', '')} 포함 8~10개
   
   ----------------------------------------
   [엔딩 공감/소통 문구]
   포스팅이 재미있고 유익하셨다면 하단의 공감(좋아요)과 따뜻한 댓글 부탁드립니다... (이웃 추가 유도)

3. [DALL-E 3 전용 4분할 영문 이미지 프롬프트 2장]
   - 이미지 1: 4-panel vertical 2x2 grid comic strip, numbered ①, ②, ③, ④. 3D Pixar style. Characters: {chars_joined_en}. Scene 1~4.
   - 이미지 2: 4-panel vertical 2x2 grid comic strip, numbered ⑤, ⑥, ⑦, ⑧. 3D Pixar style. Same characters. Scene 5~8.
   - STRICT CONSTRAINT: NO speech bubbles, NO letters inside images.
"""
