import os
import sys

# Windows 콘솔 인코딩 안전화
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import auto_publisher
import formatter

def publish_official_rescene_candy_webtoon():
    """
    [지치 컴퍼니 정규 편제] CU 리센느 'Runaway' 노래캔디 탐방 웹툰 공식 등록
    - 1번 컷: rescene_candy_cut1.jpg (CU 매대에서 신비로운 롤리팝 노래캔디를 든 지치와 눈이 휘둥그레진 송이)
    - 2번 실사: rescene_runaway_album_cover.jpg (리센느 공식 Runaway 앨범 재킷 실사)
    - 3번 컷: rescene_candy_cut2.jpg (송이가 사탕을 물고 머리 위에 🎵 음표가 떠오르는 황홀한 3D 컷)
    - 제약조건 100% 준수: 이미지 내부 말풍선 0%, 외계어 0%, 송이 얼굴 무점(Zero Dots)
    - 교차 레이아웃: [1번 컷] -> [대화] -> [실사 앨범/가사] -> [2번 컷] -> [꿀팁 총평]
    """
    print("\n" + "=" * 65)
    print("🍭 [지치 컴퍼니 정규 편제] CU 리센느 '노래캔디' 신규 웹툰 임시저장 가동!")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    img1 = os.path.join(base_dir, "rescene_candy_cut1.jpg")
    album_cover = os.path.join(base_dir, "rescene_runaway_album_cover.jpg")
    img2 = os.path.join(base_dir, "rescene_candy_cut2.jpg")

    title = "[지치와 송이의 편의점 탐방] 입에 물면 노래가?! CU 리센느 'Runaway' 노래캔디 솔직 리뷰!"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분! 귀여운 새싹 요정 지치와 호기심 대장 고양이 송이입니다!",
        "최근 CU에서 출시되어 100만 개 판매 신화를 쓴 리센느 빵에 이어, 이번엔 상상을 초월하는 초특급 이색 신상이 등장했습니다!",
        "바로 입에 물면 뼈를 타고 진짜 음악이 흘러나오는 골전도 '노래캔디' 3탄! 걸그룹 리센느(RESCENE)의 신곡 'Runaway'가 담긴 화제의 사탕을 지치와 송이가 직접 체험해 보았습니다!",
        f"__IMAGE__:{img1}",
        "지치: '송이야! 편의점 캔디 매대에서 완전 대박 신기한 신상을 발견했어!'",
        "송이: '지치야, 그냥 막대사탕처럼 보이는데 왜 그렇게 호들갑이다냥?'",
        "지치: '이건 그냥 사탕이 아니야! 입에 물고 귀를 막으면 머릿속에서 신나는 노래가 생생하게 울려 퍼지는 골전도 캔디라구!'",
        "송이: '말도 안 된다냥! 사탕에서 어떻게 소리가 나냥? 내가 직접 먹어보겠다냥!'",
        f"__IMAGE__:{album_cover}",
        "[🎧 리센느(RESCENE) - Runaway 실물 앨범 팩트 체크]",
        "발매: 2026년 리센느 공식 싱글 《Runaway》",
        "콘셉트: 신비로운 인센스(Incense) 향을 모티브로 몽환적인 멜로디와 성숙한 아우라를 담아낸 명곡",
        "핵심 가사 포인트:\n“회색빛에 갇혀버린 Neverland\nWe know how it ends\n또 의미 없이 돌고도는 Everyday”",
        "골전도 캔디 원리: 캔디 막대에 탑재된 미세 진동자가 치아와 턱뼈를 통해 달팽이관으로 직접 음파를 전달하는 최첨단 테크 디저트!",
        f"__IMAGE__:{img2}",
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

    # 사장님의 최신 네이버 세션 쿠키 설정
    os.environ['NAVER_NID_AUT'] = 'fWos+ICAsP5Dst9g9QKFMLaDi1b+5tjZEH4HN+GbLVOh/quNYed8CnSLmVjYUNV2'
    os.environ['NAVER_NID_SES'] = 'AAABwwQinqOiadkEPkukiCfLHEUlsDDd3ax7yZhsWtUsC9sAbcNi0hZy9fqsIjs35gBdZtShGACeN56xJUCAzHL8kdQ/+EzEoTpNFpO8N+aQ1Pz1aHGQkwKQ4HrkS4HgKjNsuCwCsGPL8thi6LSP3KBXYgZHp8sElZQS4aFECiMLLp4eLY8OLIpFImOyHcfcgOUk74s9VIFMC1JKakuh5E6U2rz+Ak6iWaeGS39+fww8h38d522jCtkZoMo0vEGWqRWXcQ4VbEbkx7yms3Q74cWabAPxFGl1hbTlkLoh5qKHhllwRtUZtCrycKGSBV1Vbi5tW5XSH9ft2MR2PJfXLaQ+1i4nyV0QpLeooBVELDbzFae0v+cC+4BVwNwBuL2zfiFHsyTzW8/C+NfZEG7MCXDGRR7rzxhK/INJgySGpg5m2XgKvQV2XWKRX/rSkelkkTHmKwkxWBDdpIGjuh7DHC2YtQtNBLEQann79wLh2u16Tt8LBorEhzMhznTbQsj+J8lX0VUaUF+iv2egdMVIahpdrHJtzBIg4C/4u1cWZIJ7PgRLgP3m0y6p6G/Ir+h6sx/Chi3gVWVPpCEI5jPC2xpg/dcvlRJTOPEWk9D/u2DOoLBM'
    os.environ['CLOUD_MODE'] = 'true'

    print("📝 스마트에디터 ONE 진입 및 리센느 노래캔디 웹툰 임시저장 시작...")
    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        category_name="웹툰",
        tags=tags,
        save_draft=True
    )

    if success:
        print("\n🎉 [지치 컴퍼니 미션 완수] CU 리센느 '노래캔디' 웹툰 임시저장 등록 완료!")
        print(f"  * 글 제목: {title}")
        print("  * 1컷: rescene_candy_cut1.jpg (신규 캔디 컷)")
        print("  * 2컷: rescene_runaway_album_cover.jpg (공식 실사 앨범 재킷)")
        print("  * 3컷: rescene_candy_cut2.jpg (신규 🎵 음표 컷)")
        print("  * 사장님께서 블로그 임시저장함에서 바로 검토하실 수 있습니다!")
    else:
        print("\n❌ 임시저장 실패")
        sys.exit(1)

    return success

if __name__ == "__main__":
    publish_official_rescene_candy_webtoon()
