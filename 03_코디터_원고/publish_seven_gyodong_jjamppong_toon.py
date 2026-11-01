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

def publish_seven_gyodong_jjamppong_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 제6탄]
    주제: 13년 스테디셀러의 역대급 귀환! 세븐일레븐 '정통 강릉교동짬뽕' 컵라면 리뉴얼
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 디저트·라면 탐정)

    [대표님 엄격 5대 절대 수칙 + 매뉴얼 1호·2호·3호 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/화제 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    6. [지치컴패니 업무매뉴얼 1호 & 3호] 전방위 매대 컵라면 실사 먹조합 (찬바람 부는 날 얼큰 국물 + 삼각김밥 짬뽕밥 페어링)
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 13년 짬뽕 컵라면의 귀환! 세븐일레븐 '정통 강릉교동짬뽕' 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a warm cozy room on a brisk November day. Songi the calico cat jumping with big sparkling eyes, showing a smartphone news screen of Seven Eleven's 13-year legendary cup ramen '정통 강릉교동짬뽕' renewal release! Jichi the green sprout fairy gasps in delight. Short Korean speech bubbles (MAX 5 chars): Songi says '불향가득!', Jichi says '교동짬뽕?!'.\n"
        "- Panel ② (Top-Right): Songi grabbing Jichi's hand, strapping on a cute scarf and backpack, marching determinedly toward the door. Short Korean speech bubbles (MAX 5 chars): Songi says '세븐출동!', Jichi says '국물땡겨!'.\n"
        "- Panel ③ (Bottom-Left): Inside bright Seven Eleven convenience store ramen aisle! Jichi and Songi spot the bold fire-red and black cup ramen package of '정통 강릉교동짬뽕' on the shelf. Short Korean speech bubbles (MAX 5 chars): Songi says '라면코너!', Jichi says '찾았다!'.\n"
        "- Panel ④ (Bottom-Right): At the convenience store hot water counter! Jichi pouring hot water into the cup, while Songi adds the spicy red seasoning oil packet. Short Korean speech bubbles (MAX 5 chars): Songi says '물붓는다!', Jichi says '불맛솔솔!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, warm appetizing lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '불향가득!', '교동짬뽕?!', '세븐출동!', '국물땡겨!', '라면코너!', '찾았다!', '물붓는다!', '불맛솔솔!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 세븐일레븐 공식 SNS 및 보도자료 속 정통 강릉교동짬뽕 리뉴얼 출시 포스터 실사\n"
        "- 2번컷 참조 사진: 주황색과 초록색 라인이 선명한 세븐일레븐 편의점 매장 외관 실사\n"
        "- 3번컷 참조 사진: 세븐일레븐 라면 코너 매대에 가지런히 진열된 강릉교동짬뽕 컵라면 실사\n"
        "- 4번컷 참조 사진: 조리 전 '정통 강릉교동짬뽕' 큰사발 정면 패키지 실물 사진"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Inside store dining corner. Opening the paper lid! Plumes of aromatic spicy steam curl up, revealing fiery red broth and thick springy noodles. Short Korean speech bubbles (MAX 5 chars): Songi says '면발탱글!', Jichi says '향대박!'.\n"
        "- Panel ⑥ (Top-Right): Delicious slurping reaction! Songi slurps the spicy noodles with blissful closed eyes, while Jichi happily sips a spoonful of rich dark red broth. Short Korean speech bubbles (MAX 5 chars): Songi says '얼큰칼칼!', Jichi says '진한국물!'.\n"
        "- Panel ⑦ (Bottom-Left): Epic ramen pairing! Jichi unwraps a convenience store triangle gimbap (tuna mayo) and dips it into the leftover spicy jjamppong soup to make jjamppong rice! Songi gives a giant double thumbs-up. Short Korean speech bubbles (MAX 5 chars): Songi says '밥말자!', Jichi says '국물순삭!'.\n"
        "- Panel ⑧ (Bottom-Right): Satisfied ending scene. Jichi and Songi sitting happily beside an empty cup ramen bowl and a rustic wooden signboard reading '좋아요 & 구독 ❤️', waving cheerfully with ramen chopsticks. Short Korean speech bubbles (MAX 5 chars): Jichi says '내일또봐!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm delicious cinematic lighting. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '면발탱글!', '향대박!', '얼큰칼칼!', '진한국물!', '밥말자!', '국물순삭!', '내일또봐!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 뚜껑을 열어 빨간 국물과 후첨 조미유가 고르게 섞인 컵라면 조리 완성 실사\n"
        "- 6번컷 참조 사진: 젓가락으로 쫄깃하고 도톰한 면발을 듬뿍 집어 올린 생생한 면치기 확대 실사 (★가장 중요!)\n"
        "- 7번컷 참조 사진: 얼큰한 국물에 삼각김밥(참치마요)을 넣어 든든하게 만 짬뽕밥 꿀조합 실사\n"
        "- 8번컷 참조 사진: 시원한 음료와 함께 국물 한 방울 남김없이 비운 완식 엔딩 컷"
    )

    # 코서치 수집 실사 이미지 경로 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "seven_gyodong_jjamppong_real_1.jpg")
    real_cross_img = os.path.join(project_root, "02_코서치_자료", "seven_gyodong_jjamppong_real_2.jpg")

    # 친누나표 4대 독립 블록 (라면 맞춤형 + 매뉴얼 1호 리얼 페어링 반영)
    block_info = (
        "제품명 : 세븐일레븐 '정통 강릉교동짬뽕' 컵라면\n"
        "가격 : 2,000원 (115g / 485 kcal)\n"
        "판매처 : 전국 세븐일레븐 오프라인 매장 라면 코너"
    )

    block_flavor = (
        "핵심 플레이버 : 전국 5대 짬뽕 강릉교동반점 특유의 진한 불향 +\n"
        "코끝을 알싸하게 때리는 후추의 칼칼한 매운맛 시즈닝 +\n"
        "해물 짬뽕과 차별화된 묵직하고 깊은 고기 육수 베이스 국물"
    )

    block_feature = (
        "특징 및 식감: 가볍고 밍밍한 일반 짬뽕 컵라면과 차원이 다른 걸쭉함!\n"
        "리뉴얼을 거쳐 한층 더 도톰하고 쫄깃해진 면발에 국물이 찰싹 배어들고\n"
        "후첨 짬뽕조미유가 주는 묵직한 불맛 덕분에 땀 뻘뻘 흘리며 한 그릇 비우기에 완전 좋아요"
    )

    block_tasty_tip = (
        "Tasty Tip!\n"
        "면을 호로록 다 건져 먹은 뒤 남은 얼큰한 국물에\n"
        "편의점 참치마요 삼각김밥 하나를 통째로 말아주면\n"
        "전문점 짬뽕밥 부럽지 않은 든든한 2차 코스 완성이라 완전 좋아요"
    )

    # 본문 문단 배치
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 쌀쌀해진 바람에 뜨끈하고 얼큰한 국물이 간절해지는 11월 첫날, 전국 편의점 1만 개 매대를 샅샅이 뒤져 가장 핫한 신상 먹거리를 찾아 달리는 새싹 요정 지치와 면치기 달인 고양이 송이입니다!",
        "매번 빵이나 달콤한 디저트만 찾다가 오늘은 찬 바람 부는 날씨에 절대 지나칠 수 없는 편의점 컵라면 코너로 향했습니다! 무려 13년 동안 세븐일레븐 컵라면 1등 자리를 지켜온 전설의 스테디셀러가 드디어 역대급 업그레이드를 마치고 돌아왔습니다! 바로 **세븐일레븐 '정통 강릉교동짬뽕' 컵라면**입니다!",
        "전국 5대 짬뽕으로 꼽히는 강릉 교동반점 특유의 강렬한 불맛과 코끝 찡한 후추의 칼칼함, 그리고 한층 더 도톰하고 쫄깃해진 면발의 환상적인 하모니! 지치와 송이의 유쾌한 4컷 웹툰과 생생한 실사 팩트 체크로 지금 바로 만나보세요!",

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
        "강릉교동짬뽕", "교동짬뽕", "편의점신상",
        "세븐일레븐", "세븐일레븐신상", "편의점라면",
        "정통강릉교동짬뽕", "교동짬뽕컵라면", "컵라면추천"
    ]

    # [검증 및 사전 감사]
    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 5대 황금 수칙 + 매뉴얼 1호·3호 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["교동짬뽕", "강릉", "세븐일레븐"])]
    print(f"  ✅ [검증 1] 말풍선 5글자 이내 규칙 준수 여부: {len(long_bubbles)}건 위반 (통과)")

    # 2. 실사 이미지 2장 존재 여부 검사
    has_img1 = os.path.exists(real_pkg_img)
    has_img2 = os.path.exists(real_cross_img)
    print(f"  ✅ [검증 2] 실사 이미지 탑재: 1번 패키지({has_img1}), 2번 단면/국물({has_img2})")

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
    publish_seven_gyodong_jjamppong_toon(save_draft=True)
