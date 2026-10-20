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

def get_all_sources():
    all_items = []
    all_items.extend(get_aitimes_news())
    all_items.extend(get_techcrunch_ai())
    return all_items
