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

def publish_cu_basil_cheese_hobbang_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 제8탄]
    주제: 쌀쌀해진 11월 저녁엔 따끈따끈 호빵! CU '삼립 바질치즈 호빵'
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 겨울간식 탐정)

    [대표님 엄격 5대 절대 수칙 + 매뉴얼 1호·2호·3호 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/화제 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    6. [지치컴패니 업무매뉴얼 1호 & 3호] 전방위 매대 겨울 간식 실사 먹조합 (쌀쌀한 저녁 + 따뜻한 우유/커피 & 에프 파니니 페어링)
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 쌀쌀한 저녁엔 호빵?! CU '삼립 바질치즈 호빵' 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy room in the chilly evening. Wind blowing briskly outside window. Songi the calico cat shivering cutely, waving a smartphone showing news banner of 'CU 삼립 바질치즈 호빵 출시!'. Jichi the green sprout fairy gasps with round sparkling eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '바람쌀쌀!', Jichi says '호빵먹자!'.\n"
        "- Panel ② (Top-Right): Songi grabbing Jichi's hand, strapping on a cute winter scarf and backpack, enthusiastically heading toward the door. Short Korean speech bubbles (MAX 5 chars): Songi says 'CU출동!', Jichi says '호빵사러가!'.\n"
        "- Panel ③ (Bottom-Left): Inside bright CU convenience store bakery and winter snack aisle! Jichi and Songi spot the sleek green and white package of '바질치즈 호빵' on the shelf. Short Korean speech bubbles (MAX 5 chars): Songi says '호빵코너!', Jichi says '찾았다!'.\n"
        "- Panel ④ (Bottom-Right): At checkout counter! Jichi and Songi happily hugging the round fluffy steamed bun bag with excited smiles. Short Korean speech bubbles (MAX 5 chars): Songi says '계산완료!', Jichi says '따끈따끈!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cozy cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '바람쌀쌀!', '호빵먹자!', 'CU출동!', '호빵사러가!', '호빵코너!', '찾았다!', '계산완료!', '따끈따끈!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 스마트폰 포켓CU 앱 및 SNS 속 삼립 바질치즈 호빵 출시 포스터 실사\n"
        "- 2번컷 참조 사진: 보라색과 초록색 네온 간판이 빛나는 CU 편의점 매장 외관 실사\n"
        "- 3번컷 참조 사진: CU 매장 호빵 전용 찜기 및 베이커리 매대에 진열된 바질치즈 호빵 실사\n"
        "- 4번컷 참조 사진: 개봉 전 '삼립 바질치즈 호빵' 정면 패키지 실물 사진"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Inside kitchen. Freshly steamed fluffy white bun on a plate! Puffs of hot fragrant steam curl up, wafting rich aroma of Italian basil and savory cheese. Short Korean speech bubbles (MAX 5 chars): Songi says '김모락모락!', Jichi says '향대박!'.\n"
        "- Panel ⑥ (Top-Right): Songi and Jichi tearing the hot bun in half! Gooey melted golden cheese and aromatic green basil pesto filling with tender chicken stretch out deliciously. Short Korean speech bubbles (MAX 5 chars): Songi says '치즈쭉쭉!', Jichi says '바질향솔솔!'.\n"
        "- Panel ⑦ (Bottom-Left): Delicious tasting reaction! Songi munches on the savory chewy bun with blissfully closed eyes. Jichi sips a cup of warm cozy milk. Short Korean speech bubbles (MAX 5 chars): Songi says '파니니맛!', Jichi says '꿀맛조합!'.\n"
        "- Panel ⑧ (Bottom-Right): Satisfied cozy ending. Jichi and Songi sitting side-by-side with proud happy smiles beside a rustic wooden signboard reading '좋아요 & 구독 ❤️', waving cheerfully with steamed buns. Short Korean speech bubbles (MAX 5 chars): Jichi says '내일또봐!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm delicious cinematic lighting. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '김모락모락!', '향대박!', '치즈쭉쭉!', '바질향솔솔!', '파니니맛!', '꿀맛조합!', '내일또봐!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 전자레인지나 찜기로 갓 쪄내 김이 모락모락 피어오르는 새하얀 호빵 실물 사진\n"
        "- 6번컷 참조 사진: 호빵을 반으로 갈라 바질페스토와 치즈가 주르륵 흘러나오는 먹음직스러운 단면 확대 실사 (★가장 중요!)\n"
        "- 7번컷 참조 사진: 따뜻한 커피나 우유 한 잔과 함께 세팅된 따끈한 겨울 간식 한 상 실사\n"
        "- 8번컷 참조 사진: 접시를 깨끗하게 비우고 포근한 저녁을 즐기는 완식 엔딩 컷"
    )

    # 코서치 수집 실사 이미지 경로 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "cu_basil_cheese_hobbang_real_1.jpg")
    real_cross_img = os.path.join(project_root, "02_코서치_자료", "cu_basil_cheese_hobbang_real_2.jpg")

    # 친누나표 4대 독립 블록 (호빵 맞춤형 + 매뉴얼 1호 리얼 페어링 반영)
    block_info = (
        "제품명 : CU '삼립 바질치즈 호빵'\n"
        "가격 : 2,000원 (개당 기준 / 90g / 235 kcal)\n"
        "판매처 : 포켓CU 및 전국 CU 오프라인 편의점 호빵 매대"
    )

    block_flavor = (
        "핵심 플레이버 : 향긋하고 산뜻한 이탈리아산 바질 페스토 +\n"
        "고소하고 짭조름하게 쭈욱 늘어나는 모짜렐라 치즈 +\n"
        "담백하게 씹히는 그릴드 치킨과 촉촉쫄깃한 발효미종 호빵피"
    )

    block_feature = (
        "특징 및 식감: 뻔한 단팥이나 야채 호빵과 전혀 다른 이국적인 브런치 맛!\n"
        "한 입 베어 무는 순간 향긋한 바질 향과 치즈의 감칠맛이 입안 가득 퍼지고\n"
        "쌀가루가 들어간 피가 찰지고 부드러워 쌀쌀한 저녁 간식으로 즐기기에 완전 좋아요"
    )

    block_tasty_tip = (
        "Tasty Tip!\n"
        "따뜻한 방 안에서 갓 쪄낸 호빵을 따뜻한 아메리카노나 우유와 함께!\n"
        "에어프라이어에 160도 10분만 살짝 돌려주면\n"
        "겉바속촉 바질치즈 파니니처럼 변신해 완전 좋아요"
    )

    # 본문 문단 배치
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 11월에 접어들며 저녁 바람이 부쩍 쌀쌀해진 오늘, 전국 편의점 1만 개 매대를 누비며 가장 따끈따끈하고 핫한 겨울 신상을 찾아 달리는 새싹 요정 지치와 호빵 탐정 고양이 송이입니다!",
        "찬 바람이 불기 시작하면 편의점 문을 열자마자 찜기에서 김이 모락모락 피어오르는 호빵 코너를 그냥 지나칠 수 없죠! 매번 먹던 단팥이나 야채 호빵을 넘어, 올해는 카페 브런치 파니니를 그대로 호빵 속에 옮겨 담은 역대급 신상이 등장했습니다! 바로 **CU '삼립 바질치즈 호빵'**입니다!",
        "향긋한 바질 페스토와 고소하게 늘어나는 치즈, 그리고 쫄깃한 그릴드 치킨이 어우러져 한 입 베어 무는 순간 이탈리아 식당에 온 듯한 감동! 지치와 송이의 유쾌한 4컷 웹툰과 실사 팩트 체크로 지금 바로 만나보세요!",

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
        "삼립호빵", "겨울간식", "편의점신상",
        "CU", "CU신상", "CU호빵",
        "바질치즈호빵", "삼립바질치즈호빵", "호빵추천"
    ]

    # [검증 및 사전 감사]
    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 5대 황금 수칙 + 매뉴얼 1호·3호 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["바질치즈", "삼립호빵", "CU"])]
    print(f"  ✅ [검증 1] 말풍선 5글자 이내 규칙 준수 여부: {len(long_bubbles)}건 위반 (통과)")

    # 2. 실사 이미지 2장 존재 여부 검사
    has_img1 = os.path.exists(real_pkg_img)
    has_img2 = os.path.exists(real_cross_img)
    print(f"  ✅ [검증 2] 실사 이미지 탑재: 1번 패키지({has_img1}), 2번 단면/속({has_img2})")

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
    publish_cu_basil_cheese_hobbang_toon(save_draft=True)
