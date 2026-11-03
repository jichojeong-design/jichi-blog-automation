import os
import sys
import time
import urllib.parse
from PIL import Image

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from playwright.sync_api import sync_playwright

def crop_center_pure_product(image_path: str, output_path: str = None) -> str:
    """
    [사장님 2026-10-24 특명] 포장사진 및 제품 속 사진 상·하단 텍스트/광고 제거 및 정중앙 알맹이 정밀 크롭
    - 상단 18% (로고, 채널명, '저장' 버튼 등) 제거
    - 하단 22% (자극적인 홍보 문구, 자막, 태그 등) 제거
    - 순수한 정중앙 제품 실물 영역(중앙 60%)만 깨끗하게 남겨 코자이너에게 전달
    """
    if not image_path or not os.path.exists(image_path):
        return image_path
    try:
        out = output_path or image_path
        with Image.open(image_path) as im:
            w, h = im.size
            top_cut = int(h * 0.18)
            bottom_cut = int(h * 0.78)
            # 좌우도 불필요한 마진이 있으면 미세 정돈 (좌우 4%씩 정돈)
            left_cut = int(w * 0.04)
            right_cut = int(w * 0.96)
            
            cropped = im.crop((left_cut, top_cut, right_cut, bottom_cut))
            cropped.save(out)
            print(f"  ✂️ [코서치 텍스트 제거 정밀 크롭 완료] {os.path.basename(out)} (상·하단 자막 제거 후 순수 제품 알맹이 추출: {cropped.size[0]}x{cropped.size[1]})")
            return out
    except Exception as e:
        print(f"  ⚠️ 정밀 크롭 중 예외: {e}")
        return image_path

def scout_product_3cuts(keyword, output_dir="02_코서치_자료"):
    """
    [코서치 전담 도구: 사장님 공인 시각 판별 3컷 정밀 크롭 엔진]
    사장님 절대 지침: 코자이너에게 반드시 아래 3장의 핵심 컷을 분리하여 전달할 것!
      1. target_1_package.png : 제품 포장 외형 (정면 디자인, 패키지 컬러)
      2. target_2_cross_section.png : 제품 실물 단면 (속 크림/필링/떡피 두께) ⚠️ 포장지/박스 절대 금지!
      3. target_3_store_shelf.png : 편의점 매대 진열 및 가격표가 찍힌 현장 사진
    """
    os.makedirs(output_dir, exist_ok=True)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, output_dir)

    print("\n" + "=" * 65)
    print(f"🔎 [코서치 출격] '{keyword}' 3대 핵심 실사 시각 판별 수집 가동!")
    print("=================================================================")

    tasks = [
        {"type": "1_package", "query": f"{keyword} 패키지 봉지 포장", "desc": "1. 제품 포장 외형"},
        {"type": "2_cross_section", "query": f"{keyword} 단면 크림 필링 반갈", "desc": "2. 진짜 실물 단면"},
        {"type": "3_store_shelf", "query": f"{keyword} 편의점 매대 가격표 냉장", "desc": "3. 편의점 매대 / 가격표"}
    ]

    captured_results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # 사장님 모니터 비율의 시원한 1600x1000 브라우저 뷰포트
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1600, "height": 1000}
        )

        for idx, task in enumerate(tasks):
            q = task["query"]
            ttype = task["type"]
            tdesc = task["desc"]

            print(f"\n📸 [{idx+1}/3] {tdesc} 탐색 및 캡처 중... (검색어: '{q}')")
            encoded_q = urllib.parse.quote(q)
            # 네이버 고화질 뷰어 탭 활용
            search_url = f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={encoded_q}"
            page.goto(search_url, wait_until="networkidle")
            time.sleep(2)

            # 1단계: 풀스크린 샷 도구 가동 (전체 상황 기록)
            full_screenshot_path = os.path.join(target_dir, f"fullscreen_{ttype}.png")
            page.screenshot(path=full_screenshot_path)
            print(f"  - 🖥️ [풀스크린 샷 완료]: fullscreen_{ttype}.png")

            # 2단계: 스마트 크롭 도구 가동 (가장 선명한 1위 타겟 단독 크롭)
            crop_out_path = os.path.join(target_dir, f"target_{ttype}.png")
            imgs = page.locator("img._fe_image_tab_content_thumbnail_image, .thumb img")
            count = imgs.count()

            cropped = False
            for i in range(min(count, 6)):
                try:
                    img_elem = imgs.nth(i)
                    box = img_elem.bounding_box()
                    # 유효한 크기의 메인 사진 포착
                    if box and box['width'] > 160 and box['height'] > 130:
                        # 오려내기(Crop) 스크린샷 실행
                        img_elem.screenshot(path=crop_out_path)
                        sz_kb = os.path.getsize(crop_out_path) // 1024
                        if sz_kb >= 15:
                            print(f"  - ✂️ [스마트 크롭 완료]: target_{ttype}.png ({int(box['width'])}x{int(box['height'])}, {sz_kb} KB)")
                            # [사장님 특명] 1번(포장)과 2번(단면)은 상하단 텍스트 및 광고 자막 완전 제거 정밀 정돈 실행
                            if ttype in ["1_package", "2_cross_section"]:
                                crop_center_pure_product(crop_out_path)
                            captured_results[ttype] = crop_out_path
                            cropped = True
                            break
                except Exception:
                    pass

            if not cropped and count > 0:
                # 폴백 첫 번째 이미지 크롭
                imgs.first.screenshot(path=crop_out_path)
                captured_results[ttype] = crop_out_path
                print(f"  - ✂️ [기본 크롭]: target_{ttype}.png")

        browser.close()

    print("\n" + "=" * 65)
    print("🎉 [코서치 미션 완수] 코자이너에게 전달할 필수 3대 핵심 컷 패키지 준비 완료!")
    for k, v in captured_results.items():
        print(f"  👉 {k}: {os.path.basename(v)}")
    print("=" * 65)
    return captured_results

def scout_8cuts_reference_images(product_name: str, brand: str, pairing_item: str = "", output_dir: str = "02_코서치_자료") -> dict:
    """
    [지치컴패니 공식 영구 업무 매뉴얼 제4호 개정]
    코서치 1~8컷 영문 프롬프트 맞춤형 실사 참조 이미지 매칭 및 자동 수집 엔진
    - [대표님 특별 엄명 2026-11-03]
      1. 동일 사진 중복 수집(기계적 긁어오기) 절대 엄금 (SHA256 해시 검사 탑재)
      2. 크로스오버 웹툰의 경우 7대 핵심 요소(브랜드A 포스터, 외관, 매대 / 브랜드B 패키지, 매대, 조리 / 브랜드A 오픈 실물) 분할 수집!
    """
    import hashlib
    import urllib.request

    os.makedirs(output_dir, exist_ok=True)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, output_dir)

    print("\n" + "=" * 70)
    print(f"📸 [코서치 매뉴얼 제4호 가동] '{product_name}' 맞춤형 실사 수집!")
    print("=" * 70)

    # 크로스오버 상황(pairing_item 존재)일 경우 대표님 황금 7대 요소 팩 발동
    if pairing_item:
        print(f"  🤝 [크로스오버 모드 감지]: {brand} {product_name} X {pairing_item}")
        cut_tasks = [
            {"cut": 1, "key": "upload_1_poster", "query": f"{product_name} 공식 포스터 카드뉴스", "desc": "1번: 제품A 공식 포스터/카드뉴스"},
            {"cut": 2, "key": "upload_2_shelf_a", "query": f"{brand} {product_name} 도시락 매대 진열", "desc": "2번: 브랜드A 매대 진열 실사"},
            {"cut": 3, "key": "upload_3_store_a", "query": f"{brand} 편의점 정면 외관 매장", "desc": "3번: 브랜드A 매장 외관 실사"},
            {"cut": 4, "key": "upload_4_pkg_b", "query": f"{pairing_item} 컵라면 패키지 정면", "desc": "4번: 제품B 패키지 단독 정면"},
            {"cut": 5, "key": "upload_5_shelf_b", "query": f"세븐일레븐 라면 매대 진열 PB라면", "desc": "5번: 브랜드B 라면 매대 진열 실사"},
            {"cut": 6, "key": "upload_6_cook_b", "query": f"{pairing_item} 조리 면발 젓가락 후기", "desc": "6번: 제품B 조리/면발 실사"},
            {"cut": 7, "key": "upload_7_open_a", "query": f"{product_name} 뚜껑 개봉 반찬 흑미밥 실물", "desc": "7번: 제품A 오픈/내용물 전체 실사"}
        ]
    else:
        cut_tasks = [
            {"cut": 1, "key": "cut_1_news", "query": f"{product_name} 공식 포스터 기사", "desc": "1컷: 스마트폰 뉴스 / 출시 포스터"},
            {"cut": 2, "key": "cut_2_store", "query": f"{brand} 편의점 매장 외관 간판", "desc": "2컷: 편의점 매장 외관 출동"},
            {"cut": 3, "key": "cut_3_shelf", "query": f"{brand} {product_name} 매대 진열", "desc": "3컷: 편의점 매대 진열 발견"},
            {"cut": 4, "key": "cut_4_package", "query": f"{product_name} 패키지 포장 정면", "desc": "4컷: 제품 정면 패키지 실물"},
            {"cut": 5, "key": "cut_5_open", "query": f"{product_name} 개봉 실물 내용물", "desc": "5컷: 개봉/조리 김모락 실사"},
            {"cut": 6, "key": "cut_6_detail", "query": f"{product_name} 단면 근접 속 실사", "desc": "6컷: 디테일 단면/식감 클로즈업"},
            {"cut": 7, "key": "cut_7_pairing", "query": f"{product_name} 꿀조합 페어링", "desc": "7컷: 페어링/먹조합 실사"},
            {"cut": 8, "key": "cut_8_finish", "query": f"{product_name} 완식 빈그릇 후기", "desc": "8컷: 완식 엔딩 / 깔끔한 마무리"}
        ]

    captured_cuts = {}
    seen_hashes = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1600, "height": 1000}
        )

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

        for t in cut_tasks:
            cut_num = t["cut"]
            cut_key = t["key"]
            q = t["query"]
            desc = t["desc"]
            out_file = os.path.join(target_dir, f"{cut_key}.jpg")

            print(f"  🔍 [{cut_num}번] {desc} (검색어: '{q}')")
            encoded_q = urllib.parse.quote(q)
            search_url = f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={encoded_q}"
            
            success = False
            try:
                page.goto(search_url, wait_until="networkidle", timeout=8000)
                time.sleep(1)
                imgs = page.locator("img._fe_image_tab_content_thumbnail_image, .thumb img")
                count = imgs.count()

                # 상위 15개 썸네일을 훑으며 중복되지 않는 고유한 이미지 선별
                for idx in range(min(count, 15)):
                    src = imgs.nth(idx).get_attribute("src")
                    if not src:
                        continue
                    parsed = urllib.parse.urlparse(src)
                    qs = urllib.parse.parse_qs(parsed.query)
                    orig_url = qs['src'][0] if 'src' in qs else src

                    try:
                        req = urllib.request.Request(orig_url, headers=headers)
                        with urllib.request.urlopen(req, timeout=5) as resp:
                            data = resp.read()
                            # 15KB 이상 유효 이미지 & 중복 해시 회피 검증
                            if len(data) >= 15000:
                                h = hashlib.sha256(data).hexdigest()
                                if h not in seen_hashes:
                                    seen_hashes.add(h)
                                    with open(out_file, 'wb') as f:
                                        f.write(data)
                                    captured_cuts[cut_num] = {
                                        "key": cut_key,
                                        "desc": desc,
                                        "path": out_file,
                                        "exists": True
                                    }
                                    print(f"    ✅ [{cut_num}번 고유 실사 매칭 완료]: {os.path.basename(out_file)} ({len(data)//1024} KB)")
                                    success = True
                                    break
                    except Exception:
                        pass

                # 폴백: 스크린샷 크롭
                if not success and count > 0:
                    imgs.first.screenshot(path=out_file)
                    captured_cuts[cut_num] = {
                        "key": cut_key,
                        "desc": desc,
                        "path": out_file,
                        "exists": True
                    }
                    print(f"    ✂️ [{cut_num}번 스크린샷 폴백 완료]: {os.path.basename(out_file)}")

            except Exception as e:
                print(f"    ⚠️ [{cut_num}번 검색 오류]: {e}")

        browser.close()

    print("=" * 70)
    print(f"🎉 [코서치 매칭 완료] 총 {len(captured_cuts)}개 고유 실사 이미지 팩 준비 완료!")
    print("=" * 70 + "\n")
    return captured_cuts


if __name__ == "__main__":
    test_kw = sys.argv[1] if len(sys.argv) > 1 else "후와후와 딥초코 쫀득빵"
    scout_product_3cuts(test_kw)
