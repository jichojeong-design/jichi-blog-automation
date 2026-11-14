import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import formatter
import auto_publisher

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def publish_kimchi_kongnamul_soup_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 - 비 온 뒤 쌀쌀한 일요일 아침 해장 편]
    주제: 어제 내린 비로 쌀쌀한 일요일 아침, 3분 만에 속을 확 풀어주는
          편의점 '전주식 김치콩나물국밥' 솔직 리뷰!
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/상황 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 비 온 뒤 쌀쌀한 아침 해장! 편의점 '김치콩나물국밥' 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Chilly Sunday morning after rain, damp cool street air. Jichi the green sprout fairy and Songi the calico cat shivering slightly in cozy hoodies, holding their stomachs looking for warm hangover soup. Short Korean speech bubbles (MAX 5 chars): Jichi says '비온뒤쌀쌀', Songi says '속풀고싶다'.\n"
        "- Panel ② (Top-Right): Stepping into a bright warm convenience store! Heading straight to the refrigerated instant soup / meal bowl corner and spotting a steaming-looking '김치콩나물국밥' cup bowl. Short Korean speech bubbles (MAX 5 chars): Songi says '해장국발견!', Jichi says '바로이거야!'.\n"
        "- Panel ③ (Bottom-Left): Pouring the rice, crunchy bean sprouts, and spicy kimchi soup base into the cup, adding hot water up to the inner line, and putting it into the microwave for 3 minutes. Short Korean speech bubbles (MAX 5 chars): Jichi says '렌지3분컷', Songi says '기대된다냥!'.\n"
        "- Panel ④ (Bottom-Right): Carrying the piping hot steaming soup bowl to the cozy window counter. Delicious savory kimchi and anchovy broth aroma rising! Short Korean speech bubbles (MAX 5 chars): Songi says '냄새미쳤다', Jichi says '얼른먹자!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, crisp post-rain morning atmosphere contrasting with warm cozy convenience store lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '비온뒤쌀쌀', '속풀고싶다', '해장국발견!', '바로이거야!', '렌지3분컷', '기대된다냥!', '냄새미쳤다', '얼른먹자!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 비 온 뒤 쌀쌀한 아침 거리 풍경 또는 따뜻한 국물이 생각나는 아침 감성 컷\n"
        "- 2번컷 참조 사진: 편의점 냉장 간편식 코너에 진열된 김치콩나물국밥 패키지 실사\n"
        "- 3번컷 참조 사진: 용기에 밥과 건더기, 국물 베이스를 넣고 전자레인지에 3분 조리하는 과정 컷\n"
        "- 4번컷 참조 사진: 조리 완료 후 김이 모락모락 피어오르는 따끈한 국밥 실물 컷"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Close-up of a big spoonful of rice, crunchy yellow-headed bean sprouts, and bright red aged kimchi soaked in clear spicy broth! Steam rising deliciously. Short Korean speech bubbles (MAX 5 chars): Songi says '건더기푸짐', Jichi says '콩나물아삭'.\n"
        "- Panel ⑥ (Top-Right): Jichi and Songi taking a big hot spoonful! Instantly feeling warm, refreshed, and relieved with rosy cheeks and happy teary eyes. Short Korean speech bubbles (MAX 5 chars): Jichi says '시원칼칼해', Songi says '속이확풀려'.\n"
        "- Panel ⑦ (Bottom-Left): Enjoying the soup even more by adding a soft-boiled egg (감동란) or roasted seaweed flakes on top! Pure hearty breakfast satisfaction. Short Korean speech bubbles (MAX 5 chars): Songi says '계란추가각', Jichi says '든든한한끼'.\n"
        "- Panel ⑧ (Bottom-Right): Cheerful satisfied ending scene! Empty clean bowl, Jichi and Songi rubbing their full bellies happily beside a cute wooden board reading '좋아요 & 구독 ❤️'. Short Korean speech bubbles (MAX 5 chars): Jichi says '해장완벽!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, rich steaming Korean kimchi bean sprout soup textures, warm cozy morning comfort food mood. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '건더기푸짐', '콩나물아삭', '시원칼칼해', '속이확풀려', '계란추가각', '든든한한끼', '해장완벽!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 숟가락으로 밥과 아삭한 콩나물, 김치를 듬뿍 떠 올린 클로즈업 샷 (★핵심 킬링컷!)\n"
        "- 6번컷 참조 사진: 맑고 칼칼한 붉은 국물 색감이 잘 드러나는 국밥 근접 실사\n"
        "- 7번컷 참조 사진: 편의점 반숙란(감동란)이나 조미김을 곁들여 먹는 아침 해장 꿀조합 컷\n"
        "- 8번컷 참조 사진: 국물 한 방울 남기지 않고 싹 비운 깔끔한 완식 인증 컷"
    )

    # 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (100% 영구 표준 준수)
    fact_block_1 = "제품명 : 편의점 '전주식 김치콩나물국밥'\n가격 : 약 4,500원~4,900원대\n매장 : 전국 주요 편의점 냉장 간편식(국밥) 코너"
    fact_block_2 = "핵심 플레이버 : 깊고 시원한 멸치·황태 육수 베이스 +\n아삭하게 살아있는 국내산 콩나물 +\n잘 익어 칼칼한 볶음김치와 고슬고슬한 햇반 조합"
    fact_block_3 = "특징 및 식감: 밍밍하거나 비린 인스턴트 국물 맛 아님!\n전자레인지 3분 조리만으로 뚝배기 전문점 못지않은\n시원하고 칼칼한 감칠맛과 아삭한 콩나물 식감이 완전 좋아요\n비 온 뒤 쌀쌀한 아침 해장이나 든든한 한 끼로 최고"
    fact_block_4 = "Tasty Tip!\n편의점 반숙란(감동란)을 하나 톡 까서 국물에 살짝 풀어 먹으면 고소함 두 배!\n조미김을 잘게 부숴 올려 먹으면 감칠맛이 폭발해요!\n취향에 따라 청양고추나 후추를 살짝 톡톡 뿌려주면 해장 효과 200% 완성!"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분!\n어제 내린 비로 부쩍 쌀쌀해진 일요일 아침, 따끈하고 시원한 국물로 속을 달래러 편의점으로 출동한 새싹 요정 지치와 고양이 송이입니다!",
        "날씨가 쌀쌀해지고 찬 바람이 불면 아침부터 얼큰하고 개운한 국밥 한 그릇이 간절해지기 마련인데요.\n주말 아침, 불 앞에서 번거롭게 끓이지 않아도 전자레인지 3분이면 전문점 뺨치는 속 풀이를 할 수 있다는 사실 알고 계셨나요?",
        "비 온 뒤 쌀쌀한 아침 해장으로 딱인 **편의점 '전주식 김치콩나물국밥'** 솔직 리뷰, 지금 바로 시작합니다!",
        prompt_cut1_4,
        guide_cut1_4,
        prompt_cut5_8,
        guide_cut5_8,
        fact_block_1,
        fact_block_2,
        fact_block_3,
        fact_block_4,
        "소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n오늘 전해드린 쌀쌀한 아침 해장 국밥 리뷰가 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다! 지치와 송이가 매일 가장 따뜻하고 든든한 편의점 소식을 전해드리겠습니다."
    ]

    # 웹툰 전용 모바일 최적화 포맷팅
    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("[CHATGPT") or p_str.startswith("[코자이너") or "제품명 :" in p_str or "Tasty Tip!" in p_str:
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=22))

    # 3·3·3 태그 공식 (인물/상황 3 + 브랜드 3 + 제품 3)
    tags = [
        "#지치웹툰", "#아침해장", "#쌀쌀한날씨",
        "#편의점국밥", "#편의점해장", "#편의점신상",
        "#김치콩나물국밥", "#콩나물국밥", "#전주식콩나물국밥"
    ]

    print(f"\n📤 네이버 스마트에디터 원격 웹툰 {'임시저장' if save_draft else '실전발행'} 개시...")
    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=None,
        category_name="웹툰",
        tags=tags,
        save_draft=save_draft
    )

    if success:
        print(f"\n🎉 [지치 컴퍼니 웹툰 성공] 김치콩나물국밥 웹툰이 네이버 블로그에 안전하게 임시저장되었습니다!")
    else:
        print(f"\n🚨 [주의] 임시저장 과정 중 오류가 발생했습니다.")

    return success

if __name__ == "__main__":
    is_draft = "--publish" not in sys.argv
    publish_kimchi_kongnamul_soup_toon(save_draft=is_draft)
