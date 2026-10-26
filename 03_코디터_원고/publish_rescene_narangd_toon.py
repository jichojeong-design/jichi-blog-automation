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
    [지치 컴퍼니 정규 편의점 음료/웹툰 프로젝트]
    주제: 공원 러닝 후 갈증 해소! 리센느(RESCENE) 전속 모델 '나랑드 사이다' 탐방기
    등장인물: 지치(새싹 요정) + 초코(턱시도 고양이)
    형식: 네이버 블로그 임시저장 (save_draft=True, category="웹툰")
    """
    title = "[지치와 초코의 편의점 탐방 웹툰] 러닝 후 갈증 폭발?! 리센느의 나랑드 사이다 제로 전격 추천!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (지치와 초코 배정, 시트 사진 위임)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): In a vibrant green city park trail with blue sky, Jichi and Choco are finishing a vigorous running workout. Jichi has a tiny sweatband on head, panting with lots of cute sweat droplets flying. Choco looks energetic, wiping brow playfully.\n"
        "- Panel ② (Top-Right): Inside a brightly lit, air-conditioned convenience store beverage aisle. Jichi walks up to the glowing drink cooler with tongue out from thirst, staring at the refreshing ice-cold rows of cans.\n"
        "- Panel ③ (Bottom-Left): Jichi spots the bright blue and white Narangd Cider can with a poster of girl group RESCENE above it. Jichi gasps in pure delight, eyes sparkling wide while pointing at the can.\n"
        "- Panel ④ (Bottom-Right): Choco smiles confidently with paws crossed on chest, nodding proudly and telling Jichi: 'Narangd Cider has been my all-time favorite zero-calorie drink!'\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic atmosphere. Maintain the exact character designs of Jichi (sprout fairy) and Choco (black-and-white tuxedo cat) from reference sheets. Strictly NO messy random text or fake letters. Speech bubbles contain ONLY short Korean keywords or simple emoticons ('?!', '갈증 폭발!', '나랑드!'). Panel badges ① ② ③ ④ clearly marked.\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (언제부터 모델이었는지 + 맛 추천 + 8컷 엔딩 패널 시각적 CTA)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Jichi eagerly asks Choco while holding the can: 'When did girl group RESCENE become the official model?' Choco winks with a smart finger raised, explaining the refreshing 2024 campaign.\n"
        "- Panel ⑥ (Top-Right): In front of the shelf, Choco examines three colorful Narangd Cider cans: Plain (Blue), Pineapple (Yellow), and Green Apple (Green). Choco checks phone reviews with an expert critic expression.\n"
        "- Panel ⑦ (Bottom-Left): Choco excitedly hands Jichi the yellow Pineapple and green Green Apple cans, recommending them as the ultimate fruity zero-cider picks! Jichi takes a refreshing sip, eyes bursting with cool fizzy sparkling bubbles.\n"
        "- Panel ⑧ (Bottom-Right): Cozy warm room ending scene. Jichi and Choco waving happily side-by-side with joyful bright smiles, holding ice-cold Narangd cans. In front of them, a cute rustic wooden sign clearly reads '좋아요 & 구독 ❤️'. A cheerful speech bubble above says '파이팅!'. Warm golden sunlight streaming in, inviting viewers to like and subscribe.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm vibrant cinematic feel. Strictly NO garbled text. Only short Korean keywords or emoticons ('좋아요 & 구독 ❤️', '파이팅!'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    poster_img = os.path.join(project_root, "02_코서치_자료", "narangd_rescene_poster.png")
    flavor_img = os.path.join(project_root, "02_코서치_자료", "narangd_flavor_1.jpg")

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 쾌청한 날씨를 맞아 건강하게 땀 흘리고 돌아온 귀여운 새싹 요정 지치와 든든한 턱시도 고양이 초코입니다!",
        "오늘 근처 공원에서 초코와 함께 파워 러닝을 신나게 달리고 났더니 온몸에 땀이 비 오듯 쏟아지고 목이 타들어갈 것 같더라고요! 그래서 갈증을 단숨에 날려버리기 위해 곧장 편의점 음료수 코너로 달려갔습니다.",
        "그런데 시원한 냉장 매대에서 지치의 눈을 단번에 사로잡은 주인공이 있었으니, 바로 대세 걸그룹 **리센느(RESCENE)**가 상큼하게 반겨주는 **나랑드 사이다 제로**였습니다! 지치와 초코의 유쾌한 8컷 편의점 탐방 웹툰으로 지금 바로 확인해보세요!",

        f"__IMAGE__:{poster_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        "1컷 · 푸른 공원 산책로에서 숨을 헐떡이며 러닝을 마친 지치와 초코.",
        "지치: \"헉... 헉... 초코야, 오늘 러닝 진짜 제대로 불태웠다!\"",
        "초코: \"지치야, 땀 엄청 흘렸네! 얼른 시원한 거 마시러 가자냥!\"",

        "2컷 · 시원한 에어컨이 나오는 편의점 음료수 냉장 매대로 돌진하는 지치.",
        "지치: \"목말라 죽겠어! 시원한 탄산음료 어디 있지?!\"",
        "초코: \"음료수 코너는 내가 꽉 잡고 있으니 따라와라냥!\"",

        "3컷 · 매대에서 상큼한 리센느 포스터와 나랑드 사이다를 발견하고 눈이 번쩍 뜨인 지치.",
        "지치: \"어?! 대세 걸그룹 리센느가 왜 여기서 나와?! 나랑드 사이다 모델이었어?!\"",
        "초코: \"오! 나랑드 사이다! 내가 평소에도 칼로리 없어서 엄청 애정하는 음료다냥!\"",

        "4컷 · 가슴을 펴고 뿌듯한 미소를 짓는 초코.",
        "지치: \"초코 넌 원래부터 나랑드 사이다 좋아했어?\"",
        "초코: \"당연하지냥! 제로 칼로리 사이다 원조라 운동 후에 이만한 게 없다냥!\"",

        f"__IMAGE__:{flavor_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "5컷 · 캔을 만지작거리며 리센느 모델 발탁 시기를 물어보는 지치.",
        "지치: \"근데 초코야, 나랑드 사이다가 언제부터 리센느였어?\"",
        "초코: \"이번 2024년 7월에 동아오츠카에서 청량함의 끝판왕으로 리센느를 전격 발탁했다냥! 신곡과 함께 TV 광고까지 완전 핫하다냥!\"",

        "6컷 · 플레인, 파인애플, 그린애플 3종 캔을 꼼꼼히 살피며 리뷰를 검색하는 초코.",
        "지치: \"오리지널 말고 파인애플이랑 그린애플도 있네?! 어떤 맛이 제일 맛있어?\"",
        "초코: \"잠깐만 기다려봐냥! 초코의 특급 리뷰 분석 레이더를 가동해 보겠다냥!\"",

        "7컷 · 초코가 지치에게 과일맛 캔을 쥐여주며 최고의 맛을 추천한다.",
        "초코: \"리뷰를 싹 분석해 보니, 톡 쏘는 탄산에 달콤한 과즙 향이 팡팡 터지는 '파인애플'이랑 상큼한 '그린애플'이 인기 폭발이다냥!\"",
        "지치: \"(한 모금 꿀꺽 마신 뒤) 캬아아! 속이 뻥 뚫려! 파인애플 향 진짜 달콤하고 청량해!\"",

        "8컷 · 얼음처럼 시원한 캔을 들고 활짝 웃으며 건배하는 지치와 초코.",
        "지치: \"칼로리 부담도 제로인데 갈증까지 싹 날아가네! 초코 추천 최고야!\"",
        "초코: \"운동 끝나고 마시는 리센느의 나랑드 사이다, 앞으로 우리 러닝 필수템이다냥!\"",

        "[지치와 초코의 나랑드 사이다 제로 3종 전격 분석 & 200% 꿀조합 팁]",
        "리센느가 전속 모델로 활약 중인 동아오츠카 나랑드 사이다는 4가지 제로(칼로리, 슈거, 색소, 보존료)를 자랑하는 대한민국 대표 제로 탄산음료입니다.",
        "초코의 실시간 편의점 리뷰 분석에 따르면, 오리지널 플레인은 특유의 깔끔하고 개운한 청량감이 돋보이며, 파인애플과 그린애플은 과일 본연의 향긋한 풍미가 톡 쏘는 탄산과 어우러져 디저트 음료로도 큰 사랑을 받고 있습니다.",
        "특히 야외 러닝이나 운동 후 땀을 많이 흘렸을 때 살얼음이 띄워진 얼음컵에 파인애플이나 그린애플을 부어 마시면 카페 에이드 못지않은 극상의 시원함을 느끼실 수 있습니다.",

        "[지치와 초코의 미각 톡]",
        "지치와 초코가 공원 운동 후 직접 편의점에서 내돈내산으로 시원하게 즐긴 솔직 음료 리뷰예요!\n입맛에 따라 선호하는 과일 향이 다를 수 있으니 취향에 맞게 골라보세요."
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

    tags = [
        "#나랑드사이다",
        "#나랑드사이다제로",
        "#리센느",
        "#RESCENE",
        "#편의점음료",
        "#제로칼로리",
        "#지치웹툰",
        "#편의점신상",
        "#솔직후기",
        "#동아오츠카"
    ]

    print("\n" + "=" * 65)
    print("🥤 [지치 컴퍼니] 리센느 x 나랑드 사이다 웹툰 원격 임시저장 개시!")
    print(f"  - 제목: {title}")
    print(f"  - 카테고리: 웹툰")
    print(f"  - 포스터 실사: {poster_img} (존재: {os.path.exists(poster_img)})")
    print(f"  - 3종 실사: {flavor_img} (존재: {os.path.exists(flavor_img)})")
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
        print("\n🎉 [성공] 리센느 x 나랑드 사이다 웹툰이 네이버 블로그 임시저장함에 완벽히 등록되었습니다!")
    else:
        print("\n⚠️ [확인 필요] 임시저장 중 문제가 발생했습니다.")

    return success

if __name__ == "__main__":
    publish_rescene_narangd_toon()
