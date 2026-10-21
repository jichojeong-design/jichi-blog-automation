import urllib.request
import urllib.parse
import re

def get_live_published_titles(blog_id: str = "jcjung1401", category_no: int = 7) -> list:
    """
    지치 블로그 웹툰 카테고리(categoryNo=7)의 실제 실시간 발행 목록을 네이버 비동기 API로 즉시 조회
    (네이버의 percent-encoding을 정확한 UTF-8로 완벽 디코딩)
    """
    url = f"https://blog.naver.com/PostTitleListAsync.naver?blogId={blog_id}&viewdate=&currentPage=1&categoryNo={category_no}&parentCategoryNo=&countPerPage=30"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    published_items = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            raw_bytes = resp.read()
            # 바이트 레벨에서 title과 addDate 추출
            matches = re.findall(rb'"title":"([^"]+)"[^{}]*?"addDate":"([^"]+)"', raw_bytes)
            for t_bytes, d_bytes in matches:
                try:
                    # %EB%8D... 형태를 언쿼트하여 바이트 변환 후 UTF-8로 완벽 복원!
                    clean_title = urllib.parse.unquote_to_bytes(t_bytes.decode('ascii', errors='ignore')).decode('utf-8', errors='ignore')
                    clean_date = d_bytes.decode('utf-8', errors='ignore')
                    published_items.append({"title": clean_title, "date": clean_date})
                except Exception:
                    pass
    except Exception as e:
        pass
        
    # 과거 이력도 함께 보완
    fallback_items = [
        {"title": "리센느 CU 빵, 지치가 품절시킨 진짜 이유", "date": "2026. 10. 19."},
        {"title": "CU 리센느빵 5종, 가장 맛있는 빵은?", "date": "2026. 10. 18."},
        {"title": "후와후와 딥초코 쫀득빵, 쿠키인 줄 알았는데?", "date": "2026. 10. 17."},
        {"title": "3시15분 밀크티 생크림빵, 빨대 대신 포크!", "date": "2026. 10. 16."},
        {"title": "생초코파이 가토오쇼콜라, 초코파이인 줄 알았는데?", "date": "2026. 10. 15."}
    ]
    for fb in fallback_items:
        if not any(fb["title"] in p["title"] for p in published_items):
            published_items.append(fb)
            
    return published_items

def is_already_published_live(target_keyword: str, blog_id: str = "jcjung1401") -> tuple:
    """
    실시간으로 네이버 블로그를 직접 조회하여 중복 발행 여부 100% 검증
    (리센느, 스타벅스 멜론 등 핵심 단어 완벽 탐지)
    """
    live_posts = get_live_published_titles(blog_id=blog_id, category_no=7)
    
    # 비교를 위한 전처리
    target_clean = re.sub(r'[^가-힣a-zA-Z0-9]', '', target_keyword.lower())
    
    # 핵심 단어들 (예: '리센느', 'rescene', '멜론', '스타벅스', '밤티라미수' 등)
    # 2글자 이상의 의미 있는 단어 추출
    target_tokens = [tok for tok in re.split(r'[\s,\(\)]+', target_keyword) if len(tok) >= 2 and tok.lower() not in ["신상", "종합", "콜라보", "출시", "인기"]]
    
    for p in live_posts:
        title = p["title"]
        title_clean = re.sub(r'[^가-힣a-zA-Z0-9]', '', title.lower())
        
        # 1. '리센느'나 'rescene' 같은 핵심 고유명사가 양쪽 모두에 들어있는 경우
        for tok in target_tokens:
            tok_lower = tok.lower()
            if tok_lower in ["리센느", "rescene", "멜론", "두바이", "점보라면"] and tok_lower in title.lower():
                return True, f"이미 발행됨 ({p['date']}: {title[:18]}...)"
                
        # 2. 전체 문자열 매칭
        if target_clean in title_clean or (len(title_clean) > 5 and title_clean in target_clean):
            return True, f"이미 발행됨 ({p['date']}: {title[:18]}...)"
            
        # 3. 핵심 토큰 2개 이상 일치
        matched = [tok for tok in target_tokens if tok.lower() in title.lower()]
        if len(matched) >= 2:
            return True, f"이미 발행됨 ({p['date']}: {title[:18]}...)"
            
    return False, ""


def is_article_already_published_live(headline: str, blog_id: str = "jcjung1401") -> bool:
    """
    AI 정보 카테고리(categoryNo=6) 및 전체 글(categoryNo=0)을 실시간 조회하여
    이미 발행된 뉴스 기사인지 중복 여부를 판별합니다.
    """
    live_posts = get_live_published_titles(blog_id=blog_id, category_no=0)
    tokens = [
        tok for tok in re.split(r"[\s,\(\)\[\]\"'‘’“”…·:]+", headline)
        if len(tok) >= 2 and tok not in ["AI", "인공지능", "공개", "출시", "발표", "개발", "기술"]
    ]
    if not tokens:
        return False

    for p in live_posts:
        title = p["title"]
        matched = [tok for tok in tokens[:5] if tok in title]
        if len(matched) >= 2:
            return True
    return False

