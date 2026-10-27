import os
import sys
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import formatter
import auto_publisher

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def produce_culinary_tiramisu_webtoon():
    """
    [지치 컴퍼니 정규 편의점 디저트 웹툰 - 흑백요리사 밤 티라미수 컵 에디션]
    주제: 흑백요리사 찐팬 송이와 지치의 CU '밤 티라미수 컵' 오픈런 득템 & 천상계 미식 리뷰!
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 - 흑백요리사 열혈 팬)
    형식: 네이버 블로그 임시저장 (save_draft=True, category="웹툰")
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 흑백요리사 우승작 실물 영접?! CU '밤 티라미수 컵' 오픈런 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (대표님 특명: 2번 컷 흑백요리사 포스터 영역 완전 평면 90도 정면 배치, 뒤틀림/왜곡 제로!)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left, Cut 1): Inside a cozy living room, Jichi (cute green sprout fairy) and Songi (calico cat with big expressive eyes) are watching a cooking survival show on a living room TV. Songi's eyes are glowing with passionate food-lover stars, holding paws to cheeks in pure amazement: 'Jichi! The legendary chestnut tiramisu from the show is officially sold at convenience stores!' Jichi looks on with curious round eyes.\n"
        "- Panel ② (Top-Right, Cut 2 - CRITICAL FLAT POSTER FRAME): Songi enthusiastically gestures toward ONE large vertical rectangular poster hanging on the wall. ***STRICT REQUIREMENT FOR POSTER: The poster MUST be perfectly perpendicular to the camera at an exact 90-degree front-facing angle, 100% FLAT, ZERO perspective distortion, ZERO 3D tilt, ZERO slanted angle, crisp sharp rectangular edges, completely distortion-free***. Songi stands neatly next to it pointing proudly. Jichi nods with glowing admiration.\n"
        "- Panel ③ (Bottom-Left, Cut 3): Energetic outdoor motion scene! Songi passionately grabs Jichi's hand and dashes toward a bright blue-and-purple CU convenience store down the street, running at full speed with cute motion dash-lines and determination: 'Hurry Jichi! Before it sells out!'\n"
        "- Panel ④ (Bottom-Right, Cut 4): Inside the air-conditioned convenience store refrigerated dessert showcase. Jichi and Songi spot the very last glowing 'Chestnut Tiramisu Cup' on the shelf, eyes wide in ecstatic euphoria, raising paws in triumphant celebration!\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, vibrant colors, warm cinematic lighting. Strictly follow official character sheets of Jichi (sprout fairy with leaf on head) and Songi (tri-color calico cat). Panel ② poster MUST remain totally flat and square-on to camera without perspective warping. Strictly NO garbled fake text. Only short cute Korean keywords or emoticons ('대박!', '출동!'). Panel badges ① ② ③ ④ clearly displayed.\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***: You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy and Songi the calico cat) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (디저트 단면 클로즈업 + 안성재 패러디 이븐(Even) 리액션)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left, Cut 5): Clean wooden dining table setting. Jichi and Songi admiring the sleek Chestnut Tiramisu Cup packaging placed in the center. Songi enthusiastically explains the layers: rich autumn chestnut cream, aromatic toffee nut cream, crunchy chocolate granola, and espresso ladyfingers.\n"
        "- Panel ⑥ (Top-Right, Cut 6 - Dessert Cross-Section): Close-up dessert shot! A golden dessert spoon scoops deep into the tiramisu, revealing rich multi-textured layers of smooth chestnut whipped cream, chocolate ganache, and golden crunchy granola toppings. Front-facing, mouth-watering gourmet dessert rendering with zero weird angle distortion.\n"
        "- Panel ⑦ (Bottom-Left, Cut 7 - The Even Reaction): Songi takes a big blissful bite and undergoes a hilarious, dramatic gourmet judge moment (parodying Chef Ahn Sung-jae): eyes wide in heavenly shock, surrounded by dramatic culinary light beams, holding paws up in critique: 'The chestnut sweetness and cream cheese balance is SO EVEN! 100 points out of 100!' Jichi also tastes it with euphoric heart eyes!\n"
        "- Panel ⑧ (Bottom-Right, Cut 8 - Cozy Ending & Subscribe): Jichi and Songi sitting together with happy dessert spoons, giving big thumbs-up with satisfied smiles. In front of them, a cute rustic wooden signboard clearly reads '좋아요 & 구독 ❤️'. Warm golden afternoon sunlight, inviting viewers to like and subscribe.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm gourmet atmosphere. Maintain character fidelity for Jichi and Songi. Keep dessert textures realistic and delectable. Strictly NO garbled text. Only short Korean keywords ('좋아요 & 구독 ❤️', '최고다냥!'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***: You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy and Songi the calico cat) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    search_dir = os.path.join(project_root, "02_코서치_자료")

    # 대표님이 사진을 구해 넣어주실 3대 실사 배치 경로 (기존 파일 또는 신규 배치 대기)
    poster_path = os.path.join(search_dir, "culinary_class_wars_poster.png")
    tiramisu_cup_path = os.path.join(search_dir, "tiramisu_cup_real.png")
    tiramisu_spoon_path = os.path.join(search_dir, "tiramisu_spoon_real.png")

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 맛있는 신상 간식이라면 언제나 레이더를 바짝 세우고 출동하는 귀여운 새싹 요정 지치와 삼색 고양이 송이입니다!",
        "요즘 대한민국을 가장 뜨겁게 달군 화제의 넷플릭스 예능, 다들 보셨나요?! 바로 《흑백요리사: 요리 계급 전쟁》인데요! 흑백요리사의 열렬한 광팬인 송이가 며칠 전부터 밤잠을 설치며 노래를 부르던 초특급 화제템이 드디어 편의점에 실물로 출시되었습니다!",
        "편의점 재료 미션에서 심사위원들의 극찬을 받으며 압도적 1위를 차지했던 나폴리 맛피아(권성준 셰프)의 전설적인 디저트, **CU '밤 티라미수 컵'**을 지치와 송이가 오픈런으로 어렵게 공수해 왔습니다! 포켓CU 사전예약 오픈 20분 만에 완판되며 전국적인 품절 대란을 일으킨 그 화제의 맛, 지치와 송이의 유쾌한 8컷 웹툰으로 만나보세요!",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        "1컷 · 아늑한 거실 TV 앞에서 흑백요리사를 초집중해서 보며 눈을 반짝이는 송이와 호기심 가득한 지치.",
        "송이: \"지치야! 대박 사건이다냥! 흑백요리사에서 나폴리 맛피아가 만든 그 밤 티라미수가 CU에 진짜로 출시됐다냥!\"",
        "지치: \"우와, 진짜?! 심사위원들이 극찬했던 그 편의점 레시피 디저트 말이야?!\"",

        "2컷 · 벽에 걸린 흑백요리사 공식 포스터를 가리키며 열변을 토하는 송이.",
        "송이: \"맞다냥! 사전예약 열리자마자 20분 만에 전량 매진된 바로 그 전설의 화제작이다냥! 지금 당장 편의점으로 달려가야 한다냥!\"",
        "지치: \"품절되기 전에 얼른 신발 신고 출동하자!\"",

        f"__IMAGE__:{poster_path}",

        "3컷 · 송이가 지치의 손을 잡고 동네 CU 편의점을 향해 쏜살같이 전력 질주하는 둘.",
        "송이: \"품절되면 울 거다냥! 전속력으로 달린다냥!\"",
        "지치: \"송이야, 같이 가! 편의점 냉장 디저트 코너로 직행하자!\"",

        "4컷 · CU 편의점 냉장 디저트 매대에서 기적처럼 딱 하나 남은 '밤 티라미수 컵'을 발견하고 환호하는 둘.",
        "지치: \"찾았다! 여기 딱 하나 남아있어! 우리가 마지막 주인공이야!\"",
        "초코: \"대박이다냥! 갓 나온 밤 티라미수 컵 영접 성공이다냥!\"",

        f"__IMAGE__:{tiramisu_cup_path}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "5컷 · 깔끔한 원목 테이블 위에 밤 티라미수 컵을 모셔두고 경건하게 패키지를 감상하는 둘.",
        "송이: \"가을 제철 밤 생크림에 고소한 토피넛 라떼 크림, 그리고 바삭한 초콜릿 그래놀라가 층층이 쌓여 있다냥!\"",
        "지치: \"비주얼부터 편의점 디저트 퀄리티를 훌륭하게 뛰어넘었어!\"",

        "6컷 · 스푼으로 밤 티라미수를 깊숙이 푹 떠올려 단면의 풍성한 밤 크림과 그래놀라 층을 보여주는 둘.",
        "지치: \"숟가락으로 푹 뜨니까 속 안에 에스프레소 시트랑 크림이 묵직하게 가득 차 있어!\"",
        "송이: \"달콤하고 고소한 가을 밤 향기가 코끝을 확 스친다냥!\"",

        f"__IMAGE__:{tiramisu_spoon_path}",

        "7컷 · 한 입 가득 맛보고 눈에 별이 번쩍 뜨이며 안성재 심사위원 빙의 리액션하는 송이.",
        "송이: \"(심각한 표정으로 감탄하며) ...이건 밤의 단맛과 크림치즈의 밸런스가 아주 '이븐(Even)'하게 완벽하다냥! 100점 만점에 100점이다냥!\"",
        "지치: \"(눈이 땡그래지며) 우와! 진짜 고급 레스토랑에서 먹는 티라미수처럼 입안에서 사르르 녹아내려!\"",

        "8컷 · 둘이 행복하게 웃으며 디저트 스푼을 들고 건배하는 훈훈한 엔딩.",
        "지치: \"오픈런으로 어렵게 구한 보람이 200% 있어! 올가을 최고의 편의점 인생 디저트야!\"",
        "송이: \"맛도 감동도 최고! 밤 티라미수 꼭 드셔보시라냥! 좋아요와 구독 꾹 눌러주세요냥!\"",

        "[지치와 송이의 CU 흑백요리사 '밤 티라미수 컵' 팩트 체크]",
        "1. 상품명 및 가격: CU '밤 티라미수 컵' / 4,900원 (포켓CU 및 오프라인 매장)",
        "2. 핵심 플레이버: 달콤하고 부드러운 밤 생크림 + 고소한 토피넛 라떼 크림 + 쌉싸름한 에스프레소 시트 + 바삭한 오트 그래놀라와 초콜릿 칩 토핑",
        "3. 특징 및 식감: 단순한 단맛이 아닌, 묵직한 밤 퓨레와 크림치즈의 밸런스가 뛰어나며 중간중간 씹히는 그래놀라 토핑이 씹는 재미를 극대화해 줍니다.",
        "4. 맛있게 먹는 꿀팁: 진하고 달콤한 편이므로 차가운 아이스 아메리카노나 따뜻한 얼그레이 홍차와 함께 곁들이면 깔끔하게 완벽한 조화를 이룹니다.",

        "[지치와 송이의 미각 톡]",
        "지치와 송이가 화제의 흑백요리사 디저트를 직접 내돈내산으로 솔직하게 맛보고 전해드린 100% 리얼 후기예요!\n품절 대란템인 만큼 포켓CU 앱 재고 조회를 활용해 꼭 득템해 보세요."
    ]

    # [코디터 1차 포맷팅]
    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            clean_marker = re.sub(r'[\r\n]+', '', p_str)
            formatted_paragraphs.append(clean_marker)
        elif p_str.startswith("[CHATGPT") or p_str.startswith("PANEL LAYOUT"):
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=22))

    tags = [
        "#CU신상",
        "#흑백요리사",
        "#밤티라미수",
        "#밤티라미수컵",
        "#나폴리맛피아",
        "#권성준셰프",
        "#편의점디저트",
        "#안성재",
        "#지치웹툰",
        "#편의점신상",
        "#디저트추천",
        "#내돈내산"
    ]

    print("\n" + "=" * 65)
    print("🌰 [지치 컴퍼니] CU 흑백요리사 '밤 티라미수 컵' 웹툰 원고 네이버 블로그 임시저장 등록 시작!")
    print(f"  - 제목: {title}")
    print(f"  - 카테고리: 웹툰")
    print(f"  - 총 태그 수: {len(tags)}개 ({', '.join(tags[:6])}...)")
    print(f"  - 총 단락 수: {len(formatted_paragraphs)}")
    print("=" * 65)

    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=[],
        tags=tags,
        category_name="웹툰",
        save_draft=True
    )

    if success:
        print("\n🎉 [임시저장 성공] CU 흑백요리사 '밤 티라미수 컵' 웹툰 원고 및 프롬프트가 네이버 블로그 임시저장함에 안전 등록되었습니다!")
    else:
        print("\n⚠️ [확인 필요] 임시저장 중 문제가 발생했습니다.")

    return success


if __name__ == "__main__":
    produce_culinary_tiramisu_webtoon()
