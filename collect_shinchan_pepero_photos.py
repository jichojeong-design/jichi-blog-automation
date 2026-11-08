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

output_dir = os.path.abspath("02_코서치_자료/gs25_shinchan_pepero")
os.makedirs(output_dir, exist_ok=True)

targets = [
    {
        "file": "upload_1_poster.jpg",
        "query": "GS25 짱구 빼빼로 포스터 짱구는못말려 필름카메라",
        "fallback_query": "GS25 짱구 빼빼로데이 포스터"
    },
    {
        "file": "upload_2_store.jpg",
        "query": "GS25 편의점 매장 외관 정면 간판 야경",
        "fallback_query": "GS25 편의점 외관"
    },
    {
        "file": "upload_3_shelf.jpg",
        "query": "GS25 편의점 빼빼로데이 매대 진열 짱구",
        "fallback_query": "편의점 빼빼로데이 매대 진열"
    },
    {
        "file": "upload_4_package.jpg",
        "query": "GS25 짱구 필름카메라 빼빼로 세트 패키지 상자",
        "fallback_query": "짱구 빼빼로 기획세트 상자"
    },
    {
        "file": "upload_5_unboxing.jpg",
        "query": "GS25 짱구 빼빼로 필름카메라 언박싱 개봉",
        "fallback_query": "짱구 필름카메라 실물 언박싱"
    },
    {
        "file": "upload_6_camera_detail.jpg",
        "query": "짱구 필름카메라 실물 디테일 접사 토이카메라",
        "fallback_query": "짱구는못말려 토이 필름카메라"
    },
    {
        "file": "upload_7_pairing.jpg",
        "query": "빼빼로 아메리카노 커피 꿀조합 디저트",
        "fallback_query": "빼빼로 우유 디저트 페어링"
    },
    {
        "file": "upload_8_finish.jpg",
        "query": "빼빼로 다먹음 빈상자 완식 짱구",
        "fallback_query": "필름카메라 사진 찰칵 완식"
    }
]

print("=" * 70)
print("🚀 [코서치] GS25 짱구 빼빼로 기획 세트 8컷 실사 참조 이미지 팩 수집 개시!")
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
