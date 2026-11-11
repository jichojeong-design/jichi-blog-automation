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

def publish_gs25_jumbo_dosirak_hangang_toon(save_draft: bool = True):
    """
    [지치 컴퍼니 정규 편의점 신상 웹툰 - 한강 야경 먹방 낭만 편]
    주제: 퇴근길 한강공원 벤치에서 즐기는 역대급 스케일!
          GS25 '점보라면 킹도시락' (기존 4배 대용량 컵라면)
          "쌀쌀한 강바람 맞으며 김 모락모락 라면 호로록 면치기하는 한강 낭만 먹방"
    등장인물: 지치(새싹 요정) + 송이(삼색 고양이 한강 라면 탐식가)

    [대표님 엄격 5대 절대 수칙 100% 완전 준수]:
    1. 4컷 이후 불필요한 긴 대화 대본 전면 삭제 (방문객 이탈 방지)
    2. 코자이너 웹툰 말풍선은 무조건 '5글자 이내' 초심플 한글 키워드 엄수!
    3. 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (구분선 없이 바로 제품명 시작, 컴팩트 줄바꿈 + 블록 간 빈 줄)
    4. 프롬프트 바로 아래 코자이너의 '1~8컷별 실사 이미지 배치 & 첨부 가이드' 의무 작성!
    5. 3·3·3 태그 공식 (인물/상황 3 + 브랜드 3 + 제품 3) 및 에디터 전역 '바른히피' 서체 강제 주입!
    """
    title = "[지치와 송이의 편의점 탐방 웹툰] 한강 벤치에서 먹는 역대급 스케일! GS25 '점보라면 킹도시락' 솔직 리뷰!"

    # 1~4컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut1_4 = (
        "[CHATGPT 컷 1~4 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ①, ②, ③, ④ on top-left of each panel):\n"
        "- Panel ① (Top-Left): Inside GS25 convenience store near Han River park. Jichi the green sprout fairy and Songi the calico cat gasping with huge round eyes in front of the gigantic, enormous square package of '점보라면 킹도시락' on the ramen shelf. Short Korean speech bubbles (MAX 5 chars): Songi says '크기대박!', Jichi says '진짜크다!'.\n"
        "- Panel ② (Top-Right): Hot water station inside GS25! Pouring copious hot boiling water from two thermoses into the giant square ramen tub. Steam rising gloriously as 4 blocks of dried noodles soak. Short Korean speech bubbles (MAX 5 chars): Songi says '물붓는다!', Jichi says '김모락!'.\n"
        "- Panel ③ (Bottom-Left): Walking joyfully carrying the steaming giant square ramen box together with two hands towards the breezy Han River park at night. Glowing city bridge lights sparkling on the dark water. Short Korean speech bubbles (MAX 5 chars): Songi says '한강가자!', Jichi says '야경최고!'.\n"
        "- Panel ④ (Bottom-Right): Sitting side-by-side on a rustic wooden park bench overlooking the glistening Han River night view. Setting down the massive steaming ramen tub and two pairs of wooden chopsticks on the bench table. Short Korean speech bubbles (MAX 5 chars): Songi says '벤치착석!', Jichi says '먹방준비!'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, romantic evening Han River park lighting with sparkling city lights, cozy night picnic mood. Speech bubbles MUST ONLY contain the exact ultra-short Korean words (5 characters or fewer: '크기대박!', '진짜크다!', '물붓는다!', '김모락!', '한강가자!', '야경최고!', '벤치착석!', '먹방준비!'). Panel badges ① ② ③ ④ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos (from Jichi Company Star Character Sheet: Jichi the green sprout fairy with two leaf sprouts and Songi the calico cat with distinct tricolor patches) as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity to the attached images!\n"
        "[CHATGPT 컷 1~4 복사 끝]"
    )

    # 코자이너 1~4컷 실사 이미지 배치 가이드
    guide_cut1_4 = (
        "[코자이너 1컷~4컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 1번컷 참조 사진: GS25 편의점 매대에 진열된 거대한 점보라면 킹도시락 패키지 정면 실사\n"
        "- 2번컷 참조 사진: 점보라면 뚜껑을 열고 대용량 온수를 콸콸 붓는 편의점 조리 실사\n"
        "- 3번컷 참조 사진: 한강 다리 불빛과 강물이 반짝이는 낭만적인 한강공원 야경 실사\n"
        "- 4번컷 참조 사진: 한강공원 벤치 위에 김이 모락모락 피어오르는 점보 도시락 뚜껑을 올려둔 실물 컷"
    )

    # 5~8컷 ChatGPT용 4분할 프롬프트 (5글자 이내 말풍선 엄수)
    prompt_cut5_8 = (
        "[CHATGPT 컷 5~8 복사 시작]\n"
        "PANEL LAYOUT (2x2 Grid with subtle circular badge numbers ⑤, ⑥, ⑦, ⑧ on top-left of each panel):\n"
        "- Panel ⑤ (Top-Left): Removing the giant square lid! A massive ocean of curly yellow ramen noodles in rich, savory orange broth with floating dried beef cakes and green scallions wafting thick steam into the cool evening breeze. Short Korean speech bubbles (MAX 5 chars): Songi says '오픈이다!', Jichi says '푸짐하다!'.\n"
        "- Panel ⑥ (Top-Right): Slurping noodles with blissful faces! Songi lifting a huge cluster of springy noodles with long wooden chopsticks, blowing gently before a big slurp. Jichi slurping a spoonful of piping-hot soup. Short Korean speech bubbles (MAX 5 chars): Songi says '면치기호록!', Jichi says '속풀린다!'.\n"
        "- Panel ⑦ (Bottom-Left): Cheerful eating together on the park bench! Chilly autumn river wind blowing their hair gently, but their cheeks are flushed red and warm from the spicy broth. Sharing noodles happily under park lamp. Short Korean speech bubbles (MAX 5 chars): Songi says '꿀맛조합!', Jichi says '힐링제대로!'.\n"
        "- Panel ⑧ (Bottom-Right): Triumphant ending scene! Looking into the nearly empty giant tub with huge satisfied smiles, giving enthusiastic double thumbs-up beside a rustic wooden signboard reading '좋아요 & 구독 ❤️'. Short Korean speech bubbles (MAX 5 chars): Jichi says '완전정복!', Songi says '좋아요❤️'.\n\n"
        "STYLE & CONSTRAINTS: Pixar 3D CGI animation, warm delicious mouthwatering steam contrast against cool night breeze, cheerful comedic friendship. Speech bubbles MUST ONLY contain ultra-short Korean words (5 characters or fewer: '오픈이다!', '푸짐하다!', '면치기호록!', '속풀린다!', '꿀맛조합!', '힐링제대로!', '완전정복!', '좋아요❤️'). Panel badges ⑤ ⑥ ⑦ ⑧ clearly marked.\n\n"
        "***CRITICAL MANDATORY INSTRUCTION FOR CHARACTER CONSISTENCY***:\n"
        "You MUST strictly use the attached character reference sheet photos as the absolute visual anchor. Follow this prompt strictly and maintain 100% faithful character fidelity!\n"
        "[CHATGPT 컷 5~8 복사 끝]"
    )

    # 코자이너 5~8컷 실사 이미지 배치 가이드
    guide_cut5_8 = (
        "[코자이너 5컷~8컷 실사 이미지 배치 & 첨부 가이드]\n"
        "- 5번컷 참조 사진: 뚜껑을 완전히 열어 4배 면발과 큼직한 건더기가 먹음직스럽게 익은 점보라면 실사\n"
        "- 6번컷 참조 사진: 젓가락으로 면발을 듬뿍 집어 올려 한강 야경을 배경으로 찍은 클로즈업 실사 (★가장 중요!)\n"
        "- 7번컷 참조 사진: 벤치에서 단무지나 볶음김치를 곁들여 먹는 리얼 먹방 컷\n"
        "- 8번컷 참조 사진: 깨끗하게 비워낸 점보 용기를 분리수거하기 전 찍은 완식 기념 컷"
    )

    # 친누나표 '팩트 체크 & Tasty Tip!' 황금 양식 (100% 영구 표준 준수)
    fact_block_1 = "제품명 : GS25 팔도 '점보라면 킹도시락' (기존 4배 대용량)\n가격 : 8,500원 (총 중량 약 650g / 8인분급 면발)\n매장 : 전국 GS25 편의점 및 우리동네GS 재고 찾기"
    fact_block_2 = "핵심 플레이버 : 추억의 오리지널 도시락 육수 +\n칼칼하고 구수한 쇠고기 분말 스프 +\n면발 4개 꽉 채운 압도적 볼륨감의 쫄깃한 면발"
    fact_block_3 = "특징 및 식감: 팅팅 불어 터지는 흉내만 낸 라면 아님!\n추억의 도시락 얇은 면발 특유의 쫄깃한 식감과\n찬 바람 부는 야외에서 먹을 때 온몸이 녹아내리는 감칠맛\n혼자는 무리지만 둘셋이 벤치에 모여 먹으면 최고의 추억"
    fact_block_4 = "Tasty Tip!\n한강공원 벤치에서 먹을 땐 뜨거운 물을 넉넉히 붓고 뚜껑 꼭 닫기!\n쌀쌀한 강바람에 국물이 식을 수 있으니 3분 칼같이 지키기!\n편의점 볶음김치나 단무지 하나 곁들이면 물릴 틈 없이 완벽해요"

    paragraphs = [
        "안녕하세요, 지치 블로그를 찾아주신 여러분!\n퇴근 후 낭만 가득한 한강공원으로 라면 원정을 떠난 귀여운 새싹 요정 지치와 고양이 송이입니다!",
        "수요일 밤, 고단했던 하루를 마치고 시원한 강바람 쐬러 한강에 가면 편의점 컵라면 하나 때리는 게 국룰이잖아요.\n그런데 이번엔 평범한 컵라면이 아니라 무려 기존 도시락 라면의 4배 크기를 자랑하는 초대형 신상, **GS25 점보라면 킹도시락**을 들고 한강 벤치로 출동했습니다!",
        "반짝이는 한강 야경을 바라보며 김 펄펄 나는 거대 라면을 친구와 호로록 면치기하는 낭만 끝판왕 먹방, 지금 바로 시작합니다!",
        prompt_cut1_4,
        guide_cut1_4,
        prompt_cut5_8,
        guide_cut5_8,
        fact_block_1,
        fact_block_2,
        fact_block_3,
        fact_block_4,
        "소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n오늘 전해드린 한강 벤치 점보라면 킹도시락 먹방 웹툰이 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다! 지치와 송이가 매일 가장 유쾌하고 낭만 있는 편의점 소식을 전해드리겠습니다."
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
        "#지치웹툰", "#한강라면", "#한강공원먹방",
        "#GS25", "#GS25신상", "#편의점라면",
        "#점보라면", "#킹도시락", "#대용량라면"
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
        print(f"\n🎉 [지치 컴퍼니 웹툰 성공] 한강공원 벤치 점보라면 킹도시락 웹툰이 네이버 블로그에 안전하게 임시저장되었습니다!")
    else:
        print(f"\n🚨 [주의] 임시저장 과정 중 오류가 발생했습니다.")

    return success

if __name__ == "__main__":
    is_draft = "--publish" not in sys.argv
    publish_gs25_jumbo_dosirak_hangang_toon(save_draft=is_draft)
