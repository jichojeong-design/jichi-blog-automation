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
    print("=" * 75)
    print("🚀 [코서치 2단계 신상 발굴 & 네이버 데이터랩 실시간 검증 레이더 가동]")
    print("=" * 75)

    queries = get_smart_week_queries()
    print(f"\n📌 [1단계] 주차별 스마트 탐색 쿼리 (월초 직전 주 자동 병행):")
    for q in queries[:6]:
        print(f"  - {q}")

    # 2026년 10월 4주차 ~ 11월 1주차 발굴 핵심 미발행 신상 후보 5종 데이터랩 비교 (순수 신상 제품명 대결)
    candidates = [
        {"title": "GS25 한정선 요거트찹쌀떡", "keywords": ["한정선 요거트 찹쌀떡", "요거트 찹쌀떡", "GS25 요거트찹쌀떡"]},
        {"title": "CU 모찌파베초콜릿 말차", "keywords": ["모찌파베초콜릿 말차", "모찌 파베 초콜릿 말차", "CU 말차 모찌"]},
        {"title": "CU 삼립 다마고치 호빵", "keywords": ["다마고치 호빵", "삼립 다마고치 호빵", "CU 다마고치 호빵"]},
        {"title": "세븐 토라쿠 크림브륄레푸딩", "keywords": ["토라쿠 푸딩", "토라쿠 크림브륄레", "크림브륄레 푸딩"]},
        {"title": "GS25 태극당 버터크림빵", "keywords": ["GS25 태극당", "태극당 버터크림빵", "태극당 빵"]}
    ]

    print("\n📈 [2단계] 네이버 데이터랩 (datalab.naver.com) 최근 30일 관심도 지수(0~100) 비교:")
    trends = get_naver_datalab_trends(candidates, days=30)
    for t in sorted(trends, key=lambda x: x["recent_3d_avg"], reverse=True):
        print(
            f"  👉 [{t['title']}] 최근3일평균: {t['recent_3d_avg']} | 최근7일평균: {t['recent_7d_avg']} "
            f"| 최고점: {t['peak_value']} | 최신({t.get('latest_date','')}): {t['latest_value']} | 추세: {t['trend_direction']}"
        )
