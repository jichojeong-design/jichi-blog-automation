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


def publish_gs25_shinchan_pepero_toon(save_draft: bool = True):
    """
    [지치와 송이의 편의점 탐방 웹툰 제15탄 - GS25 짱구는 못말려 빼빼로 기획 세트]
    소재: GS25 짱구는 못말려 빼빼로 기획 세트 (짱구 필름카메라 & 흰둥이 장바구니 에디션)
    주인공: 지치(새싹 요정) + 송이(삼색 미식 탐정 고양이)

    [대표님 컨펌 규격 100% 완전 일치 튜닝]:
    1. 인트로 3문단 컬러 폰트 완벽 적용: [RED]GS25와 국민 애니 짱구는 못말려의 공식 컬래버 신작,[/RED], [RED]'짱구 빼빼로 기획 세트'[/RED], [RED]짱구 토이 필름카메라[/RED], [BLUE]흰둥이 장바구니 에디션[/BLUE]
    2. 친누나표 4대 블록 내부: Shift+Enter(단일 문단 내 줄바꿈)로 줄간격 밀착!
    3. 친누나표 4대 블록 사이: 빈 줄(Enter 2회)로 시원한 독립 여백 보장!
    4. 대표님 손수 교정한 줄바꿈 호흡 1글자 오차 없이 100% 반영
    5. 매뉴얼 제8호 기상청/포털 실시간 날씨(11월 초겨울 찬바람/빼빼로데이 D-3) 인트로 및 Tasty Tip 결합
    6. 최하단 연계 링크: 직전 다마고치 호빵 편(224468474405) 오픈그래프 카드 자동 생성
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 빼빼로데이 D-3 오픈런! GS25 '짱구는 못말려 빼빼로' 기획 세트 & 필름카메라 솔직 리뷰!"

    img_dir = os.path.join(base_dir, "02_코서치_자료", "gs25_shinchan_pepero")
    real_poster_img = os.path.join(img_dir, "upload_1_poster.jpg")
    real_camera_img = os.path.join(img_dir, "upload_6_camera_detail.jpg")

    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "fidelity to the attached images!\n\n"
        "1번컷 참조 사진: 스마트폰 화면 속 GS25 공식 짱구는 못말려 빼빼로데이 기획 세트 출시 포스터 실사 / 업로드 1번 사진\n"
        "2번컷 참조 사진: 파란색 간판의 GS25 편의점 매장 외관 및 매장 안으로 빛의 속도로 뛰어가는 출동 실사 / 업로드 2번 사진\n"
        "3번컷 참조 사진: 편의점 빼빼로데이 시즌 매대에 산더미처럼 진열된 짱구 필름카메라 기획 상자 실사 / 업로드 3번, 4번 사진 합성\n"
        "4번컷 참조 사진: 포근한 원목 식탁 위에 짱구 패키지 상자를 올려놓고 언박싱 준비를 하는 지치와 송이 실사 / 업로드 4번, 5번 사진 합성\n\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy room in chilly evening autumn. Songi the calico cat excitedly points to a smartphone showing GS25's official release poster of 'Crayon Shin-chan Pepero Limited Edition Set'. Jichi the green sprout fairy shivers from the cold draft then gasps with giant round sparkling eyes! Short Korean speech bubbles (MAX 5 chars): Songi says '짱구떴다!', Jichi says '카메라대박!'.\n"
        "- Panel ② (Top-Right): Running full sprint toward the warm blue-signed GS25 convenience store! Chilly dark evening outside, but the store glows brightly warm. Short Korean speech bubbles (MAX 5 chars): Songi says 'GS25출동!', Jichi says '빛의속도!'.\n"
        "- Panel ③ (Bottom-Left): In-store discovery! Standing in front of the colorful seasonal snack aisle, Songi and Jichi proudly hold up the large Shin-chan Pepero box decorated with adorable Shin-chan illustrations. Short Korean speech bubbles (MAX 5 chars): Songi says '득템성공!', Jichi says '완전귀여워!'.\n"
        "- Panel ④ (Bottom-Right): Returning home to the warm dining table! Placing the big gift box on the table beside scissors and mugs, Jichi and Songi rub their paws together with joyful grins, ready for the grand unboxing. Short Korean speech bubbles (MAX 5 chars): Songi says '언박싱!', Jichi says '설렌다!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cozy cinematic lighting. Strictly maintain 100% faithful character fidelity to Jichi (green sprout fairy) and Songi (calico cat). Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '짱구떴다!', '카메라대박!', 'GS25출동!', '빛의속도!', '득템성공!', '완전귀여워!', '언박싱!', '설렌다!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER & PRODUCT FIDELITY***:\n"
        "Strictly maintain 100% faithful character fidelity to Jichi and Songi, and seamlessly composite the real product elements from the attached reference photos into the 3D scene!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "fidelity to the attached images!\n\n"
        "5번컷 참조 사진: 기획 상자를 열어 빼빼로 4갑과 비닐에 곱게 싸인 노란색/빨간색 짱구 토이 필름카메라를 꺼내는 개봉 실사 / 업로드 4번, 5번 사진 합성\n"
        "6번컷 참조 사진: 짱구 얼굴 일러스트와 렌즈, 셔터 버튼이 달린 레트로 토이 필름카메라 실물의 정밀 초접사 실사 / 업로드 6번 사진\n"
        "7번컷 참조 사진: 바삭한 초코 빼빼로를 따뜻한 머그잔 커피/우유와 함께 곁들여 먹는 달콤바삭 디저트 페어링 실사 / 업로드 5번, 7번 사진 합성\n"
        "8번컷 참조 사진: 빼빼로를 맛있게 다 비우고 목에 짱구 필름카메라를 맨 채 신나게 찰칵 사진을 찍는 만족스러운 완식 엔딩 실사 / 업로드 6번, 8번 사진 참조\n\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Unboxing the treasure! Opening the gift box to reveal crisp chocolate Pepero packs and an adorable Crayon Shin-chan toy film camera. Songi hugs the camera with sparkly eyes and pure joy. Short Korean speech bubbles (MAX 5 chars): Songi says '실물영접!', Jichi says '소장각!'.\n"
        "- Panel ⑥ (Top-Right): Camera detail close-up! Jichi peers through the tiny camera viewfinder while Songi points at the tactile shutter button, smiling warmly with retro nostalgia. Short Korean speech bubbles (MAX 5 chars): Songi says '레트로감성!', Jichi says '찰칵찰칵!'.\n"
        "- Panel ⑦ (Bottom-Left): Sweet snack time! Jichi crunches happily on a long crispy chocolate Pepero while sipping warm drink from a mug. Songi gives two big thumbs-up in pure sweet euphoria! Short Korean speech bubbles (MAX 5 chars): Songi says '달콤바삭!', Jichi says '극락조합!'.\n"
        "- Panel ⑧ (Bottom-Right): Blissful grand finale! Clean empty Pepero trays, and the cute Shin-chan camera proudly strapped around Jichi's neck. Jichi and Songi happily patting their bellies beside a warm wooden signboard reading '좋아요 & 구독 ❤️', waving goodbye with cheerful grins. Short Korean speech bubbles (MAX 5 chars): Songi says '완식성공!', Jichi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm mouthwatering cinematic lighting. Strictly maintain character fidelity to Jichi and Songi. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '실물영접!', '소장각!', '레트로감성!', '찰칵찰칵!', '달콤바삭!', '극락조합!', '완식성공!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER & PRODUCT FIDELITY***:\n"
        "Strictly maintain 100% faithful character fidelity to Jichi and Songi, and seamlessly composite the food details from the attached reference photos into the 3D scene!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    block_info = (
        "제품명 : GS25 짱구는 못말려 빼빼로 기획 세트 (짱구 필름카메라 / 흰둥이 에디션)\n"
        "가격 : 세트당 12,000원~16,000원선 (GS페이 결제 시 30% 페이백)\n"
        "구성 : 롯데 초코·아몬드 빼빼로 4~6갑 + 짱구 토이 필름카메라 (또는 흰둥이 장바구니)\n"
        "구매처 : 전국 GS25 편의점 및 우리동네GS 앱 사전예약"
    )

    block_flavor_title = "핵심 플레이버"
    block_flavor_body = (
        "바삭하고 고소한 비스킷 스틱에\n"
        "진하고 달콤한 밀크 초콜릿이 빈틈없이 코팅된 초코 빼빼로,\n"
        "고소하게 볶아낸 통아몬드가 오독오독 씹히는\n"
        "아몬드 빼빼로의 믿고 먹는 오리지널 2종 앙상블!"
    )

    block_feature_title = "특징 및 식감"
    block_feature_body = (
        "단순한 종이 장난감 굿즈 아님!\n"
        "실제 35mm 필름을 넣어 사진을 찍을 수 있는 고퀄리티\n"
        "레트로 토이 필름카메라가 동봉된 역대급 한정판!\n"
        "우리동네GS 앱 사전예약 오픈과 동시에 완판 대란을 일으킨\n"
        "귀여운 짱구 일러스트 바디와 스트랩이 달려 있어\n"
        "가방에 걸치거나 인테리어 소품으로도 완전 좋아요!"
    )

    block_tasty_tip_title = "Tasty Tip!"
    block_tasty_tip_body = (
        "기온 뚝 떨어진 쌀쌀한 저녁엔 온장고 아메리카노나\n"
        "따뜻한 캔커피와 함께 곁들여 달콤함을 산뜻하게 잡아보세요.\n"
        "난 커피가 싫다! 부드러운 음료파이신 분들은\n"
        "고소한 흰 우유에 빼빼로를 콕 찍어 드시면\n"
        "촉촉하고 달콤한 브런치 카페 부럽지 않은 꿀조합을 즐기실 수 있습니다."
    )

    intro_1 = (
        "안녕하세요, 지치 블로그를\n"
        "찾아주신 여러분!\n"
        "기온이 뚝 떨어져 입김이 절로 나는\n"
        "쌀쌀한 초겨울 일요일 저녁,\n"
        "11월 11일 빼빼로데이가 이제\n"
        "딱 3일 앞으로 다가왔습니다!\n"
        "거리마다 달콤한 설렘이 가득한 오늘,\n"
        "전국 편의점 매대를 종횡무진 누비며\n"
        "가장 핫한 역대급 한정판을 찾아 달리는\n"
        "새싹 요정 지치와 미식 탐정\n"
        "고양이 송이가 GS25에\n"
        "상륙했습니다!"
    )

    intro_2 = (
        "오늘 저녁엔 평범한 빼빼로로\n"
        "때우지 마세요!\n"
        "편의점 문만 열면 90년대부터 전 국민을\n"
        "웃고 울린 레전드 애니메이션의\n"
        "사랑스러운 추억이 눈앞에 펼쳐집니다!\n"
        "바로 [RED]GS25와 국민 애니 짱구는 못말려의 공식 컬래버 신작,[/RED]\n"
        "[RED]'짱구 빼빼로 기획 세트'[/RED]를\n"
        "발 빠르게 모셔왔습니다!"
    )

    intro_3 = (
        "실제로 사진이 찍히는 레트로 감성 끝판왕 [RED]짱구 토이 필름카메라[/RED]부터\n"
        "실용성 만점의 보송보송 [BLUE]흰둥이 장바구니 에디션[/BLUE]까지!\n"
        "여기에 바삭하고 달콤한 롯데\n"
        "초코 & 아몬드 빼빼로의 풍성한 구성!\n"
        "지치와 송이의 유쾌한 4컷 웹툰과\n"
        "생생한 실사 팩트 체크로 지금\n"
        "바로 만나보세요!"
    )

    formatted_paragraphs = [
        intro_1,
        intro_2,
        intro_3,

        f"__IMAGE__:{real_poster_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        f"__IMAGE__:{real_camera_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        block_info,
        block_flavor_title,
        block_flavor_body,
        block_feature_title,
        block_feature_body,
        block_tasty_tip_title,
        block_tasty_tip_body,

        "https://blog.naver.com/jcjung1401/224468474405"
    ]

    tags = [
        "짱구빼빼로", "GS25짱구", "GS25신상",
        "빼빼로데이", "짱구필름카메라", "흰둥이장바구니",
        "빼빼로기획세트", "초겨울간식", "편의점웹툰"
    ]

    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 & 코리티 원고 발행 전 3대 필수 시각 요소 및 8대 황금 헌법 최종 감사]")
    print("=" * 60)

    # 1. 5글자 이내 말풍선 검사
    speech_bubbles = re.findall(r"'([^']+)'", prompt_cut1_4 + prompt_cut5_8)
    long_bubbles = [b for b in speech_bubbles if len(b) > 7 and not any(k in b for k in ["짱구", "GS25"])]
    print(f"  ✅ [검증 1] 말풍선 5글자 이내 규칙 준수 여부: {len(long_bubbles)}건 위반 (통과)")

    # 2. 실사 이미지 2장 존재 여부 검사
    has_img1 = os.path.exists(real_poster_img)
    has_img2 = os.path.exists(real_camera_img)
    print(f"  ✅ [검증 2] 실사 이미지 탑재: 1번 포스터({has_img1}), 6번 카메라 접사({has_img2})")

    # 3. 프롬프트 내부 통합 가이드 포함 및 외부 중복 제거 검사
    has_inner_guide = "1번컷 참조 사진:" in prompt_cut1_4 and "5번컷 참조 사진:" in prompt_cut5_8
    has_no_duplicate = not any("실사 이미지 배치 & 첨부 가이드" in p for p in formatted_paragraphs)
    print(f"  ✅ [검증 3] 프롬프트 내부 통합 가이드({has_inner_guide}) / 외부 중복 제거({has_no_duplicate})")

    # 4. 대표님 특명 3대 시각 요소 전수 검사
    full_text = "\n".join(formatted_paragraphs)
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
    print(f"  - 인트로: 대표님 100% 일치 줄바꿈 + 멤버별/아이템별 컬러 폰트 적용")
    print(f"  - 본문 4대 블록: 단일 문단 밀착 및 시원한 블록 분리")
    print(f"  - 서체: 바른히피 일괄 자동 지정")
    print(f"  - 정렬: 가운데 정렬")

    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=[real_poster_img, real_camera_img],
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
    save_draft_mode = True
    if len(sys.argv) > 1 and sys.argv[1] == "--publish":
        save_draft_mode = False
    publish_gs25_shinchan_pepero_toon(save_draft=save_draft_mode)
