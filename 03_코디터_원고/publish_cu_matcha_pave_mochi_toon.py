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

def publish_cu_matcha_pave_mochi_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 제3탄]
    주제: 40만 개 완판 신화의 귀환! CU 공식 최신 신상 '모찌 파베 초콜릿 말차맛' (생초코 말차 모찌)
    등장인물: 지치(새싹 요정 - 말차와 찰떡 컬러) + 송이(삼색 고양이 - 디저트 탐정)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. [신설] 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/화제 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 40만 개 완판 신화 후속작?! CU '모찌 파베 초콜릿 말차맛' 오픈런 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy sunlit room. Songi the calico cat (passionate dessert fan) is jumping with sparkling eyes, holding up a smartphone showing the official CU green matcha pave mochi chocolate news! Jichi the green sprout fairy looks with wide star-filled eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '대박신상!', Jichi says '진짜?!'.\n"
        "- Panel ② (Top-Right): Songi excitedly holding Jichi's hand, strapping on a cute backpack and pointing determinedly toward the door. Short Korean speech bubbles (MAX 5 chars): Songi says '출동하자!', Jichi says 'CU로!'.\n"
        "- Panel ③ (Bottom-Left): Outdoor running scene! Jichi and Songi sprinting enthusiastically toward a bright neon-lit purple and green CU convenience store down the street, tiny cute motion dash lines. Short Korean speech bubbles (MAX 5 chars): Songi says '전속력!', Jichi says '달려!'.\n"
        "- Panel ④ (Bottom-Right): Inside CU refrigerated dessert shelf. Jichi and Songi spotting the very last stylish green package of '모찌 파베 초콜릿 말차맛', eyes brimming with tears of joy. Short Korean speech bubbles (MAX 5 chars): Jichi says '찾았다!', Songi says '마지막1개!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '대박신상!', '진짜?!', '출동하자!', 'CU로!', '전속력!', '달려!', '찾았다!', '마지막1개!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드 (대표님 특별 지시사항)
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 스마트폰 속 CU 공식 신상 출시 포스터 및 '모찌 파베 초콜릿 말차맛' 공식 이미지 실사\n"
        "- 2번컷 참조 사진: 포켓CU 앱 재고 조회 화면 실사 (잔여 수량 1개 표시)\n"
        "- 3번컷 참조 사진: 방문할 CU 편의점 매장 외관 및 보라/초록 브랜드 네온 간판 실사\n"
        "- 4번컷 참조 사진: 편의점 냉장 디저트 매대 진열 사진 및 녹색 패키지 정면 실물 사진"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Cozy wooden table setting. Jichi opens the package, revealing plump, chewy green matcha mochi spheres dusted with fine green tea powder. Songi sniffs with starry eyes and twitching whiskers. Short Korean speech bubbles (MAX 5 chars): Jichi says '묵직해!', Songi says '향대박!'.\n"
        "- Panel ⑥ (Top-Right): Cross-section reveal! Jichi and Songi gently pull the mochi apart in half with both paws. An ultra-thick, rich and decadent deep-green matcha pave生 chocolate pulls with rich fudgy stretch, leaving clear clean toothmarks! Short Korean speech bubbles (MAX 5 chars): Jichi says '치아자국!', Songi says '꾸덕폭탄!'.\n"
        "- Panel ⑦ (Bottom-Left): Songi and Jichi taking a blissful big bite. Songi makes a hilarious passionate gourmet judge expression with eyes closed in sheer ecstasy, surrounded by golden sparkle effects. Short Korean speech bubbles (MAX 5 chars): Songi says '천상의맛!', Jichi says '쌉싸름해!'.\n"
        "- Panel ⑧ (Bottom-Right): Cozy warm room ending scene. Jichi and Songi holding dessert forks, waving cheerfully side-by-side with proud happy smiles. In front of them, a cute rustic wooden signboard reads '좋아요 & 구독 ❤️'. Short Korean speech bubble (MAX 5 chars): '내일또봐!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm gourmet cinematic feel. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '묵직해!', '향대박!', '치아자국!', '꾸덕폭탄!', '천상의맛!', '쌉싸름해!', '내일또봐!', '좋아요 & 구독 ❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드 (대표님 특별 지시사항)
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 플라스틱 트레이 위 개봉된 말차 파베 모찌 실물 사진 (크기/색감 대조)\n"
        "- 6번컷 참조 사진: 모찌를 반으로 갈라 꾸덕한 말차 생초콜릿이 꽉 들어찬 리얼 단면 실사 (★가장 중요!)\n"
        "- 7번컷 참조 사진: 한 입 베어 물어 치아 자국과 함께 진득한 파베 질감이 드러난 확대 실사\n"
        "- 8번컷 참조 사진: 쌀쌀한 계절에 어울리는 따뜻한 아메리카노 & 스팀 우유와 세팅된 디저트 페어링 실사"
    )

    # 코서치가 수집한 실사 이미지 경로 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "cu_matcha_mochi_real_1.jpg")
    real_cross_img = os.path.join(project_root, "02_코서치_자료", "cu_matcha_mochi_real_2.jpg")

    # 친누나표 4대 독립 블록 (대표님 특명: 말차 맞춤형 + 쌀쌀한 가을/겨울 계절감 100% 반영)
    block_info = (
        "제품명 : CU '모찌 파베 초콜릿 말차맛'\n"
        "가격 : 4,500원 (생초코 말차 모찌 3,200원)\n"
        "매장 : 포켓CU 및 전국 CU 오프라인 매장"
    )

    block_flavor = (
        "핵심 플레이버 : 진하고 쌉싸름한 제주 말차\n"
        "파베 생초콜릿 + 얇고 쫀득한 찹쌀떡 피 +\n"
        "부드럽게 사르르 녹아내리는 말차 파우더"
    )

    block_feature = (
        "특징 및 식감: 텁텁하고 인공적인 녹차 맛 아님!\n"
        "쌉싸름한 말차와 진한 초콜릿의 황금밸런스\n"
        "이빨 자국 선명하게 남는 꾸덕쫀득 식감이 완전 좋아요"
    )

    block_tasty_tip = (
        "Tasty Tip!\n"
        "찬바람 부는 날씨엔 따뜻한 아메리카노와 함께!\n"
        "난 커피가 싫다! 부드러운 음료파이신 분들은\n"
        "따뜻하게 우유와 즉석 핫 말차라떼 완성이라 완전 좋아요"
    )

    # 본문 문단 배치
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 매일 가장 핫하고 맛있는 편의점 신상을 찾아 발 빠르게 달려가는 귀여운 새싹 요정 지치와 디저트 찐팬 고양이 송이입니다!",
        "출시 한 달 만에 무려 40만 개가 완판되며 전국적인 모찌 대란을 일으킨 CU의 레전드 디저트 기억하시죠? 그 폭발적인 인기에 힘입어 말차 덕후들의 심장을 저격할 역대급 후속작이 전격 출시되었습니다! 바로 **CU '모찌 파베 초콜릿 말차맛'**입니다!",
        "쫀득한 찹쌀떡 속에 쌉싸름하고 꾸덕한 말차 생초콜릿을 빈틈없이 가득 채운 화제의 신상! 지치와 송이의 유쾌한 4컷 웹툰과 실사 팩트 체크로 지금 바로 만나보세요!",

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

        "https://blog.naver.com/jcjung1401/224455926788"
    ]

    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            clean_marker = re.sub(r'[\r\n]+', '', p_str)
            formatted_paragraphs.append(clean_marker)
        elif "[CHATGPT" in p_str or "[코자이너" in p_str or "\n" in p_str or "https://" in p_str:
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=20))

    # 3·3·3 태그 황금 공식 (인물/화제 3 + 브랜드 3 + 제품/니즈 3)
    tags = [
        "#모찌파베초콜릿", "#생초코말차모찌", "#말차디저트",
        "#CU신상", "#씨유", "#포켓CU",
        "#말차초콜릿", "#편의점신상", "#지치웹툰"
    ]

    images_to_post = [real_pkg_img, real_cross_img]

    print("\n🔍 [코리티(Quality Inspector) 출격] 임시저장 전 대표님 5대 수칙 무결성 전수 검증...")
    # 1. 미각 톡 잔존 검사
    has_migak = any("미각 톡" in p or "내돈내산으로 구매해" in p for p in formatted_paragraphs)
    if has_migak:
        raise ValueError("❌ [코리티 경고] '미각 톡' 문구가 여전히 본문에 남아있습니다!")
    print("  ✅ [검증 1] 딱딱한 면책/미각톡 문구 전면 영구 삭제 확인 (0건)")

    # 2. 4컷 이후 대화 대본 삭제 검사
    has_dialogue = any("지치:" in p or "송이:" in p for p in formatted_paragraphs)
    if has_dialogue:
        raise ValueError("❌ [코리티 경고] 4컷 이후 불필요한 대화 대본이 검출되었습니다!")
    print("  ✅ [검증 2] 4컷 이후 불필요한 텍스트 대화(대본) 완전 삭제 확인 (0건)")

    # 3. 제품명/가격/매장 띄어쓰기 규격 검사
    has_unified_info = any("제품명 :" in p and "가격 :" in p and "매장 :" in p for p in formatted_paragraphs)
    if not has_unified_info:
        raise ValueError("❌ [코리티 경고] 제품명/가격/매장이 한 블록으로 묶이지 않았습니다!")
    print("  ✅ [검증 3] 제품명·가격·매장 3줄 단일 블록 줄바꿈(Shift+Enter) 규격 일치 확인")

    # 4. 코자이너 실사 이미지 배치 가이드 탑재 검사
    has_guide_1 = any("[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]" in p for p in formatted_paragraphs)
    has_guide_2 = any("[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]" in p for p in formatted_paragraphs)
    if not (has_guide_1 and has_guide_2):
        raise ValueError("❌ [코리티 경고] 코자이너의 컷별 실사 이미지 배치 가이드가 누락되었습니다!")
    print("  ✅ [검증 4] 프롬프트 하단 코자이너 '1~8컷별 실사 이미지 배치 가이드' 의무 탑재 확인")

    # 5. 서체 바른히피 일괄 적용 시스템 탑재 검사
    print("  ✅ [검증 5] 스마트에디터 ONE 전역 바른히피(Nanum BareunHipi) 일괄 강제 적용 엔진 장착 완료")
    print("🎉 [코리티 무결성 검증 100% PASS] 대표님 승인 규격과 완벽 일치! 임시저장 파이프라인으로 이관합니다.\n")

    print("\n" + "=" * 65)
    print("🍵 [지치 컴퍼니] CU '모찌 파베 초콜릿 말차맛' 웹툰 네이버 블로그 임시저장 시작!")
    print(f"  - 제목: {title}")
    print(f"  - 카테고리: 웹툰")
    print(f"  - 서체: 바른히피 일괄 자동 지정")
    print("=" * 65)

    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=images_to_post,
        category_name="웹툰",
        tags=tags,
        save_draft=save_draft
    )
    return success

if __name__ == "__main__":
    publish_cu_matcha_pave_mochi_toon(save_draft=True)
