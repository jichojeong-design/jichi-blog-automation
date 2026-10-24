import os
import sys
import formatter
import auto_publisher

# Windows 콘솔 utf-8 설정
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def publish_tesla_spacex_toon():
    """
    [지치 컴퍼니 정규 AI 테크 뉴스 웹툰]
    주제: 테슬라·스페이스X 합병 논의와 초대형 통합 AI 기업의 탄생 쟁점
    등장인물: 지치(새싹 요정) + 초코(턱시도 고양이) + AI로봇(비저 디스플레이 장착 스마트 미니 로봇)
    형식: 네이버 블로그 임시저장 (save_draft=True, category="웹툰")
    """
    title = "[지치와 초코의 AI 테크툰] 테슬라와 스페이스X 합병설 총정리! 4,600조 원 초대형 AI 제국 탄생할까?"

    # 프롬프트 1 (1~4컷) - 캐릭터 외형 설명 완전 삭제 & 사장님 지정 컷별 복사 태그
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Jichi holding a tablet showing news with Tesla and SpaceX logos merging. AI Robot hovers beside Jichi with glowing question marks on visor. Choco perks ears up with huge curious eyes.\n"
        "- Panel ② (Top-Right): In a high-tech cozy lab, AI Robot projects a giant glowing blue holographic calculator displaying '3.5 Trillion Dollars' ($3.5T). Choco falls back comically with eyes wide open and paws on cheeks in pure disbelief. Jichi looks stunned.\n"
        "- Panel ③ (Bottom-Left): A split futuristic diagram in soft cute style: Left shows a sleek autonomous Tesla car driving smoothly alongside an Optimus humanoid robot; Right shows a Starlink satellite constellation orbiting Earth beaming high-speed data down. AI Robot points proudly with tiny robotic pointer.\n"
        "- Panel ④ (Bottom-Right): AI Robot displays xAI's giant supercomputer brain 'Colossus' with glowing brain nodes connecting Tesla cars and Starlink satellites. Jichi nods with an excited bright smile, understanding the master plan.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic atmosphere. Strictly NO messy random text or fake letters. Speech bubbles contain ONLY short Korean keywords or simple emoticons ('?!', '대박!', '4600조원!'). Panel badges ① ② ③ ④ clearly marked.\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 프롬프트 2 (5~8컷) - 캐릭터 외형 설명 완전 삭제 & 사장님 지정 컷별 복사 태그
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): AI Robot shows a scale balance tilting unsteadily. On one side are Tesla shareholders looking concerned, on the other side is a big space rocket. Jichi looks thoughtful with a finger on chin.\n"
        "- Panel ⑥ (Top-Right): Choco scratches its black ear with a cute puzzled frown, watching a mock Wall Street chart with rising and dipping arrow graphs. AI Robot floats with a thoughtful '...' dot expression on its visor.\n"
        "- Panel ⑦ (Bottom-Left): A dynamic futuristic synergy scene: Sleek Tesla electric vehicle, Starlink global space satellite net, and Optimus humanoid robot moving together in perfect harmony under a bright sunrise horizon. Jichi, Choco, and AI Robot cheer happily together.\n"
        "- Panel ⑧ (Bottom-Right): Cozy warm room ending scene. Jichi and Choco waving happily side-by-side with AI Robot blinking a cute heart '<3' on its visor screen. In front of them, a cute rustic wooden sign clearly reads '좋아요 & 구독 ❤️'. A cheerful speech bubble above says '파이팅!'. Warm golden sunlight streaming in, inviting viewers to like and subscribe.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm vibrant cinematic feel. Strictly NO garbled text. Only short Korean keywords or emoticons ('좋아요 & 구독 ❤️', '파이팅!'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 귀여운 새싹 요정 지치와 호기심 대장 턱시도 고양이 초코, 그리고 똑똑한 AI로봇이 함께하는 AI 테크툰 시간입니다!",
        "최근 월가와 실리콘밸리를 발칵 뒤집어 놓은 초특급 메가톤급 뉴스가 터졌더라고요. 바로 일론 머스크가 이끄는 전기차 제국 '테슬라'와 우주 탐사 기업 '스페이스X'의 공식 합병 논의 소식입니다!",
        "두 공룡 기업이 하나로 뭉치면 기업 가치만 무려 3조 5,000억 달러, 우리 돈으로 약 4,634조 원에 달하는 사상 최대의 통합 AI 제국이 탄생하게 되는데요. 지치와 초코, 그리고 AI로봇이 알기 쉽게 핵심만 쏙쏙 짚어 정리해 드립니다!",
        
        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        "1컷 · 테슬라와 스페이스X의 깜짝 합병 뉴스에 눈이 똥그래진 지치와 초코.",
        "지치: \"초코야 이것 봐! 테슬라랑 스페이스X가 하나로 합병할 수도 있대!\"",
        "초코: \"우주 로켓 쏘는 회사랑 자동차 회사가 왜 합치는 거냥?\"",

        "2컷 · AI로봇이 3조 5,000억 달러라는 천문학적 숫자를 홀로그램으로 띄운다.",
        "AI로봇: \"합병 시 예상 기업가치만 약 4,634조 원! 지구상 가장 거대한 AI 우주 기업이 탄생하는 셈입니다 삐리릭!\"",
        "초코: \"4,600조?! 츄르를 지구 몇 바퀴나 살 수 있는 돈이다냥!\"",

        "3컷 · 우주와 지상을 잇는 미래 기술 연결도를 가리키는 AI로봇.",
        "AI로봇: \"단순한 결합이 아닙니다. 테슬라의 자율주행과 로봇, 그리고 스페이스X의 스타링크 위성 통신망이 완벽히 하나로 이어지게 됩니다!\"",
        "지치: \"우주 인터넷으로 전 세계 테슬라 로봇과 자동차가 24시간 실시간 소통하는 거네!\"",

        "4컷 · 거대 AI 슈퍼컴퓨터와 두뇌 모델 xAI를 설명하는 AI로봇.",
        "AI로봇: \"여기에 일론 머스크의 인공지능 xAI 모델까지 결합하면, 하드웨어와 소프트웨어를 모두 독점하는 완전체 AI 기업이 됩니다!\"",
        "지치: \"말 그대로 지상과 우주를 아우르는 절대 강자가 나오는 거구나!\"",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "5컷 · 턱을 괴고 합병의 현실적인 걸림돌을 고민하는 지치.",
        "지치: \"하지만 합병이 그렇게 쉽게 술술 풀릴 수 있을까? 테슬라는 상장사고 스페이스X는 비상장사잖아.\"",
        "AI로봇: \"맞습니다! 두 회사의 기업 가치를 공정하게 매기는 합병 비율을 두고 주주들의 의견이 팽팽히 맞서고 있습니다.\"",

        "6컷 · 복잡한 월가 주식 차트를 보며 머리를 긁적이는 초코.",
        "초코: \"테슬라 주주들이 손해 본다고 생각하면 강력하게 반대할 수도 있겠다냥!\"",
        "AI로봇: \"게다가 독점 규제 당국의 까다로운 심사도 큰 숙제로 남아 있습니다 삐릭!\"",

        "7컷 · 자율주행차, 스타링크 위성, 휴머노이드 로봇이 나란히 달리는 미래 시너지.",
        "지치: \"그래도 이 거대한 퍼즐이 완성되면 미래 기술 발전 속도가 어마어마하게 빨라질 것 같아!\"",
        "초코: \"지구 어디서든 끊김 없는 인공지능 세상을 진짜 눈으로 보게 될지도 모른다냥!\"",

        "8컷 · 지치와 초코, AI로봇이 손을 흔들며 활짝 웃는다.",
        "지치: \"상상만 해도 흥미진진한 테슬라와 스페이스X의 빅딜! 과연 최종 성사될지 우리 다 함께 지켜봐요!\"",
        "초코: \"오늘 소식 흥미로우셨다면 공감과 이웃 추가 잊지 말라냥!\"",

        "[지치와 초코의 테슬라·스페이스X 합병 핵심 총평]",
        "이번 합병 논의의 진짜 본질은 단순한 몸집 불리기가 아니라, 지상 자율주행(FSD)과 휴머노이드 로봇(옵티머스), 그리고 지구 전역을 덮는 저궤도 위성망(스타링크)을 통합 AI 두뇌(xAI) 하나로 묶는 수직 통합에 있습니다.",
        "성공한다면 전 세계 어떤 빅테크도 흉내 내기 힘든 막강한 하드웨어 및 데이터 생태계가 구축되겠지만, 비상장사인 스페이스X와의 공정한 합병 비율 산정과 주주 설득, 그리고 반독점 규제 당국의 엄격한 심사를 넘어서는 것이 최대 관건이 될 것으로 보입니다.",

        "[안내 및 정보 출처]",
        "본 웹툰과 콘텐츠는 글로벌 테크 및 비즈니스 공식 보도 자료를 바탕으로 비전공자분들도 알기 쉽게 제작된 기술 분석 스토리입니다.\n특정 종목에 대한 투자 권유가 아니며, 모든 투자 및 의사결정의 책임은 투자자 본인에게 있습니다.",
        "테슬라·스페이스X 합병 논의와 통합 AI 기업의 쟁점 원문 보러가기:",
        "https://blog.naver.com/jcjung1401/224450973813"
    ]

    # 모바일 최적화 포맷팅
    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        # 프롬프트 블록이나 영문 프롬프트는 줄바꿈을 과하게 쪼개지 않음
        if p_str.startswith("[ChatGPT") or "A charming 4-panel" in p_str:
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=22))

    tags = [
        "#테슬라",
        "#스페이스X",
        "#일론머스크",
        "#xAI",
        "#스타링크",
        "#옵티머스로봇",
        "#AI뉴스",
        "#테크웹툰",
        "#지치웹툰",
        "#인공지능트렌드"
    ]

    print("\n" + "=" * 65)
    print("🚀 [지치 컴퍼니] 테슬라·스페이스X 합병 테크웹툰 원격 임시저장 개시!")
    print(f"  - 제목: {title}")
    print(f"  - 카테고리: 웹툰")
    print(f"  - 단락 수: {len(formatted_paragraphs)}")
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
        print("\n🎉 [성공] 테슬라·스페이스X AI 테크웹툰이 네이버 블로그 임시저장함에 완벽히 등록되었습니다!")
    else:
        print("\n⚠️ [확인 필요] 임시저장 과정 중 오류가 발생했거나 창이 닫혔습니다.")

if __name__ == "__main__":
    publish_tesla_spacex_toon()
