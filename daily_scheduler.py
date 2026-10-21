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

def run_ai_article_routine(article_index: int):
    """
    AI 트렌드 기사 풀버전 고품질 발행 루틴 (10년 차 테크 기자 어조 + 1,500자 + 1691x930 썸네일)
    """
    print(f"\n[{datetime.datetime.now()}] 📰 [AI 트렌드 기사 #{article_index}] 고품질 자동 생성 & 발행 시작!")
    articles = collector.get_all_sources()
    if not articles or len(articles) < article_index:
        print("❌ 수집된 최신 기사가 부족합니다.")
        return False

    target = articles[article_index - 1]
    
    # 1. 10년 차 IT 테크 기자의 심층 분석 원고 생성 (Gemini / GPT)
    print(f"🤖 AI 기사 심층 분석 원고 생성 중... ({target['title'][:15]}...)")
    generated = content_generator.generate_article_with_ai(target['title'], target['url'])
    
    title = generated.get("title", f"[AI 분석] {target['title'][:25]}")
    body_text = generated.get("body", target['title'])
    
    # 2. 25자 가독성 줄바꿈 포맷팅 적용
    formatted_body = formatter.format_mobile_text(body_text)
    paragraphs = formatted_body.split("\n\n")

    # 3. 1691x930 맞춤 썸네일 합성
    thumb_path = os.path.join(os.getcwd(), "완성_썸네일_1691x930.png")
    
    # 4. 네이버 블로그 'AI 정보' 카테고리 및 검색 태그 5~8개 발행
    tags = generated.get("tags", ["#인공지능", "#AI트렌드", "#테크뉴스", "#IT기사", "#지치블로그", "#신기술", "#AI정보"])
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
        
    # 5. 🕵️‍♂️ [코부장 전수 품질 검사 실시!]
    time.sleep(5)
    quality_inspector.inspect_latest_post_quality(expected_category="AI 정보", is_article=True)
    return True

def run_ai_webtoon_routine(webtoon_index: int):
    """
    AI 웹툰 풀버전 고품질 발행 루틴:
    - [웹툰 1편]: 사장님 전략 반영! 조회수 폭발 화제템 '리센느(RESCENE) 콜라보 신상 탐방' 고정!
    - [웹툰 2편]: 실시간 1~5위 트렌드 중 기발행 제외 검증된 1등 신상(연세우유 밤티라미수 등) 고정!
    """
    if webtoon_index == 1:
        print(f"\n[{datetime.datetime.now()}] 🎨 [AI 웹툰 #1] 🔥 화제성 1등 '리센느(RESCENE)' 고정 에피소드 발행 시작!")
        target = {
            "keyword": "CU 리센느(RESCENE) 빵 5종 (시나몬롤·메론빵·옥수수빵)",
            "tag": "🔥 걸그룹 콜라보 품절 대란 신상 (조회수 1등 화제작)",
            "youtube": "포토카드 모으는 재미와 빵 자체 퀄리티가 편의점 수준을 넘었다는 극찬 리뷰 다수.",
            "naver": "에어프라이어에 3분 돌려먹으면 겉바속촉 갓 구운 빵집 퀄리티 완성! 시나몬 향이 진해서 커피랑 찰떡궁합."
        }
        chars = ["지치 (새싹 요정)", "송이 (삼색 고양이)"]
    else:
        print(f"\n[{datetime.datetime.now()}] 🎨 [AI 웹툰 #2] 🍰 편의점/카페 실시간 인기 신상 에피소드 발행 시작!")
        ranked = snack_trends.get_realtime_ranked_trends()
        # 리센느를 제외한 미발행 최우선 신상 선정
        valid_picks = [x for x in ranked if not x.get("is_duplicate") and "리센느" not in x.get("keyword", "")]
        target = valid_picks[0] if valid_picks else ranked[0]
        chars = ["지치 (새싹 요정)", "초코 (턱시도 고양이)"]

    # AI 기반 지치와 친구들의 티키타카 리뷰 대본 생성
    wt_data = content_generator.generate_webtoon_with_ai(
        snack_name=target['keyword'],
        tag=target['tag'],
        youtube=target['youtube'],
        naver=target['naver'],
        chars=chars
    )

    success = auto_publisher.post_to_naver_blog(
        title=wt_data["title"],
        content_paragraphs=wt_data["content_paragraphs"],
        category_name="웹툰",
        tags=wt_data.get("tags", ["#편의점신상", "#디저트추천", "#솔직후기", "#내돈내산", "#지치웹툰", "#신상리뷰", "#편의점꿀팁"])
    )
    
    if success:
        time.sleep(5)
        quality_inspector.inspect_latest_post_quality(expected_category="웹툰", is_article=False)

    return success

def execute_daily_sequence():
    """
    클라우드 가상 머신용: 켜지자마자 정해진 시간차(10분, 20분)를 두고 즉시 순차 실행
    09:00 기사 1 ➡️ 10분 후 기사 2 ➡️ 10분 후 기사 3 ➡️ 20분 후 웹툰 1 ➡️ 20분 후 웹툰 2
    """
    print("=" * 60)
    print("🚀 [클라우드 09:00 KST 즉시 순차 발행 파이프라인 가동]")
    print("=" * 60)

    # 1. 09:00 기사 1
    success = run_ai_article_routine(1)
    if not success:
        print("⚠️ 기사 1편 발행 실패로 10분 대기 건너뜁니다.")
    else:
        print("\n⏳ 10분 대기 후 기사 2편 발행 (09:10)...")
        time.sleep(600)
    
    # 2. 09:10 기사 2
    success2 = run_ai_article_routine(2)
    if not success2:
        print("⚠️ 기사 2편 발행 실패로 10분 대기 건너뜁니다.")
    else:
        print("\n⏳ 10분 대기 후 기사 3편 발행 (09:20)...")
        time.sleep(600)
    
    # 3. 09:20 기사 3
    run_ai_article_routine(3)
    
    print("\n⏳ 20분 대기 후 웹툰 1편 발행 (09:40)...")
    time.sleep(1200)
    
    # 4. 09:40 웹툰 1
    run_ai_webtoon_routine(1)
    
    print("\n⏳ 20분 대기 후 웹툰 2편 발행 (10:00)...")
    time.sleep(1200)
    
    # 5. 10:00 웹툰 2
    run_ai_webtoon_routine(2)
    print("\n🎉 오늘 하루 5개 포스팅 전체 자동 완료!")

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
