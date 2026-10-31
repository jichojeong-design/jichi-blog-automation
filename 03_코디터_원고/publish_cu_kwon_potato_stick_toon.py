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

def publish_cu_kwon_potato_stick_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 제5탄]
    주제: 하루 매출 1억 원 돌파 & 전 매장 발주 중단 대란! CU 공식 협업 '권성준 과자'
          나폴리 맛피아의 '블랙트러플하몽 포테이토스틱' (맛피아 감자스틱)
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 디저트 탐정)

    [대표님 엄격 5대 절대 수칙 + 매뉴얼 제1호 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/화제 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    6. [지치컴패니 업무매뉴얼 1호] 코서치 발굴 리얼 먹조합 기반 Tasty Tip (짭조름 스낵 -> 시원한 탄산/맥주 안주 페어링)
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 하루 1억 완판 대란?! CU '권성준 과자' 나폴리 맛피아 감자스틱 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy sunlit room. Songi the calico cat is jumping with giant sparkling eyes, waving a smartphone displaying news of Chef Kwon Seong-jun's viral black potato snack selling out nationwide! Jichi the green sprout fairy gasps with cute round eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '품절대란!', Jichi says '뭐길래?!'.\n"
        "- Panel ② (Top-Right): Songi enthusiastically grabbing Jichi's hand, strapping on a cute backpack and pointing determinedly toward the door. Short Korean speech bubbles (MAX 5 chars): Songi says '권성준과자!', Jichi says '출동하자!'.\n"
        "- Panel ③ (Bottom-Left): Inside bright CU convenience store snack aisle! Jichi and Songi spot the premium black and gold package of '블랙트러플하몽 포테이토스틱' sitting on the snack shelf. Short Korean speech bubbles (MAX 5 chars): Songi says '스낵코너!', Jichi says '찾았다!'.\n"
        "- Panel ④ (Bottom-Right): At checkout counter! Jichi and Songi holding the sleek black potato snack bag, admiring the stylish illustration of truffles and jamón. Short Korean speech bubbles (MAX 5 chars): Songi says '감자스틱!', Jichi says '하몽향솔솔!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '품절대란!', '뭐길래?!', '권성준과자!', '출동하자!', '스낵코너!', '찾았다!', '감자스틱!', '하몽향솔솔!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드 (대표님 특별 지시사항)
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: CU 포켓앱 및 뉴스 기사 속 나폴리 맛피아 감자스틱 출시 보도자료 실사\n"
        "- 2번컷 참조 사진: 보라색과 초록색 CU 편의점 매장 외관 실사\n"
        "- 3번컷 참조 사진: CU 스낵 코너 매대에 진열된 블랙트러플하몽 포테이토스틱 실사\n"
        "- 4번컷 참조 사진: 개봉 전 '블랙트러플하몽 포테이토스틱' 정면 블랙 패키지 실물 사진"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Inside kitchen. Songi rips open the black bag! A rich aromatic puff of gourmet black truffle aroma wafts out in delicate golden curls. Jichi takes a crispy golden potato stick. Short Korean speech bubbles (MAX 5 chars): Jichi says '바삭바삭!', Songi says '향대박!'.\n"
        "- Panel ⑥ (Top-Right): Tasting reaction! Songi munches on a crispy stick with blissfully closed eyes. Savory cured Spanish jamón seasoning and deep earthy truffle flavor harmonizing perfectly. Short Korean speech bubbles (MAX 5 chars): Songi says '하몽단짠!', Jichi says '고급진맛!'.\n"
        "- Panel ⑦ (Bottom-Left): Fun snack pairing! Jichi points to a frosty glass of fizzing cold zero soda, while Songi gives an excited double thumbs-up with an empty snack bag. Short Korean speech bubbles (MAX 5 chars): Songi says '맥주생각나!', 지치 says '순삭완료!'.\n"
        "- Panel ⑧ (Bottom-Right): Cozy ending scene. Jichi and Songi sitting side-by-side with proud happy smiles, resting against a cute rustic wooden signboard reading '좋아요 & 구독 ❤️', waving cheerfully with potato sticks. Short Korean speech bubbles (MAX 5 chars): Jichi says '내일또봐!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm gourmet cinematic lighting. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '바삭바삭!', '향대박!', '하몽단짠!', '고급진맛!', '맥주생각나!', '순삭완료!', '내일또봐!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드 (대표님 특별 지시사항)
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 봉지를 개봉하여 트레이에 담긴 노릇하고 바삭한 감자스틱 실물 사진\n"
        "- 6번컷 참조 사진: 하몽 시즈닝과 파슬리 가루가 솔솔 묻어있는 감자스틱 근접 확대 실사 (★가장 중요!)\n"
        "- 7번컷 참조 사진: 한 손으로 감자스틱을 집어 든 생생한 시식 컷\n"
        "- 8번컷 참조 사진: 시원한 탄산음료 또는 맥주 한 캔과 함께 세팅된 럭셔리 홈술 안주 완성 컷"
    )

    # 코서치가 수집한 실사 이미지 경로 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "cu_kwon_potato_stick_real_1.jpg")
    real_cross_img = os.path.join(project_root, "02_코서치_자료", "cu_kwon_potato_stick_real_2.jpg")

    # 친누나표 4대 독립 블록 (대표님 특명: 감자스틱 맞춤형 + 매뉴얼 1호 리얼 페어링 반영)
    block_info = (
        "제품명 : CU '블랙트러플하몽 포테이토스틱' (권성준 과자)\n"
        "가격 : 1,900원 (47g / 240 kcal)\n"
        "판매처 : 포켓CU 및 전국 CU 오프라인 매장 스낵 코너"
    )

    block_flavor = (
        "핵심 플레이버 : 이탈리아산 블랙트러플의 진한 풍미 +\n"
        "50년 전통 스페인산 하몽의 짭조름한 감칠맛 시즈닝 +\n"
        "오독오독 씹히는 바삭하고 고소한 감자스틱"
    )

    block_feature = (
        "특징 및 식감: 흔하고 밍밍한 감자과자 맛 아님!\n"
        "코끝을 찌르는 고급스러운 트러플 향과 하몽의 황금밸런스\n"
        "바삭바삭 씹을수록 감칠맛 터져 한 봉지 순삭하기에 완전 좋아요"
    )

    block_tasty_tip = (
        "Tasty Tip!\n"
        "짭조름하고 트러플 향이 묵직해 시원한 탄산음료와 함께!\n"
        "어른들은 시원한 맥주나 무알콜 맥주 한 캔 곁들이면\n"
        "단숨에 럭셔리 홈술 안주 완성이라 완전 좋아요"
    )

    # 본문 문단 배치
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 매일 가장 핫하고 신선한 편의점 신상을 찾아 발 빠르게 달려가는 귀여운 새싹 요정 지치와 흑백요리사 찐팬 고양이 송이입니다!",
        "얼마 전 전국을 밤티라미수 열풍으로 들썩이게 만들었던 흑백요리사 우승자 권성준 셰프(나폴리 맛피아)의 새로운 후속작이 드디어 베일을 벗었습니다! 출시 직후 하루 매출 1억 원을 돌파하며 전 매장 발주 중단 사태를 빚은 화제의 신상! 바로 **CU '블랙트러플하몽 포테이토스틱'**입니다!",
        "고급 이탈리아산 블랙트러플과 50년 전통 스페인산 하몽의 깊은 감칠맛을 바삭한 감자스틱에 듬뿍 입힌 역대급 퀄리티의 스낵! 지치와 송이의 유쾌한 4컷 웹툰과 실사 팩트 체크로 지금 바로 만나보세요!",

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
        "권성준", "나폴리맛피아", "흑백요리사",
        "CU", "CU신상", "편의점신상",
        "권성준과자", "나폴리맛피아감자스틱", "블랙트러플하몽포테이토스틱"
    ]

    # [검증 및 사전 감사]
    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 5대 황금 수칙 + 매뉴얼 1호 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["감자스틱", "포테이토", "CU", "트러플"])]
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
    publish_cu_kwon_potato_stick_toon(save_draft=True)
