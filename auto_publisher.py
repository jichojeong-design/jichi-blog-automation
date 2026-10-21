import os
import re
import time
from playwright.sync_api import sync_playwright


def _upload_single_image(page, img_path: str) -> bool:
    """
    네이버 스마트에디터 ONE의 상단 [사진] 툴바 버튼을 실제 마우스 이벤트(Playwright native click)로 클릭하고,
    File Chooser를 가로채 이미지를 업로드한 뒤 에디터 내 이미지 렌더링까지 검증합니다.
    """
    if not img_path or not os.path.exists(img_path):
        print(f"  ⚠️ 이미지 파일이 존재하지 않습니다: {img_path}")
        return False

    abs_img = os.path.abspath(img_path)
    print(f"  🖼️ 이미지 업로드 시작: {os.path.basename(abs_img)} ({os.path.getsize(abs_img) // 1024} KB)")

    before_count = page.locator(".se-component.se-image, img.se-image-resource").count()
    uploaded = False

    # 1차 시도: Playwright native click + expect_file_chooser
    try:
        img_btn = page.locator(
            "button.se-image-toolbar-button, "
            "button[data-name='image'], "
            ".se-toolbar-item-image button"
        ).first
        with page.expect_file_chooser(timeout=10000) as fc_info:
            img_btn.click(timeout=5000)
        file_chooser = fc_info.value
        file_chooser.set_files(abs_img)
        uploaded = True
        print("  ✅ File Chooser 인터셉트 파일 주입 성공! 네이버 이미지 서버 업로드 대기 중...")
    except Exception as fc_err:
        print(f"  ⚠️ File Chooser 1차 예외 ({fc_err}), input[type='file'] 직접 탐색 시도...")
        try:
            file_input = page.locator("input[type='file']").first
            file_input.set_input_files(abs_img)
            uploaded = True
            print("  ✅ input[type='file'] 직접 주입 성공!")
        except Exception as in_err:
            print(f"  ❌ 이미지 첨부 실패: {in_err}")
            return False

    if uploaded:
        # 에디터 DOM에 .se-image 컴포넌트가 실제로 추가될 때까지 최대 12초 대기
        for _ in range(24):
            time.sleep(0.5)
            now_count = page.locator(".se-component.se-image, img.se-image-resource").count()
            if now_count > before_count:
                break
        time.sleep(2.5)
        after_count = page.locator(".se-component.se-image, img.se-image-resource").count()
        print(f"  📸 에디터 내 이미지 컴포넌트 확인: {before_count}개 -> {after_count}개")

        # 이미지 아래의 본문 텍스트 영역으로 커서 안전 이동
        page.keyboard.press("ArrowDown")
        time.sleep(0.3)
        page.keyboard.press("Enter")
        time.sleep(0.5)
        try:
            text_mod = page.locator(".se-component.se-text .se-module-text").last
            if text_mod.is_visible(timeout=2000):
                text_mod.click()
                time.sleep(0.3)
        except Exception:
            pass
    return uploaded


def _enable_center_alignment(page):
    """
    스마트에디터 ONE의 정렬 툴바 드롭다운을 실제 마우스 클릭으로 열어 '가운데 정렬'을 활성화합니다.
    """
    try:
        align_btn = page.locator(
            "button.se-alignment-toolbar-button, "
            "button[data-name='align-drop-down-with-justify'], "
            ".se-toolbar-item-align button"
        ).first
        if align_btn.is_visible(timeout=2500):
            align_btn.click()
            time.sleep(0.5)
            center_opt = page.locator(
                "button[data-value='center'], "
                "button[data-name='align-center'], "
                ".se-toolbar-option-align-center-button"
            ).first
            if center_opt.is_visible(timeout=2500):
                center_opt.click()
                time.sleep(0.4)
                print("  📐 가운데 정렬(Center) 툴바 클릭 완료")
                return
    except Exception as e:
        print(f"  ⚠️ 가운데 정렬 클릭 중 예외: {e}")


def post_to_naver_blog(
    title: str,
    content_paragraphs: list,
    image_paths: list = None,
    category_name: str = "AI 정보",
    tags: list = None
) -> bool:
    """
    네이버 블로그 스마트에디터 ONE 무인 자동 발행 엔진 (아르곤 High 완결판)
    """
    is_cloud = os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CLOUD_MODE") == "true"
    naver_id = os.environ.get("NAVER_ID", "jcjung1401")
    naver_pw = os.environ.get("NAVER_PW", "")
    nid_aut = os.environ.get("NAVER_NID_AUT", "")
    nid_ses = os.environ.get("NAVER_NID_SES", "")

    target_cat_no = "7" if "웹툰" in category_name else "6"
    target_cat_keyword = "웹툰" if target_cat_no == "7" else "AI정보"

    with sync_playwright() as p:
        browser = None
        context = None

        if not is_cloud:
            chrome_user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
            try:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=chrome_user_data,
                    channel="chrome",
                    headless=False,
                    viewport={"width": 1400, "height": 950},
                    args=["--disable-blink-features=AutomationControlled"]
                )
            except Exception as e:
                print(f"⚠️ 로컬 크롬 프로필 사용 중, 독립 브라우저로 실행합니다: {e}")
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(viewport={"width": 1400, "height": 950})
                if nid_aut and nid_ses:
                    context.add_cookies([
                        {"name": "NID_AUT", "value": nid_aut, "domain": ".naver.com", "path": "/"},
                        {"name": "NID_SES", "value": nid_ses, "domain": ".naver.com", "path": "/"}
                    ])
        else:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                viewport={"width": 1400, "height": 950}
            )

            if nid_aut and nid_ses:
                context.add_cookies([
                    {"name": "NID_AUT", "value": nid_aut, "domain": ".naver.com", "path": "/"},
                    {"name": "NID_SES", "value": nid_ses, "domain": ".naver.com", "path": "/"}
                ])
            elif naver_id and naver_pw:
                page = context.new_page()
                page.goto("https://nid.naver.com/nidlogin.login")
                time.sleep(1)
                page.evaluate(f"""
                    document.getElementById('id').value = '{naver_id}';
                    document.getElementById('pw').value = '{naver_pw}';
                """)
                time.sleep(1)
                page.click("#log\\.login")
                time.sleep(3)
                page.close()

        page = context.pages[0] if context.pages else context.new_page()

        try:
            write_url = f"https://blog.naver.com/jcjung1401/postwrite?categoryNo={target_cat_no}"
            print(f"🚀 블로그 글쓰기 진입 중... ({write_url} | 제목: {title[:18]}...)")
            page.goto(write_url, wait_until="domcontentloaded", timeout=60000)
            time.sleep(5)

            if "nidlogin" in page.url or "login" in page.url:
                print("❌ 네이버 로그인 인증이 필요합니다! (세션 만료 또는 로그인 페이지로 리다이렉트됨)")
                context.close()
                if browser:
                    browser.close()
                return False

            print("🔍 에디터 로딩 및 팝업 정리 중...")
            try:
                cancel_btn = page.locator("button.se-popup-button-cancel")
                if cancel_btn.is_visible(timeout=4000):
                    cancel_btn.click()
                    print("  - 작성 중인 임시저장 글 팝업 취소 완료")
                    time.sleep(1)
            except Exception:
                pass

            try:
                help_close = page.locator("button.se-help-panel-close-button")
                if help_close.is_visible(timeout=2000):
                    help_close.click()
                    print("  - 도움말 패널 닫기 완료")
                    time.sleep(0.5)
            except Exception:
                pass

            # 1. 제목 입력
            print("📝 제목 입력 중...")
            title_area = page.locator(
                ".se-documentTitle .se-placeholder, "
                ".se-documentTitle [contenteditable='true'], "
                ".se-documentTitle .se-module-text"
            ).first
            try:
                title_area.click(timeout=5000)
            except Exception:
                page.keyboard.press("Tab")

            page.keyboard.type(title)
            print(f"  - 제목 입력 완료: {title}")
            time.sleep(1)

            # 2. 본문 영역 진입
            print("📄 본문 진입 및 이미지/원고 작성 시작...")
            body_area = page.locator(".se-component.se-text .se-module-text, .se-content [contenteditable='true']").last
            try:
                body_area.click(timeout=4000)
            except Exception:
                page.keyboard.press("Enter")
            time.sleep(1)

            # 인라인 이미지 마커(__IMAGE__:)가 없는 일반 기사인 경우 최상단에 대표 썸네일 업로드
            has_inline_markers = any(str(p).strip().startswith("__IMAGE__:") for p in content_paragraphs)
            if not has_inline_markers:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                default_thumb = os.path.join(base_dir, "완성_썸네일_1691x930.png")
                target_images = image_paths if image_paths else ([default_thumb] if os.path.exists(default_thumb) else [])
                for img_path in target_images:
                    _upload_single_image(page, img_path)

            # 본문 타이핑 시작 전 가운데 정렬 활성화
            _enable_center_alignment(page)

            # 3. 문단별 정밀 타이핑 (소제목 앞뒤 2줄 공백, 일반 문단 1줄 공백, 인라인 웹툰 이미지 업로드)
            for para in content_paragraphs:
                p_text = str(para).strip()
                if not p_text:
                    continue

                if p_text.startswith("__IMAGE__:"):
                    inline_img = p_text.split("__IMAGE__:", 1)[1].strip()
                    _upload_single_image(page, inline_img)
                    _enable_center_alignment(page)
                    continue

                is_subheading = bool(re.match(r"^\[\d+\.\s*[^\]]+\]$", p_text))
                if is_subheading:
                    page.keyboard.press("Enter")
                    time.sleep(0.1)
                    page.keyboard.type(p_text)
                    page.keyboard.press("Enter")
                    page.keyboard.press("Enter")
                    page.keyboard.press("Enter")
                    time.sleep(0.15)
                else:
                    lines = p_text.split("\n")
                    for l_i, line in enumerate(lines):
                        clean_line = line.strip()
                        if clean_line:
                            page.keyboard.type(clean_line)
                        if l_i < len(lines) - 1:
                            page.keyboard.press("Enter")
                    page.keyboard.press("Enter")
                    page.keyboard.press("Enter")
                    time.sleep(0.1)

            # 본문 하단 해시태그 텍스트 추가 (네이버 본문 검색 인덱싱 보장)
            if tags:
                clean_hashtags = [f"#{t.replace('#', '').strip()}" for t in tags[:7] if t.strip()]
                if clean_hashtags:
                    page.keyboard.press("Enter")
                    for ht in clean_hashtags:
                        page.keyboard.type(ht)
                        page.keyboard.press("Enter")
                    time.sleep(0.5)

            # 4. 상단 [발행] 버튼 클릭하여 발행 설정 서랍(Drawer) 열기
            print("📤 1단계 상단 [발행] 버튼 클릭 중...")
            pub_trigger = page.locator("button[class*='publish_btn'], .se-publish-button").first
            if pub_trigger.is_visible(timeout=3000):
                pub_trigger.click()
            else:
                page.locator("button", has_text="발행").first.click()
            time.sleep(2.5)

            # 5. 발행 설정 서랍 내 카테고리 2단계 드롭다운 정밀 선택 (Playwright Native Click)
            print(f"📁 카테고리 [{target_cat_no}] ('{category_name}') 2단계 드롭다운 검증 및 선택 중...")
            try:
                cat_btn = page.locator(
                    "[aria-label*='카테고리'], [class*='option_category'] button, [class*='selectbox_button']"
                ).first
                if cat_btn.is_visible(timeout=3000):
                    current_cat_txt = re.sub(r"\s+", "", cat_btn.inner_text() or "")
                    print(f"  - 현재 표시된 카테고리: '{current_cat_txt}'")
                    if target_cat_keyword not in current_cat_txt:
                        cat_btn.click()
                        print("  - 카테고리 드롭다운 목록 열기 완료")
                        time.sleep(1.0)
                        cat_pattern = re.compile(r"AI\s*정보" if target_cat_no == "6" else r"웹툰")
                        opt = page.locator(
                            "[class*='option_category'] label, [class*='option_category'] li, "
                            "[class*='selectbox'] label, [class*='selectbox'] li, label"
                        ).filter(has_text=cat_pattern).first
                        if opt.is_visible(timeout=3000):
                            opt.click()
                            print(f"  ✅ 카테고리 '{category_name}' 클릭 완료!")
                            time.sleep(1.0)
                    else:
                        print(f"  ✅ 이미 목표 카테고리('{current_cat_txt}')로 자동 설정되어 있습니다!")
            except Exception as cat_err:
                print(f"  ⚠️ 카테고리 드롭다운 제어 중 예외: {cat_err}")

            # 6. 발행 설정 서랍 내 태그 입력칸(Tag Input) 입력
            if tags:
                print(f"🏷️ 발행창 태그 입력 중... ({', '.join(tags[:5])})")
                try:
                    tag_input = page.locator(
                        "input[placeholder*='태그'], textarea[placeholder*='태그'], "
                        "input.tag_input, [class*='tag_input'] input, #tag-input"
                    ).first
                    if tag_input.is_visible(timeout=3000):
                        tag_input.click()
                        for t in tags[:7]:
                            clean_t = t.replace("#", "").strip()
                            if clean_t:
                                page.keyboard.type(clean_t)
                                page.keyboard.press("Enter")
                                time.sleep(0.25)
                        print("  ✅ 발행창 태그 입력 완료!")
                except Exception as tag_err:
                    print(f"  ⚠️ 발행창 태그 입력 중 예외: {tag_err}")
            time.sleep(1.0)

            # 7. 최종 [발행] 확인 버튼 클릭 (Playwright Native Click)
            print("📤 2단계 최종 [발행] 확인 버튼 클릭 중...")
            confirm_btn = page.locator("button[class*='confirm_btn'], [data-testid='seOnePublishBtn']").first
            if confirm_btn.is_visible(timeout=3000):
                confirm_btn.click()
            else:
                page.locator("button", has_text="발행").last.click()
            time.sleep(7)

            print(f"✅ 포스팅 최종 완료: {title} (URL: {page.url})")
            context.close()
            if browser:
                browser.close()
            return True

        except Exception as e:
            print(f"❌ 포스팅 실패: {e}")
            context.close()
            if browser:
                browser.close()
            return False


if __name__ == "__main__":
    print("스마트에디터 포스팅 모듈(아르곤 High 완결판) 준비 완료")
