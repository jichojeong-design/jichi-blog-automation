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

def publish_lalasweet_parfait_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 디저트 웹툰]
    주제: CU 라라스윗 저당 파르페 요거놀라 (요아정 부럽지 않은 가성비 저당 파르페)
    원칙:
    1. 코서치가 수집한 '진짜 실물 사진(패키지 및 내용물 오픈 컷)' 2장을 본문에 적재적소 배치
    2. 코디터는 실사 사진과 팩트에 맞춰 알차고 생생한 본문 구성
    3. 코자이너의 웹툰 프롬프트는 임의 생성 삽입하지 않고, 대표님께서 직접 생성하실 수 있도록 '명령 프롬프트 블록'으로만 본문에 완벽 배치
    4. 임시저장(save_draft=True, category="웹툰")으로 등록
    """
    title = "[지치와 송이의 편의점 웹툰] CU 라라스윗 저당 파르페 요거놀라 솔직 후기! 요아정 부럽지 않은 가성비 끝판왕"

    # 코자이너 1~4컷 ChatGPT용 4분할 프롬프트
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a bright and clean modern CU convenience store. Jichi the green sprout fairy discovers a transparent cup dessert '라라스윗 저당 파르페 요거놀라' in the ice cream freezer. Visible through the clear cup are rich honey-grapefruit syrup drizzles on the inner walls and crunchy chocolate balls on top. Jichi points at it with sparkling excited eyes. Songi the calico cat jumps up beside Jichi with cheerful joy.\n"
        "- Panel ② (Top-Right): In a cozy warm room at a wooden table. Jichi carefully opens the clear plastic lid of the parfait cup. The top is generously loaded with giant crunchy chocolate balls and golden roasted granola over white yogurt ice cream. Songi sniffs the sweet honey-grapefruit scent with curious round eyes and twitching whiskers.\n"
        "- Panel ③ (Bottom-Left): Jichi holds a dessert spoon and scoops a big bite showing layers: crunchy chocolate ball, crispy granola, pinkish grapefruit jam drizzle, and smooth white yogurt ice cream. Songi watches in awe with paws raised in eager anticipation.\n"
        "- Panel ④ (Bottom-Right): Jichi and Songi both tasting the parfait. Jichi's eyes widen with joy from the crispy, sweet and tangy combination. Songi smiles blissfully with tiny cute heart effects floating around.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic lighting. Strictly NO random gibberish text or messy letters. Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 5~8컷 ChatGPT용 4분할 프롬프트
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Close-up shot of the parfait layers. Jichi shows a clear comparison graphic pointing out 'Only 8g Sugar! 195 kcal!' with a happy thumb-up. Songi pats its tummy in relief, smiling happily knowing it's a healthy low-sugar dessert.\n"
        "- Panel ⑥ (Top-Right): Creative food hack moment. On the wooden table, Jichi sprinkles extra frozen mango and blueberries next to the parfait cup, turning it into a luxurious high-end dessert cafe style parfait. Songi drools happily with paws clapped together.\n"
        "- Panel ⑦ (Bottom-Left): Jichi and Songi scooping the bottom layer where the smooth tangy yogurt ice cream blends harmoniously with the bittersweet honey-grapefruit syrup. A clean spoon leaving a swirl in the ice cream cup.\n"
        "- Panel ⑧ (Bottom-Right): Warm cozy ending scene. Jichi and Songi standing side by side waving happily with bright friendly smiles. In front of them, a cute rustic wooden signboard reads '좋아요 & 댓글 ❤️'. Soft golden sunlight in the background, creating a cozy and inviting vibe for readers to leave likes and subscribe.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm vibrant cinematic feel. Strictly NO garbled text. Only short Korean keywords or emoticons ('좋아요 & 댓글 ❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코서치가 수집한 고화질 진짜 실사 사진 2장 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "lalasweet_parfait_real_1.jpg")
    real_open_img = os.path.join(project_root, "02_코서치_자료", "lalasweet_parfait_real_2.jpg")

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 매일 가장 핫하고 맛있는 편의점 신상을 찾아 발 빠르게 달려가는 귀여운 새싹 요정 지치와 호기심 대장 고양이 송이입니다!",
        "요즘 SNS 디저트계를 뜨겁게 달구고 있는 요거트 아이스크림 열풍, 다들 알고 계시죠? 전문점에서 토핑 몇 개만 얹어도 1만 원을 훌쩍 넘겨 부담스러우셨던 분들을 위해 CU 편의점에서 가성비 끝판왕 역대급 신상을 내놓았습니다. 바로 **'라라스윗 저당 파르페 요거놀라'**입니다!",
        "3,500원이라는 착한 가격에 대왕 초코볼과 바삭한 그래놀라, 달콤쌉싸름한 꿀자몽 시럽에 새하얀 요거트 아이스크림까지 알차게 꽉 채운 특급 신상! 지치와 송이의 유쾌한 8컷 웹툰과 실사 팩트체크로 지금 바로 만나보세요!",
        
        # 코서치 수집 실사 1: 제품 패키지 실물 컷
        f"__IMAGE__:{real_pkg_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        "1컷 · 편의점 아이스크림 냉동고에서 화제의 파르페를 발견한 지치.",
        "지치: \"송이야 여기 봐! SNS에서 요아정 가성비 저격템으로 난리 난 요거놀라 파르페 드디어 찾았어!\"",
        "송이: \"투명 컵 사이로 꿀자몽 시럽 흘러내리는 비주얼 좀 보라냥! 포장부터 침샘 폭발이다냥!\"",

        "2컷 · 뚜껑을 열자 큼직한 초코볼과 고소한 그래놀라가 소복이 쏟아져 나온다.",
        "송이: \"우와! 뚜껑 끝까지 대왕 초코볼이랑 그래놀라가 꽉 차 있다냥!\"",
        "지치: \"토핑 아끼지 않고 듬뿍 올린 거 실화야?! 달콤한 자몽 향도 은은하게 올라와!\"",

        "3컷 · 스푼 가득 초코볼, 그래놀라, 요거트 아이스크림을 듬뿍 떠올리는 지치.",
        "지치: \"스푼으로 크게 한 술 떴더니 바삭한 토핑 밑으로 부드러운 하얀 요거트가 사르르 따라올라와!\"",
        "송이: \"얼른 한입 크게 먹어보고 맛을 알려달라냥!\"",

        "4컷 · 한입 가득 넣고 바삭 상큼한 맛에 눈이 번쩍 뜨인 지치와 송이.",
        "지치: \"바사삭 씹히는 초코볼에 상큼하고 시원한 요거트 아이스크림이 입안에서 사르르 녹아내려!\"",
        "송이: \"꿀자몽 시럽의 새콤달콤함이 밋밋함을 싹 잡아줘서 끝없이 들어가는 맛이다냥!\"",

        # 코서치 수집 실사 2: 내용물 오픈 및 토핑 디테일 컷
        f"__IMAGE__:{real_open_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "5컷 · 영양 성분표를 확인하고 당류 수치에 놀라는 지치와 송이.",
        "지치: \"이렇게 달콤하고 토핑이 가득한데 당류가 고작 8g에 195 칼로리밖에 안 돼!\"",
        "송이: \"일반 파르페 칼로리의 절반 수준이다냥! 늦은 밤에 야식으로 먹어도 양심에 안 찔린다냥!\"",

        "6컷 · 집에 있는 냉동 망고와 블루베리를 곁들여 초호화 파르페를 만드는 지치.",
        "지치: \"편의점 냉동 과일을 살짝 곁들이면 전문점 8,000원짜리 생과일 요거트 파르페로 변신해!\"",
        "송이: \"가성비로 홈카페 파르페를 완벽하게 즐기는 최고의 꿀조합이다냥!\"",

        "7컷 · 바닥의 상큼한 요거트와 꿀자몽 시럽을 싹싹 긁어먹는 송이.",
        "지치: \"마지막 한 스푼까지 꿀자몽 잼이 알차게 스며있어서 전혀 물리지 않아!\"",
        "송이: \"스푼을 내려놓을 수가 없다냥! 올여름 인생 디저트로 정했다냥!\"",

        "8컷 · 만족스럽게 배를 두드리며 독자들에게 손을 흔드는 지치와 송이.",
        "지치: \"3,500원으로 누리는 최고의 요거트 파르페 행복! 여러분도 CU에서 꼭 맛보세요!\"",
        "송이: \"맛있게 보셨다면 공감과 댓글 꾹! 내일 또 맛있는 신상 들고 찾아오겠다냥!\"",

        "[CU 라라스윗 저당 파르페 요거놀라 팩트 체크]",
        "- 가격: 3,500원 (전국 CU 편의점 단독 판매)",
        "- 용량 및 칼로리: 215ml / 195 kcal (일반 파르페 대비 약 50% 가벼운 열량)",
        "- 핵심 성분: 당류 단 8g (대체당 알룰로스 설계로 당류 부담 대폭 감소)",
        "- 3단 레이어 구조: 상단 바삭한 대왕 초코볼 & 고소한 그래놀라 + 측면 달콤쌉싸름 꿀자몽 시럽 드리즐 + 베이스 새하얀 플레인 저당 요거트 아이스크림",

        "[지치와 송이의 솔직 총평 & 200% 맛있게 먹는 꿀조합 팁]",
        "1. 처음부터 섞지 마시고 윗부분의 바삭한 초코볼과 그래놀라의 크런치한 식감을 먼저 즐기신 뒤, 중간부터 스푼을 깊숙이 넣어 벽면의 꿀자몽 잼과 요거트 아이스크림을 골고루 섞어 드시면 마지막 한입까지 환상적인 조화를 만끽하실 수 있습니다.",
        "2. 편의점 냉동 코너의 '냉동 망고'나 '블루베리'를 몇 알 얹어 함께 드시면 프리미엄 요거트 전문점 부럽지 않은 고급 과일 파르페로 완벽 업그레이드됩니다.",
        "3. 달콤한 디저트가 간절하지만 식단 관리나 칼로리 때문에 망설여지실 때, 당류 8g의 라라스윗 요거놀라 파르페가 가장 훌륭하고 현명한 선택지가 되어줄 것입니다.",

        "[지치와 송이의 미각 톡]",
        "지치와 송이가 CU 편의점에서 직접 내돈내산으로 구매해 솔직하게 맛본 후기입니다!\n개인의 입맛에 따라 산미와 달콤함의 선호도가 다를 수 있으니 가볍게 참고해 주세요."
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
        elif "[CHATGPT" in p_str:
            # 프롬프트 원문은 마크다운 코드 블록으로 가독성 보존
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=18))

    tags = [
        "#CU신상", "#라라스윗", "#파르페요거놀라", "#저당파르페",
        "#요거트아이스크림", "#편의점디저트", "#저당디저트", "#지치웹툰"
    ]

    # 코서치 실사 2장 이미지 경로
    images_to_post = [real_pkg_img, real_open_img]

    print(f"  * 본문 총 단락 수: {len(formatted_paragraphs)}개")
    print(f"  * 삽입될 코서치 실사 이미지: {images_to_post}")

    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=images_to_post,
        category_name="웹툰",
        tags=tags,
        save_draft=save_draft
    )

    if success:
        print(f"\n🎉 [CU 라라스윗 파르페 웹툰] 네이버 블로그 임시저장함 등록 완벽 성공!")
    return success

if __name__ == "__main__":
    publish_lalasweet_parfait_toon(save_draft=True)
