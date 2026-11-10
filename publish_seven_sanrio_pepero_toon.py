import os
import sys
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
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

def publish_seven_sanrio_pepero_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 - 빼빼로데이 D-1 연인 공략 특집]
    주제: 내일(11/11) 빼빼로데이 실전 공략!
          세븐일레븐 '산리오 캐릭터즈' 빼빼로 기획 세트 (쿠로미·시나모롤·마이멜로디 미니 파우치 & 키링)
          "흔한 빼빼로는 그만! 여심 저격 굿즈로 점수 따는 연인 맞춤 선물 비법"
    등장인물: 지치(연애 코칭 새싹 요정) + 송이(산리오 러버 깐깐냥)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/상황 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 빼빼로데이 D-1 연인 선물 종결! 세븐일레븐 '산리오 캐릭터즈' 기획 세트 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a cozy room in the evening. Jichi the green sprout fairy looking worried while holding a plain basic Pepero box. Songi the stylish calico cat wags her paw with expert advice: 'A plain box won't touch her heart! It needs cute Sanrio goods!'. Short Korean speech bubbles (MAX 5 chars): Jichi says '선물고민!', Songi says '산리오다냥!'.\n"
        "- Panel ② (Top-Right): Running fast down the evening street towards the bright neon sign of Seven Eleven! Couples holding hands on the sidewalk. Jichi and Songi on a romantic mission. Short Korean speech bubbles (MAX 5 chars): Jichi says '세븐출동!', Songi says '여심저격!'.\n"
        "- Panel ③ (Bottom-Left): Inside Seven Eleven convenience store special Pepero Day event stand! Breathtaking pastel display of 'Sanrio Characters' Pepero special sets featuring Kuromi, Cinnamoroll, and My Melody mini pouches and keyrings. Jichi's eyes pop with wonder. Short Korean speech bubbles (MAX 5 chars): Songi says '심쿵비주얼!', Jichi says '마지막세트!'.\n"
        "- Panel ④ (Bottom-Right): At the checkout counter with proud victorious smiles! Holding the lovely pastel pink-and-purple Kuromi & Cinnamoroll Pepero gift boxes tied with delicate satin ribbons. Short Korean speech bubbles (MAX 5 chars): Songi says '연인필수!', Jichi says '감동예약!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, romantic cozy pastel lighting, ultra-cute dating atmosphere. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '선물고민!', '산리오다냥!', '세븐출동!', '여심저격!', '심쿵비주얼!', '마지막세트!', '연인필수!', '감동예약!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 빼빼로데이 선물 고민을 자아내는 편의점 매대 앞 풍경 또는 기념일 달력 실사\n"
        "- 2번컷 참조 사진: 빼빼로데이 시즌 현수막이 걸린 세븐일레븐 편의점 외관 실사\n"
        "- 3번컷 참조 사진: 세븐일레븐 매대 중앙에 화려하게 진열된 산리오 캐릭터즈 기획 세트 단체 실사\n"
        "- 4번컷 참조 사진: 산리오 쿠로미·시나모롤 패키지 상자를 양손에 든 실물 선물 박스 세팅 컷"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Unboxing the gift set! Opening the lovely box to reveal an adorable, fluffy Sanrio plush mini pouch and sparkling acrylic keychain alongside classic crunchy Pepero sticks. Short Korean speech bubbles (MAX 5 chars): Songi says '파우치대박!', Jichi says '실물갑!'.\n"
        "- Panel ⑥ (Top-Right): Romantic gift-giving moment! Under romantic evening streetlights, a joyful boyfriend handing the Sanrio Pepero set to his delighted girlfriend whose eyes sparkle with happy tears. Songi and Jichi peeking proudly from behind a bench. Short Korean speech bubbles (MAX 5 chars): Songi says '완전감동!', Jichi says '센스만점!'.\n"
        "- Panel ⑦ (Bottom-Left): Sweet tasting scene! Sweethearts sharing a chocolate-almond Pepero stick sweetly, happily clipping the cute Kuromi keychain onto her canvas bag. Short Korean speech bubbles (MAX 5 chars): Songi says '달콤지수!', Jichi says '사랑뿜뿜!'.\n"
        "- Panel ⑧ (Bottom-Right): Cheerful closing scene! Jichi and Songi smiling warmly side-by-side with thumbs up beside a rustic wooden signboard reading '좋아요 & 구독 ❤️', wishing all couples a happy Pepero Day. Short Korean speech bubbles (MAX 5 chars): Jichi says '사랑해!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm romantic cinematic lighting, sweet emotional couple moment. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '파우치대박!', '실물갑!', '완전감동!', '센스만점!', '달콤지수!', '사랑뿜뿜!', '사랑해!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 기획 세트 개봉 후 나오는 산리오 미니 파우치 및 한정판 키링 실물 굿즈 디테일 실사\n"
        "- 6번컷 참조 사진: 빼빼로 과자들과 함께 굿즈를 예쁘게 늘어놓은 언박싱 실물 정면 컷\n"
        "- 7번컷 참조 사진: 에코백이나 가방에 산리오 키링을 실제로 달아놓은 여심 저격 활용 실사 (★가장 중요!)\n"
        "- 8번컷 참조 사진: 빼빼로데이 기념 리본 장식과 함께한 로맨틱 엔딩 컷"
    )

    # 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (100% 영구 표준 준수)
    fact_block_1 = "제품명 : 세븐일레븐 '산리오 캐릭터즈' 빼빼로 기획 세트 (쿠로미 & 시나모롤)\n가격 : 구성별 12,000원 ~ 18,000원 선 (빼빼로 + 파우치/키링 한정 굿즈 포함)\n매장 : 전국 세븐일레븐 편의점 시즌 특별 매대"
    fact_block_2 = "핵심 플레이버 : 달콤한 오리지널 & 아몬드 빼빼로 +\n귀여움 한도 초과 산리오 쿠로미·시나모롤\n미니 파우치 & 소장 가치 200% 아크릴 키링"
    fact_block_3 = "특징 및 식감: 과자만 먹고 버리는 흔한 선물 아님!\n여자친구 취향 저격 산리오 정품 굿즈가 들어있어서\n가방에 달고 다닐 때마다 센스 넘치는 선물로 기억에 남아요\n부담 없는 가격대로 감동과 실용성을 동시에 잡는 필살기"
    fact_block_4 = "Tasty Tip!\n내일 빼빼로데이 당일엔 품절되니 오늘 밤 퇴근길 선점 필수!\n선물 상자 안에 손편지 한 장 쏙 넣어주면 감동 지수 500% 상승!\n과자는 같이 나눠 먹고 키링은 커플 가방에 달아주면 완벽해요"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분!\n내일이면 다가오는 11월 11일 빼빼로데이를 앞두고 연인 맞춤 특급 선물을 찾아 출동한 지치와 고양이 송이입니다!",
        "솔직히 빼빼로데이라고 해서 그냥 기본 빼빼로 서너 갑 덜렁 사서 주면 성의 없어 보일까 봐 고민되시는 분들 많으시죠?\n이럴 때 편의점에서 파는 **산리오 캐릭터즈 한정판 기획 세트** 하나 딱 챙겨주면, 귀여운 파우치에 키링까지 들어있어서 여심을 200% 사로잡을 수 있답니다!",
        "연인에게 센스 만점 남친·여친으로 점수 제대로 따는 세븐일레븐 산리오 빼빼로 솔직 리뷰와 공략 비법, 지금 바로 시작합니다!",
        prompt_cut1_4,
        guide_cut1_4,
        prompt_cut5_8,
        guide_cut5_8,
        fact_block_1,
        fact_block_2,
        fact_block_3,
        fact_block_4,
        "소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n오늘 전해드린 빼빼로데이 연인 공략 세븐일레븐 산리오 리뷰가 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다! 지치와 송이가 매일 가장 사랑스럽고 핫한 편의점 소식을 전해드리겠습니다."
    ]

    # 웹툰 전용 모바일 최적화 포맷팅
    formatted_paragraphs = []
    for p in paragraphs:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("[CHATGPT") or p_str.startswith("[코자이너") or "제품명 :" in p_str or "Tasty Tip!" in p_str:
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=22))

    # 3·3·3 태그 공식 (인물/상황 3 + 브랜드 3 + 제품 3)
    tags = [
        "#지치웹툰", "#빼빼로데이선물", "#연인선물추천",
        "#세븐일레븐", "#세븐일레븐신상", "#편의점빼빼로",
        "#산리오빼빼로", "#쿠로미키링", "#시나모롤파우치"
    ]

    print(f"\n📤 네이버 스마트에디터 원격 웹툰 {'임시저장' if save_draft else '실전발행'} 개시...")
    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=formatted_paragraphs,
        image_paths=None,
        category_name="웹툰",
        tags=tags,
        save_draft=save_draft
    )

    if success:
        print(f"\n🎉 [지치 컴퍼니 웹툰 성공] 세븐일레븐 산리오 빼빼로데이 연인 공략 웹툰이 네이버 블로그에 안전하게 임시저장되었습니다!")
    else:
        print(f"\n🚨 [주의] 임시저장 과정 중 오류가 발생했습니다.")

    return success

if __name__ == "__main__":
    is_draft = "--publish" not in sys.argv
    publish_seven_sanrio_pepero_toon(save_draft=is_draft)
