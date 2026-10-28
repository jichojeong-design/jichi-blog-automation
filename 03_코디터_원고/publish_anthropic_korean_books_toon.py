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


def produce_anthropic_korean_books_webtoon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 IT/테크 웹툰 프로젝트]
    주제: 한국 책 41만 권, 앤트로픽은 왜 샀나? (부산항에서 미국으로 간 165톤 종이책의 비밀)
    등장인물: 지치(새싹 요정) + 초코(턱시도 고양이) + 코봇(귀여운 AI 컴패니언 로봇)
    형식: 네이버 블로그 임시저장 (save_draft=True, category="웹툰")
    """
    title = "[지치와 초코의 테크 웹툰] 한국 책 41만 권, 글로벌 AI 기업 앤트로픽은 왜 부산항에서 배로 실어갔을까?!"

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    search_dir = os.path.join(project_root, "02_코서치_자료")

    img_bulk_carrier = os.path.join(search_dir, "bulk_carrier_books.png")
    img_anthropic_ai = os.path.join(search_dir, "anthropic_ai_concept.png")

    # 1~4컷 ChatGPT용 4분할 프롬프트 (대표님 2대 캐릭터 붕괴 방지 수칙 100% 반영)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left, Cut 1): Inside a modern tech-cozy study room, Jichi (cute green sprout fairy with a leaf on head) is holding a digital tablet with eyes wide in shock, pointing at a breaking news article. Beside Jichi, Choco (sleek black-and-white tuxedo cat) tilts his head in deep curiosity. A cute friendly floating AI robot (sleek white pebble-shaped body, soft glowing blue LED smiling eyes) hovers beside them.\n"
        "- Panel ② (Top-Right, Cut 2): Choco curiously scratches his furry chin, asking the AI robot: 'Wait, 410,000 physical books?! Why would an advanced AI company ship tons of heavy paper books on ocean cargo ships instead of downloading PDF files?' Jichi nods in agreement with puzzled round eyes.\n"
        "- Panel ③ (Bottom-Left, Cut 3 - Giant Book Cargo Ship): The AI robot projects a vivid holographic vision of an epic ocean scene: A massive ocean bulk carrier ship sailing across the vast Pacific ocean from Busan port under golden sunlight, its entire deck piled high with towering stacks of colorful books traveling to America. Jichi and Choco watch the projection in total amazement.\n"
        "- Panel ④ (Bottom-Right, Cut 4): The AI robot demonstrates the book scanning process through a clear projection: Thick hardcover books having their spines carefully cut and unbound, feeding into a high-speed scanner, transforming into glowing digital data streams while paper is neatly recycled. Jichi gasps: 'They unbind and scan physical books?!'\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, warm cinematic tech lighting. Maintain strict fidelity to official reference sheets for Jichi (sprout fairy), Choco (tuxedo cat), and companion robot. Strictly NO garbled fake text. Only short Korean keywords or emoticons ('?!', '대박!'). Panel badges ① ② ③ ④ clearly marked.\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***: You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the sprout fairy and Choco the tuxedo cat) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (앤트로픽 vs 저작권 소송 비하인드 & 훈훈한 결말)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left, Cut 5): Choco asks sharply with paws crossed: 'Why go through all that trouble and expense? Free pirate sites on the internet have millions of books!' The AI robot displays the bold glowing 'ANTHROPIC' logo intersecting with dynamic neural network lines.\n"
        "- Panel ⑥ (Top-Right, Cut 6 - Court Verdict & Fair Use): The AI robot shows a symbolic scales of justice: On one side, pirate downloads marked with a red 'X' (court ruled illegal). On the other side, legitimately purchased physical books scanned for training marked with a green checkmark 'FAIR USE'. Jichi's eyes widen: 'So buying physical books was their legal shield against copyright lawsuits!'\n"
        "- Panel ⑦ (Bottom-Left, Cut 7 - Creators' Rights): Choco thoughtfully touches a warm open book on the desk: 'Still, buying a copy doesn't mean authors agreed to train AI. Transparent book lists and fair compensation for creators must be discussed.' Jichi and the AI robot nod thoughtfully in deep respect for human authors.\n"
        "- Panel ⑧ (Bottom-Right, Cut 8 - Cozy Ending & Subscribe): Jichi, Choco, and the friendly AI robot sitting warmly side-by-side, proudly holding a stack of classic books together, beaming with bright smiles. In front of them, a cute rustic wooden signboard reads '좋아요 & 구독 ❤️'. Golden afternoon sunlight streaming in, inviting viewers to like and subscribe.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm gourmet tech atmosphere. Maintain 100% character design consistency. Keep book textures realistic and beautiful. Strictly NO garbled text. Only short Korean keywords ('좋아요 & 구독 ❤️', '파이팅!'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***: You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the sprout fairy and Choco the tuxedo cat) as the absolute visual anchor. Do NOT rely on prior conversational memory or hallucinate new character designs. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 전 세계 흥미진진한 테크 이슈와 AI 트렌드를 가장 알기 쉽게 전달해 드리는 귀여운 새싹 요정 지치와 턱시도 고양이 초코, 그리고 스마트한 AI 로봇 코봇입니다!",
        "최근 국내 IT 및 출판계에 엄청난 화제를 불러일으킨 뉴스가 있었습니다! 바로 미국 생성형 AI 대표 주자인 **앤트로픽(Anthropic)**이 부산항을 통해 **한국어 종이책 165톤(약 41만 4천 권 추정치)**을 미국으로 실어 날랐다는 소식인데요!",
        "디지털 시대에 왜 인터넷 파일이 아닌 엄청난 무게의 '종이책'을 직접 배로 운송했을까요? 그리고 미국 법원 판결문 속에 숨겨진 놀라운 AI 저작권 비하인드는 무엇일까요? 지치, 초코, 코봇의 흥미진진한 8컷 웹툰으로 그 비밀을 명쾌하게 파헤쳐 드립니다!",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        "1컷 · 아늑한 서재에서 태블릿 뉴스를 보던 지치가 깜짝 놀라며 외친다.",
        "지치: \"초코야, 코봇아! 이거 뉴스 봤어?! 미국의 거대 AI 기업 앤트로픽이 한국 종이책을 무려 41만 권이나 사갔대!\"",
        "초코: \"(눈이 땡그래지며) 뭐냥?! 41만 권?! 도서관 몇 개가 통째로 태평양을 건넌 거냥?!\"",

        "2컷 · 초코가 턱을 긁적이며 AI 로봇 코봇에게 날카로운 의문을 던진다.",
        "초코: \"그런데 코봇아, 요즘 세상에 PDF 같은 디지털 파일로 받으면 1초면 끝나는데, 왜 그 무거운 종이책을 배로 실어 나른 거냥?\"",
        "코봇: \"삐빅! 바로 거기에 앤트로픽의 아주 치밀하고 고도화된 법적 전략이 숨어있어!\"",

        f"__IMAGE__:{img_bulk_carrier}",

        "3컷 · 코봇이 홀로그램으로 부산항을 출발해 태평양을 건너는 거대한 벌크선 화물선을 보여준다.",
        "코봇: \"선적 데이터에 따르면 실제 총중량만 165.69톤! 책 1권당 400g으로 계산하면 약 41만 4천 권에 달하는 규모야. 부산항을 출발해 미국 워싱턴주 타코마항으로 향했지!\"",
        "지치: \"와... 165톤이라니! 바다 위에 떠 있는 거대한 떠돌이 도서관이 따로 없었겠네!\"",

        "4컷 · 코봇이 미국 현지 작업실에서 책의 제본을 뜯어 스캔하는 과정을 보여준다.",
        "코봇: \"미국에 도착한 책들은 제본을 뜯고 페이지를 잘라 초고속 스캐너로 디지털 검색 파일로 변환됐어. 그리고 원본 종이책은 전량 폐기 처리되었단다!\"",
        "초코: \"새 책을 사서 제본을 뜯고 파쇄했다고냥?! 점점 더 미스터리하다냥!\"",

        f"__IMAGE__:{img_anthropic_ai}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "5컷 · 초코가 팔짱을 끼며 고개를 갸우뚱한다.",
        "초코: \"인터넷 해적 사이트나 전자책을 다운받으면 돈도 안 들고 훨씬 편할 텐데, 앤트로픽은 왜 수억 원을 들여 종이책을 사서 뜯은 거냥?\"",
        "코봇: \"핵심은 바로 '저작권 소송 방어'야!\"",

        "6컷 · 코봇이 법원의 정의의 저울을 띄우며 결정적인 판결 비하인드를 설명한다.",
        "코봇: \"미국 법원의 '바츠 대 앤트로픽' 판결에 따르면, 불법 해적 사이트에서 받은 파일은 공정 이용으로 인정받지 못했어. 하지만 정식 구매한 종이책을 스캔해 AI 학습에 쓰는 행위는 합법적인 '공정 이용(Fair Use)'으로 인정받았거든!\"",
        "지치: \"아하! 법적으로 100% 안전하고 깨끗한 학습 데이터를 만들기 위해 진짜 종이책을 구매한 거구나!\"",

        "7컷 · 책을 어루만지며 생각에 잠긴 초코.",
        "초코: \"하지만 종이책 1권을 샀다고 해서 작가님이 AI 학습에 동의한 건 아니지 않냥? 우리 출판계에서도 상세 도서 목록 공개와 정당한 보상 기준을 요구하고 있다냥.\"",
        "지치: \"맞아. 창작자들의 권리가 존중받아야 미래에도 훌륭한 책과 콘텐츠가 계속 나올 수 있으니까!\"",

        "8컷 · 지치와 초코, 코봇이 다 함께 책을 들고 독자들에게 미소를 지으며 전하는 엔딩.",
        "코봇: \"결국 최첨단 AI의 눈부신 지능 뒤에는 인간이 피땀 흘려 써 내려간 소중한 책과 문화라는 데이터 공급망이 있었던 셈이지!\"",
        "초코: \"책도 읽고 AI 상식도 쌓고! 유익하셨다면 공감과 이웃 추가 꾹 눌러주세요냥!\"",

        "[지치와 초코의 테크 톡: 한국 책 41만 권 앤트로픽 사태 5대 팩트 체크]",
        "1. 41만 권의 실체: 실제 권수를 일일이 센 것이 아니라, 수출입 선적 데이터의 총중량 165.69톤을 단행본 평균 무게(400g)로 나눈 추정 수치입니다. 중복 도서나 잡지 포함 여부는 미공개 상태입니다.",
        "2. 유통 및 조달 경로: 국내 대형 도서 유통사인 웅진북센이 도서 공급 계약을 체결했으며, 부산항에서 출발해 미국 워싱턴주 타코마항의 도서 유통사 '베터 월드 북스(Better World Books)'로 인도되었습니다.",
        "3. 종이책 스캔 후 파쇄 방식: 앤트로픽은 구매한 종이책의 제본을 절단하여 고속 스캔한 뒤 원본 종이를 폐기하고 검색 가능한 디지털 텍스트로 전환하여 AI 학습 중앙 자료실을 구축했습니다.",
        "4. 미국 법원의 공정 이용 판결: 미국 법원은 정식 구매한 종이책의 스캔 및 폐기, 그리고 AI 학습 활용을 '형식 전환에 따른 공정 이용'으로 인정했습니다. 반면, 해적 사이트 다운로드 데이터는 불법으로 판단했습니다.",
        "5. 남은 과제와 시사점: 미국 판결이 한국 저작권법에 곧바로 적용되지는 않으며, 종이책 구매가 곧 창작자의 AI 학습 동의를 뜻하지는 않습니다. 향후 데이터 투명성과 정당한 보상 체계 마련이 글로벌 AI 업계의 핵심 화두로 떠오르고 있습니다.",

        "[지치 컴퍼니 테크 에필로그]",
        "지치와 초코, 그리고 코봇이 함께 살펴본 앤트로픽의 한국 책 수급 작전!\n서버와 GPU 반도체뿐만 아니라 인간의 지혜가 담긴 책이야말로 가장 강력한 AI 원유라는 사실을 실감하게 됩니다.\n오늘 분석이 유익하셨다면 공감(좋아요)과 이웃 추가 부탁드립니다!"
    ]

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
        "#앤트로픽",
        "#Anthropic",
        "#클로드",
        "#Claude",
        "#AI학습데이터",
        "#저작권이슈",
        "#공정이용",
        "#웅진북센",
        "#지치웹툰",
        "#IT뉴스",
        "#인공지능",
        "#테크이슈"
    ]

    print("\n" + "=" * 65)
    print("📚 [지치 컴퍼니] 앤트로픽 한국 책 41만 권 웹툰 원고 준비 완료!")
    print(f"  - 제목: {title}")
    print(f"  - 카테고리: 웹툰")
    print(f"  - 벌크선 이미지 경로: {img_bulk_carrier} (존재: {os.path.exists(img_bulk_carrier)})")
    print(f"  - 앤트로픽 AI 이미지 경로: {img_anthropic_ai} (존재: {os.path.exists(img_anthropic_ai)})")
    print(f"  - 총 태그 수: {len(tags)}개 ({', '.join(tags[:6])}...)")
    print(f"  - 총 문단 수: {len(formatted_paragraphs)}")
    print("=" * 65)

    if save_draft:
        success = auto_publisher.post_to_naver_blog(
            title=title,
            content_paragraphs=formatted_paragraphs,
            image_paths=[p for p in [img_bulk_carrier, img_anthropic_ai] if os.path.exists(p)],
            tags=tags,
            category_name="웹툰",
            save_draft=True
        )
        if success:
            print("\n🎉 [성공] 앤트로픽 한국 책 41만 권 웹툰이 네이버 블로그 임시저장함에 안전 등록되었습니다!")
        return success

    return True


if __name__ == "__main__":
    produce_anthropic_korean_books_webtoon(save_draft=True)
