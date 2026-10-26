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

def publish_rescene_narangd_toon():
    """
    [지치 컴퍼니 정규 편의점 음료/웹툰 프로젝트 - 포토카드 대란 업그레이드 완결판]
    주제: 공원 러닝 후 갈증 폭발! 리센느 찐팬 초코의 나랑드 사이다 맛 추천 & 한정판 포토카드 득템 작전!
    등장인물: 지치(새싹 요정) + 초코(턱시도 고양이 - 리센느 열혈 팬)
    형식: 네이버 블로그 임시저장 (save_draft=True, category="웹툰")
    """
    title = "[지치와 초코의 편의점 탐방 웹툰] 러닝 후 갈증 폭발?! 리센느의 나랑드 사이다 제로와 한정판 포토카드 득템기!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (포토카드 키포인트 반영)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): In a sunlit city park, Jichi and Choco are finishing a vigorous running workout. Jichi is panting heavily with cute sweat drops flying, hands on knees. Choco is wiping brow, looking spirited.\n"
        "- Panel ② (Top-Right): Inside a cool, brightly lit convenience store. Exhausted Jichi stumbles toward the drink refrigerator with tongue out, looking for any cold beverage to quench extreme thirst.\n"
        "- Panel ③ (Bottom-Left): In the drink cooler, Jichi randomly picks up a cold blue Narangd Cider can. Behind Jichi, Choco's eyes suddenly turn into giant shining stars, pointing at the can in shock and sheer excitement.\n"
        "- Panel ④ (Bottom-Right): Choco passionately grabs Jichi's shoulders with fiery fan enthusiasm, squealing: 'Jichi! That's Narangd Cider with my ultimate favorite idol group RESCENE as official models!' Jichi blinks in surprised awe.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic atmosphere. Maintain the exact character designs of Jichi (sprout fairy) and Choco (black-and-white tuxedo cat) from reference sheets. Strictly NO messy random text or fake letters. Speech bubbles contain ONLY short Korean keywords or simple emoticons ('?!', '헉!', '리센느!'). Panel badges ① ② ③ ④ clearly marked.\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (맛 추천 + 포토카드 필수 구매 강조 + 지치도 입덕)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Choco dramatically explains the deliciousness, pointing at Pineapple and Green Apple Narangd cans. Choco insists: 'The fizzy sweet Pineapple and tart Green Apple are unbeatable zero-calorie kings!'\n"
        "- Panel ⑥ (Top-Right): Choco proudly pulls out an official RESCENE photo card from pocket, showing it to Jichi with sparkling eyes: 'And the absolute best part? You can get rare limited-edition RESCENE photo cards! We MUST buy it!'\n"
        "- Panel ⑦ (Bottom-Left): Jichi's eyes instantly widen with huge hearts, jumping up with both paws raised: 'Wait, I'm a huge RESCENE fan too! We are definitely getting both flavors and the photo cards!'\n"
        "- Panel ⑧ (Bottom-Right): Cozy warm room ending scene. Jichi and Choco happily holding ice-cold Narangd Cider cans and shiny RESCENE photo cards together, smiling joyfully. In front of them, a cute rustic wooden sign clearly reads '좋아요 & 구독 ❤️'. A cheerful speech bubble above says '파이팅!'. Warm golden sunlight streaming in, inviting viewers to like and subscribe.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm vibrant cinematic feel. Strictly NO garbled text. Only short Korean keywords or emoticons ('좋아요 & 구독 ❤️', '파이팅!'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    poster_img = os.path.join(project_root, "02_코서치_자료", "narangd_rescene_poster.png")
    flavor_img = os.path.join(project_root, "02_코서치_자료", "narangd_flavor_1.jpg")
    photocard_img = os.path.join(project_root, "02_코서치_자료", "narangd_photocard_1.jpg")

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 푸른 가을 날씨에 공원 러닝을 신나게 뛰고 온 귀여운 새싹 요정 지치와 열정 넘치는 턱시도 고양이 초코입니다!",
        "오늘 초코와 공원에서 파워 러닝을 마치고 났더니 온몸에 땀이 쏟아지고 목이 바짝 말라 시원한 음료를 마시러 편의점으로 직행했는데요. 냉장 매대에서 우연히 나랑드 사이다를 집어 들자마자, 갑자기 초코의 눈빛이 180도 돌변했습니다!",
        "바로 대세 걸그룹 **리센느(RESCENE)**의 열렬한 찐팬이었던 초코의 폭풍 영업이 시작된 건데요! 갈증을 싹 날려주는 상큼한 맛 추천은 물론, 팬들의 심장을 뛰게 만드는 **한정판 리센느 포토카드** 득템 꿀팁까지! 지치와 초코의 리얼 덕질 8컷 웹툰으로 만나보세요!",

        f"__IMAGE__:{poster_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        "1컷 · 햇살 좋은 공원 산책로에서 숨을 헐떡이며 러닝을 마친 지치와 초코.",
        "지치: \"헉... 헉... 초코야, 오늘 러닝 진짜 제대로 불태웠다! 목말라!\"",
        "초코: \"지치야, 땀 엄청 흘렸네냥! 얼른 시원한 편의점으로 피신하자냥!\"",

        "2컷 · 편의점 음료 냉장 코너로 땀을 흘리며 비틀비틀 걸어가는 지치.",
        "지치: \"갈증 폭발 직전이야! 시원한 탄산음료 아무거나 빨리 마실래!\"",
        "초코: \"음료수는 어떤 걸 골라도 시원하니까 편하게 골라봐라냥!\"",

        "3컷 · 냉장고에서 파란색 나랑드 사이다 캔을 우연히 쏙 집어 드는 지치.",
        "지치: \"오! 이거 시원해 보인다! 나랑드 사이다 제로 마셔야지!\"",
        "초코: \"(순간 눈이 휘둥그레지며) ...어?! 지치야, 방금 그거 집은 거 맞냥?!\"",

        "4컷 · 지치의 어깨를 붙잡고 불타는 눈빛으로 폭풍 영업을 시작하는 초코.",
        "초코: \"지치야! 대박 사건이다냥! 그거 내가 제일 사랑하는 걸그룹 리센느가 전속 모델이다냥!\"",
        "지치: \"으응?! 초코 너 리센느 팬이었어?! 나랑드 사이다 모델이 리센느였어?!\"",

        f"__IMAGE__:{flavor_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "5컷 · 플레인, 파인애플, 그린애플 캔을 가리키며 열정적으로 맛을 설명하는 초코.",
        "초코: \"나랑드 사이다는 제로 칼로리라 운동 끝나고 마시기 최고인데, 톡 쏘는 파인애플이랑 상큼한 그린애플이 진짜 천상의 맛이다냥!\"",
        "지치: \"우와, 과일 맛도 있어?! 땀 흘리고 마시면 진짜 속이 뻥 뚫리겠다!\"",

        "6컷 · 비장의 무기처럼 반짝이는 리센느 포토카드를 짠 꺼내 보여주는 초코.",
        "초코: \"하지만 진짜 핵심은 따로 있다냥! 나랑드 사이다 패키지를 사면 한정판 리센느 포토카드를 준다냥! 이건 무조건 사먹어야 한다냥!\"",
        "지치: \"(눈이 하트로 변하며) 헉! 포토카드까지 준다고?! 대박!\"",

        f"__IMAGE__:{photocard_img}",

        "7컷 · 지치도 팬심이 폭발하여 양손에 캔을 들고 활짝 웃는다.",
        "지치: \"사실 나도 리센느 완전 좋아하잖아! 맛있는 파인애플맛도 마시고 포카도 모아야지! 나도 살래!\"",
        "초코: \"크으으! 역시 지치도 리센느의 매력을 아는구나냥! 우리 오늘부터 1일 1나랑드다냥!\"",

        "8컷 · 시원한 나랑드 사이다 캔과 반짝이는 리센느 포토카드를 들고 건배하는 둘.",
        "지치: \"갈증도 싹 날리고 최애 포카까지 득템해서 기분 최고야!\"",
        "초코: \"맛도 제로, 기분은 100점! 리센느와 나랑드 사이다 파이팅이다냥!\"",

        "[지치와 초코의 리센느 x 나랑드 사이다 제로 & 포토카드 완전 정복 팁]",
        "동아오츠카 나랑드 사이다는 제로 칼로리, 제로 슈거로 운동 후 칼로리 부담 없이 청량감을 만끽할 수 있는 대표 탄산음료입니다.",
        "오리지널 플레인의 깔끔한 탄산감도 훌륭하지만, 러닝 후 당길 때는 달콤한 파인애플과 상큼한 그린애플 향이 피로를 날려주는 최고의 선택이 됩니다.",
        "특히 팬들의 뜨거운 반응을 얻고 있는 한정판 리센느 포토카드 증정 이벤트는 온라인 기획전 및 굿즈 패키지를 통해 한정 수량으로 진행되니, 최애 멤버 포카를 노리시는 분들은 재고 소진 전에 서두르시는 것을 추천드립니다.",

        "[지치와 초코의 미각 톡]",
        "지치와 초코가 공원 러닝 후 직접 편의점에서 내돈내산으로 상큼하게 즐긴 솔직 음료 리뷰예요!\n입맛에 따라 선호하는 과일 향이 다를 수 있으니 취향에 맞게 골라보세요."
    ]

    # [코디터 1차 자체 검열 및 포맷팅]
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

    # 대표님 특명: 리센느 및 나랑드 관련 태그 10~12개 풍성하게 세팅
    tags = [
        "#나랑드사이다",
        "#나랑드사이다제로",
        "#리센느",
        "#RESCENE",
        "#리센느포토카드",
        "#리센느포카",
        "#나랑드사이다포토카드",
        "#편의점음료추천",
        "#제로칼로리탄산",
        "#지치웹툰",
        "#동아오츠카",
        "#편의점신상"
    ]

    print("\n" + "=" * 65)
    print("🥤 [지치 컴퍼니] 리센느 x 나랑드 사이다 (포토카드 에디션) 웹툰 임시저장 개시!")
    print(f"  - 제목: {title}")
    print(f"  - 카테고리: 웹툰")
    print(f"  - 포스터 실사: {poster_img} (존재: {os.path.exists(poster_img)})")
    print(f"  - 3종 실사: {flavor_img} (존재: {os.path.exists(flavor_img)})")
    print(f"  - 포토카드 실사: {photocard_img} (존재: {os.path.exists(photocard_img)})")
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
        print("\n🎉 [성공] 포토카드 키포인트 반영 리센느 x 나랑드 사이다 웹툰이 네이버 블로그 임시저장함에 완벽히 등록되었습니다!")
    else:
        print("\n⚠️ [확인 필요] 임시저장 중 문제가 발생했습니다.")

    return success

if __name__ == "__main__":
    publish_rescene_narangd_toon()
