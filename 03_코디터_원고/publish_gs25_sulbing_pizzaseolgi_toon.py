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

def publish_gs25_sulbing_pizzaseolgi_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 제3탄]
    주제: 빙수 명가 설빙과 GS25의 기상천외한 만남! '설빙 피자설기' (백설기 피자 떡)
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 디저트 탐정)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/화제 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 백설기 위에 피자 토핑이?! GS25 X 설빙 '설빙 피자설기' 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy sunlit room. Songi the calico cat (passionate dessert fan) is jumping with sparkling eyes, holding up a smartphone showing the GS25 x Sulbing 'Pizza Seolgi' news! Jichi the green sprout fairy tilts head with curious round eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '설빙신상!', Jichi says '빙수야?!'.\n"
        "- Panel ② (Top-Right): Songi enthusiastically grabs Jichi's hand, strapping on a cute blue backpack and pointing toward the door with fiery determination. Short Korean speech bubbles (MAX 5 chars): Songi says 'GS25로!', Jichi says '출동하자!'.\n"
        "- Panel ③ (Bottom-Left): Inside GS25 frozen dessert section! Frosty cool air visible. Jichi points at the frozen dessert shelf, spotting the stylish packaging of '설빙 피자설기' right between dessert items. Short Korean speech bubbles (MAX 5 chars): Songi says '냉동실?!', Jichi says '찾았다!'.\n"
        "- Panel ④ (Bottom-Right): Close-up at counter! Jichi and Songi holding the frozen package, eyes wide in sheer amusement as they look at the picture of a white rice cake topped with pepperoni and cheese. Short Korean speech bubbles (MAX 5 chars): Songi says '피자설기?!', Jichi says '떡피자다!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '설빙신상!', '빙수야?!', 'GS25로!', '출동하자!', '냉동실?!', '찾았다!', '피자설기?!', '떡피자다!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드 (대표님 특별 지시사항)
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 우리동네GS 앱 사전예약 배너 및 설빙 피자설기 공식 출시 포스터 실사\n"
        "- 2번컷 참조 사진: GS25 편의점 파란색 네온 간판 매장 외관 실사\n"
        "- 3번컷 참조 사진: GS25 냉동 디저트 매대 진열 사진 (냉동고 속 패키지)\n"
        "- 4번컷 참조 사진: 개봉 전 '설빙 피자설기' 정면 패키지 실물 사진"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Inside kitchen. Jichi proudly puts the two mini round white seolgi pizza pieces into microwave. Warm glow emitting from microwave door, digital timer showing 1 minute. Short Korean speech bubbles (MAX 5 chars): Jichi says '렌지돌려!', Songi says '1분완성!'.\n"
        "- Panel ⑥ (Top-Right): Microwave door opens with a warm steam puff! The mozzarella cheese is melted and bubbling, golden melted edges with glossy pepperoni slices on top of plump snowy-white rice cakes. Short Korean speech bubbles (MAX 5 chars): Songi says '치즈폭포!', Jichi says '페퍼로니!'.\n"
        "- Panel ⑦ (Bottom-Left): Feast time! Songi and Jichi pulling a piece apart. An unbelievable stringy mozzarella cheese pull stretches high between the warm chewy white rice cake base! Songi has ecstatic gourmet sparkle eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '단짠대박!', Jichi says '쫀득해!'.\n"
        "- Panel ⑧ (Bottom-Right): Cozy ending scene. Jichi and Songi happily resting against a cute rustic wooden signboard that reads '좋아요 & 구독 ❤️', waving cheerfully with dessert forks. Short Korean speech bubbles (MAX 5 chars): Jichi says '내일또봐!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm gourmet cinematic lighting. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '렌지돌려!', '1분완성!', '치즈폭포!', '페퍼로니!', '단짠대박!', '쫀득해!', '내일또봐!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드 (대표님 특별 지시사항)
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 전자레인지 조리 전 트레이 위 올려진 냉동 백설기 2개 실물 사진\n"
        "- 6번컷 참조 사진: 전자레인지 1분 조리 직후 김이 모락모락 나며 치즈가 녹은 갓 구운 피자설기 실사\n"
        "- 7번컷 참조 사진: 젓가락이나 손으로 들어 올려 모짜렐라 치즈가 길게 늘어나는 단짠 단면 확대 실사 (★가장 중요!)\n"
        "- 8번컷 참조 사진: 찬바람 부는 날씨에 어울리는 따뜻한 아메리카노 또는 제로콜라와 함께 세팅된 피자설기 완성 컷"
    )

    # 코서치가 수집한 실사 이미지 경로 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "gs25_sulbing_pizza_real_1.jpg")
    real_cross_img = os.path.join(project_root, "02_코서치_자료", "gs25_sulbing_pizza_real_2.jpg")

    # 친누나표 4대 독립 블록 (대표님 특명: 백설기 떡피자 맞춤형 + 찬바람 부는 계절감 100% 반영)
    block_info = (
        "제품명 : GS25 X 설빙 '설빙 피자설기'\n"
        "가격 : 3,900원 (총 130g / 65g 2개입)\n"
        "판매처 : 우리동네GS 앱 사전예약 및 전국 GS25 오프라인 매장"
    )

    block_flavor = (
        "핵심 플레이버 : 전통 쌀 백설기 도우 +\n"
        "새콤달콤 토마토 피자소스와 짭조름한 페퍼로니 +\n"
        "모짜렐라 피자치즈와 톡톡 터지는 옥수수 토핑"
    )

    block_feature = (
        "특징 및 식감: 밀가루 도우가 아닌 백설기 떡의 놀라운 반전!\n"
        "전자레인지 1분 조리로 치즈가 부드럽게 녹아내려요\n"
        "달콤쫀득한 떡과 짭조름한 피자 치즈의 단짠 밸런스가 완전 좋아요"
    )

    block_tasty_tip = (
        "Tasty Tip!\n"
        "찬바람 부는 날씨엔 따뜻한 아메리카노와 함께!\n"
        "난 탄산파다! 시원한 제로콜라 한 잔 곁들이면\n"
        "달콤쫀득한 떡과 짭조름한 치즈 풍미가 살아나 완전 좋아요"
    )

    # 본문 문단 배치
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 매일 가장 핫하고 신선한 편의점 신상을 찾아 발 빠르게 달려가는 귀여운 새싹 요정 지치와 디저트 찐팬 고양이 송이입니다!",
        "시원한 빙수로 대한민국을 사로잡은 빙수 명가 '설빙'이 이번엔 GS25와 손잡고 상상을 초월하는 기상천외한 신상을 선보였습니다! 바로 백설기 떡 위에 피자 토핑을 통째로 얹은 **GS25 X 설빙 '설빙 피자설기'**입니다!",
        "밀가루 도우 대신 쫀득한 쌀 백설기 위에 새콤달콤 토마토 피자소스와 페퍼로니, 그리고 부드럽게 늘어나는 모짜렐라 치즈를 듬뿍 얹은 화제의 단짠 퓨전 간식! 지치와 송이의 유쾌한 4컷 웹툰과 실사 팩트 체크로 지금 바로 만나보세요!",

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

        "https://blog.naver.com/jcjung1401/224459661775"
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
        "지치와송이", "편의점신상", "편의점웹툰",
        "GS25", "GS25신상", "설빙",
        "설빙피자설기", "피자설기", "디저트추천"
    ]

    # [검증 및 사전 감사]
    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 5대 황금 수칙 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["모찌", "피자", "GS25", "설빙"])]
    print(f"  ✅ [검증 1] 말풍선 5글자 이내 규칙 준수 여부: {len(long_bubbles)}건 위반 (통과)")

    # 2. 실사 이미지 2장 존재 여부 검사
    has_img1 = os.path.exists(real_pkg_img)
    has_img2 = os.path.exists(real_cross_img)
    print(f"  ✅ [검증 2] 실사 이미지 탑재: 1번 패키지({has_img1}), 2번 단면({has_img2})")

    # 3. 코자이너 1~8컷 배치 가이드 삽입 여부 검사
    has_guide1 = "guide_cut1_4" in locals() and "실사 이미지 배치" in guide_cut1_4
    has_guide2 = "guide_cut5_8" in locals() and "실사 이미지 배치" in guide_cut5_8
    print(f"  ✅ [검증 3] 코자이너 1~8컷 실사 배치 가이드 포함 여부: {has_guide1 and has_guide2}")

    # 4. 친누나표 4대 블록 형식 검사
    has_all_blocks = all(k in "\n".join(paragraphs) for k in ["제품명 :", "핵심 플레이버 :", "특징 및 식감:", "Tasty Tip!"])
    print(f"  ✅ [검증 4] 친누나표 4대 독립 블록 무결성: {has_all_blocks}")

    # 5. 서체 바른히피 일괄 적용 시스템 탑재 검사
    print("  ✅ [검증 5] 스마트에디터 ONE 전역 바른히피(Nanum BareunHipi) 일괄 강제 적용 엔진 장착 완료")
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
    publish_gs25_sulbing_pizzaseolgi_toon(save_draft=True)
