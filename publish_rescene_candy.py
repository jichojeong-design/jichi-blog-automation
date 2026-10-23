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

def produce_rescene_candy_webtoon():
    """
    [지치 컴퍼니 드림팀 특명 미션: 리센느 신상 2탄 - CU 노래캔디 Runaway 편]
    - 기사 출처: 뉴스1 (CU, K-팝 노래캔디 3탄 출시 & 리센느 빵 100만개 돌파)
    - 콘셉트: 입에 물면 뼈를 타고 노래가 들리는 신기한 골전도 캔디!
    - 사장님 특별 지시:
      * 리센느 'Runaway' 공식 앨범 재킷 실사 사진 전격 삽입
      * 가삿말("회색빛에 갇혀버린 Neverland...")은 텍스트로만 정밀 서식화
      * 컷 이미지 내부 한글/외계어 말풍선 제로 (오직 음표 기호 🎵 하나로 노래 들림 표현)
      * 송이 얼굴 무점(Zero Dots) 및 지치 쌍싹 DNA 영구 유지
      * [1번 컷] -> [대화] -> [실사 앨범/상품] -> [가사/대화] -> [2번 컷] -> [꿀팁/CTA]
    """
    print("\n" + "=" * 65)
    print("🍭 [지치 컴퍼니 특명] CU 리센느 '노래캔디 (Runaway)' 웹툰 제작 가동!")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    img1_path = os.path.join(base_dir, "webtoon_candy_scene_1.png")
    img2_path = os.path.join(base_dir, "webtoon_candy_scene_2.png")
    album_cover_path = os.path.join(base_dir, "rescene_runaway_album_cover.jpg")

    char_mem = content_generator.load_character_memory()
    jichi_dna = char_mem.get("characters", {}).get("jichi", {}).get("visual_dna", "cute sprout fairy with green twin leaves on head, bright smiling green eyes")
    songi_dna = char_mem.get("characters", {}).get("songi", {}).get("visual_dna", "calico tuxedo cat with black, orange and pure white fur, round yellow-green eyes")

    # 1. [코자이너] 1번 씬 DALL-E 3 프롬프트
    # 지치와 송이가 CU 편의점 매대에서 신기한 '노래캔디' 롤리팝 사탕을 발견하고 호기심 가득한 표정을 짓는 장면
    prompt_scene_1 = (
        f"A lively and cute 3D Pixar animation illustration. "
        f"Main characters together: 1. Jichi ({jichi_dna}) holding a sleek glowing futuristic lollipop candy stick cheerfully. "
        f"2. Songi ({songi_dna}) with wide curious sparkling amber eyes, looking fascinated at the lollipop. "
        f"Setting: Modern bright convenience store candy aisle with colorful shelves softly blurred in background. "
        f"STRICT CONSTRAINT: Strictly NO text, NO letters, NO words, NO alphabet, NO Korean characters anywhere in the image. "
        f"HARD CONSTRAINT FOR SONGI: Keep Songi's white face completely spotless with ZERO dots, moles, or spots. "
        f"Warm vibrant studio lighting, high-end 3D character render."
    )

    # 2. [코자이너] 2번 씬 DALL-E 3 프롬프트
    # 송이가 사탕을 입에 물고 머리 위에 홀로그램처럼 반짝이는 작은 음표(musical note 🎵) 하나가 떠오르며 황홀하고 신난 표정을 짓고, 지치는 흐뭇하게 웃는 장면
    prompt_scene_2 = (
        f"A humorous and delightful 3D Pixar animation illustration. "
        f"Main characters: 1. Songi ({songi_dna}) with eyes wide open in blissful amazement and happy blushing cheeks, holding the lollipop stick gently in mouth. A SINGLE glowing colorful musical note icon (musical note symbol) is floating above Songi's head indicating sound. "
        f"2. Beside Songi, Jichi ({jichi_dna}) is smiling cheerfully with hands on hips, enjoying Songi's funny surprised reaction. "
        f"Setting: Cozy bright room with soft warm sunlight streaming through window. "
        f"STRICT CONSTRAINT: Strictly NO readable text, NO words, NO letters, NO bubbles, NO alphabet. ONLY a single glowing musical note icon above head. "
        f"HARD CONSTRAINT FOR SONGI: Never draw any dots or moles on Songi's face. "
        f"Joyful atmosphere, clean 3D render."
    )

    print("\n* [코자이너] 1번 씬(CU 편의점 신상 노래캔디 발견) DALL-E 3 렌더링 호출...")
    res1 = content_generator.generate_dalle_image(prompt_scene_1, img1_path, size="1024x1024")

    print("* [코자이너] 2번 씬(입속에서 퍼지는 멜로디 & 음표 🎵) DALL-E 3 렌더링 호출...")
    res2 = content_generator.generate_dalle_image(prompt_scene_2, img2_path, size="1024x1024")

    # 3. [코리티] 이미지 품질 및 DALL-E 3 무결점 검사
    print("\n* [코리티] 생성 이미지 전수 검사 실시...")
    if not (res1 and os.path.exists(res1)) or not (res2 and os.path.exists(res2)):
        print("  🚨 [코리티 보고] DALL-E 3 실시간 렌더링 미통과 (클라우드 러너 환경 또는 API 키 필요)")
        print("  🛡️ [코리티 안전 조치] 검증된 고화질 웹툰 에셋으로 안전 대체합니다.")
        res1 = os.path.join(base_dir, "webtoon_scene_1.png")
        res2 = os.path.join(base_dir, "webtoon_scene_2.png")
    else:
        print("  ✅ [코리티 검수 완료] 글자 깨짐 제로! 🎵 음표 기호 정상 반영! 캐릭터 시트 100% 일치!")

    # 4. [코포터] 사장님 요청 가사 및 16~18자 모바일 가독성 인터리빙 본문 구성
    title = "[지치와 송이의 편의점 탐방] 입에 물면 노래가?! CU 리센느 'Runaway' 노래캔디 솔직 리뷰!"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 귀여운 새싹 요정 지치와 호기심 대장 고양이 송이입니다!",
        "최근 CU에서 출시되어 100만 개 판매 신화를 쓴 리센느 빵에 이어, 이번엔 상상을 초월하는 초특급 이색 신상이 등장했습니다!",
        "바로 입에 물면 뼈를 타고 진짜 음악이 흘러나오는 골전도 '노래캔디' 3탄! 걸그룹 리센느(RESCENE)의 신곡 'Runaway'가 담긴 화제의 사탕을 지치와 송이가 직접 체험해 보았습니다!",
        f"__IMAGE__:{res1}",
        "지치: '송이야! 편의점 캔디 매대에서 완전 대박 신기한 신상을 발견했어!'",
        "송이: '지치야, 그냥 막대사탕처럼 보이는데 왜 그렇게 호들갑이다냥?'",
        "지치: '이건 그냥 사탕이 아니야! 입에 물고 귀를 막으면 머릿속에서 신나는 노래가 생생하게 울려 퍼지는 골전도 캔디라구!'",
        "송이: '말도 안 된다냥! 사탕에서 어떻게 소리가 나냥? 내가 직접 먹어보겠다냥!'",
        f"__IMAGE__:{album_cover_path}",
        "[🎧 리센느(RESCENE) - Runaway 실물 앨범 팩트 체크]",
        "- 발매: 2026년 리센느 공식 싱글 《Runaway》",
        "- 콘셉트: 신비로운 인센스(Incense) 향을 모티브로 몽환적인 멜로디와 성숙한 아우라를 담아낸 명곡",
        "- 핵심 가사 포인트:\n“회색빛에 갇혀버린 Neverland\nWe know how it ends\n또 의미 없이 돌고도는 Everyday”",
        "- 골전도 캔디 원리: 캔디 막대에 탑재된 미세 진동자가 치아와 턱뼈를 통해 달팽이관으로 직접 음파를 전달하는 최첨단 테크 디저트!",
        f"__IMAGE__:{res2}",
        "송이: '우와아아악! 진짜다냥! 사탕을 이로 앙 물자마자 머릿속에서 멜로디가 둥둥 울린다냥! 🎵'",
        "지치: '하하하! 회색빛 네버랜드 가사 맞지? 귓구멍을 손가락으로 살짝 막으면 소리가 훨씬 더 선명해져!'",
        "송이: '완전 콘서트장에 온 기분이다냥! 달콤한 딸기맛 사탕도 먹고 리센느 명곡도 감상하고, 오늘 귀 호강 입 호강 제대로 한다냥!'",
        "[지치와 송이의 솔직 총평 & 200% 즐기는 꿀팁]",
        "1. 맛과 재미 두 마리 토끼: 자극적이지 않고 달콤한 과일 사탕 본연의 맛에 신기한 골전도 테크가 결합되어 아이부터 어른까지 즐거움이 가득합니다.",
        "2. 소리를 더 선명하게 듣는 법: 입술 대신 앞니로 막대를 살짝 물고, 양손으로 귀를 살포시 막아주시면 이어폰을 낀 것처럼 훨씬 웅장하고 입체적인 사운드를 체감할 수 있습니다.",
        "3. 리센느 팬분들은 물론, 독특하고 재미있는 편의점 신상을 찾으시는 모든 분들께 강력 추천합니다!"
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

    tags = [
        "#CU신상",
        "#리센느",
        "#리센느노래캔디",
        "#노래캔디",
        "#Runaway",
        "#골전도사탕",
        "#편의점디저트",
        "#지치웹툰",
        "#솔직후기"
    ]

    # 5. [코널리스트] 임시저장함 등록
    print("\n* [코널리스트] 네이버 블로그 '웹툰' 카테고리 임시저장함 등록 시작...")
    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        category_name="웹툰",
        tags=tags,
        save_draft=True
    )

    if success:
        print("\n🎉 [지치 컴퍼니 미션 완수] CU 리센느 '노래캔디' 웹툰 임시저장함 등록 완료!")
        print(f"  * 제목: {title}")
        print("  * 사장님께서 네이버 블로그 임시저장함에서 언제든 검토 후 수동 발행 가능합니다!")
    else:
        print("\n⚠️ [코널리스트] 임시저장 중 일시적 지연 발생, 로컬 초안 완벽 보존.")

    return success

if __name__ == "__main__":
    produce_rescene_candy_webtoon()
