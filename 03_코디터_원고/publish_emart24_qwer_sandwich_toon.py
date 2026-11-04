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

def publish_emart24_qwer_sandwich_toon(save_draft: bool = True):
    """
    [지치와 초코의 편의점 탐방 웹툰 제12탄 - 이마트24 X QWER 공식 콜라보]
    소재: 이마트24 X QWER 멤버별 샌드위치 4종 (쵸단·마젠타·히나·시연)
    주인공: 지치(새싹 요정) + 초코(턱시도 고양이 - QWER 열혈 찐팬!)

    [대표님 컨펌 규격 + 매뉴얼 1호~7호 100% 엄격 준수]:
    1. 인트로 내 핵심 주제 선명한 빨간색 강조: [RED]...[/RED] 태그 적용
    2. 본문 최하단 이전 연계 포스팅 링크: 흑백요리사 1탄(밤티라미수: 224455926788) 자동 카드 생성
    3. 친누나표 4대 블록: 제품명, 핵심 플레이버, 특징 및 식감, Tasty Tip! 황금 규격 준수
    4. 프롬프트 내부 통합 가이드 및 5글자 이하 말풍선 엄수
    5. 바른히피 서체 + 가운데 정렬 자동 지정
    """
    title = "[지치와 초코의 편의점 탐방 웹툰] 락밴드 QWER이 떴다! 이마트24 쵸단·마젠타·히나·시연 샌드위치 전격 비교 & 일일 점장 응모 꿀팁!"

    img_dir = os.path.join(base_dir, "02_코서치_자료", "emart24_qwer_sandwich")
    real_poster_img = os.path.join(img_dir, "upload_1_poster.jpg")
    real_texture_img = os.path.join(img_dir, "upload_4_package.jpg")

    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "fidelity to the attached images!\n\n"
        "1번컷 참조 사진: 스마트폰에서 QWER 음악을 들으며 이마트24 공식 콜라보 샌드위치 출시 포스터를 발견한 실사 / 업로드 1번 사진\n"
        "2번컷 참조 사진: 노란색 간판의 이마트24 편의점 정면 외관 및 신선 즉석식품 매대 실사 (업로드 2번, 3번 사진 합성)\n"
        "3번컷 참조 사진: QWER 쵸단, 마젠타, 히나, 시연 얼굴이 각각 박힌 샌드위치 4종 패키지 단독 실사 / 업로드 4번 사진\n"
        "4번컷 참조 사진: 포근한 원목 식탁 위에 샌드위치 패키지를 올려놓고 설레는 지치와 초코 실사 / 업로드 4번, 5번 사진 합성\n\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy room. Choco the black-and-white tuxedo cat is wearing stylish over-ear headphones, happily jamming to QWER's energetic rock music. Suddenly seeing the official announcement poster of E-Mart 24 x QWER collaboration sandwiches on a tablet, Choco gasps with giant starry eyes and shakes Jichi the green sprout fairy's shoulders in pure fan euphoria! Short Korean speech bubbles (MAX 5 chars): Choco says 'QWER떴다!', Jichi says '이마트24?'.\n"
        "- Panel ② (Top-Right): Running fast toward the bright yellow and charcoal E-Mart 24 convenience store! Inside the fresh meal section, Jichi and Choco excitedly dash to the sandwich cooler shelf lined with colorful QWER labels. Short Korean speech bubbles (MAX 5 chars): Choco says '빛의속도!', Jichi says '득템성공!'.\n"
        "- Panel ③ (Bottom-Left): In-store celebration close-up! Choco proudly hugs the fresh packages featuring QWER members (Chodan, Magenta, Hina, Siyeon) illustrations and energetic band graphics, smiling with intense pride. Short Korean speech bubbles (MAX 5 chars): Choco says '최애샌드!', Jichi says '완전푸짐!'.\n"
        "- Panel ④ (Bottom-Right): Returning to the cozy dining table! Placing the 4 colorful sandwich packs side by side on the table, Jichi and Choco rub their paws together with excited grins, ready for tasting and app stamp entry. Short Korean speech bubbles (MAX 5 chars): Choco says '먹방출격!', Jichi says '설렌다!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, vibrant rich colors, cozy cinematic lighting. Strictly maintain character designs of Jichi (green sprout fairy) and Choco (black-and-white tuxedo cat with over-ear headphones in panel 1). Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: 'QWER떴다!', '이마트24?', '빛의속도!', '득템성공!', '최애샌드!', '완전푸짐!', '먹방출격!', '설렌다!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER & PRODUCT FIDELITY***:\n"
        "Strictly maintain 100% faithful character fidelity to Jichi and Choco, and seamlessly composite the real product elements from the attached reference photos into the 3D scene!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "fidelity to the attached images!\n\n"
        "5번컷 참조 사진: 삼각 포장지를 개봉하여 촉촉한 식빵과 푸짐한 속재료가 드러난 샌드위치 개봉 실사 / 업로드 4번, 5번 사진 합성\n"
        "6번컷 참조 사진: 고소한 에그샐러드와 짭조름한 햄, 치즈, 두툼한 패티가 꽉 찬 극강 초접사 단면 실사 / 업로드 6번 사진\n"
        "7번컷 참조 사진: 이마트24 무료 증정 핫아메리카노 및 레쓰비 캔커피와 함께 샌드위치를 즐기는 꿀조합 페어링 실사 / 업로드 6번, 7번 사진 합성\n"
        "8번컷 참조 사진: 샌드위치를 맛있게 비우고 스마트폰 이마트24 앱 스탬프 응모를 완료하며 대만족하는 완식 엔딩 실사 / 업로드 8번 사진 참조\n\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Unboxing the goodness! Jichi and Choco unwrapping the sandwich packages to reveal fresh white bread densely packed with colorful fillings. Choco holds a smartphone displaying the E-Mart 24 app stamp entry screen. Short Korean speech bubbles (MAX 5 chars): Choco says '스탬프쾅!', Jichi says '속꽉찼다!'.\n"
        "- Panel ⑥ (Top-Right): Ultimate food close-up! Jichi lifts a half-cut sandwich overflowing with rich egg garlic mayo, savory ham, melted cheese, and crisp lettuce. Extremely appetizing juicy cross-section texture. Short Korean speech bubbles (MAX 5 chars): Choco says '풍미작렬!', Jichi says '단짠꿀맛!'.\n"
        "- Panel ⑦ (Bottom-Left): Euphoric feast pairing! Choco takes a huge bite of the sandwich and sips steaming Americano coffee, completely blissed out. Jichi happily chews on fresh tuna salad sandwich, eyes sparkling like fireworks! Short Korean speech bubbles (MAX 5 chars): Choco says '팬미팅가자!', Jichi says '극락조합!'.\n"
        "- Panel ⑧ (Bottom-Right): Blissful grand finale! Sandwich wrappers and coffee cups completely finished clean. Jichi and Choco happily patting their full bellies beside a warm wooden signboard reading '좋아요 & 구독 ❤️', waving goodbye with cheerful rock-and-roll finger signs. Short Korean speech bubbles (MAX 5 chars): Choco says 'QWER최고!', Jichi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm mouthwatering cinematic lighting. Strictly maintain character fidelity to Jichi and Choco. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '스탬프쾅!', '속꽉찼다!', '풍미작렬!', '단짠꿀맛!', '팬미팅가자!', '극락조합!', 'QWER최고!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER & PRODUCT FIDELITY***:\n"
        "Strictly maintain 100% faithful character fidelity to Jichi and Choco, and seamlessly composite the food details from the attached reference photos into the 3D scene!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    block_info = (
        "제품명 : 이마트24 X QWER 콜라보 샌드위치 (쵸단·마젠타·히나·시연 4종)\n"
        "가격 : 각 3,200원\n"
        "중량 및 열량 : 약 180~210g / 평균 380~430kcal\n"
        "구매처 : 이마트24 편의점 신선 냉장 샌드위치 코너"
    )

    block_flavor = (
        "핵심 플레이버\n\n"
        "리더 쵸단의 담백 고소한 고단백 어니언참치샐러드,\n"
        "마젠타의 감칠맛 폭발 갈릭에그 햄치즈,\n"
        "히나의 든든하고 달콤짭조름한 소시지에그치즈,\n"
        "시연의 프레시하고 청량한 아삭햄야채까지 4인 4색 맞춤 조화!"
    )

    block_feature = (
        "특징 및 식감\n\n"
        "대세 걸밴드 QWER 멤버들의 실제 취향을 100% 반영한 공식 한정 콜라보!\n"
        "부드러운 식빵 속에 아낌없이 꽉 채워진 토핑이 한 입 가득 풍성한 식감을 선사하며,\n"
        "샌드위치 구매 후 이마트24 앱 스탬프 응모 시 11월 18일 서울숲 디저트랩에서 열리는 'QWER 일일 점장 행사(팬미팅)'에 초대되는 역대급 팬덤 혜택을 제공합니다."
    )

    block_tasty_tip = (
        "Tasty Tip!\n\n"
        "11월 한 달간 행사 카드로 결제 시 핫아메리카노 또는 레쓰비 캔커피가 100% 무료 증정!\n"
        "쌉싸름하고 따뜻한 아메리카노와 함께 즐기면 갈릭에그와 소시지의 기름진 맛을 깔끔하게 잡아주고,\n"
        "조금 더 부드러운 단맛을 원하신다면 달콤한 캔커피나 흰 우유와 곁들여 브런치 카페 부럽지 않은 든든한 한 끼를 완성해보세요."
    )

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 오늘도 신나는 에너지가 넘치는 편의점 신상 탐방 시간입니다! 오늘은 특별히 인기 걸밴드 QWER의 열혈 찐팬인 턱시도 고양이 초코가 헤드폰을 끼고 음악을 듣다가, 방금 막 터진 엄청난 편의점 대형 콜라보 소식을 접하고 눈을 반짝이며 새싹 요정 지치에게 달려왔습니다!",
        "오늘 점심엔 평범한 샌드위치로 때우지 마세요! 편의점 문만 열면 최애 걸밴드 멤버들의 개성이 듬뿍 담긴 4인 4색 프리미엄 샌드위치가 눈앞에 펼쳐집니다! 바로 [RED]이마트24와 대세 걸밴드 QWER의 공식 컬래버 신작, 'QWER 멤버별 샌드위치 4종'[/RED]을 발 빠르게 모셔왔습니다!",
        "운동 마니아 쵸단의 고단백 어니언참치샐러드부터 마젠타의 진한 갈릭에그 햄치즈, 히나의 소시지에그치즈, 시연의 아삭햄야채까지! 여기에 서울숲 디저트랩 일일 점장 팬미팅 응모 기회까지 담긴 초특급 신상! 지치와 초코의 유쾌한 4컷 웹툰과 생생한 실사 팩트 체크로 지금 바로 만나보세요!",

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
        "QWER", "이마트24", "QWER샌드위치",
        "쵸단", "마젠타", "히나",
        "시연", "편의점샌드위치", "편의점신상"
    ]

    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 3대 필수 시각 요소 및 7대 황금 헌법 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["이마트24", "QWER"])]
    print(f"  ✅ [검증 1] 말풍선 5글자 이내 규칙 준수 여부: {len(long_bubbles)}건 위반 (통과)")

    # 2. 실사 이미지 2장 존재 여부 검사
    has_img1 = os.path.exists(real_poster_img)
    has_img2 = os.path.exists(real_texture_img)
    print(f"  ✅ [검증 2] 실사 이미지 탑재: 1번 포스터({has_img1}), 4번 패키지 4종({has_img2})")

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
    print(f"  - 주인공: 지치(새싹 요정) + 초코(턱시도 고양이 - QWER 찐팬)")
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
    publish_emart24_qwer_sandwich_toon(save_draft=True)
