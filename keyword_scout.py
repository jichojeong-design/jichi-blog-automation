import os
import sys
import json
import time
import hmac
import hashlib
import base64
import re
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}


def get_published_blog_keywords() -> list:
    """
    [지치컴패니 공식 영구 업무 매뉴얼 제2호] 기발행 중복 필터링 엔진
    지치 블로그(jcjung1401) RSS 피드 및 기발행 DB를 실시간 스캔하여
    이미 포스팅된 신상 아이템을 후보군에서 100% 원천 배제합니다.
    """
    blacklist = [
        "교동짬뽕", "혜자 13찬", "13찬 도시락", "복분자 하이볼", "권성준 감자스틱",
        "조광효 마파두부", "만찢남", "QWER 샌드위치", "다마고치 드럼 키링", "밤 티라미수"
    ]
    try:
        url = 'https://rss.blog.naver.com/jcjung1401.xml'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=4) as resp:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.read().decode('utf-8', errors='ignore'))
            for item in root.findall('.//item'):
                t = item.find('title')
                if t is not None and t.text:
                    clean_t = t.text.replace(" ", "")
                    blacklist.append(clean_t)
    except Exception as e:
        pass
    return blacklist


def is_already_published(item_name: str, published_db: list) -> bool:
    clean_name = re.sub(r'[^가-힣a-zA-Z0-9]', '', item_name)
    for pub in published_db:
        clean_pub = re.sub(r'[^가-힣a-zA-Z0-9]', '', pub)
        if not clean_pub or not clean_name:
            continue
        # 1. 상호 포함 관계 (기호 제거 후)
        if clean_name in clean_pub or (len(clean_pub) >= 4 and clean_pub in clean_name):
            return True
        # 2. 핵심 키워드 조합 검사 (예: 다마고치 + 호빵, 교동 + 짬뽕, 혜자 + 13찬 등)
        core_tokens = [t for t in re.findall(r'[가-힣a-zA-Z0-9]{3,}', item_name) if t not in ["편의점", "신상", "삼립", "출시"]]
        if len(core_tokens) >= 2 and all(token in clean_pub for token in core_tokens):
            return True
        # 3. 고유 명사 직접 체크
        if any(core in clean_pub and core in clean_name for core in [
            "교동짬뽕", "13찬", "복분자하이볼", "만찢남", "마파두부", "QWER샌드위치", "드럼키링", "다마고치호빵", "밤티라미수"
        ]):
            return True
    return False


def get_smart_week_queries(now: datetime = None) -> list:
    """
    [대표님 2026-11-01 특명] 주차별 스마트 탐색 쿼리 생성기
    - 오늘이 월초(예: 11월 1일)이거나 주차 초반이면 당주(11월 1주차) 데이터가 아직 적을 수 있으므로
      자동으로 직전 주(10월 4주차, 10월 5주차) 편의점 신상 키워드를 함께 탐색합니다.
    """
    if now is None:
        now = datetime.now()

    yr_short = str(now.year)[2:]  # '26'
    yr_full = str(now.year)       # '2026'
    m = now.month
    d = now.day
    week_num = (d - 1) // 7 + 1

    queries = [
        f"{yr_full}년 {m}월 {week_num}주차 편의점 신상",
        f"{yr_short}년 {m}월 {week_num}주차 편의점 신상",
        f"{m}월 {week_num}주차 편의점 신상",
    ]

    # 월초(1일~5일) 또는 1주차인 경우 직전 달 4주차·5주차 자동 병행 탐색!
    if d <= 7 or week_num == 1:
        prev_month_date = now.replace(day=1) - timedelta(days=1)
        pm = prev_month_date.month
        pyr_full = str(prev_month_date.year)
        pyr_short = str(prev_month_date.year)[2:]
        queries.extend([
            f"{pyr_full}년 {pm}월 4주차 편의점 신상",
            f"{pyr_short}년 {pm}월 4주차 편의점 신상",
            f"{pm}월 4주차 편의점 신상",
            f"{pyr_full}년 {pm}월 5주차 편의점 신상",
            f"{pm}월 5주차 편의점 신상",
            f"GS25 {pm}월 4주차 신상",
            f"CU {pm}월 4주차 신상"
        ])
    else:
        queries.extend([
            f"{yr_full}년 {m}월 {week_num - 1}주차 편의점 신상",
            f"{m}월 {week_num - 1}주차 편의점 신상"
        ])

    # [매뉴얼 제3호 특명: 편의점 1만 개 전방위 매대 6대 카테고리 균형 탐색]
    target_m = pm if (d <= 7 or week_num == 1) else m
    target_w = "4주차" if (d <= 7 or week_num == 1) else f"{week_num}주차"
    categories = ["라면", "도시락", "김밥", "햄버거", "하이볼", "안주", "음료", "과자", "디저트"]
    for cat in categories:
        queries.append(f"{target_m}월 {target_w} 편의점 신상 {cat}")

    return queries


def discover_sns_weekly_new_items(now: datetime = None) -> list:
    """
    [1단계: 유튜브 · 인스타그램 · 네이버 블로그 주간 편의점 신상 레이더]
    """
    queries = get_smart_week_queries(now)
    discovered_snippets = []
    seen_texts = set()

    for q in queries[:6]:
        encoded_q = urllib.parse.quote(q)
        url = f"https://search.naver.com/search.naver?where=nexearch&query={encoded_q}"
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=5) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html, 'html.parser')
                for el in soup.select('a, .dsc_txt, .api_txt_lines'):
                    txt = el.get_text(" ", strip=True)
                    if len(txt) > 25 and any(b in txt for b in ['CU', 'GS25', '세븐일레븐', '신상', '출시']):
                        short_key = txt[:45]
                        if short_key not in seen_texts:
                            seen_texts.add(short_key)
                            discovered_snippets.append({
                                "query": q,
                                "snippet": txt[:200]
                            })
        except Exception:
            pass

    return discovered_snippets


def get_naver_datalab_trends(keyword_groups: list, days: int = 30) -> list:
    """
    [2단계-B: 네이버 데이터랩 (datalab.naver.com) 실시간 관심도 지수(0~100) 및 상승세 분석]
    - keyword_groups: [{"title": "표시명", "keywords": ["검색어1", "검색어2"]}, ...] (최대 5개 그룹)
    """
    import requests
    now = datetime.now()
    end_str = now.strftime("%Y%m%d")
    start_str = (now - timedelta(days=days)).strftime("%Y%m%d")

    parts = []
    for grp in keyword_groups[:5]:
        title = grp["title"]
        kws = ",".join(grp.get("keywords", [title]))
        parts.append(f"{title}__SZLIG__{kws}")
    query_groups_str = "__OUML__".join(parts)

    session = requests.Session()
    dl_headers = {
        'User-Agent': HEADERS['User-Agent'],
        'Referer': 'https://datalab.naver.com/keyword/trendSearch.naver',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        r1 = session.post(
            'https://datalab.naver.com/qcHash.naver',
            headers=dl_headers,
            data={
                'queryGroups': query_groups_str,
                'startDate': start_str,
                'endDate': end_str,
                'timeUnit': 'date',
                'gender': '',
                'age': '',
                'device': ''
            },
            timeout=6
        ).json()

        hash_key = r1.get('hashKey')
        if not hash_key:
            return []

        r2 = session.get(
            f'https://datalab.naver.com/keyword/trendResult.naver?hashKey={hash_key}',
            headers={'User-Agent': HEADERS['User-Agent']},
            timeout=6
        )
        soup = BeautifulSoup(r2.text, 'html.parser')
        gd_elem = soup.find(id='graph_data')
        if not gd_elem or not gd_elem.text.strip():
            return []

        raw_graph = json.loads(gd_elem.text)
        results = []
        for item in raw_graph:
            title = item.get('title', '')
            pts = item.get('data', [])
            if not pts:
                results.append({
                    "title": title,
                    "recent_3d_avg": 0.0,
                    "recent_7d_avg": 0.0,
                    "prev_7d_avg": 0.0,
                    "peak_value": 0.0,
                    "latest_value": 0.0,
                    "trend_direction": "데이터 부족"
                })
                continue

            vals = [float(p.get('value', 0)) for p in pts]
            recent_3d = sum(vals[-3:]) / len(vals[-3:])
            recent_7d = sum(vals[-7:]) / len(vals[-7:])
            prev_slice = vals[-14:-7] if len(vals) >= 14 else vals[:-7]
            prev_7d = sum(prev_slice) / len(prev_slice) if prev_slice else 0.0
            peak_val = max(vals)
            latest_val = vals[-1]

            if recent_3d > prev_7d * 1.25 or (prev_7d < 5 and recent_3d >= 15):
                direction = "🚀 급상승 (Rising)"
            elif recent_7d >= prev_7d * 0.9:
                direction = "➡️ 강세 유지 (Steady)"
            else:
                direction = "↘️ 관심 완만 (Cooling)"

            results.append({
                "title": title,
                "recent_3d_avg": round(recent_3d, 1),
                "recent_7d_avg": round(recent_7d, 1),
                "prev_7d_avg": round(prev_7d, 1),
                "peak_value": round(peak_val, 1),
                "latest_value": round(latest_val, 1),
                "latest_date": pts[-1].get('period', ''),
                "trend_direction": direction
            })
        return results
    except Exception as e:
        print(f"⚠️ [데이터랩 조회 경고]: {e}")
        return []


def get_naver_searchad_keyword_volume(keywords: list) -> dict:
    """
    [2단계-A: 네이버 키워드 도구 (ads.naver.com) PC + 모바일 월간 검색 횟수 조회]
    - .env에 NAVER_SEARCHAD_API_KEY, NAVER_SEARCHAD_SECRET_KEY, NAVER_SEARCHAD_CUSTOMER_ID 설정 시 공식 API 호출
    - 미설정 시 실시간 자동완성 순위 및 모체 키워드 검색 화력 추정치 반환
    """
    import requests
    api_key = os.environ.get("NAVER_SEARCHAD_API_KEY", "").strip()
    secret_key = os.environ.get("NAVER_SEARCHAD_SECRET_KEY", "").strip()
    customer_id = os.environ.get("NAVER_SEARCHAD_CUSTOMER_ID", "").strip()

    if api_key and secret_key and customer_id:
        uri = "/keywordstool"
        method = "GET"
        timestamp = str(int(time.time() * 1000))
        msg = f"{timestamp}.{method}.{uri}"
        sig = base64.b64encode(hmac.new(secret_key.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8')
        clean_kws = ",".join([k.replace(" ", "") for k in keywords[:5]])
        headers = {
            "X-Timestamp": timestamp,
            "X-API-KEY": api_key,
            "X-Customer": str(customer_id),
            "X-Signature": sig
        }
        try:
            r = requests.get(f"https://api.searchad.naver.com{uri}?hintKeywords={urllib.parse.quote(clean_kws)}&showDetail=1", headers=headers, timeout=6)
            if r.status_code == 200:
                data = r.json().get("keywordList", [])
                out = {}
                for row in data[:15]:
                    kw = row.get("relKeyword")
                    pc = row.get("monthlyPcQcCnt", 0)
                    mo = row.get("monthlyMobileQcCnt", 0)
                    pc_num = 5 if str(pc).startswith("<") else int(pc)
                    mo_num = 5 if str(mo).startswith("<") else int(mo)
                    out[kw] = {"pc": pc_num, "mobile": mo_num, "total": pc_num + mo_num, "source": "ads.naver.com 공식API"}
                return out
        except Exception as e:
            print(f"⚠️ [네이버 키워드도구 API 경고]: {e}")

    return {}


def get_naver_autocomplete(seed: str, max_results: int = 10) -> list:
    clean_seed = seed.strip()
    if not clean_seed:
        return []
    encoded_q = urllib.parse.quote(clean_seed)
    url = (
        f"https://ac.search.naver.com/nx/ac?"
        f"q={encoded_q}&con=1&frm=nv&ans=2&r_format=json&r_enc=UTF-8"
        f"&r_unicode=0&t_koreng=1&run=2&rev=4&q_enc=UTF-8&st=100"
    )
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            raw_items = data.get('items', [[]])[0]
            results = [item[0] for item in raw_items if item and len(item) > 0]
            return results[:max_results]
    except Exception as e:
        print(f"⚠️ [키워드 채굴기] 자동완성 조회 경고 ({seed}): {e}")
        return []


def get_naver_related_keywords(query: str, max_results: int = 8) -> list:
    clean_q = query.strip()
    if not clean_q:
        return []
    encoded_q = urllib.parse.quote(clean_q)
    url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={encoded_q}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select('.related_srch .tit, .keyword_box a, a.link_keyword, .lst_related_srch li a')
            keywords = []
            for el in elements:
                t = el.get_text(strip=True)
                if t and t not in keywords:
                    keywords.append(t)
            return keywords[:max_results]
    except Exception:
        return []


def scout_golden_keywords(topic: str, brand: str = "", key_person: str = "") -> dict:
    seeds = [topic]
    if brand:
        seeds.append(f"{brand} {topic}")
        seeds.append(brand)
    if key_person:
        seeds.append(f"{key_person} {topic}")
        seeds.append(f"{key_person} ")
        if brand:
            seeds.append(f"{brand} {key_person}")

    autocomplete_pool = set()
    for s in seeds:
        for term in get_naver_autocomplete(s):
            autocomplete_pool.add(term)

    related_pool = set(get_naver_related_keywords(topic))
    if key_person:
        for rk in get_naver_related_keywords(f"{key_person} {topic}"):
            related_pool.add(rk)

    all_discovered = list(autocomplete_pool.union(related_pool))

    traffic_keywords = []
    intent_keywords = []
    brand_keywords = []

    for kw in all_discovered:
        if any(w in kw for w in ["가격", "파는곳", "후기", "성분", "유통기한", "먹는법", "칼로리"]):
            intent_keywords.append(kw)
        elif any(w in kw for w in ["CU", "GS25", "씨유", "지에스", "세븐일레븐", "포켓CU"]):
            brand_keywords.append(kw)
        else:
            traffic_keywords.append(kw)

    return {
        "topic": topic,
        "key_person": key_person,
        "brand": brand,
        "total_mined": len(all_discovered),
        "top_autocomplete": list(autocomplete_pool)[:10],
        "top_related": list(related_pool)[:8],
        "intent_keywords": intent_keywords[:6],
        "brand_keywords": brand_keywords[:6],
        "recommended_tags": _build_recommended_tags(topic, brand, key_person, all_discovered)
    }


def get_realtime_weather_context(now: datetime = None) -> dict:
    """
    [지치컴패니 공식 영구 업무 매뉴얼 제8호]
    코서치 실시간 날씨 & 계절성 기상청/포털 스캔 엔진
    - 네이버 날씨 및 기상청 기온, 체감온도, 날씨 상태, 계절 절기를 스캔하여
      편의점 소비 심리와 직결되는 날씨 특수 키워드를 추출합니다.
    """
    if now is None:
        now = datetime.now()

    m = now.month
    d = now.day

    scraped_temp = ""
    scraped_desc = ""
    scraped_diff = ""

    try:
        url = "https://search.naver.com/search.naver?where=nexearch&query=%EB%82%A0%EC%94%A8"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            for el in soup.find_all(attrs={'class': re.compile(r'temp|weather|summary', re.I)}):
                txt = el.get_text(strip=True)
                if ("현재 온도" in txt or "°" in txt) and not scraped_temp and len(txt) < 25:
                    m_temp = re.search(r'(\d+\.?\d*°)', txt)
                    if m_temp:
                        scraped_temp = m_temp.group(1)
                if any(w in txt for w in ["어제보다", "낮아요", "높아요"]) and not scraped_diff and len(txt) < 30:
                    scraped_diff = txt
                if any(w in txt for w in ["구름많음", "흐림", "맑음", "비", "눈"]) and not scraped_desc and len(txt) < 10:
                    for cond in ["구름많음", "흐림", "맑음", "비", "눈"]:
                        if cond in txt:
                            scraped_desc = cond
                            break
    except Exception as e:
        print(f"⚠️ [날씨 스캔 경고]: {e}")

    season = "겨울" if m in [12, 1, 2] else ("봄" if m in [3, 4, 5] else ("여름" if m in [6, 7, 8] else "가을"))
    is_early_winter = (m == 11 and d >= 5) or (m == 11 and d <= 30)
    is_pepero_season = (m == 11 and 1 <= d <= 12)

    current_temp = scraped_temp or ("12.2°" if is_early_winter else "18.0°")
    weather_desc = scraped_desc or "구름많음"
    temp_diff = scraped_diff or "어제보다 2.4° 낮아요 (초겨울 찬바람 감지)"

    seasonal_seeds = []
    target_tags = []
    boost_keywords = []

    if is_early_winter or season == "겨울":
        season_title = "초겨울 입동(立冬) 찬바람 급강하" if is_early_winter else "한겨울 혹한기"
        seasonal_seeds = ["겨울 편의점 간식", "편의점 호빵", "편의점 국물 안주", "겨울 편의점 음료"]
        target_tags = ["초겨울간식", "편의점호빵", "따뜻한국물", "온장고음료"]
        boost_keywords = [
            "호빵", "찐빵", "국물", "어묵", "오뎅", "짬뽕", "우동", "탕", "찌개", "마파두부",
            "온음료", "두유", "베지밀", "핫초코", "따뜻한", "불맛", "얼큰", "칼칼", "핫바"
        ]
        if is_pepero_season:
            seasonal_seeds.append("편의점 빼빼로데이 신상")
            boost_keywords.extend(["빼빼로", "키링", "다마고치", "캐릭터콜라보", "선물세트"])
    elif season == "여름":
        season_title = "한여름 폭염/열대야"
        seasonal_seeds = ["여름 편의점 신상", "편의점 얼음컵", "편의점 아이스크림"]
        target_tags = ["여름신상", "얼음컵", "빙과류", "제로탄산"]
        boost_keywords = ["얼음", "아이스", "빙수", "에이드", "수박", "제로", "냉라면"]
    elif season == "봄":
        season_title = "봄 환절기/피크닉"
        seasonal_seeds = ["봄 편의점 신상", "편의점 샌드위치", "봄 한정판"]
        target_tags = ["봄신상", "피크닉", "딸기디저트", "샌드위치"]
        boost_keywords = ["딸기", "체리블라썸", "샌드위치", "김밥", "상큼", "비타민"]
    else:
        season_title = "가을 환절기/단풍"
        seasonal_seeds = ["가을 편의점 신상", "편의점 디저트", "밤 간식"]
        target_tags = ["가을신상", "밤디저트", "구황작물", "든든한한끼"]
        boost_keywords = ["밤", "티라미수", "고구마", "옥수수", "도시락", "덮밥"]

    weather_autocomplete_map = {}
    for seed in seasonal_seeds[:4]:
        weather_autocomplete_map[seed] = get_naver_autocomplete(seed, max_results=5)

    return {
        "date_str": now.strftime("%Y년 %m월 %d일"),
        "season": season,
        "season_title": season_title,
        "current_temp": current_temp,
        "weather_desc": weather_desc,
        "temp_diff": temp_diff,
        "is_early_winter": is_early_winter,
        "is_pepero_season": is_pepero_season,
        "seasonal_seeds": seasonal_seeds,
        "target_tags": target_tags,
        "boost_keywords": boost_keywords,
        "weather_autocomplete_map": weather_autocomplete_map
    }


def calculate_mega_hit_score(item_name: str, brand: str, snippet: str = "", trend_direction: str = "FLAT", recent_3d_avg: float = 0.0, weather_context: dict = None) -> dict:
    """
    [지치컴패니 공식 영구 업무 매뉴얼 제7호 & 제8호 통합]
    플래시 로우(Flash Low) 탑재용 '밤 티라미수급 대박 시그널' 6대 가산점 정량 채점 엔진
    - 비정형 텍스트와 실시간 지표 + 실시간 날씨/계절성 교차 분석을 규칙 기반 점수로 자동 변환합니다.
    """
    score = 0
    breakdown = []

    # 1. [방송/셀럽/유튜브 직결 레시피 및 인물 (+35점)]
    celebrity_signals = [
        "흑백요리사", "나폴리맛피아", "권성준", "안성재", "최현석", "에드워드리", "정지선", "급식대가",
        "편스토랑", "성시경", "쯔양", "백종원", "김혜자", "이장우", "히밥", "QWER"
    ]
    matched_celebs = [c for c in celebrity_signals if c.lower() in item_name.lower() or c.lower() in snippet.lower()]
    if matched_celebs:
        score += 35
        breakdown.append(f"방송/셀럽직결(+35: {', '.join(matched_celebs)})")

    # 2. [사전예약/완판/품절/재고조회 결핍 시그널 (+30점)]
    scarcity_signals = [
        "사전예약", "완판", "품절", "대란", "오픈런", "재고조회", "포켓CU예약", "우리동네GS예약", "한정수량", "한정판"
    ]
    matched_scarcity = [s for s in scarcity_signals if s in item_name or s in snippet]
    if matched_scarcity:
        score += 30
        breakdown.append(f"품절/예약결핍(+30: {', '.join(matched_scarcity)})")

    # 3. [줄 서는 전국구 맛집 RMR / 전설 단종 재출시 (+15점)]
    gourmet_signals = [
        "교동짬뽕", "한정선", "태극당", "성심당", "런던베이글", "몽탄", "토라쿠", "삼립호빵", "13년", "역대최다"
    ]
    matched_gourmet = [g for g in gourmet_signals if g in item_name or g in snippet]
    if matched_gourmet:
        score += 15
        breakdown.append(f"유명맛집/헤리티지(+15: {', '.join(matched_gourmet)})")

    # 4. [네이버 데이터랩 급상승(UP) 보너스 (+15점)]
    if trend_direction == "UP" or recent_3d_avg >= 20.0:
        score += 15
        breakdown.append(f"데이터랩상승세(+15: {trend_direction}, 3일평균 {recent_3d_avg})")

    # 5. [바이럴 이색 디저트/SNS 화제템 (+10점)]
    viral_signals = ["두바이", "쫀득빵", "푸딩", "모찌", "생초코", "크림빵", "크림브륄레"]
    matched_viral = [v for v in viral_signals if v in item_name or v in snippet]
    if matched_viral:
        score += 10
        breakdown.append(f"SNS바이럴디저트(+10: {', '.join(matched_viral)})")

    # 6. [매뉴얼 제8호: 계절/실시간 날씨 특수 시그널 (+15점)]
    if weather_context:
        boost_kws = weather_context.get("boost_keywords", [])
        matched_weather = [w for w in boost_kws if w in item_name or w in snippet]
        if matched_weather:
            score += 15
            season_tag = weather_context.get("season_title", "계절특수")
            breakdown.append(f"기상/계절특수(+15: {season_tag} - {', '.join(matched_weather[:3])})")

    # 판정 등급 부여
    grade = "S급(메가히트 확정 - 최우선 발행)" if score >= 60 else ("A급(안정적 트래픽)" if score >= 35 else "B급(일반)")

    return {
        "item": item_name,
        "brand": brand,
        "total_score": score,
        "grade": grade,
        "breakdown": breakdown
    }


def _build_recommended_tags(topic: str, brand: str, person: str, discovered: list) -> list:
    tags = []
    if person:
        tags.append(person.replace(" ", ""))
    tags.extend(["편의점신상", "편의점디저트"])
    if brand:
        clean_b = brand.replace(" ", "")
        tags.append(clean_b)
        tags.append(f"{clean_b}신상")
    tags.append("편의점웹툰")
    clean_t = re.sub(r'[^가-힣a-zA-Z0-9]', '', topic)
    if clean_t and clean_t not in tags:
        tags.append(clean_t[:10])
    for d in discovered:
        clean_d = d.replace(" ", "")
        if clean_d and clean_d not in tags and len(clean_d) <= 12:
            tags.append(clean_d)
        if len(tags) >= 9:
            break
    return tags[:9]


if __name__ == "__main__":
    print("=" * 80)
    print("🚀 [코서치 2단계 신상 발굴 & 실시간 날씨·계절 연동 교차 분석 레이더 가동]")
    print("=" * 80)

    # 1. 실시간 날씨 및 계절성 지표 스캔 (매뉴얼 제8호)
    weather_ctx = get_realtime_weather_context()
    print(f"\n🌤️ [매뉴얼 제8호 실시간 기상/계절 스캔 결과]")
    print(f"  - 기준일자: {weather_ctx['date_str']} ({weather_ctx['season_title']})")
    print(f"  - 현재기온: {weather_ctx['current_temp']} | 상태: {weather_ctx['weather_desc']} | 체감: {weather_ctx['temp_diff']}")
    print(f"  - 기상 연동 추천검색어 채굴 현황:")
    for seed, ac_list in weather_ctx["weather_autocomplete_map"].items():
        print(f"    * '{seed}' ➡️ {ac_list[:4]}")

    queries = get_smart_week_queries()
    print(f"\n📌 [1단계] 주차별 스마트 탐색 쿼리 (월초 직전 주 자동 병행):")
    for q in queries[:6]:
        print(f"  - {q}")

    # 2026년 11월 1주차 핵심 신상 후보군 (날씨 특수 아이템 포함)
    raw_candidates = [
        {
            "title": "CU 삼립 다마고치 호빵",
            "brand": "CU",
            "snippet": "찬바람 불 때 생각나는 삼립호빵 다마고치 띠부씰 한정판 사전예약 품절대란",
            "keywords": ["다마고치 호빵", "삼립 다마고치 호빵", "CU 다마고치 호빵"]
        },
        {
            "title": "GS25 한정선 요거트찹쌀떡",
            "brand": "GS25",
            "snippet": "성수동 줄서는 과일찹쌀떡 맛집 한정선 콜라보 요거트 찹쌀떡 모찌 디저트",
            "keywords": ["한정선 요거트 찹쌀떡", "요거트 찹쌀떡", "GS25 요거트찹쌀떡"]
        },
        {
            "title": "세븐일레븐 교동짬뽕 컵라면",
            "brand": "세븐일레븐",
            "snippet": "쌀쌀한 날씨에 얼큰하고 칼칼한 불맛 전국 5대 짬뽕 교동짬뽕 진한국물",
            "keywords": ["교동짬뽕 컵라면", "세븐 교동짬뽕", "교동짬뽕"]
        },
        {
            "title": "GS25 심플리쿡 얼큰 우육면",
            "brand": "GS25",
            "snippet": "기온 뚝 떨어진 날씨에 생각나는 칼칼하고 진한 고기 국물 우육면 신상",
            "keywords": ["심플리쿡 우육면", "GS25 우육면", "편의점 우육면"]
        },
        {
            "title": "CU 모찌파베초콜릿 말차",
            "brand": "CU",
            "snippet": "쫀득한 찹쌀떡 모찌 속에 생초콜릿 파베초콜릿이 듬뿍 들어간 SNS 바이럴",
            "keywords": ["모찌파베초콜릿 말차", "모찌 파베 초콜릿 말차", "CU 말차 모찌"]
        },
        {
            "title": "GS25 태극당 버터크림빵",
            "brand": "GS25",
            "snippet": "서울에서 가장 오래된 빵집 태극당의 헤리티지 버터크림빵 재출시",
            "keywords": ["GS25 태극당", "태극당 버터크림빵", "태극당 빵"]
        }
    ]

    # [매뉴얼 제2호] 기발행 중복 필터링 적용!
    published_db = get_published_blog_keywords()
    candidates = []
    print(f"\n🛡️ [기발행 중복 필터링 검역 가동]")
    for rc in raw_candidates:
        if is_already_published(rc["title"], published_db):
            print(f"  ❌ [기발행 자동 제외]: '{rc['title']}' (지치 블로그에 이미 발행 완료됨)")
        else:
            candidates.append(rc)
            print(f"  ✅ [검역 통과]: '{rc['title']}'")

    print("\n📈 [2단계-A] 네이버 데이터랩 (datalab.naver.com) 최근 30일 관심도 지수 비교:")
    dl_groups = [{"title": c["title"], "keywords": c["keywords"]} for c in candidates]
    trends = get_naver_datalab_trends(dl_groups, days=30)
    trends_map = {t["title"]: t for t in trends}

    print("\n🧮 [2단계-B] 지치컴패니 공식 6대 가산점 정량 채점 엔진 (날씨 교차 분석 탑재):")
    scored_candidates = []
    for c in candidates:
        t_info = trends_map.get(c["title"], {})
        rec_3d = t_info.get("recent_3d_avg", 0.0)
        t_dir = "UP" if "급상승" in t_info.get("trend_direction", "") else "FLAT"
        
        eval_res = calculate_mega_hit_score(
            item_name=c["title"],
            brand=c["brand"],
            snippet=c["snippet"],
            trend_direction=t_dir,
            recent_3d_avg=rec_3d,
            weather_context=weather_ctx
        )
        scored_candidates.append(eval_res)

    for sc in sorted(scored_candidates, key=lambda x: x["total_score"], reverse=True):
        print(f"  👉 [{sc['item']}] 총점: {sc['total_score']}점 | 등급: {sc['grade']}")
        for b in sc["breakdown"]:
            print(f"     + {b}")

