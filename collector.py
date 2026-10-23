import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

def get_aitimes_news():
    """AI타임스 최신 뉴스 수집 (슬롯 C / B)"""
    url = "https://www.aitimes.com/news/articleList.html?sc_section_code=S1N1&view_type=sm"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    items = []
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        articles = soup.select(".list-block") or soup.select(".table-row") or soup.select("section .list")
        if not articles:
            # fallback generic
            links = soup.select("a[href*='articleView.html']")
            seen = set()
            for a in links[:10]:
                title = a.get_text(strip=True)
                href = a.get("href", "")
                if title and len(title) > 10 and href not in seen:
                    seen.add(href)
                    if not href.startswith("http"):
                        href = "https://www.aitimes.com" + href
                    items.append({
                        "source": "AI타임스",
                        "title": title,
                        "url": href,
                        "slot": "C (일반인 활용 / 국내 트렌드)"
                    })
        else:
            for art in articles[:8]:
                title_tag = art.select_one(".titles a") or art.select_one("a")
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    href = title_tag.get("href", "")
                    if not href.startswith("http"):
                        href = "https://www.aitimes.com" + href
                    items.append({
                        "source": "AI타임스",
                        "title": title,
                        "url": href,
                        "slot": "C (일반인 활용 / 국내 트렌드)"
                    })
    except Exception as e:
        pass
    return items

def get_techcrunch_ai():
    """TechCrunch AI 최신 헤드라인 수집 (슬롯 B)"""
    url = "https://techcrunch.com/category/artificial-intelligence/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    items = []
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select("a.post-block__title__link, a.loop-card__title-link, h2 a, h3 a")
        seen = set()
        for a in links[:10]:
            title = a.get_text(strip=True)
            href = a.get("href", "")
            if title and len(title) > 15 and href not in seen:
                seen.add(href)
                items.append({
                    "source": "TechCrunch AI",
                    "title": title,
                    "url": href,
                    "slot": "B (산업·투자·기업 도입)"
                })
    except Exception as e:
        pass
    return items

# 대중 검색량 및 클릭률을 폭발시키는 빅테크/글로벌 킬러 브랜드 키워드 가중치 목록
HIGH_CTR_BRAND_KEYWORDS = [
    # 1티어: 네이버/구글 검색량 최상위 빅테크
    "테슬라", "스페이스X", "오픈AI", "OpenAI", "챗GPT", "ChatGPT", "엔비디아", "NVIDIA",
    "애플", "Apple", "구글", "Google", "메타", "Meta", "마이크로소프트", "MS", "클로드", "Claude",
    # 2티어: 화제성 국내외 AI 플랫폼 및 로봇
    "네이버", "카카오", "삼성전자", "SK하이닉스", "로봇", "휴머노이드", "피규어", "스타링크",
    "소라", "Sora", "제미나이", "Gemini", "딥시크", "DeepSeek", "코파일럿", "Copilot"
]

def score_article_importance(title: str) -> int:
    """
    일반 학술/어려운 기술 용어보다 대중적인 글로벌 빅테크 브랜드 키워드가 포함된 기사에 높은 우선순위 부여!
    (일 방문자 100명 돌파를 위한 검색 유입 최적화 점수 계산)
    """
    score = 0
    t_lower = title.lower()
    for kw in HIGH_CTR_BRAND_KEYWORDS:
        if kw.lower() in t_lower:
            score += 10
            
    # 단순 정책/회의/보고서 감점, 구체적 신제품/출시/실적/충격 가점
    if any(k in title for k in ["공개", "출시", "돌파", "폭등", "급락", "최초", "반전", "대란"]):
        score += 5
    if any(k in title for k in ["간담회", "세미나", "토론회", "동향보고", "개최"]):
        score -= 5
    return score

def get_all_sources():
    all_items = []
    all_items.extend(get_aitimes_news())
    all_items.extend(get_techcrunch_ai())
    
    # 빅테크 브랜드 키워드 가중치 기반 정렬 (점수가 높은 대중적 기사가 1~3위로 전면 배치됨)
    all_items.sort(key=lambda x: score_article_importance(x["title"]), reverse=True)
    return all_items
