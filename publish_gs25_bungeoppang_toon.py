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

def publish_gs25_bungeoppang_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 - 초겨울 길거리 간식 힐링 편]
    주제: 현금 없이도 즐기는 우리동네 붕세권!
          GS25 '붕어빵엔 진심' 미니 붕어빵 2종 (달콤통단팥 & 부드러운 슈크림)
          "쌀쌀한 늦은 밤, 편의점 렌지 1분으로 즐기는 겉바속촉 붕어빵 머리vs꼬리 먹방"
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 붕어빵 감정사)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/상황 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 현금 없이 즐기는 붕세권! GS25 '붕어빵엔 진심' 미니 붕어빵 2종 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): On a chilly, dark evening street. Jichi the green sprout fairy and Songi the calico cat bundled up in cozy knit scarves, sniffing the crisp cold air for street fish-bread stalls with sad disappointed faces: 'No cash, and all street stalls are closed!'. Short Korean speech bubbles (MAX 5 chars): Jichi says '붕어빵어디!', Songi says '현금없다냥!'.\n"
        "- Panel ② (Top-Right): Bright warm neon sign of GS25 convenience store glowing on the corner! Songi spots a colorful promotional banner on the door: 'GS25 붕어빵 출시!'. Jichi jumps with joy. Short Korean speech bubbles (MAX 5 chars): Songi says 'GS25출동!', Jichi says '붕세권발견!'.\n"
        "- Panel ③ (Bottom-Left): Inside GS25 hot food / bakery warmer display! Golden brown, crispy, adorable mini fish-shaped pastries (bungeoppang) neatly resting in the warmer case, emitting mouthwatering sweet aroma. Two flavors: Sweet Red Bean & Custard Choux Cream. Short Korean speech bubbles (MAX 5 chars): Songi says '팥vs슈크림!', Jichi says '둘다사자!'.\n"
        "- Panel ④ (Bottom-Right): At the cozy convenience store counter checking out with a warm yellow paper pouch filled with piping hot mini bungeoppang. Jichi and Songi holding the steaming bag with happy rosy cheeks. Short Korean speech bubbles (MAX 5 chars): Songi says '카드결제!', Jichi says '완전따끈!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm golden convenience store interior lighting contrasting with cool evening atmosphere, cozy winter snack mood. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '붕어빵어디!', '현금없다냥!', 'GS25출동!', '붕세권발견!', '팥vs슈크림!', '둘다사자!', '카드결제!', '완전따끈!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 쌀쌀한 초겨울 저녁 골목길 가로등 풍경 또는 붕어빵 생각나는 겨울 감성 실사\n"
        "- 2번컷 참조 사진: 붕어빵 홍보 포스터가 부착된 GS25 편의점 외관 실사\n"
        "- 3번컷 참조 사진: GS25 즉석조리 온장고 매대에 노릇노릇 구워져 진열된 미니 붕어빵 실사\n"
        "- 4번컷 참조 사진: 따끈따끈한 노란색 편의점 종이봉투에 담긴 미니 붕어빵 실물 패키지 컷"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Inside a warm cozy room. Unveiling the hot mini fish-shaped breads onto a cute plate! Cute crispy waffles shaped like swimming little fish, steaming gently. Songi holding one by the tail, Jichi by the head. Short Korean speech bubbles (MAX 5 chars): Songi says '꼬리부터!', Jichi says '머리부터!'.\n"
        "- Panel ⑥ (Top-Right): Breaking them in half to reveal rich fillings! One mini fish reveals dark, glistening chunky red bean paste, and the other oozes golden, velvety custard choux cream! Steam rising beautifully. Short Korean speech bubbles (MAX 5 chars): Songi says '속꽉찼다!', Jichi says '겉바속촉!'.\n"
        "- Panel ⑦ (Bottom-Left): Blissful tasting moment! Songi taking a big bite of the sweet choux cream fish bread with blissful closed eyes, paws on cheeks. Jichi munching the sweet red bean one happily with flushed cheeks, alongside a warm cup of milk. Short Korean speech bubbles (MAX 5 chars): Songi says '달콤천국!', Jichi says '추위순삭!'.\n"
        "- Panel ⑧ (Bottom-Right): Satisfied, warm ending scene! Sitting happily side-by-side with full satisfied smiles, crumbs on lips, waving enthusiastically beside a rustic wooden signboard reading '좋아요 & 구독 ❤️'. Short Korean speech bubbles (MAX 5 chars): Jichi says '내일또먹자!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, delicious warm mouthwatering food detail with golden steam, sweet comedic friendship. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '꼬리부터!', '머리부터!', '속꽉찼다!', '겉바속촉!', '달콤천국!', '추위순삭!', '내일또먹자!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 접시 위에 나란히 올린 노릇노릇한 미니 붕어빵 실물 외관 실사\n"
        "- 6번컷 참조 사진: 붕어빵을 반으로 갈라 팥 앙금과 슈크림이 꽉 차 흘러나오는 반갈샷 실사 (★가장 중요!)\n"
        "- 7번컷 참조 사진: 에어프라이어에 3분 돌려 겉바속촉을 극대화한 뒤 따뜻한 우유와 세팅한 먹방 컷\n"
        "- 8번컷 참조 사진: 붕어빵을 든든하게 다 먹고 난 뒤의 귀여운 엔딩 인증 컷"
    )

    # 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (100% 영구 표준 준수)
    fact_block_1 = "제품명 : GS25 '붕어빵엔 진심' 미니 붕어빵 2종 (단팥 / 슈크림)\n가격 : 1봉(5개입) 3,500원 / 낱개 온장고 판매 시 개당 약 800원~900원\n매장 : 전국 GS25 편의점 즉석조리 온장고 및 냉동 베이커리 코너"
    fact_block_2 = "핵심 플레이버 : 타피오카 찹쌀 믹스로 바삭쫀득한 피 +\n달콤하게 씹히는 알찬 통단팥 앙금 +\n바닐라향 솔솔 부드러운 커스터드 슈크림"
    fact_block_3 = "특징 및 식감: 푸석푸석하고 눅눅한 빵 아님!\n찹쌀가루가 들어가 식어도 쫀득함이 살아있는 빵피와\n머리부터 꼬리 끝까지 빈틈없이 채워 넣은 필링이 완전 좋아요\n현금 없이 카드나 페이로 간편하게 갓 구운 맛을 즐기는 행복"
    fact_block_4 = "Tasty Tip!\n전자레인지 30초 돌린 뒤 에어프라이어 180도 3분이면 길거리 트럭 뺨치는 겉바속촉 완성!\n단팥 붕어빵엔 고소하고 따뜻한 흰 우유 페어링 필수!\n슈크림 붕어빵엔 쌉싸름한 핫 아메리카노와 함께하면 질릴 틈 없이 완벽해요"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분!\n초겨울 쌀쌀한 밤바람을 뚫고 길거리 국민 간식을 찾아 편의점으로 출동한 귀여운 새싹 요정 지치와 고양이 송이입니다!",
        "날씨가 추워지면 길거리에서 풍겨오는 달콤하고 고소한 붕어빵 냄새가 절로 생각나기 마련인데요.\n하지만 요즘은 길거리 붕어빵 포장마차 찾기도 하늘의 별 따기인 데다, 현금이 없어서 아쉽게 발길을 돌린 적 다들 있으시죠?",
        "이제 현금 찾아 헤매지 마세요! 편의점 렌지 1분이면 갓 구워낸 겉바속촉을 그대로 즐기는 **GS25 '붕어빵엔 진심' 미니 붕어빵 2종** 솔직 리뷰, 지금 바로 시작합니다!",
        prompt_cut1_4,
        guide_cut1_4,
        prompt_cut5_8,
        guide_cut5_8,
        fact_block_1,
        fact_block_2,
        fact_block_3,
        fact_block_4,
        "소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n오늘 전해드린 편의점 붕어빵 2종 솔직 리뷰가 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다! 지치와 송이가 매일 가장 따뜻하고 맛있는 편의점 소식을 전해드리겠습니다."
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
        "#지치웹툰", "#붕어빵", "#초겨울간식",
        "#GS25", "#GS25신상", "#편의점붕어빵",
        "#미니붕어빵", "#슈크림붕어빵", "#단팥붕어빵"
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
        print(f"\n🎉 [지치 컴퍼니 웹툰 성공] GS25 미니 붕어빵 웹툰이 네이버 블로그에 안전하게 임시저장되었습니다!")
    else:
        print(f"\n🚨 [주의] 임시저장 과정 중 오류가 발생했습니다.")

    return success

if __name__ == "__main__":
    is_draft = "--publish" not in sys.argv
    publish_gs25_bungeoppang_toon(save_draft=is_draft)
