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

def publish_yonsei_bam_tiramisu_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 디저트 웹툰]
    주제: 흑백요리사 나폴리 맛피아 공식 콜라보 2탄! CU '연세우유 맛폴리 밤 티라미수 생크림빵'
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 - 흑백요리사 광팬)
    
    [대표님 & 친누나 600+ / 1,300+ 조회수 폭발 3대 영구 수칙 100% 엄수]:
    1. 4컷 웹툰 이후 나오는 긴 텍스트 대화(대본) 전면 삭제! (방문객 이탈 방지 & 초고속 핵심 전달)
    2. 코자이너 웹툰 말풍선 글자는 무조건 '5글자 이내' 초심플 한글 키워드만 삽입!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 제품명부터 깔끔하게 시작) 100% 적용!
    4. 글씨체는 네이버 감성 손글씨 '바른히피' 기본 적용!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 흑백요리사 2탄 출시?! CU '연세우유 밤 티라미수 생크림빵' 오픈런 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (대표님 수칙: 말풍선 글자 5글자 이내 초심플 키워드 엄수!)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy living room. Songi the calico cat (passionate cooking show fan) is jumping with sheer excitement holding up a smartphone showing news of a new dessert collaboration! Jichi the green sprout fairy looks with wide sparkling eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '대박사건!', Jichi says '진짜?!'.\n"
        "- Panel ② (Top-Right): Songi excitedly holding Jichi's hand, pointing toward the door with absolute determination. A cute backpack on Jichi's back. Short Korean speech bubbles (MAX 5 chars): Songi says '출동하자!', Jichi says 'CU로!'.\n"
        "- Panel ③ (Bottom-Left): Outdoor running scene! Jichi and Songi sprinting enthusiastically toward a bright neon CU convenience store down the street, tiny motion dash lines. Short Korean speech bubbles (MAX 5 chars): Songi says '전속력!', Jichi says '달려!'.\n"
        "- Panel ④ (Bottom-Right): Inside CU bakery shelf. Jichi and Songi spotting the very last stylish black package of '연세우유 밤 티라미수 생크림빵' featuring the chef collaboration, eyes filled with blissful stars. Short Korean speech bubbles (MAX 5 chars): Jichi says '찾았다!', Songi says '마지막1개!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic lighting. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '대박사건!', '진짜?!', '출동하자!', 'CU로!', '전속력!', '달려!', '찾았다!', '마지막1개!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (대표님 수칙: 말풍선 글자 5글자 이내 초심플 키워드 엄수!)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Cozy wooden table setting. Jichi opens the black bread package, revealing a plump, soft dark-chocolate coated coffee bread. Songi sniffs with twitching whiskers and starry eyes. Short Korean speech bubbles (MAX 5 chars): Jichi says '묵직해!', Songi says '향대박!'.\n"
        "- Panel ⑥ (Top-Right): Cross-section reveal! Jichi and Songi gently pull the bread apart in half with both paws. An explosive avalanche of silky chestnut whipped cream and rich coffee custard cream oozes out luxuriously! Short Korean speech bubbles (MAX 5 chars): Jichi says '크림폭탄!', Songi says '우와아!'.\n"
        "- Panel ⑦ (Bottom-Left): Songi and Jichi taking a blissful big bite. Songi makes a hilarious passionate gourmet judge expression with eyes closed in heaven, surrounded by sparkle effects. Short Korean speech bubbles (MAX 5 chars): Songi says '이븐하다!', Jichi says '천상의맛!'.\n"
        "- Panel ⑧ (Bottom-Right): Cozy warm room ending scene. Jichi and Songi holding dessert spoons, waving cheerfully side-by-side with proud happy smiles. In front of them, a cute rustic wooden signboard reads '좋아요 & 구독 ❤️'. Short Korean speech bubble (MAX 5 chars): '내일또봐!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm gourmet cinematic feel. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '묵직해!', '향대박!', '크림폭탄!', '우와아!', '이븐하다!', '천상의맛!', '내일또봐!', '좋아요 & 구독 ❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코서치가 수집한 실물 사진 2장 경로 연동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_pkg_img = os.path.join(project_root, "02_코서치_자료", "yonsei_marron_tiramisu_real_1.jpg")
    real_cross_img = os.path.join(project_root, "02_코서치_자료", "yonsei_marron_tiramisu_real_2.jpg")

    # [대표님 & 친누나 황금 양식 100% 준수]
    # 1. 4컷 이후 나오는 불필요한 긴 대본 대화 전면 삭제!
    # 2. 구분선 없이 바로 제품명부터 깔끔하게 시작하는 친누나표 팩트 체크 & Tasty Tip!
    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 매일 가장 핫하고 맛있는 편의점 신상을 찾아 발 빠르게 달려가는 귀여운 새싹 요정 지치와 흑백요리사 찐팬 고양이 송이입니다!",
        "얼마 전 전 국민적인 품절 대란을 일으킨 나폴리 맛피아의 '밤 티라미수 컵' 기억하시죠? 그 뜨거운 인기에 힘입어 편의점 디저트의 황제 연세우유와 공식 협업한 역대급 후속작이 전격 출시되었습니다! 바로 **CU '연세우유 맛폴리 밤 티라미수 생크림빵'**입니다!",
        "묵직한 초코빵 속에 고소한 가을 밤 생크림과 쌉싸름한 커피 커스터드를 빈틈없이 가득 채운 화제의 신상! 지치와 송이의 유쾌한 웹툰과 실사 팩트 체크로 지금 바로 만나보세요!",

        f"__IMAGE__:{real_pkg_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        f"__IMAGE__:{real_cross_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "제품명 : CU 연세우유 '맛폴리 밤 티라미수 생크림빵'",

        "가격 : 3,400원 (130g / 468 kcal)",

        "매장 : 포켓CU 및 전국 CU 오프라인 매장",

        "핵심 플레이버: 진하고 부드러운 가을\n밤 생크림 + 쌉싸름한 커피 커스터드 크림 +\n촉촉하고 쫀득한 다크 초코 빵 시트",

        "특징 및 식감: 인공적인 바밤바 맛 아님!\n은은하게 퍼지는 고급스러운 밤 풍미와\n쌉싸름한 티라미수 커피 크림의 황금밸런스\n반으로 가르면 쏟아져 나오는 폭탄 크림이 완전 좋아요",

        "Tasty Tip!\n얼죽아 사람들과 딱인 깔끔한 아아와 함께!\n난 커피가 싫다! 담백한 우유러버이신 분들은\n고소하고 시원한 흰 우유와 좋아요",

        "[지치와 송이의 미각 톡]",
        "지치와 송이가 화제의 흑백요리사 신상을 직접 내돈내산으로 구매해 솔직하게 맛본 후기입니다!\n품절 대란템인 만큼 포켓CU 앱 재고 조회를 활용해 꼭 득템해 보세요."
    ]

    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            clean_marker = re.sub(r'[\r\n]+', '', p_str)
            formatted_paragraphs.append(clean_marker)
        elif "[CHATGPT" in p_str or "\n" in p_str:
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=20))

    tags = [
        "#CU신상", "#흑백요리사", "#연세우유밤티라미수", "#맛폴리",
        "#나폴리맛피아", "#밤티라미수생크림빵", "#편의점디저트", "#지치웹툰"
    ]

    images_to_post = [real_pkg_img, real_cross_img]

    print("\n" + "=" * 65)
    print("🌰 [지치 컴퍼니] CU '연세우유 밤티라미수 생크림빵' 웹툰 네이버 블로그 임시저장 시작!")
    print(f"  - 제목: {title}")
    print(f"  - 카테고리: 웹툰")
    print(f"  - 서체: 바른히피 자동 지정")
    print("=" * 65)

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
    publish_yonsei_bam_tiramisu_toon(save_draft=True)
