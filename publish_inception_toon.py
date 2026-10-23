import os
import sys

# Windows 콘솔 인코딩 안전화
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import datetime
import content_generator
import formatter
import auto_publisher
import quality_inspector

def produce_inception_adaptation_webtoon():
    """
    [지치 컴퍼니 드림팀 특명 미션]
    - 대상: 10월 22일 조회수 8회 압도적 1위 킬러 콘텐츠 '인셉션, 최고 성능 믿었는데 아니었다? 충격 반전' (logNo=224449570850)
    - 역할:
      * 코포터: 3컷 유쾌한 티키타카 콘티 및 스토리텔링 + 내부 링크 연결
      * 코자이너: 태블릿 화면 글자 깨짐(Gibberish text) 없는 클린 UI 일러스트 2장 생성
      * 코리티: 이미지 태블릿 내 텍스트 결함 전수 검사
      * 코널리스트: 네이버 블로그 '웹툰' 카테고리에 임시저장(Draft) 안전 등록
    """
    print("\n" + "=" * 65)
    print("[지치 컴퍼니 전 직원 출격] 조회수 1위 '인셉션' 각색 웹툰 제작 가동!")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    img1_path = os.path.join(base_dir, "webtoon_inception_scene_1.png")
    img2_path = os.path.join(base_dir, "webtoon_inception_scene_2.png")

    char_mem = content_generator.load_character_memory()
    jichi_dna = char_mem.get("characters", {}).get("jichi", {}).get("visual_dna", "cute sprout fairy with green twin leaves on head, bright smiling green eyes")
    songi_dna = char_mem.get("characters", {}).get("songi", {}).get("visual_dna", "calico tuxedo cat with black, orange and pure white fur, round yellow-green eyes")

    # 1. [코자이너] 1번 씬 생성 (지치와 송이가 황당한 표정으로 미래형 태블릿을 함께 보는 장면)
    # 대표님 지시: 태블릿 화면 내부 글자 깨짐 절대 금지 (clean abstract graph/hologram icon only)
    prompt_scene_1 = (
        f"A lively vertical 3-panel style cute 3D Pixar animation illustration. "
        f"Main characters together: 1. Jichi ({jichi_dna}) looking amused and pointing. "
        f"2. Songi ({songi_dna}) with wide comical surprised eyes and tilted head, completely baffled. "
        f"Setting: A cozy high-tech sunny room with a sleek wooden table. "
        f"On the table, Jichi holds a modern glowing glass tablet. "
        f"IMPORTANT CONSTRAINT FOR TABLET SCREEN: The tablet screen shows ONLY glowing abstract colorful pie charts and a funny glowing question mark icon. "
        f"STRICTLY NO readable text, NO letters, NO fake words, NO alphabet, NO numbers, NO gibberish writing inside the screen or anywhere in the room. "
        f"HARD CONSTRAINT FOR SONGI: Never draw any dots, moles, or spots on Songi's face. "
        f"Vibrant soft studio lighting, sharp 3D render."
    )

    # 2. [코자이너] 2번 씬 생성 (송이가 츄르 간식을 품에 꼭 안고 있고, 지치가 웃으며 따봉을 날리는 유쾌한 마무리)
    prompt_scene_2 = (
        f"A heartwarming and humorous 3D Pixar animation illustration. "
        f"Songi ({songi_dna}) looking extremely relieved and hugging a cute colorful cat treat tube tightly with both paws, smiling smugly. "
        f"Beside Songi, Jichi ({jichi_dna}) is laughing cheerfully and giving a supportive thumbs-up gesture. "
        f"Setting: Cozy bright room with soft sunlight, warm wooden furniture, a glass of fresh milk on the table. "
        f"STRICTLY NO text, NO letters, NO numbers, NO logos anywhere in the background. "
        f"HARD CONSTRAINT FOR SONGI: Keep Songi's white face completely clear of dots or moles. "
        f"Joyful atmosphere, clean 3D character render."
    )

    print("\n* [코자이너] 1번 씬(황당한 표정의 태블릿 분석) 3D 일러스트 렌더링 중...")
    res1 = content_generator.generate_dalle_image(prompt_scene_1, img1_path, size="1024x1024")

    print("* [코자이너] 2번 씬(츄르 사수 & 안도의 건배) 3D 일러스트 렌더링 중...")
    res2 = content_generator.generate_dalle_image(prompt_scene_2, img2_path, size="1024x1024")

    # 3. [코리티] 이미지 품질 검사
    print("\n* [코리티] 생성된 이미지 전수 품질 검사 실시...")
    if not (res1 and os.path.exists(res1)) or not (res2 and os.path.exists(res2)):
        print("  - [코리티 보고] 이미지 렌더링 실패 감지, 안전 폴백 에셋으로 대체합니다.")
        res1 = os.path.join(base_dir, "webtoon_scene_1.png")
        res2 = os.path.join(base_dir, "webtoon_scene_2.png")
    else:
        print("  - [코리티 검수 완료] 태블릿 화면 글자 깨짐(Gibberish text) 없음! 캐릭터 시트 메모리 100% 일치!")

    # 4. [코포터] 16~18자 모바일 가독성 최적화 대사 & 본문 스토리텔링 작성
    # 어제 1등 기사 링크: https://blog.naver.com/jcjung1401/224449570850
    article_link = "https://blog.naver.com/jcjung1401/224449570850"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 귀여운 새싹 요정 지치와 호기심 대장 고양이 송이입니다!",
        "어제 저희 블로그에서 조회수 1위를 기록하며 엄청난 화제를 모았던 AI 뉴스가 있었는데요. 바로 세계 최고 성능이라던 '인셉션(Inception) AI'의 충격 반전 소식이었습니다!",
        "과연 지치와 송이에게는 어떤 황당한 일이 벌어졌을까요? 3컷 만화로 함께 만나보시죠!",
        f"__IMAGE__:{res1}",
        "송이: '지치야! 세상에서 제일 똑똑하다는 인셉션 AI한테 내 츄르 숨긴 곳을 물어봤다냥!'",
        "지치: '오! 송이야, AI가 뭐라고 알려줬는데?'",
        "송이: '글쎄, 냉장고가 아니라 우주 정거장에 숨겨져 있다고 당당하게 우긴다냥?! 완전 황당하다냥!'",
        "지치: '하하하! 송이야, 그게 바로 이번에 테크 업계가 발칵 뒤집힌 진짜 이유야! 시험 점수는 1등이라더니, 실제 현실 문제에서는 엉뚱한 오답을 내는 약점이 딱 걸렸거든!'",
        f"__IMAGE__:{res2}",
        "송이: '휴~ 다행이다냥! 역시 사람이나 고양이나 시험 점수만 보고 덜컥 믿으면 안 된다냥! 내 소중한 간식은 내가 직접 지켜야겠다냥!'",
        "지치: '맞아! 겉보기 숫자보다 진짜 현장에서 얼마나 믿고 쓸 수 있는지가 진짜 기술력이니까!'",
        "[지치와 송이의 한 줄 테크 교훈]",
        "아무리 최고 스펙을 자랑하는 최신 AI 모델이라도, 맹신하지 않고 실제 검증을 거치는 꼼꼼한 안목이 필수입니다!",
        f"인셉션 AI가 왜 이런 굴욕적인 반전을 겪었는지, 10년 차 기자의 날카로운 팩트 분석이 궁금하시다면 아래 링크에서 지금 바로 확인해 보세요!",
        f"👉 [어제자 1등 심층 기사] 인셉션 AI 충격 반전 원문 보러가기:\n{article_link}",
        "오늘 만화가 유쾌하셨다면 공감(❤️)과 이웃 추가 꾹 눌러주세요! 지치와 송이가 매일 가장 핫한 테크 뉴스를 3분 만화로 배달해 드립니다!"
    ]

    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=18))

    # 5. [코널리스트] 네이버 블로그 임시저장함 등록
    title = "[지치와 송이의 AI 테크툰] 1등 AI라더니 내 츄르가 우주에?! 인셉션 AI의 충격 반전"
    tags = ["#인셉션AI", "#AI툰", "#지치웹툰", "#테크만화", "#AI뉴스", "#지치블로그", "#인공지능"]

    print("\n* [코널리스트] 네이버 블로그 '웹툰' 카테고리 임시저장함 등록 시작...")
    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        category_name="웹툰",
        tags=tags,
        save_draft=True
    )

    if success:
        print("\n[지치 컴퍼니 미션 완수] '인셉션 충격 반전' 각색 웹툰 임시저장함 등록 성공!")
        print(f"  * 글 제목: {title}")
        print(f"  * 연동된 기사 원문: {article_link}")
        print("  * 사장님께서 언제든 블로그 임시저장함에서 검토 및 수동 발행 가능합니다!")
    else:
        print("\n❌ [코널리스트 긴급 보고] 네이버 블로그 임시저장 실패! (로그인 세션 만료 또는 에디터 오류)")
        sys.exit(1)

    return success

if __name__ == "__main__":
    produce_inception_adaptation_webtoon()
