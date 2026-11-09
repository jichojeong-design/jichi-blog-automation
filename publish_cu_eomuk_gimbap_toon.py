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

def publish_cu_eomuk_gimbap_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 - 비 오는 날 야식 & 힐링 꿀조합]
    주제: 비 내리고 쌀쌀한 날씨엔 무조건 이거지!
          CU '고래사어묵 프리미엄 모둠어묵탕' X '참치마요 & 전주비빔 삼각김밥' 찍먹 조합
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 따끈 미식가)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/상황 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 비 내리고 쌀쌀한 밤엔 국물이지! CU '고래사 모둠어묵탕' X 삼각김밥 찍먹 꿀조합 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Outside in the chilly evening rain. Songi the calico cat and Jichi the green sprout fairy walking under a cute yellow umbrella, shivering slightly as raindrops splash. Songi rubs her tummy with hungry eyes. Short Korean speech bubbles (MAX 5 chars): Songi says '비온다냥!', Jichi says '출출해!'.\n"
        "- Panel ② (Top-Right): Spotting the glowing, warm neon sign of a CU convenience store! Raindrops running down the glass windows. Jichi points happily, eyes sparkling with hope for hot soup. Short Korean speech bubbles (MAX 5 chars): Jichi says '편의점행!', Songi says '국물땡겨!'.\n"
        "- Panel ③ (Bottom-Left): Inside the warm CU convenience store fresh food refrigerated aisle! Songi and Jichi enthusiastically discover the hearty cup of '고래사어묵 프리미엄 모둠어묵탕' and triangle gimbap (참치마요 & 전주비빔). Short Korean speech bubbles (MAX 5 chars): Songi says '어묵탕이다!', Jichi says '삼김추가!'.\n"
        "- Panel ④ (Bottom-Right): At the cozy convenience store window bar counter looking out at the city rain. Setting down the steaming hot eomuk cup and two triangular gimbap packages side-by-side with wooden chopsticks ready. Short Korean speech bubbles (MAX 5 chars): Songi says '완벽조합!', Jichi says '먹어보자!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, ultra cute, cozy atmospheric rainy night lighting with warm indoor glow. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '비온다냥!', '출출해!', '편의점행!', '국물땡겨!', '어묵탕이다!', '삼김추가!', '완벽조합!', '먹어보자!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 비 내리는 쌀쌀한 저녁 골목길 또는 빗방울 맺힌 창가 감성 실사\n"
        "- 2번컷 참조 사진: 비 오는 밤 따뜻한 불빛을 밝히고 있는 CU 편의점 외관 실사\n"
        "- 3번컷 참조 사진: CU 냉장 간편식 매대에 진열된 고래사 모둠어묵탕과 삼각김밥 코너 실사\n"
        "- 4번컷 참조 사진: 편의점 창가 테이블 위에 어묵탕 용기와 삼각김밥 2종을 세팅한 실물 투샷"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Opening the steaming lid of the freshly microwaved fishcake soup! Plump, juicy skewered fishcake, round eomuk, and clear golden broth with sliced red peppers emitting swirling steam. Short Korean speech bubbles (MAX 5 chars): Songi says '김모락!', Jichi says '탱글탱글!'.\n"
        "- Panel ⑥ (Top-Right): First taste of the hot broth! Songi drinks a big spoonful of golden broth, eyes sparkling with pure bliss, warming up from head to toe. Jichi bites a thick chewy fishcake with delighted cheeks. Short Korean speech bubbles (MAX 5 chars): Songi says '몸녹는다!', Jichi says '진한국물!'.\n"
        "- Panel ⑦ (Bottom-Left): The ultimate comfort dipping combination! Jichi and Songi unwrapping a Tuna-Mayo triangular gimbap, dipping the savory rice corner right into the hot eomuk broth and taking a big satisfying bite. Short Korean speech bubbles (MAX 5 chars): Songi says '삼김찍먹!', Jichi says '꿀조합!'.\n"
        "- Panel ⑧ (Bottom-Right): Satisfied, warm ending after finishing every single drop. Empty clean cups on the table. Jichi and Songi smiling warmly side-by-side beside a rustic wooden signboard reading '좋아요 & 구독 ❤️', waving cheerfully. Short Korean speech bubbles (MAX 5 chars): Jichi says '완전든든!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm delicious cinematic lighting, comforting rainy night mood. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '김모락!', '탱글탱글!', '몸녹는다!', '진한국물!', '삼김찍먹!', '꿀조합!', '완전든든!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 전자레인지 렌지업 후 김이 모락모락 피어오르는 탱글한 모둠어묵 실사\n"
        "- 6번컷 참조 사진: 숟가락으로 맑고 진한 어묵 국물을 떠올린 클로즈업 실사\n"
        "- 7번컷 참조 사진: 김을 벗긴 참치마요 삼각김밥을 뜨끈한 어묵 국물에 콕 찍어먹는 꿀조합 실사 (★가장 중요!)\n"
        "- 8번컷 참조 사진: 국물까지 싹 비워낸 빈 용기와 든든한 완식 기념 엔딩 컷"
    )

    # 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (100% 영구 표준 준수)
    fact_block_1 = "제품명 : CU 고래사어묵 '프리미엄 모둠어묵탕' & 참치마요 삼각김밥\n가격 : 어묵탕 3,900원 / 삼각김밥 1,200원 (총 5,100원 한끼 세트)\n매장 : 전국 CU 편의점 냉장 간편식 코너"
    fact_block_2 = "핵심 플레이버 : 가쓰오와 다시마로 우려낸\n깊고 칼칼한 전통 어묵 육수 +\n밀가루 없이 연육 가득 쫄깃한 프리미엄 어묵 4종"
    fact_block_3 = "특징 및 식감: 밍밍하고 팅팅 불은 어묵 아님!\n부산 고래사 특유의 쫄깃탱글한 생선살 식감과\n청양고추 살짝 더해진 칼칼하고 시원한 국물이 완전 좋아요\n비 맞고 으슬으슬할 때 속부터 든든하게 채워주는 구원투수"
    fact_block_4 = "Tasty Tip!\n비 오고 쌀쌀한 날엔 따끈한 어묵 국물에 삼각김밥 찍먹 필수!\n삼각김밥 김을 국물에 살짝 적셔 먹으면 감칠맛이 2배!\n남은 국물에 밥을 푹 말아 먹으면 전문 포차 어묵죽 완성이라 완전 좋아요"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분!\n비 내리는 쌀쌀한 저녁, 맛있는 온기를 찾아 편의점으로 출동한 귀여운 새싹 요정 지치와 고양이 송이입니다!",
        "오늘처럼 찬 바람 불고 비까지 추적추적 내리는 날엔 퇴근길이나 하굣길에 몸이 절로 움츠러들기 마련인데요.\n이럴 때 편의점 문 열고 들어가서 뜨끈하게 김 모락모락 나는 **어묵탕에 삼각김밥 하나** 말아먹으면 5천 원으로 누리는 최고의 호사잖아요!",
        "비 오는 날 감성 충전과 든든한 한 끼를 한 번에 책임지는 지치와 송이의 편의점 국물 꿀조합, 지금 바로 시작합니다!",
        prompt_cut1_4,
        guide_cut1_4,
        prompt_cut5_8,
        guide_cut5_8,
        fact_block_1,
        fact_block_2,
        fact_block_3,
        fact_block_4,
        "소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n오늘 전해드린 비 오는 날 편의점 국물 꿀조합 리뷰가 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다! 지치와 송이가 매일 가장 따뜻하고 핫한 편의점 소식을 전달해 드리겠습니다."
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
        "#지치웹툰", "#송이", "#비오는날편의점",
        "#CU편의점", "#CU신상", "#편의점꿀조합",
        "#고래사어묵탕", "#어묵탕삼각김밥", "#모둠어묵탕"
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
        print(f"\n🎉 [지치 컴퍼니 웹툰 성공] 비 오는 날 어묵탕X삼각김밥 웹툰이 네이버 블로그에 안전하게 임시저장되었습니다!")
    else:
        print(f"\n🚨 [주의] 임시저장 과정 중 오류가 발생했습니다.")

    return success

if __name__ == "__main__":
    is_draft = "--publish" not in sys.argv
    publish_cu_eomuk_gimbap_toon(save_draft=is_draft)
