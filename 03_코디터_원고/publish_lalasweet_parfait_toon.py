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
    [대표님 & 친누나 600+ 조회수 3대 영구 수칙 100% 반영]
    1. 4컷 웹툰 이후 나오는 긴 텍스트 대화(1컷~8컷 대본) 전면 삭제! (방문객에게 빠르게 신상 핵심 전달)
    2. 코자이너 웹툰 말풍선 글자는 무조건 '5글자 이내' 초심플 한글 키워드만 삽입!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 100% 적용!
    """
    title = "[지치와 송이의 편의점 웹툰] CU 라라스윗 저당 파르페 요거놀라 솔직 후기! 요아정 부럽지 않은 가성비 끝판왕"

    # 코자이너 1~4컷 ChatGPT용 4분할 프롬프트 (말풍선 5글자 이내 초심플 키워드 엄수!)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a bright modern CU convenience store. Jichi the green sprout fairy discovers '라라스윗 저당 파르페 요거놀라' in the freezer. Short Korean speech bubbles (MAX 5 chars): Jichi says '찾았다!', Songi says '대박!'.\n"
        "- Panel ② (Top-Right): At a wooden table, Jichi opens the clear lid revealing giant crunchy chocolate balls and golden granola over white yogurt ice cream. Short Korean speech bubbles (MAX 5 chars): Songi says '우와!', Jichi says '비주얼봐!'.\n"
        "- Panel ③ (Bottom-Left): Jichi scoops a big spoonful showing chocolate ball, crispy granola, pink grapefruit syrup, and white yogurt ice cream. Short Korean speech bubbles (MAX 5 chars): Jichi says '한입크게!', Songi says '침고인다냥!'.\n"
        "- Panel ④ (Bottom-Right): Jichi and Songi tasting the parfait with sparkling eyes and tiny heart effects. Short Korean speech bubbles (MAX 5 chars): Jichi says '완전상큼!', Songi says '바삭달콤!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful cute cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '찾았다!', '대박!', '우와!', '비주얼봐!', '한입크게!', '완전상큼!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 5~8컷 ChatGPT용 4분할 프롬프트 (말풍선 5글자 이내 초심플 키워드 엄수!)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Jichi points happily at the cup nutrition info with a thumbs-up. Songi pats its tummy in relief. Short Korean speech bubbles (MAX 5 chars): Jichi says '당류8g!', Songi says '살안찐다냥!'.\n"
        "- Panel ⑥ (Top-Right): Jichi adds frozen mango and blueberries next to the parfait cup on the wooden table. Short Korean speech bubbles (MAX 5 chars): Jichi says '과일추가!', Songi says '꿀조합!'.\n"
        "- Panel ⑦ (Bottom-Left): Jichi and Songi scooping the bottom yogurt ice cream blended with honey-grapefruit syrup. Short Korean speech bubbles (MAX 5 chars): Jichi says '자몽최고!', Songi says '순삭이다냥!'.\n"
        "- Panel ⑧ (Bottom-Right): Cozy ending scene. Jichi and Songi waving happily behind a cute wooden sign reading '좋아요 & 구독 ❤️'. Short Korean speech bubble (MAX 5 chars): '최고다냥!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm vibrant cinematic feel. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '당류8g!', '꿀조합!', '최고다냥!', '좋아요 & 구독 ❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "lalasweet_parfait_real_1.jpg")
    real_open_img = os.path.join(project_root, "02_코서치_자료", "lalasweet_parfait_real_2.jpg")

    # [대표님 특명 반영]
    # 1. 4컷 이후 나오는 불필요한 텍스트 대화(1컷~8컷 대사 나열) 완전 삭제!
    # 2. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 그대로 적용!
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 매일 가장 핫하고 맛있는 편의점 신상을 찾아 발 빠르게 달려가는 귀여운 새싹 요정 지치와 호기심 대장 고양이 송이입니다!",
        "요즘 SNS 디저트계를 뜨겁게 달구고 있는 요거트 아이스크림 열풍, 다들 알고 계시죠? 전문점에서 토핑 몇 개만 얹어도 1만 원을 훌쩍 넘겨 부담스러우셨던 분들을 위해 CU 편의점에서 가성비 끝판왕 역대급 신상을 내놓았습니다. 바로 **'라라스윗 저당 파르페 요거놀라'**입니다!",
        "3,500원이라는 착한 가격에 대왕 초코볼과 바삭한 그래놀라, 달콤쌉싸름한 꿀자몽 시럽에 새하얀 요거트 아이스크림까지 알차게 꽉 채운 특급 신상! 지치와 송이의 웹툰과 실사 팩트 체크로 지금 바로 만나보세요!",
        
        f"__IMAGE__:{real_pkg_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        f"__IMAGE__:{real_open_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "제품명 : CU '라라스윗 저당 파르페 요거놀라'",

        "가격 : 3,500원 (195kcal / 당류 8g)",

        "매장 : 포켓CU 및 전국 CU 오프라인 매장",

        "핵심 플레이버: 산뜻한 저당 요거트\n아이스크림 + 달콤쌉싸름 꿀자몽 시럽 +\n바삭한 오트 그래놀라 + 왕초코볼 토핑",

        "특징 및 식감: 밍밍한 다이어트 맛 아님!\n상큼한 요거트와 꿀자몽 시럽의 황금밸런스\n콰삭바삭 씹히는 왕초코볼과 그래놀라 토핑이 완전 좋아요",

        "Tasty Tip!\n요아정 러버라면 냉동 망고나 블루베리 추가와 함께!\n난 깔끔한 디저트가 좋다! 얼죽아 분들은\n아아 한 잔 곁들이면 입안이 개운해서 좋아요",

        "[지치와 송이의 미각 톡]",
        "지치와 송이가 CU 편의점에서 직접 내돈내산으로 구매해 솔직하게 맛본 후기입니다!\n품절 대란템인 만큼 포켓CU 앱 재고 조회를 활용해 꼭 득템해 보세요."
    ]

    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            clean_marker = re.sub(r'[\r\n]+', '', p_str)
            formatted_paragraphs.append(clean_marker)
        elif "[CHATGPT" in p_str or "-----" in p_str or "\n" in p_str:
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=20))

    tags = [
        "#CU신상", "#라라스윗", "#파르페요거놀라", "#저당파르페",
        "#요거트아이스크림", "#편의점디저트", "#저당디저트", "#지치웹툰"
    ]

    images_to_post = [real_pkg_img, real_open_img]

    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=images_to_post,
        category_name="웹툰",
        tags=tags,
        save_draft=save_draft
    )
    return success

if __name__ == "__main__":
    publish_lalasweet_parfait_toon(save_draft=True)
