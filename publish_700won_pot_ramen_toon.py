import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import formatter
import auto_publisher

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def publish_700won_pot_ramen_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 - 700원 냄비라면 꿀템 편]
    주제: 조리기 없이 편의점에서 냄비라면 끓이기!
          단돈 700원 전자레인지 전용 용기로 봉지라면 3분 만에 꼬들하게 완조리!
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/상황 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 조리기 없이 끓이는 700원 냄비라면! 편의점 전자레인지 꿀템 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside a neighborhood convenience store at night. Jichi the green sprout fairy and Songi the calico cat looking disappointed near the hot water dispenser because there is NO Hangang ramen induction cooker machine! Short Korean speech bubbles (MAX 5 chars): Jichi says '조리기없네', Songi says '컵라면싫어'.\n"
        "- Panel ② (Top-Right): Songi suddenly spots a special 700-won microwaveable paper/plastic ramen pot container ('오!렌지' / microwave ramen bowl) on the shelf next to bagged ramen! Eyes sparkling with discovery. Short Korean speech bubbles (MAX 5 chars): Songi says '700원발견!', Jichi says '이게뭐야?'.\n"
        "- Panel ③ (Bottom-Left): Putting a whole bagged ramen noodle block and soup powder into the 700-won microwave container, then pouring piping hot water up to the inner line. Short Korean speech bubbles (MAX 5 chars): Jichi says '봉지라면쏙', Songi says '뜨거운물!'.\n"
        "- Panel ④ (Bottom-Right): Putting the container into the convenience store microwave! The timer glows '3:30'. Both waiting excitedly watching it spin through the glass door. Short Korean speech bubbles (MAX 5 chars): Songi says '렌지3분컷', Jichi says '두근두근!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, bright warm convenience store lighting, expressive cute characters. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '조리기없네', '컵라면싫어', '700원발견!', '이게뭐야?', '봉지라면쏙', '뜨거운물!', '렌지3분컷', '두근두근!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: 라면 조리기가 없는 일반 동네 편의점 시식대 및 온수기 주변 실사\n"
        "- 2번컷 참조 사진: 편의점 라면 매대에 진열된 700원 전자레인지 전용 용기(오!렌지 등) 실물 컷\n"
        "- 3번컷 참조 사진: 전용 용기에 봉지라면 면과 스프를 넣고 눈금선까지 뜨거운 물을 붓는 과정 컷\n"
        "- 4번컷 참조 사진: 편의점 전자레인지에 용기를 넣고 3분 30초 조리하는 모습 실사"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Taking the steaming hot ramen bowl out of the microwave! Rich red spicy broth bubbling gently, wavy bouncy noodles looking just like a real pot-boiled ramen! Short Korean speech bubbles (MAX 5 chars): Songi says '냄비라면각', Jichi says '비주얼대박'.\n"
        "- Panel ⑥ (Top-Right): Lifting a big chopstick-full of glossy, chewy, springy noodles with steam rising! Jichi and Songi amazed by the firm noodle texture. Short Korean speech bubbles (MAX 5 chars): Jichi says '꼬들꼬들해', Songi says '진짜냄비맛'.\n"
        "- Panel ⑦ (Bottom-Left): Slurping the hot ramen happily at the convenience store window bar! Adding a slice of cheese or triangle kimbap on the side. Pure cozy satisfaction. Short Korean speech bubbles (MAX 5 chars): Songi says '국물끝내줌', Jichi says '가성비갑!'.\n"
        "- Panel ⑧ (Bottom-Right): Cheerful satisfied ending scene! Empty clean bowl, Jichi and Songi giving big thumbs up beside a cute wooden board reading '좋아요 & 구독 ❤️'. Short Korean speech bubbles (MAX 5 chars): Jichi says '완전꿀팁!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, steaming delicious Korean ramen textures, warm cozy night snack mood. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '냄비라면각', '비주얼대박', '꼬들꼬들해', '진짜냄비맛', '국물끝내줌', '가성비갑!', '완전꿀팁!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 전자레인지 조리 직후 김이 모락모락 피어오르는 완성된 냄비라면 실사\n"
        "- 6번컷 참조 사진: 젓가락으로 탱글탱글하고 꼬들한 면발을 들어 올린 클로즈업 샷 (★핵심 킬링컷!)\n"
        "- 7번컷 참조 사진: 편의점 시식대에서 삼각김밥이나 치즈와 함께 즐기는 꿀조합 먹방 컷\n"
        "- 8번컷 참조 사진: 국물까지 깔끔하게 비운 완식 인증 컷"
    )

    # 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (100% 영구 표준 준수)
    fact_block_1 = "제품명 : 편의점 전자레인지 라면 조리 용기 (오!렌지 등)\n가격 : 약 700원 (봉지라면 별도)\n매장 : 전국 주요 편의점 라면 매대 및 생활용품 코너"
    fact_block_2 = "핵심 포인트 : 비싼 한강 라면 조리기 기계 없이도\n매장 내 일반 전자레인지만으로\n봉지라면을 냄비에 끓인 듯 꼬들하게 완성하는 700원 꿀템"
    fact_block_3 = "특징 및 식감: 흐물흐물 불어버리는 컵라면 식감 아님!\n뜨거운 물을 먼저 붓고 전자레인지에 3분~3분 30초 돌리면\n면발에 탄력이 살아있는 진짜 냄비라면 식감이 완전 좋아요\n설거지 귀찮은 자취생이나 캠핑족에게도 최고의 가성비 아이템"
    fact_block_4 = "Tasty Tip!\n찬물 대신 반드시 편의점 온수기의 뜨거운 물을 눈금선까지 부어야 면이 안 퍼져요!\n전자레인지 사양(700W/1000W)에 따라 3분~3분 30초로 시간을 조절하세요!\n조리 후 용기가 뜨거우니 손잡이 부분을 조심해서 꺼내시고 치즈나 계란 추가하면 금상첨화!"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분!\n쌀쌀한 밤, 컵라면 대신 진짜 냄비에 끓인 봉지라면이 간절해 편의점으로 출동한 새싹 요정 지치와 고양이 송이입니다!",
        "동네 편의점에 갔는데 한강 라면 조리기가 없어서 아쉬웠던 적 다들 한 번쯤 있으시죠?\n그런데 이제 조리기가 없어도 단돈 700원짜리 전용 용기 하나만 있으면 전자레인지로 완벽한 냄비라면을 끓일 수 있다는 사실, 알고 계셨나요?",
        "요즘 화제인 **편의점 700원 전자레인지 냄비라면 꿀팁**, 지치와 송이가 직접 체험해 본 솔직 리뷰 지금 바로 시작합니다!",
        prompt_cut1_4,
        guide_cut1_4,
        prompt_cut5_8,
        guide_cut5_8,
        fact_block_1,
        fact_block_2,
        fact_block_3,
        fact_block_4,
        "소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n오늘 전해드린 700원 냄비라면 꿀팁이 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다! 지치와 송이가 매일 가장 알차고 맛있는 편의점 소식을 전해드리겠습니다."
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
        "#지치웹툰", "#편의점꿀팁", "#야식추천",
        "#편의점라면", "#전자레인지라면", "#자취꿀템",
        "#700원냄비라면", "#봉지라면", "#오렌지용기"
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
        print(f"\n🎉 [지치 컴퍼니 웹툰 성공] 700원 냄비라면 웹툰이 네이버 블로그에 안전하게 임시저장되었습니다!")
    else:
        print(f"\n🚨 [주의] 임시저장 과정 중 오류가 발생했습니다.")

    return success

if __name__ == "__main__":
    is_draft = "--publish" not in sys.argv
    publish_700won_pot_ramen_toon(save_draft=is_draft)
