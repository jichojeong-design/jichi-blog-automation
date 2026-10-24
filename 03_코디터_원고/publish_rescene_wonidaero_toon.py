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

def publish_rescene_wonidaero_toon():
    """
    [지치 컴퍼니 정규 리센느 웹툰]
    주제: 리센느 원이와 창원 '원이대로'의 운명적 만남! 마산대학교 축제 입성기
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이)
    형식: 네이버 블로그 임시저장 (save_draft=True, category="웹툰")
    """
    title = "[지치와 송이의 리센느 웹툰] 창원 '원이대로'의 주인이 떴다?! 리센느 마산대 축제 상륙 비하인드!"

    # 코자이너 1~4컷 프롬프트 (캐릭터 외형 설명 완전 배제, 사장님 캐릭터 시트 사진에 100% 위임)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Jichi holding a smartphone pointing with round eyes at a big blue Korean road sign that clearly reads '원이대로'. Beside Jichi, Songi perches up with glowing amber eyes and perked ears in hilarious excitement.\n"
        "- Panel ② (Top-Right): In a cozy room, Songi holds a glowing lightstick dreaming of K-pop girl group RESCENE. A soft dreamy cloud thought bubble shows RESCENE's stylish idol Woni smiling. Jichi smiles warmly nodding along.\n"
        "- Panel ③ (Bottom-Left): Jichi looks at a packed world tour calendar notebook sighing gently. Songi looks comically disappointed with folded ears and pouting face, wishing Woni could visit Changwon.\n"
        "- Panel ④ (Bottom-Right): Breaking news notification pops up on screen showing '마산대학교 축제 RESCENE 출동!'. Jichi and Songi jump into the air in pure joy, high-fiving with sparkling happy stars around them.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, colorful, cute cinematic atmosphere. Strictly NO messy random text or fake letters. Speech bubbles contain ONLY short Korean keywords or simple emoticons ('?!', '원이대로?!', '대박!'). Panel badges ① ② ③ ④ clearly marked.\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 5~8컷 프롬프트 (8컷 엔딩 패널 '좋아요 & 구독 ❤️' 및 '파이팅!' 반영)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Jichi driving a cute toy convertible car with Songi wearing cool sunglasses on the passenger seat, cruising down a wide sunny highway with a blue road sign '창원 원이대로'.\n"
        "- Panel ⑥ (Top-Right): University campus festival concert stage filled with energetic cheering crowd. Four stylish K-pop idol silhouettes performing under bright pink stage lights and colorful fireworks.\n"
        "- Panel ⑦ (Bottom-Left): In the front concert crowd, Songi vigorously waves a pink lightstick with teary sparkling eyes of happiness. Jichi claps excitedly cheering with a beaming smile.\n"
        "- Panel ⑧ (Bottom-Right): Cozy warm room ending scene. Jichi and Songi waving happily side-by-side with bright joyful smiles. In front of them, a cute rustic wooden sign clearly reads '좋아요 & 구독 ❤️'. A cheerful speech bubble above says '파이팅!'. Warm golden sunlight streaming in, inviting viewers to like and follow.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm vibrant cinematic feel. Strictly NO garbled text. Only short Korean keywords or emoticons ('좋아요 & 구독 ❤️', '파이팅!'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    meme_img = os.path.join(base_dir, "rescene_wonidaero_meme.png")
    stage_img = os.path.join(base_dir, "masan_univ_stage.png")

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 귀여운 새싹 요정 지치와 호기심 대장 삼색 고양이 송이입니다!",
        "K-팝 팬들 사이에서 요즘 아주 뜨겁게 회자되는 유쾌한 성지순례 밈이 있더라고요. 바로 경남 창원시에 있는 유명한 중심 도로 '원이대로' 이야기입니다!",
        "핫한 5세대 슈퍼 루키 걸그룹 리센느(RESCENE)의 매력적인 리더 '원이'의 이름과 한 글자도 틀리지 않고 똑같아서 팬들의 성지순례 필수 코스로 꼽혔는데요. 바쁜 활동으로 오기 힘들 줄 알았던 원이가 드디어 이번 10월 23일 마산대학교 축제에 공식 출동하면서 운명적인 창원 상륙이 성사되었습니다!",
        
        f"__IMAGE__:{meme_img}",

        "코자이너 1컷~4컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut1_4,

        "1컷 · 창원 도로 표지판을 보며 깜짝 놀라는 지치와 송이.",
        "송이: \"지치야! 창원에 진짜 '원이대로'라는 큰 길이 있다냥!\"",
        "지치: \"우와! 리센느 원이 이름이랑 완전 똑같잖아?\"",

        "2컷 · 응원봉을 흔들며 상상의 나래를 펴는 송이.",
        "송이: \"언젠가 리센느 원이가 이 도로를 직접 달려주면 좋겠다냥!\"",
        "지치: \"창원 팬들이 진짜 손꼽아 기다리던 꿈의 성지순례지!\"",

        "3컷 · 빽빽한 해외 투어 스케줄 표를 보며 아쉬워하는 지치.",
        "지치: \"근데 리센느가 요즘 너무 대세라 스케줄이 꽉 찼더라고.\"",
        "송이: \"창원까지 오기엔 너무 바쁜 몸이다냥... 시무룩.\"",

        "4컷 · 스마트폰 속 마산대 축제 라인업 속보에 눈이 번쩍 뜨인 송이.",
        "지치: \"송이야 속보 떴어! 이번 마산대학교 축제에 리센느가 온대!\"",
        "송이: \"드디어 소원이 이루어졌다냥! 창원으로 출동이다냥!\"",

        f"__IMAGE__:{stage_img}",

        "코자이너 5컷~8컷 이미지 프롬프트 (ChatGPT용)",
        prompt_cut5_8,

        "5컷 · 선글라스를 끼고 원이대로 표지판을 지나 축제장으로 달리는 듀오.",
        "송이: \"이게 바로 원이가 달릴 전설의 '원이대로'다냥! 부릉부릉!\"",
        "지치: \"표지판 앞에서 인증샷 찍는 팬들도 엄청 많네!\"",

        "6컷 · 핑크빛 조명 아래 마산대학교 야외 특설무대에 등장한 리센느.",
        "지치: \"무대 찢었다! 관객들 함성 소리가 창원 전역을 울려!\"",
        "송이: \"실물 미모 무슨 일이야! 춤이랑 라이브까지 갓벽하다냥!\"",

        "7컷 · 열광의 도가니 속에서 핑크 응원봉을 격하게 흔드는 송이.",
        "송이: \"원이대로의 진짜 주인이 드디어 창원에 떴다냥!\"",
        "지치: \"팬들의 간절한 소망이 드디어 현실이 된 순간이야!\"",

        "8컷 · 지치와 송이가 손을 흔들며 밝게 웃는다.",
        "지치: \"팬들과 아티스트가 함께 만든 또 하나의 특별한 추억!\"",
        "송이: \"다음에도 창원에 꼭 다시 찾아와 달라냥!\"",

        "[지치와 송이의 리센느 마산대 축제 비하인드 톡]",
        "창원 원이대로 표지판 밈에서 시작된 팬들의 유쾌한 바람이 마산대학교 축제 초청으로 이어지며 그야말로 역대급 축제 분위기를 완성했어요.",
        "칼군무와 탄탄한 라이브는 물론이고 지역 팬들과 다정하게 눈을 맞추는 특급 팬서비스까지 보여줘서 현장 반응이 정말 뜨거웠다고 하더라고요.",

        "[안내 및 정보 출처]",
        "본 웹툰은 마산대학교 축제 현장 소식과 팬 커뮤니티의 유쾌한 밈을 바탕으로 재구성한 지치컴퍼니의 순수 창작 팬툰입니다.\n모든 사진 출처는 팬 공식 후기 및 SNS 채널에 기반합니다."
    ]

    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:") or p_str.startswith("[CHATGPT") or p_str.startswith("PANEL LAYOUT"):
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=22))

    tags = [
        "#리센느",
        "#RESCENE",
        "#리센느원이",
        "#원이대로",
        "#마산대학교축제",
        "#마산대축제",
        "#창원원이대로",
        "#리센느웹툰",
        "#지치웹툰",
        "#KPOP팬툰"
    ]

    print("\n" + "=" * 65)
    print("🌸 [지치 컴퍼니] 리센느 '원이대로' 웹툰 원격 임시저장 개시!")
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
        print("\n🎉 [성공] 리센느 원이대로 웹툰이 네이버 블로그 임시저장함에 완벽히 등록되었습니다!")
    else:
        print("\n⚠️ [확인 필요] 임시저장 중 문제가 발생했습니다.")

if __name__ == "__main__":
    publish_rescene_wonidaero_toon()
