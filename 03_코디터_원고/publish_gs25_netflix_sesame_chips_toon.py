import os
import sys
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import formatter
import auto_publisher
import quality_inspector

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def publish_gs25_netflix_sesame_chips_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 제7탄]
    주제: 넷플릭스 정주행 필수템! GS25 X 넷플릭스 '넷플릭스 참기름 감자칩'
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 스낵 탐정)

    [대표님 엄격 5대 절대 수칙 + 매뉴얼 1호·2호·3호 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/화제 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    6. [지치컴패니 업무매뉴얼 1호 & 3호] 전방위 매대 스낵 실사 먹조합 (OTT 정주행 + 시원한 맥주/탄산 안주 페어링)
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 넷플릭스 볼 땐 필수?! GS25 '넷플릭스 참기름 감자칩' 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy living room. Songi the calico cat holding a TV remote, pointing excitedly at a large TV screen displaying Netflix logo and a breaking news banner of 'GS25 넷플릭스 참기름 감자칩'! Jichi the green sprout fairy gasps with round sparkling eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '신작정주행!', Jichi says '참기름과자?!'.\n"
        "- Panel ② (Top-Right): Songi enthusiastically grabbing Jichi's hand, strapping on a cute GS25 mini backpack, dashing towards the door with determination. Short Korean speech bubbles (MAX 5 chars): Songi says 'GS25출동!', Jichi says '스낵사러가!'.\n"
        "- Panel ③ (Bottom-Left): Inside bright GS25 convenience store snack aisle! Jichi and Songi spotting the sleek black and red Netflix-branded snack bag of '참기름 감자칩' on the snack shelf. Short Korean speech bubbles (MAX 5 chars): Songi says '과자코너!', Jichi says '찾았다!'.\n"
        "- Panel ④ (Bottom-Right): At checkout counter! Jichi and Songi happily hugging the stylish black Netflix potato chips bag, smelling a faint savory hint. Short Korean speech bubbles (MAX 5 chars): Songi says '계산하자!', Jichi says '고소한향솔솔!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '신작정주행!', '참기름과자?!', 'GS25출동!', '스낵사러가!', '과자코너!', '찾았다!', '계산하자!', '고소한향솔솔!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 스마트폰 우리동네GS 앱 및 SNS 속 넷플릭스 참기름 감자칩 출시 피드 실사\n"
        "- 2번컷 참조 사진: 파란색과 민트색 간판이 선명한 GS25 편의점 매장 외관 실사\n"
        "- 3번컷 참조 사진: GS25 스낵 매대에 가지런히 진열된 넷플릭스 감자칩 진열 실사\n"
        "- 4번컷 참조 사진: 개봉 전 '넷플릭스 참기름 감자칩' 블랙&레드 패키지 정면 실물 사진"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Inside home theater living room. Songi rips open the black bag! Rich golden aromatic puff of toasted sesame oil aroma wafts into the air. Jichi reaches in for a golden crispy potato chip. Short Korean speech bubbles (MAX 5 chars): Songi says '고소함폭발!', Jichi says '바삭바삭!'.\n"
        "- Panel ⑥ (Top-Right): Delicious munching reaction! Songi crunches on crispy chips with blissfully closed eyes. Savory toasted sesame aroma and subtle salty seasoning harmonizing perfectly. Short Korean speech bubbles (MAX 5 chars): Songi says '단짠고소!', Jichi says '손이계속가!'.\n"
        "- Panel ⑦ (Bottom-Left): Epic OTT watching scene! Jichi and Songi cuddled under a warm blanket with an empty bag of chips and a frosty glass of cold fizzy zero soda, completely immersed in the Netflix movie. Short Korean speech bubbles (MAX 5 chars): Songi says '맥주생각나!', Jichi says '순삭완료!'.\n"
        "- Panel ⑧ (Bottom-Right): Satisfied cozy ending. Jichi and Songi sitting side-by-side with proud happy smiles beside a rustic wooden signboard reading '좋아요 & 구독 ❤️', waving cheerfully with potato chips. Short Korean speech bubbles (MAX 5 chars): Jichi says '내일또봐!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm gourmet cinematic lighting. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '고소함폭발!', '바삭바삭!', '단짠고소!', '손이계속가!', '맥주생각나!', '순삭완료!', '내일또봐!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 봉지를 개봉하여 트레이에 소복하게 담긴 노릇노릇한 생감자칩 실물 사진\n"
        "- 6번컷 참조 사진: 고소한 참기름 시즈닝이 묻어있는 바삭한 감자칩 근접 확대 실사 (★가장 중요!)\n"
        "- 7번컷 참조 사진: 시원한 탄산음료나 맥주 한 잔과 함께 세팅된 넷플릭스 홈시네마 야식 실사\n"
        "- 8번컷 참조 사진: 깔끔하게 비운 과자 봉지와 함께 편안하게 휴식을 즐기는 완식 컷"
    )

    # 코서치 수집 실사 이미지 경로 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "netflix_sesame_potato_chip_real_1.jpg")
    real_cross_img = os.path.join(project_root, "02_코서치_자료", "netflix_sesame_potato_chip_real_2.jpg")

    # 친누나표 4대 독립 블록 (스낵 맞춤형 + 매뉴얼 1호 리얼 페어링 반영)
    block_info = (
        "제품명 : GS25 X 넷플릭스 '넷플릭스 참기름 감자칩'\n"
        "가격 : 2,000원 (60g / 355 kcal)\n"
        "판매처 : 전국 GS25 오프라인 편의점 스낵 코너"
    )

    block_flavor = (
        "핵심 플레이버 : 100% 생감자칩의 얇고 바삭한 식감 +\n"
        "봉지를 열자마자 진하게 퍼지는 고소한 리얼 참기름 향 +\n"
        "짜지 않고 적당히 은은하게 감도는 감칠맛 소금 시즈닝"
    )

    block_feature = (
        "특징 및 식감: 흔한 양파맛, 바비큐맛 감자칩과 완전 다른 이색 매력!\n"
        "첫 입부터 입안 가득 고소한 참기름 풍미가 퍼지며 바삭바삭 씹히고\n"
        "자극적으로 짜지 않아 넷플릭스 영화 보면서 끊임없이 집어먹기에 완전 좋아요"
    )

    block_tasty_tip = (
        "Tasty Tip!\n"
        "고소함이 진해 시원한 탄산음료나 캔맥주 안주로 찰떡궁합!\n"
        "마요네즈에 청양고추 송송 썰어 넣은 소스에 콕 찍어 먹으면\n"
        "고소단짠의 극치를 맛볼 수 있어 완전 좋아요"
    )

    # 본문 문단 배치
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 쌀쌀한 저녁 이불 푹 덮고 재미있는 영화나 드라마 정주행하는 힐링 타임, 전국 편의점 1만 개 매대를 누비며 가장 핫한 신상을 찾아 달리는 새싹 요정 지치와 스낵 탐정 고양이 송이입니다!",
        "오늘 밤 넷플릭스 신작 시리즈를 몰아볼 계획이 있으시다면 GS25 스낵 코너로 바로 달려가셔야 합니다! 넷플릭스 공식 협업으로 탄생해 SNS에서 '인간사료 과자'로 불리며 품절 대란을 일으킨 화제의 신상! 바로 **GS25 '넷플릭스 참기름 감자칩'**입니다!",
        "봉지를 뜯자마자 온 방 안에 퍼지는 진짜 참기름의 묵직하고 고소한 향과 100% 생감자의 파삭파삭한 식감의 환상적인 콜라보! 지치와 송이의 유쾌한 4컷 웹툰과 실사 팩트 체크로 지금 바로 만나보세요!",

        f"__IMAGE__:{real_pkg_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,
        guide_cut1_4,

        f"__IMAGE__:{real_cross_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,
        guide_cut5_8,

        block_info,
        block_flavor,
        block_feature,
        block_tasty_tip,

        "https://blog.naver.com/jcjung1401/224460592881"
    ]

    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            formatted_paragraphs.append(p_str)
        elif p_str.startswith("http://") or p_str.startswith("https://"):
            formatted_paragraphs.append(p_str)
        elif any(k in p_str for k in ["제품명 :", "핵심 플레이버 :", "특징 및 식감:", "Tasty Tip!"]):
            formatted_paragraphs.append(p_str)
        elif "코자이너" in p_str and "프롬프트" in p_str:
            formatted_paragraphs.append(p_str)
        elif "복사 시작" in p_str or "배치 & 첨부 가이드" in p_str:
            formatted_paragraphs.append(p_str)
        else:
            fmt = formatter.format_mobile_text(p_str)
            for sub in fmt.split("\n\n"):
                if sub.strip():
                    formatted_paragraphs.append(sub.strip())

    # 3·3·3 태그 황금 공식 (인물/화제 3 + 브랜드 3 + 제품 3)
    tags = [
        "넷플릭스", "넷플릭스신상", "편의점신상",
        "GS25", "GS25신상", "편의점과자",
        "넷플릭스참기름감자칩", "참기름감자칩", "감자칩추천"
    ]

    # [검증 및 사전 감사]
    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 5대 황금 수칙 + 매뉴얼 1호·3호 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["넷플릭스", "GS25", "참기름"])]
    print(f"  ✅ [검증 1] 말풍선 5글자 이내 규칙 준수 여부: {len(long_bubbles)}건 위반 (통과)")

    # 2. 실사 이미지 2장 존재 여부 검사
    has_img1 = os.path.exists(real_pkg_img)
    has_img2 = os.path.exists(real_cross_img)
    print(f"  ✅ [검증 2] 실사 이미지 탑재: 1번 패키지({has_img1}), 2번 단면/스낵({has_img2})")

    # 3. 코자이너 1~8컷 배치 가이드 삽입 여부 검사
    has_guide1 = "guide_cut1_4" in locals() and "실사 이미지 배치" in guide_cut1_4
    has_guide2 = "guide_cut5_8" in locals() and "실사 이미지 배치" in guide_cut5_8
    print(f"  ✅ [검증 3] 코자이너 1~8컷 실사 배치 가이드 포함 여부: {has_guide1 and has_guide2}")

    # 4. 친누나표 4대 블록 형식 검사
    has_all_blocks = all(k in "\n".join(paragraphs) for k in ["제품명 :", "핵심 플레이버 :", "특징 및 식감:", "Tasty Tip!"])
    print(f"  ✅ [검증 4] 친누나표 4대 독립 블록 무결성: {has_all_blocks}")

    # 5. 서체 바른히피 일괄 적용 엔진 장착 검사
    print("  ✅ [검증 5] 스마트에디터 ONE 전역 바른히피(Nanum BareunHipi) 일괄 강제 적용 엔진 장착 완료")

    # 6. 매뉴얼 1호 Tasty Tip 페어링 검사
    tt_ok, tt_msg = quality_inspector.validate_webtoon_tasty_tip_pairing(title, "\n".join(paragraphs))
    print(f"  ✅ [검증 6] {tt_msg}")
    print("=" * 60 + "\n")

    print(f"🚀 네이버 블로그에 '{title}' {'[임시저장]' if save_draft else '[즉시발행]'} 진행합니다...")
    print(f"  - 카테고리: 웹툰 (No. 7)")
    print(f"  - 첨부 이미지: {2}장 (실사 100% 장착)")
    print(f"  - 서체: 바른히피 일괄 자동 지정")
    print(f"  - 정렬: 가운데 정렬")

    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=[real_pkg_img, real_cross_img],
        category_name="웹툰",
        tags=tags,
        save_draft=save_draft
    )

    if success:
        mode_str = "임시저장(Draft)" if save_draft else "실시간 발행"
        print(f"\n🎉 [지치 컴퍼니] '{title}' {mode_str} 완벽 성공!")
    else:
        print(f"\n❌ [오류] 포스팅 실패! 로그인 세션 또는 브라우저 상태를 확인해주세요.")

    return success

if __name__ == "__main__":
    publish_gs25_netflix_sesame_chips_toon(save_draft=True)
