import time
import datetime
import os
import schedule
import collector
import formatter
import prompt_engine
import snack_trends
import auto_publisher

def run_ai_article_routine(article_index: int):
    """
    AI 트렌드 기사 발행 루틴 (1편씩 실행)
    """
    print(f"\n[{datetime.datetime.now()}] 📰 [AI 트렌드 기사 #{article_index}] 자동 수집 & 발행 시작!")
    articles = collector.fetch_curated_ai_news()
    if not articles or len(articles) < article_index:
        print("❌ 수집된 최신 기사가 부족합니다.")
        return

    target = articles[article_index - 1]
    title = f"[AI 속보] {target['title']}"
    
    # 본문 생성 및 25자 줄바꿈 포맷팅
    body_raw = f"{target['title']}\n\n최신 인공지능 트렌드와 기술적 혁신이 산업 전반에 미치는 파급력을 심층 분석합니다.\n\n출처: {target['source']}\n원문 링크: {target['link']}"
    formatted_body = formatter.format_mobile_text(body_raw)
    paragraphs = formatted_body.split("\n\n")

    # 대표 썸네일 합성 (1691x930)
    thumb_path = os.path.join(os.getcwd(), "완성_썸네일_1691x930.png")
    
    # 네이버 스마트에디터 포스팅
    auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=paragraphs,
        image_paths=[thumb_path] if os.path.exists(thumb_path) else None,
        category_name="AI 트렌드"
    )

def run_ai_webtoon_routine(webtoon_index: int):
    """
    AI 웹툰 발행 루틴 (1편씩 실행)
    """
    print(f"\n[{datetime.datetime.now()}] 🎨 [AI 웹툰 #{webtoon_index}] 실시간 트렌드 검증 & 발행 시작!")
    ranked = snack_trends.get_realtime_ranked_trends()
    best_picks = [x for x in ranked if x.get("is_selected_best")]
    
    if len(best_picks) < webtoon_index:
        # fallback to non-duplicate
        valid_picks = [x for x in ranked if not x.get("is_duplicate")]
        target = valid_picks[webtoon_index - 1] if len(valid_picks) >= webtoon_index else ranked[0]
    else:
        target = best_picks[webtoon_index - 1]

    title = f"[지치의 편의점 탐방] {target['keyword']} 솔직 시식 후기!"
    
    body_content = [
        f"오늘의 화제작: {target['keyword']}",
        f"🔥 화제 포인트: {target['tag']}",
        f"🎬 유튜브 실시간 반응: {target['youtube']}",
        f"📝 내돈내산 시식 후기 요약: {target['naver']}",
        "지치와 친구들의 생생한 리뷰 만화는 아래 컷에서 확인해 보세요!"
    ]

    auto_publisher.post_to_naver_blog(
        title=title,
        content_paragraphs=body_content,
        category_name="지치 웹툰"
    )

def start_daily_scheduler():
    """
    매일 아침 09:00 KST 정밀 5단계 스케줄러 등록
    09:00 - AI 기사 1
    09:10 - AI 기사 2
    09:20 - AI 기사 3
    09:40 - AI 웹툰 1
    10:00 - AI 웹툰 2
    """
    print("=" * 60)
    print("⏰ [지치 블로그 무인 자동화 엔진] 스케줄러 가동 중...")
    print(" 매일 아침:")
    print("  - 09:00 : AI 트렌드 기사 1편")
    print("  - 09:10 : AI 트렌드 기사 2편")
    print("  - 09:20 : AI 트렌드 기사 3편")
    print("  - 09:40 : AI 웹툰 1편 (Best 1위)")
    print("  - 10:00 : AI 웹툰 2편 (Best 2위)")
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
    start_daily_scheduler()
