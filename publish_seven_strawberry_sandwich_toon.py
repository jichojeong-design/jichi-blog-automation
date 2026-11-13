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

def publish_seven_strawberry_sandwich_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 - 겨울 시즌 한정 디저트 편]
    주제: 겨울의 시작을 알리는 붉은빛 설렘!
          세븐일레븐 '겨울 한정 설향 생딸기 샌드위치'
          "첫눈보다 반가운 편의점 생딸기 샌드위치 발견 & 진한 생크림 폭포 먹방"
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 디저트 탐험가)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/상황 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 겨울의 전령사! 세븐일레븐 '겨울 한정 설향 생딸기 샌드' 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Outside in chilly early winter evening air. Jichi the green sprout fairy and Songi the calico cat bundled in warm winter mufflers, looking around with dreamy eyes: 'Winter has arrived, which means seasonal fruit sweets are here!'. Short Korean speech bubbles (MAX 5 chars): Jichi says '겨울왔다!', Songi says '딸기시즌!'.\n"
        "- Panel ② (Top-Right): Running excitedly into a brightly lit 7-Eleven convenience store. Songi immediately dashes toward the chilled dessert sandwich refrigerator case, pointing at a dazzling pink packaging. Short Korean speech bubbles (MAX 5 chars): Songi says '세븐출동!', Jichi says '냉장고로!'.\n"
        "- Panel ③ (Bottom-Left): Close-up inside the chilled shelf! Fluffy white triangular sandwich bread stuffed with thick snowy fresh whipped cream and embedded with luscious, bright red fresh Seolhyang strawberries sliced in half. Fresh and glossy! Short Korean speech bubbles (MAX 5 chars): Songi says '생딸기다!', Jichi says '새빨갛다!'.\n"
        "- Panel ④ (Bottom-Right): At the checkout counter holding the fresh strawberry sandwich packaging triumphantly with huge sparkly eyes and rosy cheeks. Songi happily paying. Short Korean speech bubbles (MAX 5 chars): Songi says '겟했다냥!', Jichi says '완전행복!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, cozy early winter evening lighting, bright fresh convenience store colors. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '겨울왔다!', '딸기시즌!', '세븐출동!', '냉장고로!', '생딸기다!', '새빨갛다!', '겟했다냥!', '완전행복!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 초겨울 쌀쌀한 저녁 거리 풍경 또는 딸기 디저트가 생각나는 겨울 감성 컷\n"
        "- 2번컷 참조 사진: 신선 디저트 코너가 환하게 보이는 세븐일레븐 편의점 매장 입구 실사\n"
        "- 3번컷 참조 사진: 세븐일레븐 냉장 샌드위치 매대에 진열된 '설향 딸기 샌드' 패키지 실사\n"
        "- 4번컷 참조 사진: 손에 쥐었을 때 도톰하고 묵직한 딸기 샌드위치 실물 패키지 인증 컷"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Inside a cozy warm room at a wooden dining table. Unwrapping the plastic wrap to reveal super fluffy, cloud-soft white bread overflowing with thick fresh whipped cream and huge, juicy sweet strawberries. Short Korean speech bubbles (MAX 5 chars): Songi says '크림폭포!', Jichi says '두툼하다!'.\n"
        "- Panel ⑥ (Top-Right): Splitting the sandwich slightly or lifting a bite! Juicy red strawberry juice mixing beautifully into velvety sweet white cream. Jichi sniffing the sweet berry fragrance in delight. Short Korean speech bubbles (MAX 5 chars): Songi says '달콤상큼!', Jichi says '향기대박!'.\n"
        "- Panel ⑦ (Bottom-Left): Blissful eating moment! Songi taking a massive hearty bite, whipped cream adorably dabbed on whiskers, eyes sparkling with pure dessert heaven. Jichi taking a bite of sweet berry, holding a warm mug of milk. Short Korean speech bubbles (MAX 5 chars): Songi says '입안축제!', Jichi says '힐링완료!'.\n"
        "- Panel ⑧ (Bottom-Right): Cheerful satisfied ending scene! Jichi and Songi sitting happily side-by-side with contented smiling faces and thumbs up, waving warmly beside a cute wooden board reading '좋아요 & 구독 ❤️'. Short Korean speech bubbles (MAX 5 chars): Jichi says '겨울최애!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, mouthwatering juicy fruit textures, creamy rich dessert visuals, warm cozy winter healing atmosphere. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '크림폭포!', '두툼하다!', '달콤상큼!', '향기대박!', '입안축제!', '힐링완료!', '겨울최애!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 비닐을 벗겨 예쁜 접시에 담은 뽀얀 생크림과 통딸기 단면 비주얼 컷\n"
        "- 6번컷 참조 사진: 빵 사이로 새빨간 생딸기 과육과 커스터드 생크림이 터져 나오는 초근접 샷 (★핵심 킬링컷!)\n"
        "- 7번컷 참조 사진: 따뜻한 드립 커피 또는 시원한 우유와 함께 세팅한 금요일 홈카페 먹방 컷\n"
        "- 8번컷 참조 사진: 순식간에 맛있게 해치우고 기분 좋게 남기는 깔끔한 완식 인증 컷"
    )

    # 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (100% 영구 표준 준수)
    fact_block_1 = "제품명 : 세븐일레븐 '겨울 한정 설향 생딸기 샌드'\n가격 : 3,400원\n매장 : 전국 세븐일레븐 편의점 신선 냉장 샌드위치 코너"
    fact_block_2 = "핵심 플레이버 : 산지 직송 국내산 100% 설향 생딸기 +\n느끼함 잡은 산뜻 달콤 바닐라 커스터드 생크림 +\n폭신폭신 촉촉한 식빵 시트"
    fact_block_3 = "특징 및 식감: 잼이나 인공 딸기 시럽 맛 아님!\n한 입 베어 물자마자 톡 터지는 싱싱한 설향 생딸기의 상큼한 과즙과\n입안 가득 부드럽게 감싸는 진한 생크림의 황금 밸런스가 완전 좋아요\n칼로리 걱정 잊게 만드는 겨울 한정 디저트의 진정한 행복"
    fact_block_4 = "Tasty Tip!\n구매 직후 냉장 보관했다가 차갑게 먹어야 생크림이 단단해져 꿀맛 보장!\n따뜻하고 쌉싸름한 핫 아메리카노와 곁들이면 느끼함 싹 사라지는 무한 흡입 가능!\n생크림 위에 시나몬 파우더 살짝 톡톡 뿌려주면 고급 베이커리 타르트 감성 폭발!"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분!\n초겨울 쌀쌀한 밤공기를 뚫고 겨울의 전령사이자 시즌 한정 디저트를 찾아 편의점으로 출동한 귀여운 새싹 요정 지치와 고양이 송이입니다!",
        "찬 바람이 불기 시작하면 편의점 쇼케이스에서 가장 먼저 눈길을 사로잡는 붉은빛 설렘, 바로 생딸기 샌드위치의 계절이 돌아왔습니다.\n겨울 디저트 매니아라면 매년 첫 출시 소식만을 손꼽아 기다리셨을 텐데요!",
        "산지 직송 국내산 설향 생딸기와 몽글몽글 구름 같은 생크림이 듬뿍 들어간 **세븐일레븐 '겨울 한정 설향 생딸기 샌드'** 솔직 리뷰, 지금 바로 시작합니다!",
        prompt_cut1_4,
        guide_cut1_4,
        prompt_cut5_8,
        guide_cut5_8,
        fact_block_1,
        fact_block_2,
        fact_block_3,
        fact_block_4,
        "소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n오늘 전해드린 편의점 겨울 한정 생딸기 샌드 솔직 리뷰가 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다! 지치와 송이가 매일 가장 상큼하고 달콤한 편의점 소식을 전해드리겠습니다."
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
        "#지치웹툰", "#겨울신상", "#금요디저트",
        "#세븐일레븐", "#세븐일레븐신상", "#편의점디저트",
        "#딸기샌드위치", "#설향생딸기샌드", "#생딸기샌드"
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
        print(f"\n🎉 [지치 컴퍼니 웹툰 성공] 세븐일레븐 설향 생딸기 샌드 웹툰이 네이버 블로그에 안전하게 임시저장되었습니다!")
    else:
        print(f"\n🚨 [주의] 임시저장 과정 중 오류가 발생했습니다.")

    return success

if __name__ == "__main__":
    is_draft = "--publish" not in sys.argv
    publish_seven_strawberry_sandwich_toon(save_draft=is_draft)
