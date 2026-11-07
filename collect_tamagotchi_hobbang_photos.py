import os
import sys
import time
import urllib.parse
from playwright.sync_api import sync_playwright

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

output_dir = os.path.abspath("02_코서치_자료/cu_tamagotchi_hobbang")
os.makedirs(output_dir, exist_ok=True)

targets = [
    {
        "file": "upload_1_poster.jpg",
        "query": "삼립 다마고치 호빵 포스터 출시 고기부추 칠리도그",
        "fallback_query": "다마고치 호빵 신상 삼립"
    },
    {
        "file": "upload_2_store.jpg",
        "query": "CU 편의점 외관 간판 야경 매장",
        "fallback_query": "CU 편의점 매장 외관 정면"
    },
    {
        "file": "upload_3_steamer.jpg",
        "query": "편의점 호빵 찜기 기계 진열",
        "fallback_query": "CU 호빵 찜기 매대"
    },
    {
        "file": "upload_4_package.jpg",
        "query": "다마고치 호빵 구치파치 고기부추 마메치 칠리도그 봉지",
        "fallback_query": "다마고치 호빵 포장 패키지"
    },
    {
        "file": "upload_5_unboxing.jpg",
        "query": "삼립 호빵 찜기 전자레인지 따끈따끈 김",
        "fallback_query": "편의점 호빵 개봉 실물"
    },
    {
        "file": "upload_6_cross_sticker.jpg",
        "query": "다마고치 호빵 단면 띠부씰 스티커",
        "fallback_query": "다마고치 띠부씰 호빵 반갈"
    },
    {
        "file": "upload_7_pairing.jpg",
        "query": "호빵 베지밀 두유 편의점 꿀조합",
        "fallback_query": "호빵 따뜻한 우유 온음료"
    },
    {
        "file": "upload_8_finish.jpg",
        "query": "호빵 다먹음 완식 편의점",
        "fallback_query": "다마고치 띠부씰 모음 완성"
    }
]

print("=" * 70)
print("🚀 [코서치] CU 삼립 다마고치 호빵 8컷 실사 참조 이미지 팩 수집 개시!")
print("=" * 70)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        viewport={"width": 1400, "height": 900}
    )

    for idx, t in enumerate(targets):
        out_file = os.path.join(output_dir, t["file"])
        query = t["query"]
        print(f"\n📸 [{idx+1}/8] 탐색 중: '{query}' ➡️ {t['file']}")

        saved = False
        for q in [query, t["fallback_query"]]:
            encoded_q = urllib.parse.quote(q)
            search_url = f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={encoded_q}"
            try:
                page.goto(search_url, wait_until="networkidle", timeout=10000)
                time.sleep(1.5)
                imgs = page.locator("img._fe_image_tab_content_thumbnail_image, .thumb img")
                count = imgs.count()
                for i in range(min(count, 10)):
                    elem = imgs.nth(i)
                    box = elem.bounding_box()
                    if box and box['width'] > 120 and box['height'] > 100:
                        elem.screenshot(path=out_file)
                        if os.path.exists(out_file) and os.path.getsize(out_file) > 10000:
                            print(f"  ✅ [수집 완료] {t['file']} ({int(box['width'])}x{int(box['height'])}, {os.path.getsize(out_file)//1024} KB)")
                            saved = True
                            break
                if saved:
                    break
            except Exception as e:
                print(f"  ⚠️ 탐색 오류 ({q}): {e}")

        if not saved:
            print(f"  ⚠️ [네이버 미발견] 구글 검색 시도: {t['file']}")
            try:
                g_url = f"https://www.google.com/search?tbm=isch&q={urllib.parse.quote(t['fallback_query'])}"
                page.goto(g_url, wait_until="networkidle", timeout=10000)
                time.sleep(1.5)
                g_imgs = page.locator("img")
                for i in range(min(g_imgs.count(), 12)):
                    elem = g_imgs.nth(i)
                    box = elem.bounding_box()
                    if box and box['width'] > 120 and box['height'] > 100:
                        elem.screenshot(path=out_file)
                        if os.path.exists(out_file) and os.path.getsize(out_file) > 10000:
                            print(f"  ✅ [구글 수집 성공] {t['file']} ({os.path.getsize(out_file)//1024} KB)")
                            saved = True
                            break
            except Exception as ge:
                print(f"  ⚠️ 구글 탐색 오류: {ge}")

    browser.close()

print("\n" + "=" * 70)
print(f"🎉 8컷 실사 참조 이미지 패키지 수집 완료: {output_dir}")
print("=" * 70)
