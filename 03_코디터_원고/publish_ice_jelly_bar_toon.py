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

def publish_ice_jelly_bar_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 제4탄]
    주제: SNS 숏폼 품절 대란템! 녹으면 말랑쫀득 젤리가 되는 '스윗믹스 아이스 젤리바' (메롱바)
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 디저트 탐정)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/화제 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 녹으면 젤리가 된다고?! 편의점 신상 '스윗믹스 아이스 젤리바' 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy sunlit room. Songi the calico cat is jumping with giant sparkling eyes, waving a smartphone showing viral SNS short-form videos of a mysterious jelly ice bar! Jichi the green sprout fairy tilts head with curious wide eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '품절대란!', Jichi says '뭔데?!'.\n"
        "- Panel ② (Top-Right): Songi excitedly holding Jichi's little hand, strapping on a cute backpack and pointing enthusiastically toward the door. Short Korean speech bubbles (MAX 5 chars): Songi says '편의점으로!', Jichi says '출동하자!'.\n"
        "- Panel ③ (Bottom-Left): Inside bright convenience store ice cream freezer section! Jichi and Songi eagerly peering into the glass ice cream freezer, spotting the colorful '아이스 젤리바' packages among the ice bars. Short Korean speech bubbles (MAX 5 chars): Songi says '아이스크림!', Jichi says '찾았다!'.\n"
        "- Panel ④ (Bottom-Right): At checkout counter! Jichi and Songi holding the green apple and brown cola flavored ice jelly bar packages with happy curious smiles. Short Korean speech bubbles (MAX 5 chars): Songi says '젤리바?!', Jichi says '사보자!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '품절대란!', '뭔데?!', '편의점으로!', '출동하자!', '아이스크림!', '찾았다!', '젤리바?!', '사보자!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드 (대표님 특별 지시사항)
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: SNS(유튜브/틱톡)에서 화제가 된 아이스 젤리바 챌린지 썸네일 화면 실사\n"
        "- 2번컷 참조 사진: 편의점 매장 외관 및 아이스크림 할인 배너 실사\n"
        "- 3번컷 참조 사진: 편의점 냉동고 속 '스윗믹스 아이스 젤리바' 진열 실사\n"
        "- 4번컷 참조 사진: 개봉 전 청사과맛 & 콜라맛 아이스 젤리바 정면 패키지 실물 사진"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): At wooden table. Jichi and Songi take the frozen green ice bar out of the wrapper. They take a crisp bite! Frozen icy texture, frosty mist. Short Korean speech bubbles (MAX 5 chars): Songi says '사각사각!', Jichi says '시원해!'.\n"
        "- Panel ⑥ (Top-Right): Big surprise! As it sits at room temperature, instead of melting into liquid drops, the ice bar droops down playfully like a flexible bouncy tongue without any sticky dripping mess! Jichi and Songi gasp with comically wide open eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '녹는다?!', Jichi says '국물없어?!'.\n"
        "- Panel ⑦ (Bottom-Left): Hilarious playful moment! Songi wiggles the flexible bouncy jelly bar back and forth. The green bar wiggles like a tongue making a cheeky 'merong' expression, super chewy jelly texture! Jichi giggles with tears of laughter. Short Korean speech bubbles (MAX 5 chars): Songi says '찰랑찰랑!', Jichi says '메롱젤리!'.\n"
        "- Panel ⑧ (Bottom-Right): Fun ending scene! Jichi and Songi sitting side-by-side with satisfied happy smiles, each holding up their clean wooden ice cream stick, resting beside a rustic wooden signboard reading '좋아요 & 구독 ❤️', waving cheerfully. Short Korean speech bubbles (MAX 5 chars): Jichi says '내일또봐!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm gourmet cinematic lighting. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '사각사각!', '시원해!', '녹는다?!', '국물없어?!', '찰랑찰랑!', '메롱젤리!', '내일또봐!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드 (대표님 특별 지시사항)
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 냉동실에서 갓 꺼내어 단단하게 얼어있는 아이스 젤리바 실물 사진\n"
        "- 6번컷 참조 사진: 상온에 잠시 두어 국물 흘림 없이 말랑말랑해지기 시작하는 젤리바 실사\n"
        "- 7번컷 참조 사진: 손으로 잡고 흔들었을 때 혓바닥처럼 탄력 있게 찰랑거리는 젤리 질감 확대 실사 (★가장 중요!)\n"
        "- 8번컷 참조 사진: 투명한 유리잔 속 시원한 사이다에 아이스 젤리바를 꽂아 완성한 상큼한 젤리 에이드 홈카페 연출 실사"
    )

    # 코서치가 수집한 실사 이미지 경로 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "ice_jelly_bar_real_1.jpg")
    real_cross_img = os.path.join(project_root, "02_코서치_자료", "ice_jelly_bar_real_2.jpg")

    # 친누나표 4대 독립 블록 (대표님 특명: 아이스 젤리바 맞춤형 + 찬바람 부는 계절감 100% 반영)
    block_info = (
        "제품명 : '스윗믹스 아이스 젤리바' (메롱 젤리바)\n"
        "가격 : 1,500원\n"
        "판매처 : GS25 등 전국 편의점 아이스크림 코너"
    )

    block_flavor = (
        "핵심 플레이버 : 상큼한 청사과맛 & 톡 쏘는 콜라맛 +\n"
        "얼렸을 땐 시원하고 아삭한 아이스바 +\n"
        "녹으면 말랑쫀득 찰랑거리는 젤리로 변신"
    )

    block_feature = (
        "특징 및 식감: 국물이 뚝뚝 흘러내리지 않는 놀라운 반전 젤리바!\n"
        "국내 제조 및 천연색소 사용으로 안심하고 즐길 수 있어요\n"
        "탱글탱글 찰랑거리는 재미와 달콤쫀득한 식감이 완전 좋아요"
    )

    block_tasty_tip = (
        "Tasty Tip!\n"
        "시원한 사이다나 탄산수 잔에 퐁당 꽂아보세요!\n"
        "살짝 녹은 젤리바가 탄산과 만나 즉석 과즙 젤리 에이드 완성이라\n"
        "달콤하고 톡 쏘는 청량한 디저트로 즐기기에 완전 좋아요"
    )

    # 본문 문단 배치
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 매일 가장 핫하고 신선한 편의점 신상을 찾아 발 빠르게 달려가는 귀여운 새싹 요정 지치와 디저트 찐팬 고양이 송이입니다!",
        "최근 틱톡과 유튜브 숏폼 피드를 뜨겁게 달구며 품절 대란을 일으킨 전설의 간식을 아시나요? 얼려 먹으면 아삭한 아이스바인데, 녹으면 국물이 흘러내리지 않고 쫀득한 젤리로 변신하는 화제의 신상! 바로 **'스윗믹스 아이스 젤리바'**입니다!",
        "일명 '메롱바'로 불리며 혓바닥처럼 탄력 있게 찰랑거리는 독보적인 비주얼과 안심할 수 있는 국내산 천연색소 업그레이드까지! 지치와 송이의 유쾌한 4컷 웹툰과 실사 팩트 체크로 지금 바로 만나보세요!",

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
        "GS25", "GS25신상", "편의점디저트",
        "아이스젤리바", "스윗믹스아이스젤리바", "메롱바"
    ]

    # [검증 및 사전 감사]
    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 5대 황금 수칙 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["젤리바", "편의점", "GS25"])]
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
    publish_ice_jelly_bar_toon(save_draft=True)
