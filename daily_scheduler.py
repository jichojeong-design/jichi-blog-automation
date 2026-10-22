import sys
import time
import datetime
import os
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
    AI 트렌드 기사 풀버전 고품질 발행 루틴
    - 원문 팩트 크롤링 + 10년 차 테크 기자 어조 (1,500~1,800자)
    - DALL-E 3 1:1 일러스트 생성 후 1691x930 썸네일 자동 합성
    - 'AI 정보' 카테고리(categoryNo=6) + 가운데 정렬 + 25자 서식 + 태그 자동 입력
    """
    print(f"\n[{datetime.datetime.now()}] 📰 [AI 트렌드 기사 #{article_index}] 고품질 자동 생성 & 발행 시작!")
    all_articles = collector.get_all_sources()
    if not all_articles:
        print("❌ 수집된 최신 기사가 없습니다.")
        return False

    # 사장님 지정 순위(예: 4위 실시간 테스트) 또는 미발행 최신 기사 타겟팅
    if 1 <= article_index <= len(all_articles):
        target = all_articles[article_index - 1]
    else:
        fresh_articles = [
            a for a in all_articles
            if not history_checker.is_article_already_published_live(a["title"])
        ]
        pool = fresh_articles if fresh_articles else all_articles
        target = pool[0]

    # 1. 원문 크롤링 기반 10년 차 IT 테크 기자의 심층 분석 원고 생성 (Gemini 2.5 / GPT-4o)
    print(f"🤖 AI 기사 심층 분석 원고 생성 중... ({target['title'][:25]}...)")
    generated = content_generator.generate_article_with_ai(target["title"], target["url"])

    title = generated.get("title", f"[AI 분석] {target['title'][:22]}")
    body_text = generated.get("body", target["title"])
    image_prompt = generated.get("image_prompt", "")

    # 2. 25자 가독성 줄바꿈 포맷팅 적용 (URL 잘림 방지 및 소제목 앞뒤 여백 확보)
    formatted_body = formatter.format_mobile_text(body_text)
    paragraphs = [p for p in formatted_body.split("\n\n") if p.strip()]

    # 3. DALL-E 3 일러스트 생성 + 사장님 1691x930 원본 템플릿 자동 합성 (우측 상단 1~2줄 요약 포함)
    thumb_filename = f"완성_썸네일_1691x930.png"
    summary_lines = generated.get("summary_lines", [f"{target['title'][:12]} 전격 공개!", "글로벌 AI 시장 파장 분석"])
    thumb_path = content_generator.generate_article_thumbnail(
        topic=target["title"],
        image_prompt=image_prompt,
        output_path=thumb_filename,
        summary_lines=summary_lines,
        article_index=article_index
    )

    # 4. 네이버 블로그 'AI 정보' 카테고리 및 검색 태그 5~8개 발행
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
        print(f"🚨 [긴급] 기사 #{article_index} 포스팅 실패 감지! 사장님께 비상 알림 메일 발송 중...")
        notifier.send_emergency_alert(
            failed_task_name=f"AI 트렌드 기사 #{article_index}",
            error_detail="네이버 스마트에디터 발행 단계 중 지연 또는 일시적 오류 발생"
        )
        return False

    # 5. 코부장 전수 품질 검사 실시
    time.sleep(5)
    quality_inspector.inspect_latest_post_quality(expected_category="AI 정보", is_article=True)
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
        )
    )

    if success:
        time.sleep(5)
        quality_inspector.inspect_latest_post_quality(expected_category="웹툰", is_article=False)

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
    else:
        target_idx = int(os.environ.get("TARGET_ARTICLE_INDEX", "4"))
        for arg in sys.argv:
            if arg.startswith("--article-index="):
                try:
                    target_idx = int(arg.split("=")[1])
                except Exception:
                    pass
        print("=" * 60)
        print(f"🚀 [즉시 실행 테스트: AI 기사 #{target_idx}편 집중 발행 가동 (웹툰 안전 보류)]")
        print("=" * 60)
        run_ai_article_routine(target_idx)
        print(f"\n🎉 AI 기사 #{target_idx}편 발행 완료!")


def start_daily_scheduler():
    """로컬 컴퓨터 24시간 상주 모드"""
    print("=" * 60)
    print("⏰ [로컬 데스크탑 무인 자동화 엔진] 스케줄러 가동 중...")
    print("=" * 60)
    schedule.every().day.at("09:00").do(run_ai_article_routine, article_index=1)
    schedule.every().day.at("09:10").do(run_ai_article_routine, article_index=2)
    schedule.every().day.at("09:20").do(run_ai_article_routine, article_index=3)
    schedule.every().day.at("09:40").do(run_ai_webtoon_routine, webtoon_index=1)
    schedule.every().day.at("10:00").do(run_ai_webtoon_routine, webtoon_index=2)

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    if "--cloud-mode" in sys.argv or os.environ.get("GITHUB_ACTIONS") == "true":
        execute_daily_sequence()
    else:
        start_daily_scheduler()
