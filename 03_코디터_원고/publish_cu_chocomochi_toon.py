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

def publish_cu_chocomochi_toon():
    """
    [지치 컴퍼니 정규 편의점 신상 디저트 웹툰]
    주제: CU 대란 신상 - 쫀득한 찹쌀떡 속 꾸덕한 파베 생초코 가득! '생초코 모찌' 탐방기
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이)
    형식: 네이버 블로그 임시저장 (save_draft=True, category="웹툰")
    """
    title = "[지치와 송이의 신상 디저트 웹툰] CU 생초코 모찌, 떡이야 초콜릿이야?! 달콤쫀득 끝판왕!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (캐릭터 외형 묘사 완전 배제, 시트 사진 위임)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a brightly lit modern convenience store. Jichi discovers a sleek packaged chocolate dessert '생초코 모찌' in the dessert cooler shelf, eyes sparkling with sheer excitement. Songi jumps up excitedly beside Jichi.\n"
        "- Panel ② (Top-Right): In a cozy warm kitchen, Jichi opens the package on a wooden table, revealing two plump, round, cocoa-dusted dark chocolate mochi balls. Songi sniffs curiously with round, curious eyes.\n"
        "- Panel ③ (Bottom-Left): Jichi gently presses one mochi with a finger, showing its ultra-stretchy, soft, chewy mochi texture. Songi watches in awe with paws raised in anticipation.\n"
        "- Panel ④ (Bottom-Right): Jichi cuts the mochi in half, revealing a super dense, fudgy, rich dark chocolate ganache filling oozing slightly. Songi gasps happily with open paws in delight.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic atmosphere. Strictly NO messy random text or fake letters. Speech bubbles contain ONLY short Korean keywords or simple emoticons ('?!', '초코모찌!', '대박!'). Panel badges ① ② ③ ④ clearly marked.\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (8컷 엔딩 패널 시각적 CTA 반영)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Jichi taking a small bite of the chocolate mochi, smiling warmly with joyful blush on cheeks as rich chocolate melts softly.\n"
        "- Panel ⑥ (Top-Right): Songi takes a bite with eyes squeezed shut in absolute bliss, tiny flower and heart effects floating around Songi's head.\n"
        "- Panel ⑦ (Bottom-Left): Jichi pours a cold glass of fresh white milk and an iced americano on the table. Songi claps paws eagerly for the ultimate dessert pairing.\n"
        "- Panel ⑧ (Bottom-Right): Cozy warm room ending scene. Jichi and Songi waving happily side-by-side with joyful bright smiles. In front of them, a cute rustic wooden sign clearly reads '좋아요 & 구독 ❤️'. A cheerful speech bubble above says '파이팅!'. Warm golden sunlight streaming in, inviting viewers to like and subscribe.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm vibrant cinematic feel. Strictly NO garbled text. Only short Korean keywords or emoticons ('좋아요 & 구독 ❤️', '파이팅!'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pkg_img = os.path.join(project_root, "02_코서치_자료", "chocomochi_sample_1.jpg")
    cross_img = os.path.join(project_root, "02_코서치_자료", "chocomochi_sample_2.jpg")

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 매일 가장 핫하고 맛있는 신상 디저트를 찾아 떠나는 귀여운 새싹 요정 지치와 호기심 대장 고양이 송이입니다!",
        "요즘 편의점 디저트 코너에서 입고되자마자 품절 대란을 일으키며 떡지순례 필수템으로 떠오른 화제의 신상이 있더라고요. 바로 쫀득한 찹쌀떡 속에 진하고 꾸덕한 생초콜릿을 가득 채운 **CU 생초코 모찌**입니다!",
        "겉모습은 평범한 찹쌀떡 같지만, 한 입 베어 무는 순간 입안 가득 퍼지는 달콤쌉싸름한 파베 초콜릿의 황홀한 맛! 지치와 송이의 유쾌한 8컷 웹툰으로 먼저 만나보세요!",
        
        f"__IMAGE__:{pkg_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        "1컷 · 편의점 냉장 매대에서 생초코 모찌를 발견한 지치.",
        "지치: \"드디어 찾았다! 요즘 편의점마다 품절 대란인 생초코 모찌!\"",
        "송이: \"포장부터 달콤한 초코 향이 솔솔 나는 것 같다냥!\"",

        "2컷 · 포장을 열자 코코아 가루가 곱게 뿌려진 통통한 초코모찌가 나온다.",
        "송이: \"우와! 진짜 까맣고 동글동글 귀엽다냥!\"",
        "지치: \"완전 겉면에 코코아 파우더가 소복하게 내려앉았어!\"",

        "3컷 · 찹쌀떡을 손가락으로 살짝 눌러 쫀득함을 확인하는 지치.",
        "지치: \"살짝 눌렀는데도 떡피가 말랑말랑 탄력이 넘쳐!\"",
        "송이: \"얼른 반으로 갈라서 속을 보여달라냥!\"",

        "4컷 · 반으로 가르자 묵직하고 꾸덕한 파베 생초콜릿이 가득 차 있다.",
        "송이: \"크아아앙! 속이 전부 새까만 생초콜릿이다냥!\"",
        "지치: \"빈틈없이 꽉 차 있어! 완전 초코 폭탄이야!\"",

        f"__IMAGE__:{cross_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "5컷 · 한 입 맛보며 초콜릿의 부드러움에 감탄하는 지치.",
        "지치: \"떡은 쫄깃하게 감기고 속은 사르르 녹아내려!\"",
        "송이: \"겉은 쫀득, 속은 사르르! 완벽한 식감 꿀조합이다냥!\"",

        "6컷 · 눈을 감고 달콤한 행복을 만끽하는 송이.",
        "송이: \"이건 그냥 초콜릿이 아니라 예술이다냥!\"",
        "지치: \"고급 파베 초콜릿 전문점 부럽지 않은 퀄리티야!\"",

        "7컷 · 고소한 흰 우유와 아이스 아메리카노를 준비하는 지치.",
        "지치: \"달콤함이 묵직하니까 시원한 음료랑 같이 먹으면 딱이야!\"",
        "송이: \"우유 한 모금, 모찌 한 입! 무한 흡입 가능하다냥!\"",

        "8컷 · 서로 마주보며 행복하게 웃는 지치와 송이.",
        "지치: \"오늘의 편의점 디저트 탐방도 대성공이야!\"",
        "송이: \"내일 또 편의점 달려가서 쟁여둬야겠다냥!\"",

        "[지치와 송이의 솔직 먹방 총평 & 200% 맛있게 먹는 꿀팁]",
        "지치와 송이가 직접 편의점에서 사서 먹어보니, 얇고 찰기 넘치는 찹쌀떡 피와 묵직하고 진한 생초콜릿 가나슈의 밸런스가 정말 환상적이었습니다.",
        "냉장고에서 꺼낸 직후 바로 드시면 꾸덕하고 묵직한 식감을 즐길 수 있고, 상온에 5분 정도 두었다가 드시면 부드러운 생초콜릿이 입안에서 크림처럼 녹아내려 또 다른 매력을 느낄 수 있어요.",
        "진한 단맛이 돋보이기 때문에 쌉싸름한 아이스 아메리카노나 담백한 흰 우유와 함께 곁들이시는 것을 강력 추천합니다.",

        "[지치와 송이의 미각 톡]",
        "지치와 송이가 편의점에서 직접 골라 맛본 내돈내산 솔직 리뷰예요!\n입맛에 따라 느끼는 달콤함은 다를 수 있으니 가볍게 참고해 주세요."
    ]

    # [코디터 1차 자체 검열 및 포맷팅]
    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            # 이미지 마커는 줄바꿈 없이 순수 한 줄로 완벽 보존
            clean_marker = re.sub(r'[\r\n]+', '', p_str)
            formatted_paragraphs.append(clean_marker)
        elif p_str.startswith("[CHATGPT") or p_str.startswith("PANEL LAYOUT"):
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=22))

    tags = [
        "#CU신상",
        "#생초코모찌",
        "#편의점신상",
        "#편의점디저트",
        "#초코모찌",
        "#지치웹툰",
        "#편의점웹툰",
        "#CU디저트",
        "#솔직후기",
        "#디저트추천"
    ]

    print("\n" + "=" * 65)
    print("🍡 [지치 컴퍼니] CU 생초코 모찌 웹툰 원격 임시저장 개시!")
    print(f"  - 제목: {title}")
    print(f"  - 카테고리: 웹툰")
    print(f"  - 포장 실사: {pkg_img} (존재: {os.path.exists(pkg_img)})")
    print(f"  - 단면 실사: {cross_img} (존재: {os.path.exists(cross_img)})")
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
        print("\n🎉 [성공] CU 생초코 모찌 웹툰이 네이버 블로그 임시저장함에 완벽히 등록되었습니다!")
    else:
        print("\n⚠️ [확인 필요] 임시저장 중 문제가 발생했습니다.")

    return success

if __name__ == "__main__":
    publish_cu_chocomochi_toon()
