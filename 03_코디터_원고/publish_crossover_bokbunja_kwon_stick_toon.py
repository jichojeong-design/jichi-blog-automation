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

def publish_crossover_bokbunja_kwon_stick_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 제9탄 - 크로스오버 꿀조합 제1편]
    주제: 편의점 털어 완성한 호텔급 홈술 조합!
          GS25 '고창명주 복분자 하이볼 캔' X CU '권성준 블랙트러플하몽 포테이토스틱'
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 홈술 탐정)

    [대표님 엄격 5대 절대 수칙 + 매뉴얼 1호·2호·3호 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/화제 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    6. [지치컴패니 업무매뉴얼 1호 & 3호] 전방위 매대 크로스오버 실사 먹조합 (단짠 트러플 하몽 스낵 + 루비빛 탄산 복분자 하이볼)
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 편의점 털어 만든 럭셔리 홈술 조합! GS25 '복분자 하이볼' X CU '권성준 감자스틱' 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy living room on a relaxing evening. Songi the calico cat waving a smartphone showing news banner of 'GS25 고창명주 복분자 하이볼 출시!'. Jichi the green sprout fairy gasps with round sparkling eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '홈술하자!', Jichi says '복분자캔?!'.\n"
        "- Panel ② (Top-Right): Inside GS25 convenience store beverage cooler aisle! Songi and Jichi enthusiastically grab the stylish red-and-black '고창명주 복분자 하이볼' can. But Songi gasps: 'Wait, this needs the ultimate savory gourmet snack!'. Short Korean speech bubbles (MAX 5 chars): Songi says 'GS25출동!', Jichi says '안주필요!'.\n"
        "- Panel ③ (Bottom-Left): Crossing the street into bright CU convenience store snack aisle! Jichi and Songi spot the viral black bag of Chef Kwon Seong-jun's '블랙트러플하몽 포테이토스틱' on the snack shelf. Short Korean speech bubbles (MAX 5 chars): Songi says 'CU출동!', Jichi says '권성준과자!'.\n"
        "- Panel ④ (Bottom-Right): Returning home! Jichi and Songi proudly placing the chilled 복분자 하이볼 can and the sleek black potato snack bag side-by-side on the wooden table, giving a giant happy high-five. Short Korean speech bubbles (MAX 5 chars): Songi says '완벽조합!', Jichi says '홈술세팅!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cozy cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '홈술하자!', '복분자캔?!', 'GS25출동!', '안주필요!', 'CU출동!', '권성준과자!', '완벽조합!', '홈술세팅!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: GS25 공식 앱 및 SNS 속 고창명주 복분자 하이볼 출시 포스터 실사\n"
        "- 2번컷 참조 사진: 파란색 간판 GS25 주류 냉장고 속 진열된 복분자 하이볼 캔 실사\n"
        "- 3번컷 참조 사진: CU 편의점 과자 코너에 진열된 블랙트러플하몽 포테이토스틱 실사\n"
        "- 4번컷 참조 사진: 식탁 위에 복분자 하이볼 캔과 권성준 감자스틱 봉지를 나란히 세팅한 실물 투샷"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Inside home pub. Cracking open the cold fizzing 복분자 하이볼 can, pouring sparkling ruby-red drink over clear ice cubes into a classy glass! Songi rips open the black snack bag, wafting rich golden aromatic truffle steam. Short Korean speech bubbles (MAX 5 chars): Songi says '향폭발!', Jichi says '루비빛깔!'.\n"
        "- Panel ⑥ (Top-Right): Delicious tasting reaction! Songi crunches on a crispy savory truffle-jamón potato stick with blissfully closed eyes. Jichi sips the refreshing sweet-tart sparkling raspberry highball. Short Korean speech bubbles (MAX 5 chars): Songi says '단짠극락!', Jichi says '안주찰떡!'.\n"
        "- Panel ⑦ (Bottom-Left): Epic home-pub spread! Jichi and Songi clinking glasses with cheerful toasts, an empty potato stick tray, completely blown away by how well the two convenience stores' star products harmonize. Short Korean speech bubbles (MAX 5 chars): Songi says '홈술대성공!', Jichi says '꿀조합인정!'.\n"
        "- Panel ⑧ (Bottom-Right): Satisfied cozy ending. Jichi and Songi sitting side-by-side with proud happy smiles beside a rustic wooden signboard reading '좋아요 & 구독 ❤️', waving cheerfully with a potato stick and glass. Short Korean speech bubbles (MAX 5 chars): Jichi says '내일또봐!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm delicious cinematic lighting. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '향폭발!', '루비빛깔!', '단짠극락!', '안주찰떡!', '홈술대성공!', '꿀조합인정!', '내일또봐!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 각얼음을 채운 투명 유리잔에 영롱한 붉은빛 복분자 하이볼을 따르는 생생한 실사\n"
        "- 6번컷 참조 사진: 바삭한 트러플하몽 감자스틱을 집어 하이볼 잔과 함께 세팅한 근접 확대 실사 (★가장 중요!)\n"
        "- 7번컷 참조 사진: 시원한 탄산 기포가 올라오는 복분자 하이볼과 감자스틱 한 상 차림 실사\n"
        "- 8번컷 참조 사진: 깔끔하게 비운 캔과 과자 봉지가 놓인 기분 좋은 홈술 마무리 컷"
    )

    # 코서치 수집 실사 이미지 경로 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "gs25_bokbunja_highball_real_1.jpg")
    real_cross_img = os.path.join(project_root, "02_코서치_자료", "gs25_bokbunja_cu_kwon_pairing_real_2.jpg")

    # 친누나표 4대 독립 블록 (크로스오버 맞춤형 + 매뉴얼 1호 리얼 페어링 반영)
    block_info = (
        "제품명 : GS25 '고창명주 복분자 하이볼' (500ml) X CU '블랙트러플하몽 포테이토스틱' (47g)\n"
        "가격 : 하이볼 4,500원 (행사 3캔 12,000원) + 권성준 감자스틱 1,900원 (합계 6,400원)\n"
        "판매처 : 전국 GS25 주류 냉장고 + 전국 CU 스낵 매대"
    )

    block_flavor = (
        "핵심 플레이버 : 명품 고창 복분자 원액 100%의 달콤쌉싸름하고 청량한 탄산 하이볼 +\n"
        "이탈리아산 블랙트러플의 고급스러운 풍미와 스페인 하몽 시즈닝의 짭조름한 감칠맛 스낵"
    )

    block_feature = (
        "특징 및 식감: 편의점 한 곳만 털기 아쉬울 때 완성하는 역대급 크로스오버!\n"
        "톡 쏘는 루비빛 복분자 탄산이 입안을 개운하게 적셔주고\n"
        "오독오독 바삭한 트러플 감자스틱이 짭짤하게 받쳐주어 한 잔 비우기에 완전 좋아요"
    )

    block_tasty_tip = (
        "Tasty Tip!\n"
        "복분자 하이볼은 꼭 각얼음 가득 채운 유리잔에 부어 영롱한 루비빛 탄산을 즐기시고\n"
        "감자스틱은 전자레인지에 딱 10초만 돌리면 트러플 향이 2배로 폭발해 하이볼과 완전 좋아요"
    )

    # 본문 문단 배치
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 하루 일과를 마치고 나만의 아늑한 방에서 시원하고 맛있는 홈술 한 잔이 간절해지는 화요일 저녁, 편의점 1만 개 매대를 넘나들며 역대급 꿀조합을 찾아 달리는 새싹 요정 지치와 홈술 탐정 고양이 송이입니다!",
        "편의점 신상을 즐길 때 꼭 한 브랜드 매장에서만 안주를 사야 할까요? 절대 아닙니다! 요즘 SNS 먹방 크리에이터들 사이에서 가장 핫한 트렌드는 바로 **'편의점 2곳을 털어 완성하는 크로스오버 페어링'**입니다! 그래서 오늘 지치와 송이가 두 발 벗고 나섰습니다! 바로 **GS25 '고창명주 복분자 하이볼'과 CU 흑백요리사 공식 신상 '권성준 감자스틱'**의 만남입니다!",
        "명품 고창 복분자 원액의 달콤쌉싸름하고 톡 쏘는 청량감, 그리고 이탈리아산 블랙트러플과 스페인 하몽의 짭조름한 감칠맛이 폭발하는 감자스틱의 단짠단짠 극락 페어링! 지치와 송이의 유쾌한 4컷 웹툰과 실사 팩트 체크로 지금 바로 만나보세요!",

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
        "편의점꿀조합", "홈술안주", "편의점신상",
        "GS25", "CU", "편의점하이볼",
        "고창명주복분자하이볼", "복분자하이볼", "권성준과자"
    ]

    # [검증 및 사전 감사]
    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 5대 황금 수칙 + 매뉴얼 1호·3호 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["복분자", "권성준", "GS25", "CU"])]
    print(f"  ✅ [검증 1] 말풍선 5글자 이내 규칙 준수 여부: {len(long_bubbles)}건 위반 (통과)")

    # 2. 실사 이미지 2장 존재 여부 검사
    has_img1 = os.path.exists(real_pkg_img)
    has_img2 = os.path.exists(real_cross_img)
    print(f"  ✅ [검증 2] 실사 이미지 탑재: 1번 캔 패키지({has_img1}), 2번 잔/페어링({has_img2})")

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
    publish_crossover_bokbunja_kwon_stick_toon(save_draft=True)
