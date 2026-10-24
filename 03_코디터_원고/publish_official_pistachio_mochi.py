import os
import sys
import time

# Windows 콘솔 인코딩 안전화
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import auto_publisher
import formatter

def produce_and_draft_pistachio_webtoon(cut1_path: str = None, cut2_path: str = None) -> bool:
    """
    [지치 컴퍼니 정규 웹툰 자동화] GS25 한정선 피스타치오 찹쌀떡 탐방 웹툰 공식 등록
    - 코서치(Scout) 엄격 3대 실사 컷(포장, 진짜 단면 반갈, 편의점 매대) 100% 실측 연동
    - 코자이너 3D 픽사 스타일 지치 & 송이 캐릭터 만화 컷 2장 인터리빙
    - 코디터 모바일 최적화(18~24자) 스토리텔링 및 팩트체크/꿀팁
    - 네이버 블로그 임시저장(save_draft=True)으로 안전 등록하여 사장님 최종 검토 지원
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. 코서치 실사 3컷 경로 확인
    shelf_img = os.path.join(base_dir, "pistachio_shelf.png")
    pkg_img = os.path.join(base_dir, "pistachio_package.png")
    cross_img = os.path.join(base_dir, "pistachio_cross_section.png")

    # 2. 3D 만화 컷 경로 확인 (파라미터가 없으면 기본 경로 탐색)
    if not cut1_path or not os.path.exists(cut1_path):
        cut1_path = os.path.join(base_dir, "webtoon_pistachio_cut1.png")
    if not cut2_path or not os.path.exists(cut2_path):
        cut2_path = os.path.join(base_dir, "webtoon_pistachio_cut2.png")

    print("\n" + "=" * 65)
    print("🍡 [지치 컴퍼니] GS25 한정선 피스타치오 찹쌀떡 웹툰 임시저장 시작!")
    print(f"  - 3D 컷 1: {cut1_path} (존재: {os.path.exists(cut1_path)})")
    print(f"  - 매대 실사: {shelf_img} (존재: {os.path.exists(shelf_img)})")
    print(f"  - 포장 실사: {pkg_img} (존재: {os.path.exists(pkg_img)})")
    print(f"  - 단면 실사: {cross_img} (존재: {os.path.exists(cross_img)})")
    print(f"  - 3D 컷 2: {cut2_path} (존재: {os.path.exists(cut2_path)})")
    print("=" * 65)

    title = "[지치와 송이의 신상 디저트 탐방] 두바이 초콜릿 잇는 품절 대란?! GS25 한정선 피스타치오 찹쌀떡 솔직 리뷰!"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 맛있는 신상 디저트를 찾아 떠나는 귀여운 새싹 요정 지치와 미식가 삼색 고양이 송이입니다!",
        "요즘 SNS와 커뮤니티에서 오픈런 없이는 못 산다, 두바이 초콜릿을 능가하는 극강의 고소함이라며 품절 대란을 일으키고 있는 디저트가 있습니다. 바로 GS25 편의점과 프리미엄 찹쌀떡 명가 한정선의 초특급 콜라보, **한정선 피스타치오 찹쌀떡**입니다!",
        f"__IMAGE__:{shelf_img}",
        "[GS25 매대 현장 팩트 체크: 한정선 콜라보의 정체]",
        "가격은 개당 5,900원으로 편의점 디저트 라인 중에서는 확실한 프리미엄 포지셔닝입니다.",
        "성수동과 유명 백화점 팝업스토어에서 줄 서서 먹는 수제 찹쌀떡 명가 한정선이 GS25와 단독 제휴하여 편의점용으로 특별 출시했습니다.",
        "출시 직후부터 각 매장마다 입고 즉시 완판 행진을 기록하며 디저트 오픈런 신드롬을 이어가고 있습니다.",
        f"__IMAGE__:{pkg_img}",
        "지치: '패키지 포장부터 한정선 특유의 단아한 한옥 감성이 물씬 풍겨! 고급스러운 전통 한지 질감 디자인에 꽁꽁 밀봉되어 있어서 신선도가 그대로 유지되네!'",
        "송이: '얼른 봉지를 열어보자냥! 과연 5,900원의 몸값을 톡톡히 해낼지 송이의 깐깐한 미식가 코로 전격 감정해 보겠다냥!'",
        f"__IMAGE__:{cross_img}",
        "[반갈 샷 실물 전격 해부: 두툼한 원물 필링 크림의 진실]",
        "국내산 찹쌀로 빚어낸 떡피는 당일 갓 찧은 인절미처럼 찰기 넘치고 쫀득하게 감기는 극상의 식감을 선사합니다.",
        "단순한 인공 색소가 아닌 고급 피스타치오 원물을 아낌없이 갈아 넣어 묵직하고 꾸덕한 버터크림 앙금이 가득 들어차 있습니다.",
        "크림 속에 콕콕 박힌 통 피스타치오 분태가 씹힐 때마다 오독오독 터지며 진한 견과류 본연의 고소함을 극대화합니다.",
        "송이: '크아아앙! 한 입 베어 물자마자 입안 가득 피스타치오 고소한 향이 팡팡 터진다냥! 쫀득한 떡이랑 진한 크림이 부드럽게 감기면서 완전 천국의 맛이다냥!'",
        "지치: '맞아! 과하게 달지 않고 견과류 본연의 묵직한 고소함이 입안에 맴돌아서 전혀 물리지 않아! 왜 편의점마다 품절 대란이 났는지 바로 납득되는 맛이야!'",
        "[지치와 송이의 솔직 총평 & 맛있게 먹는 꿀팁]",
        "살짝 얼려 먹는 크림 모찌 꿀팁으로, 상온에서 완전히 녹여 드시기보다 냉동실에서 꺼낸 뒤 딱 5분에서 10분 정도 자연 해동했을 때 드시면 겉은 쫀득하고 속은 고급 피스타치오 젤라또처럼 사르르 녹아내려 만족감이 배가됩니다.",
        "커피 페어링으로는 피스타치오의 묵직한 버터리함이 돋보이므로 산미가 있는 깔끔한 아이스 아메리카노나 진한 콜드브루와 곁들이면 최고급 디저트 카페 부럽지 않은 조화를 이룹니다.",
        "품절 대란 구매 팁으로 GS25 공식 앱인 우리동네GS의 재고 찾기 기능을 활용해 주변 매장 입고 시간을 미리 확인 후 방문하시면 헛걸음 없이 겟하실 수 있습니다.",
        "\n\n소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n오늘 전해드린 편의점 신상 리뷰가 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다! 지치와 송이가 매일 가장 핫한 편의점 신상과 최신 트렌드를 전달해 드리겠습니다."
    ]

    # 모바일 최적화 줄바꿈 포맷팅 (이미지 마커 보존)
    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=22))

    tags = [
        "#GS25신상",
        "#한정선",
        "#한정선피스타치오",
        "#피스타치오찹쌀떡",
        "#편의점디저트",
        "#GS25디저트",
        "#지치웹툰",
        "#편의점신상추천",
        "#솔직후기",
        "#두바이초콜릿"
    ]

    all_images = [cut1_path, shelf_img, pkg_img, cross_img, cut2_path]
    valid_images = [img for img in all_images if img and os.path.exists(img)]

    print(f"\n📤 네이버 스마트에디터 원격 임시저장 개시 (유효 이미지: {len(valid_images)}장)...")
    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=valid_images,
        category_name="웹툰",
        tags=tags,
        save_draft=True
    )

    if success:
        print(f"\n🎉 [미션 완수] GS25 피스타치오 찹쌀떡 웹툰이 네이버 블로그 임시저장함에 안전 등록되었습니다!")
    else:
        print(f"\n🚨 [주의] 임시저장 과정 중 오류가 발생했습니다.")

    return success

if __name__ == "__main__":
    c1 = sys.argv[1] if len(sys.argv) > 1 else None
    c2 = sys.argv[2] if len(sys.argv) > 2 else None
    produce_and_draft_pistachio_webtoon(c1, c2)
