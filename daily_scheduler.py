import sys
import time
import datetime
import os

# Windows 콘솔 인코딩 안전화
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import schedule
import collector
import formatter
import prompt_engine
import snack_trends
import auto_publisher
import notifier
import content_generator
import quality_inspector
import history_checker


def run_ai_article_routine(article_index: int):
    """
    [지치 컴퍼니 AI 드림팀 협업 파이프라인]
    - 코치(소재 발굴) -> 코포터(기사 집필) -> 코자이너(썸네일 디자인) -> 코리티(품질 검사 및 수리) -> 코널리스트(발행 및 통계)
    """
    print(f"\n[{datetime.datetime.now()}] 🏢 [지치 컴퍼니] AI 정규 기사 #{article_index} 협업 파이프라인 가동!")
    
    # 1. 🔎 [코치] 실시간 트렌드 및 빅테크 킬러 소재 탐색
    print("  🔎 [코치] 전 세계 빅테크 이슈 및 검색량 1위 킬러 소재 발굴 중...")
    all_articles = collector.get_all_sources()
    if not all_articles:
        print("  ❌ [코치] 수집된 최신 기사가 없습니다.")
        return False

    if 1 <= article_index <= len(all_articles):
        target = all_articles[article_index - 1]
    else:
        fresh_articles = [
            a for a in all_articles
            if not history_checker.is_article_already_published_live(a["title"])
        ]
        pool = fresh_articles if fresh_articles else all_articles
        target = pool[0]

    print(f"  🎯 [코치] 오늘의 1등 타겟 소재 확정: '{target['title'][:30]}...'")

    # 2. ✍️ [코포터] 10년 차 IT 테크 기자 심층 원고 집필
    print(f"  ✍️ [코포터] 1,500자 심층 분석 원고 및 가독성 볼드 하이라이트 작성 중...")
    generated = content_generator.generate_article_with_ai(target["title"], target["url"])

    title = generated.get("title", f"[AI 분석] {target['title'][:22]}")
    body_text = generated.get("body", target["title"])
    image_prompt = generated.get("image_prompt", "")
    summary_lines = generated.get("summary_lines", [f"{target['title'][:12]} 전격 공개!", "글로벌 테크 시장 술렁"])

    # 16~18자 모바일 가독성 줄바꿈 적용
    formatted_body = formatter.format_mobile_text(body_text)
    paragraphs = [p for p in formatted_body.split("\n\n") if p.strip()]

    # 3. 🎨 [코자이너] 100% OpenAI DALL-E 3 전용 3D 일러스트 렌더링 & 1691x930 썸네일 합성
    print(f"  🎨 [코자이너] OpenAI DALL-E 3 기반 3D 일러스트 생성 및 1691x930 썸네일 카드 정밀 합성 중...")
    thumb_filename = f"완성_썸네일_1691x930.png"
    thumb_path = content_generator.generate_article_thumbnail(
        topic=target["title"],
        image_prompt=image_prompt,
        output_path=thumb_filename,
        summary_lines=summary_lines,
        article_index=article_index
    )

    # 4. 🕵️‍♂️ [코리티] 포스팅 전 선제 품질 검사 (이미지 DALL-E 3 무결점 + 제목 + 요약 + 줄바꿈)
    print("  🕵️‍♂️ [코리티] 5대 선제 품질 검사(DALL-E 3 이미지 무결점/제목/요약/줄바꿈/소제목 여백) 가동...")
    is_valid, title, summary_lines, paragraphs = quality_inspector.validate_and_repair_article_pre_publish(
        title=title,
        summary_lines=summary_lines,
        paragraphs=paragraphs,
        topic=target["title"],
        article_index=article_index,
        thumb_path=thumb_path
    )

    if not is_valid:
        print(f"  🛑 [코리티 책임 발행 중단] 기사 #{article_index} 이미지 품질/DALL-E 3 검증 미통과로 발행을 즉시 중단합니다!")
        notifier.send_emergency_alert(
            failed_task_name=f"기사 #{article_index} 발행 긴급 중단 (코리티 품질 방어선)",
            error_detail="OpenAI DALL-E 3 이미지 생성 실패 또는 제미니 우회 차단 규정으로 인해 안전하게 발행을 취소했습니다."
        )
        return False

    # 5. 📊 [코널리스트] 17px 볼드 소제목 + 센터 정렬 + 해시태그 스마트에디터 정밀 발행
    print(f"  📊 [코널리스트] 네이버 스마트에디터 원격 발행 개시 (카테고리: AI 정보)...")
    tags = generated.get(
        "tags",
        ["#인공지능", "#AI트렌드", "#테크뉴스", "#IT기사", "#지치블로그", "#신기술", "#AI정보"]
    )
    success = auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=paragraphs,
        image_paths=[thumb_path] if os.path.exists(thumb_path) else None,
        category_name="AI 정보",
        tags=tags
    )

    if not success:
        print(f"  🚨 [비상] 기사 #{article_index} 포스팅 실패 감지! 대표님께 비상 알림 발송 중...")
        notifier.send_emergency_alert(
            failed_task_name=f"AI 트렌드 기사 #{article_index}",
            error_detail="네이버 스마트에디터 발행 단계 중 지연 또는 일시적 오류 발생"
        )
        return False

    # 6. 🕵️‍♂️ [코리티] 최종 발행 후 독자 모드 실시간 품질 검증
    time.sleep(5)
    print("  🕵️‍♂️ [코리티] 블로그 라이브 발행물 최종 무결점 검증...")
    quality_inspector.inspect_latest_post_quality(expected_category="AI 정보", is_article=True)
    print(f"  🎉 [지치 컴퍼니] 기사 #{article_index} 미션 성공 완료!\n")
    return True


def run_ai_webtoon_routine(webtoon_index: int):
    """
    AI 웹툰 풀버전 고품질 발행 루틴:
    - [웹툰 1편]: 조회수 폭발 화제템 '리센느(RESCENE) 콜라보 신상 탐방' 시리즈
    - [웹툰 2편]: 실시간 1~5위 트렌드 중 미발행 검증된 1등 신상(연세우유 밤티라미수 등)
    - DALL-E 3 세로형 3컷 만화 2장 실시간 생성 및 대사 상단 인터리빙 배치
    """
    if webtoon_index == 1:
        print(f"\n[{datetime.datetime.now()}] 🎨 [AI 웹툰 #1] 화제성 1등 '리센느(RESCENE)' 탐방 에피소드 발행 시작!")
        target = {
            "keyword": "CU 리센느(RESCENE) 콜라보 베이커리 5종 (시나몬롤·메론빵·옥수수크림빵)",
            "tag": "걸그룹 콜라보 품절 대란 신상 (조회수 1등 화제작)",
            "youtube": "포토카드 30종 수집 재미와 함께 베이커리 자체 완성도가 편의점 수준을 뛰어넘었다는 호평 다수.",
            "naver": "에어프라이어 180도 3분 조리 시 겉바속촉 갓 구운 빵집 퀄리티가 살아나며 커피나 우유와 찰떡궁합이라는 후기."
        }
        chars = ["지치 (새싹 요정)", "송이 (삼색 고양이)"]
    else:
        print(f"\n[{datetime.datetime.now()}] 🎨 [AI 웹툰 #2] 편의점/카페 실시간 인기 신상 에피소드 발행 시작!")
        ranked = snack_trends.get_realtime_ranked_trends()
        valid_picks = [x for x in ranked if not x.get("is_duplicate") and "리센느" not in x.get("keyword", "")]
        target = valid_picks[0] if valid_picks else ranked[0]
        chars = ["지치 (새싹 요정)", "초코 (턱시도 고양이)"]

    wt_data = content_generator.generate_webtoon_with_ai(
        snack_name=target["keyword"],
        tag=target["tag"],
        youtube=target["youtube"],
        naver=target["naver"],
        chars=chars,
        generate_images=True
    )

    # 🕵️‍♂️ [코리티 웹툰 이미지 전수 검사] DALL-E 3 이미지 정상 생성 여부 확인
    webtoon_imgs = wt_data.get("image_paths") or []
    valid_webtoon_imgs = [p for p in webtoon_imgs if p and os.path.exists(p) and os.path.getsize(p) > 10000]
    if not valid_webtoon_imgs:
        print(f"  🚨 [코리티 웹툰 긴급 권한 발동] DALL-E 3 웹툰 이미지 생성 실패/부재 감지!")
        print("  🛑 [웹툰 발행 즉시 중지] 사장님 방침에 따라 비정상 이미지/타사 우회 상태에서는 발행하지 않습니다.")
        notifier.send_emergency_alert(
            failed_task_name=f"웹툰 #{webtoon_index} 발행 긴급 중단 (코리티 방어선)",
            error_detail="OpenAI DALL-E 3 웹툰 이미지 생성에 실패하여 품질 보호를 위해 발행을 중단했습니다."
        )
        return False

    # 이미지 마커(__IMAGE__:)는 그대로 유지하고 일반 대사/문단만 26자 모바일 줄바꿈 적용
    formatted_paragraphs = []
    for p in wt_data["content_paragraphs"]:
        p_str = str(p).strip()
        if not p_str:
            continue
        if p_str.startswith("__IMAGE__:"):
            formatted_paragraphs.append(p_str)
        else:
            formatted_paragraphs.append(formatter.format_mobile_text(p_str, max_chars=26))

    success = auto_publisher.post_to_naver_blog(
        title=wt_data["title"],
        content_paragraphs=formatted_paragraphs,
        image_paths=wt_data.get("image_paths"),
        category_name="웹툰",
        tags=wt_data.get(
            "tags",
            ["#편의점신상", "#디저트추천", "#솔직후기", "#내돈내산", "#지치웹툰", "#신상리뷰", "#편의점꿀팁"]
        ),
        save_draft=True
    )

    if success:
        print(f"✅ [웹툰 임시저장 성공] 사장님 퇴근 후 검토를 위해 블로그 임시저장함에 안전 등록 완료: {wt_data['title']}")

    return success


def run_rescene_draft_routine():
    """
    [사장님 특별 지시] CU 리센느 '제나의 딸기잼 샌드' 실물 사진 + 공식 캐릭터 시트 메모리 잠금 웹툰 임시저장 루틴
    - 1번 사진(webtoon_scene_1.png): 실제 CU 편의점 매장 내부 배경 + 공식 지치 & 송이 캐릭터 ("우와!")
    - 2번 사진(webtoon_scene_2.png): 3번 실사 사진의 실제 '제나의 딸기잼 샌드' 핑크 패키지를 들고 있는 지치 & 송이 ("대박!")
    - 3번 사진(rescene_detail_2.jpg): 실제 '제나의 딸기잼 샌드' 패키지 + 제나 포토카드 + 빵 단면 실사 사진
    - 4번 사진(webtoon_scene_4.png): 실제 리센느(RESCENE) 제나 포토카드를 앞에 두고 우유 건배하는 지치 & 송이
    - 임시저장(save_draft=True)으로 진행하여 사장님께서 블로그 임시저장함에서 직접 검토/수정 가능
    """
    print(f"\n[{datetime.datetime.now()}] 🍓 [CU 리센느 딸기샌드 실물 연동 + 캐릭터 시트 메모리 잠금 웹툰] 임시저장 생성 시작!")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scene1 = os.path.join(base_dir, "webtoon_scene_1.png")
    scene2 = os.path.join(base_dir, "webtoon_scene_2.png")
    real_photo = os.path.join(base_dir, "rescene_detail_2.jpg")
    scene4 = os.path.join(base_dir, "webtoon_scene_4.png")

    paragraphs = [
        "안녕하세요, 지치의 블로그를 찾아주신 여러분! 귀여운 마스코트 새싹 요정 지치와 삼색 고양이 송이입니다!",
        "오늘 지치와 송이가 출동한 곳은 요즘 포토카드 수집 열풍과 품절 대란을 일으키고 있는 CU 편의점입니다! 걸그룹 리센느(RESCENE) 콜라보 신상 디저트, '제나의 딸기잼 샌드'를 직접 만나러 왔어요.",
        f"__IMAGE__:{scene1}",
        "지치: '우와! 송이야, 편의점 매대 쪽으로 가보자! 오늘 우리가 찾던 신상이 입고됐을까?'",
        "송이: '두근두근하다냥! 품절되기 전에 얼른 베이커리 코너부터 살펴보자냥!'",
        f"__IMAGE__:{scene2}",
        "지치: '찾았다! 여기 제나 사진이 콕 박힌 핑크색 봉지, 제나의 딸기잼 샌드 실물이야!'",
        "송이: '대박이다냥! 실물 패키지가 러블리한 핑크빛이라 매대에서 단번에 눈에 띈다냥!'",
        "집으로 돌아와 지치와 송이가 설레는 마음으로 봉지를 개봉해 보았습니다.",
        f"__IMAGE__:{real_photo}",
        "[CU 리센느 '제나의 딸기잼 샌드' 실물 팩트 체크]",
        "- 가격: 2,500원 (CU 단독 출시 콜라보 베이커리)",
        "- 콘셉트: 일본식 딸기 마가린빵에서 아이디어를 얻어 개발된 촉촉하고 부드러운 샌드빵",
        "- 내용물: 폭신한 식빵 결 사이에 상큼달콤한 딸기잼과 부드러운 화이트 버터크림이 듬뿍!",
        "- 특별 구성: 리센느 멤버 포토카드(총 27종 중 랜덤 1종) 동봉! 이번 개봉에서는 패키지 주인공인 멤버 '제나(ZENA)'의 실물 포토카드가 쏙 나왔습니다.",
        f"__IMAGE__:{scene4}",
        "지치: '폭신한 빵 사이에 달콤한 딸기잼이랑 고소한 크림이 어우러져서 입안 가득 행복해지는 맛이야!'",
        "송이: '시원한 흰 우유 한 잔이랑 짠! 하고 같이 먹으니까 완전 환상의 짝꿍이다냥! 제나 포토카드까지 뽑아서 오늘 운 최고다냥!'",
        "[지치와 송이의 솔직 총평 & 맛있게 먹는 꿀팁]",
        "1. 퍽퍽함 없이 폭신한 식빵 식감에 상큼한 딸기잼과 부드러운 크림의 조화가 호불호 없이 즐길 수 있는 정석 디저트입니다.",
        "2. 시원한 흰 우유나 아이스 아메리카노를 곁들이면 달콤함이 훨씬 깔끔하게 살아납니다.",
        "3. 리센느 팬분들의 포토카드 컬렉션은 물론, 달콤한 편의점 빵을 좋아하시는 분들께 강력 추천합니다!",
        "오늘 리뷰가 도움 되셨다면 공감(❤️)과 이웃 추가 꾹 눌러주세요! 지치와 송이가 매일 핫한 편의점 신상과 최신 AI 소식을 전해드립니다!"
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

    # 네이버 여성/디저트/아이돌 덕질 검색 유입 1위 타겟 키워드 8종 풀배치
    rescene_tags = [
        "#CU신상", "#리센느", "#제나의딸기잼샌드", "#리센느빵",
        "#리센느포토카드", "#제나포카", "#포카깡", "#편의점디저트"
    ]

    success = auto_publisher.post_to_naver_blog(
        title="[지치와 송이의 편의점 탐방] CU 리센느 '제나의 딸기잼 샌드' 실물 & 제나 포카 개봉 솔직 후기!",
        content_paragraphs=formatted_paragraphs,
        category_name="웹툰",
        tags=rescene_tags,
        save_draft=True
    )
    return success


def execute_daily_sequence():
    """
    클라우드(GitHub Actions) 실행 시퀀스:
    - 매일 아침 09:00 KST 정기 스케줄(schedule) 실행 시: 기사 3편(10분 간격) + 웹툰 2편(20분 간격) 풀코스 발행
    - 수동 즉시 실행(workflow_dispatch) 시: 핵심 기사 1편 + (2분 후) 리센느 웹툰 1편 고속 검증 발행
    """
    event_name = os.environ.get("GITHUB_EVENT_NAME", "workflow_dispatch")

    if event_name == "schedule" or "--full-daily" in sys.argv:
        print("=" * 60)
        print("🚀 [09:00 KST 정규 무인 스케줄러: AI 기사 3편 연속 발행 가동 (웹툰은 사장님 지시로 일시 보류)]")
        print("=" * 60)
        for i in range(1, 4):
            run_ai_article_routine(i)
            if i < 3:
                print(f"\n⏳ 네이버 봇 필터링 우회를 위해 10분 대기 후 기사 #{i+1} 발행을 시작합니다...")
                time.sleep(600)

        print("\n🎉 오늘 하루치 정규 기사 3편 발행 완료! (웹툰 자동화는 사장님 지시로 안전 보류되었습니다)")
    elif "--inception" in sys.argv:
        print("=" * 60)
        print("🚀 [즉시 실행: 1위 기사 '인셉션 충격 반전' 각색 웹툰 임시저장 가동]")
        print("=" * 60)
        import publish_inception_toon
        publish_inception_toon.produce_inception_adaptation_webtoon()
        print("\n🎉 네이버 블로그 임시저장함 등록 완료!")
    else:
        print("=" * 60)
        print("🚀 [즉시 실행: CU 리센느 'Runaway' 노래캔디 웹툰 임시저장 가동]")
        print("=" * 60)
        import publish_rescene_candy
        publish_rescene_candy.produce_rescene_candy_webtoon()
        print("\n🎉 네이버 블로그 임시저장함 등록 완료!")


def start_daily_scheduler():
    """로컬 컴퓨터 24시간 상주 모드"""
    print("=" * 60)
    print("⏰ [로컬 데스크탑 무인 자동화 엔진] 스케줄러 가동 중...")
    print("=" * 60)
    schedule.every().day.at("09:00").do(run_ai_article_routine, article_index=1)
    schedule.every().day.at("09:10").do(run_ai_article_routine, article_index=2)
    schedule.every().day.at("09:20").do(run_ai_article_routine, article_index=3)
    # [사장님 특별 지시] 웹툰은 수동 검토를 거쳐 발행하므로 자동발행 스케줄(09:40, 10:00)은 안전 비활성화 (AI 기사만 자동발행)
    # schedule.every().day.at("09:40").do(run_ai_webtoon_routine, webtoon_index=1)
    # schedule.every().day.at("10:00").do(run_ai_webtoon_routine, webtoon_index=2)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    if "--cloud-mode" in sys.argv or os.environ.get("GITHUB_ACTIONS") == "true":
        execute_daily_sequence()
    else:
        start_daily_scheduler()
