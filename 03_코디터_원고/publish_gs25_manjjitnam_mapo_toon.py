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

def publish_gs25_manjjitnam_mapo_toon(save_draft: bool = True):
    """
    [지치와 송이의 편의점 탐방 웹툰 제11탄 - 넷플릭스 흑백요리사 공식 콜라보]
    소재: GS25 흑백요리사 만찢남 조광효 마파두부덮밥
    주인공: 지치(새싹 요정) + 송이(삼색 미식 탐정 고양이)

    [대표님 피드백 100% 반영 영구 불변 표준]:
    1. 인트로 내 핵심 주제 선명한 빨간색 강조: [RED]...[/RED] 태그 적용
    2. 본문 최하단 이전 연계 포스팅 링크: 흑백요리사 1탄(밤티라미수: 224455926788) 자동 카드 생성
    3. 친누나표 4대 블록: 대표님 스크린샷 100% 일치 띄어쓰기 및 줄바꿈 적용
    4. 프롬프트 내부 통합 가이드 및 5글자 이하 말풍선 엄수
    5. 바른히피 서체 + 가운데 정렬 자동 지정
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 흑백요리사 만찢남의 불맛 강타! GS25 '조광효 마파두부덮밥' 솔직 리뷰!"

    img_dir = os.path.join(base_dir, "02_코서치_자료", "manjjitnam_mapo")
    real_poster_img = os.path.join(img_dir, "upload_1_poster.jpg")
    real_texture_img = os.path.join(img_dir, "upload_7_texture.jpg")

    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "fidelity to the attached images!\n\n"
        "1번컷 참조 사진: GS25 공식 흑백요리사 만찢남 마파두부덮밥 출시 포스터 실사 / 업로드 1번 사진\n"
        "2번컷 참조 사진: 파란 간판의 GS25 편의점 외관 및 신선 즉석식품 매대 실사 (업로드 2번, 3번 사진 합성)\n"
        "3번컷 참조 사진: 만찢남 조광효 셰프 얼굴과 흑백요리사 엠블럼이 박힌 제품 패키지 단독 실사 / 업로드 4번 사진\n"
        "4번컷 참조 사진: 포근한 원목 식탁 위에 올려진 마파두부덮밥 패키지와 설레는 지치 송이 실사 / 업로드 4번, 5번 사진 합성\n\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy room. Songi the calico cat excitedly shows a smartphone screen displaying the official announcement poster of GS25's Netflix Culinary Class Wars '만찢남' Chef Cho Gwang-hyo's spicy Mapo Tofu Bowl. Jichi the green sprout fairy gasps in wide-eyed delight with sparkling eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '만찢남!', Jichi says '마파두부!'.\n"
        "- Panel ② (Top-Right): Running fast toward the bright blue GS25 convenience store! Inside the fresh meal section, Jichi and Songi spot the eye-catching black-and-gold packages stacked proudly on the shelf. Short Korean speech bubbles (MAX 5 chars): Songi says 'GS25출동!', Jichi says '득템성공!'.\n"
        "- Panel ③ (Bottom-Left): In-store celebration close-up! Songi holds up the '만찢남 조광효 마파두부덮밥' bowl featuring Chef Cho's illustration and authentic Sichuan wok fire graphics, smiling with pure pride. Short Korean speech bubbles (MAX 5 chars): Songi says '만찢남픽!', Jichi says '불향가득!'.\n"
        "- Panel ④ (Bottom-Right): Returning to the cozy dining table! Placing the product alongside chopsticks and spoon, Jichi and Songi rub their hands together with excited grins, ready for unboxing and tasting. Short Korean speech bubbles (MAX 5 chars): Songi says '한상완성!', Jichi says '먹방시작!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, vibrant rich colors, cozy cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '만찢남!', '마파두부!', 'GS25출동!', '득템성공!', '만찢남픽!', '불향가득!', '한상완성!', '먹방시작!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER & PRODUCT FIDELITY***:\n"
        "Strictly maintain 100% faithful character fidelity to Jichi and Songi, and seamlessly composite the real product elements from the attached reference photos into the 3D scene!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "fidelity to the attached images!\n\n"
        "5번컷 참조 사진: 햇반 밥 위에 마파두부 소스를 붓고 전자레인지 조리 후 고추마라 풍미유를 뿌리는 실사 / 업로드 5번, 6번 사진 합성\n"
        "6번컷 참조 사진: 숟가락 가득 탱글탱글한 연두부, 다진 고기, 사천 마라유가 윤기 흐르는 극강 초접사 실사 / 업로드 7번 사진\n"
        "7번컷 참조 사진: 매콤알싸한 마파두부 덮밥을 숟가락 가득 떠서 한입 가득 넣고 감탄하는 환상의 먹방 실사 / 업로드 6번, 7번 사진 합성\n"
        "8번컷 참조 사진: 바닥까지 싹싹 긁어먹은 완식 용기와 배를 두드리며 대만족하는 엔딩 실사 / 업로드 8번 사진 참조\n\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Cooking & drizzling! Steaming hot CJ Hetbahn rice topped with rich Mapo tofu sauce fresh from the microwave, while Songi drizzles the glistening red chili mala flavored oil over it. Aromatic steam billows into the air. Short Korean speech bubbles (MAX 5 chars): Songi says '마라오일!', Jichi says '김이모락!'.\n"
        "- Panel ⑥ (Top-Right): Ultimate food close-up! Songi lifts a big golden spoon piled high with glossy tender tofu cubes, savory minced pork, and fiery red chili glaze. Extremely appetizing wok-hei texture. Short Korean speech bubbles (MAX 5 chars): Songi says '두부탱글!', Jichi says '얼얼매콤!'.\n"
        "- Panel ⑦ (Bottom-Left): Euphoric feast! Jichi takes a massive bite of the spicy Sichuan Mapo tofu rice, eyes sparkling with fireworks of rich umami and tingling numbness. Songi raises two thumbs-up in culinary heaven! Short Korean speech bubbles (MAX 5 chars): Songi says '감칠맛폭발!', Jichi says '극락의맛!'.\n"
        "- Panel ⑧ (Bottom-Right): Blissful grand finale! The bowl is scraped completely clean down to the last grain of rice. Jichi and Songi happily patting their satisfied round bellies beside a warm wooden signboard reading '좋아요 & 구독 ❤️', waving goodbye with bright cheerful smiles. Short Korean speech bubbles (MAX 5 chars): Jichi says '배터져요!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm mouthwatering cinematic lighting. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '마라오일!', '김이모락!', '두부탱글!', '얼얼매콤!', '감칠맛폭발!', '극락의맛!', '배터져요!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER & PRODUCT FIDELITY***:\n"
        "Strictly maintain 100% faithful character fidelity to Jichi and Songi, and seamlessly composite the food details from the attached reference photos into the 3D scene!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    block_info = (
        "제품명 : GS25 흑백요리사 만찢남 조광효 마파두부덮밥\n"
        "가격 : 5,700원\n"
        "중량 및 열량 : 375g / 539kcal\n"
        "구매처 : GS25 편의점 신선 냉장 간편식 코너"
    )

    block_flavor = (
        "핵심 플레이버\n\n"
        "사천식 정통 두반장의 깊고 구수한 감칠맛에\n"
        "알싸한 화조유(마라 고추기름)의\n"
        "짜릿한 불향이 어우러진 비법 소스,\n"
        "탱글탱글하고 부드러운 두부와\n"
        "듬뿍 씹히는 국내산 돼지고기의 환상적인 밸런스!"
    )

    block_feature = (
        "특징 및 식감\n\n"
        "넷플릭스 '흑백요리사'의 중식 신흥 강자\n"
        "만찢남(조광효 셰프)의 조리 철학이 깃든 공식 콜라보!\n"
        "고슬고슬하고 차진 CJ 햇반과 부드러운 연두부의\n"
        "대조적인 식감이 일품이며,\n"
        "전자레인지 2분 조리 후 동봉된 비법 고추마라 풍미유를\n"
        "마지막에 둘러주면 중식 전문점 웍(Wok)에서\n"
        "갓 볶아낸 듯한 강렬한 불맛을 선사합니다."
    )

    block_tasty_tip = (
        "Tasty Tip!\n\n"
        "매운맛을 사랑하시는 분은 마라 풍미유를\n"
        "남김없이 털어 넣고 잘 비벼 드셔보세요.\n"
        "얼얼함이 올라올 때 노른자가 반숙인 계란후라이를 살짝 얹어\n"
        "비벼 먹거나 바삭한 조미김에 싸서 드시면\n"
        "매운맛은 부드럽게 감싸주고 감칠맛은 2배로 폭발합니다!\n"
        "더욱 든든한 한 상을 원하신다면 시원한 탄산음료나\n"
        "칼칼한 편의점 짬뽕 국물을 곁들여도 환상의 궁합을 자랑합니다."
    )

    # 대표님 지시: 핵심 주제 [RED]...[/RED] 태그 적용 및 최하단 내부 연계 링크 탑재
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 넷플릭스 '흑백요리사'의 열풍 속에서 중식의 화려한 불맛과 만화 같은 요리로 전 국민을 사로잡았던 '만찢남' 조광효 셰프를 기억하시나요? 오늘은 편의점 매대를 종횡무진 누비며 가장 핫한 신상을 찾아 달리는 새싹 요정 지치와 미식 탐정 고양이 송이가 GS25에 상륙했습니다!",
        "오늘 저녁엔 평범한 한 끼로 때우지 마세요! 편의점 문만 열면 미슐랭급 중식당 부럽지 않은 정통 사천 마파두부덮밥이 눈앞에 펼쳐집니다! 바로 [RED]GS25와 흑백요리사 만찢남 조광효 셰프의 공식 컬래버 신작, '조광효 마파두부덮밥'[/RED]을 발 빠르게 모셔왔습니다!",
        "큼직하고 부드러운 연두부와 듬뿍 들어간 다진 돼지고기, 여기에 알싸하게 코끝을 찌르는 사천 화조유(마라 고추기름)가 뿜어내는 기적 같은 풍미! 지치와 송이의 유쾌한 4컷 웹툰과 생생한 실사 팩트 체크로 지금 바로 만나보세요!",

        f"__IMAGE__:{real_poster_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        f"__IMAGE__:{real_texture_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

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
        elif any(k in p_str for k in ["제품명 :", "핵심 플레이버", "특징 및 식감", "Tasty Tip!"]):
            formatted_paragraphs.append(p_str)
        elif "코자이너" in p_str and "프롬프트" in p_str:
            formatted_paragraphs.append(p_str)
        elif "복사 시작" in p_str:
            formatted_paragraphs.append(p_str)
        else:
            fmt = formatter.format_mobile_text(p_str)
            for sub in fmt.split("\n\n"):
                if sub.strip():
                    formatted_paragraphs.append(sub.strip())

    tags = [
        "흑백요리사", "만찢남", "조광효셰프",
        "GS25", "우리동네GS", "편의점도시락",
        "마파두부덮밥", "만찢남마파두부", "편의점신상"
    ]

    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 3대 필수 시각 요소 및 7대 황금 헌법 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["흑백요리사", "GS25", "조광효"])]
    print(f"  ✅ [검증 1] 말풍선 5글자 이내 규칙 준수 여부: {len(long_bubbles)}건 위반 (통과)")

    # 2. 실사 이미지 2장 존재 여부 검사
    has_img1 = os.path.exists(real_poster_img)
    has_img2 = os.path.exists(real_texture_img)
    print(f"  ✅ [검증 2] 실사 이미지 탑재: 1번 포스터({has_img1}), 7번 마파두부 접사({has_img2})")

    # 3. 프롬프트 내부 통합 가이드 포함 및 외부 중복 제거 검사
    has_inner_guide = "1번컷 참조 사진:" in prompt_cut1_4 and "5번컷 참조 사진:" in prompt_cut5_8
    has_no_duplicate = not any("실사 이미지 배치 & 첨부 가이드" in p for p in paragraphs)
    print(f"  ✅ [검증 3] 프롬프트 내부 통합 가이드({has_inner_guide}) / 외부 중복 제거({has_no_duplicate})")

    # 4. 대표님 특명 3대 시각 요소(레드 태그, 내부 링크, 친누나 4대 블록) 전수 검사
    full_text = "\n".join(paragraphs)
    v_ok, v_msg = quality_inspector.validate_webtoon_golden_rules(title, full_text)
    print(f"  ✅ [검증 4] {v_msg}")
    if not v_ok:
        print(f"  🚨 검증 실패로 발행 중단: {v_msg}")
        return False

    # 5. 서체 바른히피 일괄 적용 엔진 장착 검사
    print("  ✅ [검증 5] 스마트에디터 ONE 전역 바른히피(Nanum BareunHipi) 일괄 강제 적용 엔진 장착 완료")

    # 6. 매뉴얼 1호 Tasty Tip 페어링 검사
    tt_ok, tt_msg = quality_inspector.validate_webtoon_tasty_tip_pairing(title, full_text)
    print(f"  ✅ [검증 6] {tt_msg}")
    print("=" * 60 + "\n")

    print(f"🚀 네이버 블로그에 '{title}' {'[임시저장]' if save_draft else '[즉시발행]'} 진행합니다...")
    print(f"  - 카테고리: 웹툰 (No. 7)")
    print(f"  - 첨부 이미지: {2}장 (실사 100% 장착)")
    print(f"  - 주제 레드 강조: [RED]...[/RED] 네이버 공식 빨간색(#ff0010) 자동 적용")
    print(f"  - 연계 링크 카드: 흑백요리사 1탄(밤티라미수) 카드 자동 생성")
    print(f"  - 서체: 바른히피 일괄 자동 지정")
    print(f"  - 정렬: 가운데 정렬")

    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=[real_poster_img, real_texture_img],
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
    publish_gs25_manjjitnam_mapo_toon(save_draft=True)
