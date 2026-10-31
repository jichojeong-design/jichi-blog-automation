import urllib.request
import urllib.parse
import json
import re
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def get_naver_autocomplete(seed: str, max_results: int = 10) -> list:
    """
    네이버 실시간 검색어 자동완성(Autocomplete) API를 호출하여
    대중이 모바일/PC에서 실제로 가장 많이 타이핑하고 있는 연관 검색어를 채굴합니다.
    """
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
    """
    네이버 통합검색 결과 페이지에서 네이버 알고리즘이 공식 추천하는 '연관 검색어'를 추출합니다.
    """
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
            
            # 네이버 모바일/PC 통합검색 연관검색어 셀렉터
            elements = soup.select('.related_srch .tit, .keyword_box a, a.link_keyword, .lst_related_srch li a')
            keywords = []
            for el in elements:
                t = el.get_text(strip=True)
                if t and t not in keywords:
                    keywords.append(t)
            return keywords[:max_results]
    except Exception as e:
        print(f"⚠️ [키워드 채굴기] 연관검색어 추출 경고 ({query}): {e}")
        return []


def scout_golden_keywords(topic: str, brand: str = "", key_person: str = "") -> dict:
    """
    [지치 컴퍼니 영업사원 코서치 전용 황금 키워드 레이더]
    - 주제어, 브랜드, 화제 인물(셰프/아이돌 등)을 기반으로 실시간 대중 유입 키워드를 다각도 채굴합니다.
    - 권성준(55.87%) 사례처럼 '실명/본명'과 '대중적 호기심(가격/파는곳/성분)'을 결합합니다.
    """
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

    # 카테고리별 분류
    traffic_keywords = []   # 본명+제품명 고유 조합 (검색량 독점용)
    intent_keywords = []    # 가격, 파는곳, 후기 등 전환 키워드
    brand_keywords = []     # 편의점/브랜드 키워드

    for kw in all_discovered:
        if any(w in kw for w in ["가격", "파는곳", "후기", "성분", "유통기한", "먹는법", "칼로리"]):
            intent_keywords.append(kw)
        elif any(w in kw for w in ["CU", "GS25", "씨유", "지에스", "세븐일레븐", "포켓CU"]):
            brand_keywords.append(kw)
        else:
            traffic_keywords.append(kw)

    report = {
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

    return report


def _build_recommended_tags(topic: str, brand: str, person: str, discovered: list) -> list:
    """3·3·3 황금 태그 공식 기반 태그 자동 산출"""
    tags = []
    
    # 1. 인물/화제 3개
    if person:
        tags.append(person.replace(" ", ""))
    tags.extend(["편의점신상", "편의점디저트"])
    
    # 2. 브랜드 3개
    if brand:
        clean_b = brand.replace(" ", "")
        tags.append(clean_b)
        tags.append(f"{clean_b}신상")
    tags.append("편의점웹툰")
    
    # 3. 제품/핵심키워드 3개
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
    import sys
    if sys.platform.startswith('win'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    print("🔍 [코서치 황금 키워드 채굴기 테스트]")
    res = scout_golden_keywords("감자스틱", brand="CU", key_person="권성준")
    print(f"발굴된 총 키워드: {res['total_mined']}개")
    print("실시간 자동완성 TOP:", res["top_autocomplete"])
    print("추천 3·3·3 태그:", res["recommended_tags"])
