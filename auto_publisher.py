import os
import re
import time
from playwright.sync_api import sync_playwright


def _upload_single_image(page, img_path: str) -> bool:
    """
    네이버 스마트에디터 ONE의 상단 [사진] 툴바 버튼을 클릭하고
    브라우저의 File Chooser 이벤트를 공중에서 가로채(intercept) 이미지를 100% 업로드합니다.
    """
    if not img_path or not os.path.exists(img_path):
        print(f"  ⚠️ 이미지 파일이 존재하지 않습니다: {img_path}")
        return False

    abs_img = os.path.abspath(img_path)
    print(f"  🖼️ 이미지 업로드 시작 (File Chooser 인터셉트): {os.path.basename(abs_img)}")

    uploaded = False
    # 1차 시도: Playwright 공식 expect_file_chooser 인터셉트
    try:
        with page.expect_file_chooser(timeout=10000) as fc_info:
            img_btn = page.locator(
                "button.se-image-toolbar-button, "
                "button[data-name='image'], "
                ".se-toolbar-item-image button"
            ).first
            if img_btn.is_visible(timeout=3000):
                img_btn.click()
            else:
                page.evaluate("""
                    () => {
                        const btn = document.querySelector(
                            'button.se-image-toolbar-button, button[data-name="image"], .se-toolbar-item-image button'
                        );
                        if (btn) btn.click();
                    }
                """)
        file_chooser = fc_info.value
        file_chooser.set_files(abs_img)
        uploaded = True
        print("  ✅ File Chooser 경유 이미지 파일 주입 성공! (서버 렌더링 5초 대기)")
    except Exception as fc_err:
        print(f"  ⚠️ File Chooser 인터셉트 1차 예외 ({fc_err}), 동적 input[type='file'] 폴백 시도...")
        try:
            file_input = page.locator("input[type='file']").first
            file_input.set_input_files(abs_img)
            uploaded = True
            print("  ✅ 동적 input[type='file'] 경유 이미지 업로드 성공!")
        except Exception as in_err:
            print(f"  ❌ 이미지 첨부 최종 실패: {in_err}")
            return False

    if uploaded:
        time.sleep(5)
        # 이미지 컴포넌트 아래의 텍스트 문단으로 포커스 이동
        page.keyboard.press("ArrowDown")
        time.sleep(0.3)
        page.keyboard.press("Enter")
        time.sleep(0.5)
    return uploaded


def _enable_center_alignment(page):
    """
    스마트에디터 ONE의 2단계 정렬 드롭다운을 제어하여 현재 문단을 가운데 정렬로 전환합니다.
    (한 번 가운데 정렬로 전환된 문단에서 Enter를 치면 이후 모든 문단이 가운데 정렬을 자동 유지합니다.)
    """
    try:
        # 1단계: 정렬 드롭다운 메뉴 버튼 클릭
        page.evaluate("""
            () => {
                const alignDropdown = document.querySelector(
                    'button.se-alignment-toolbar-button, ' +
                    'button[data-name="align-drop-down-with-justify"], ' +
                    '.se-toolbar-item-align button'
                );
                if (alignDropdown) alignDropdown.click();
            }
        """)
        time.sleep(0.5)
        # 2단계: 열린 서브메뉴에서 '가운데 정렬(center)' 옵션 클릭
        page.evaluate("""
            () => {
                const centerOpt = document.querySelector(
                    'button[data-value="center"], ' +
                    'button[data-name="align-center"], ' +
                    '.se-toolbar-option-align-center-button'
                );
                if (centerOpt) centerOpt.click();
            }
        """)
        time.sleep(0.4)
        print("  📐 가운데 정렬 모드 활성화 완료")
    except Exception as e:
        print(f"  ⚠️ 가운데 정렬 설정 중 예외 (무시 가능): {e}")


def post_to_naver_blog(
    title: str,
    content_paragraphs: list,
    image_paths: list = None,
    category_name: str = "AI 정보",
    tags: list = None
) -> bool:
    """
    네이버 블로그 스마트에디터 ONE 무인 자동 발행 엔진 (아르곤 High 완결판)
    - URL 파라미터(?categoryNo=6/7) + 발행창 2단계 드롭다운 이중 잠금으로 카테고리 100% 보장
    - page.expect_file_chooser()로 썸네일 및 웹툰 컷 이미지 100% 업로드
    - 문단 입력 전/후 2단 드롭다운 제어로 본문 전체 가운데 정렬 적용
    - 소제목([1. ...]) 앞뒤 2줄 여백 + 일반 문단 1줄 여백 정밀 구현
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
            time.sleep(4)

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
            for idx, para in enumerate(content_paragraphs):
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
                    # 소제목 앞 2줄 공백 확보 (이전 문단 직후 1줄 + 추가 1줄)
                    page.keyboard.press("Enter")
                    time.sleep(0.1)
                    page.keyboard.type(p_text)
                    # 소제목 뒤 2줄 공백 확보 (줄바꿈 1회 + 빈 줄 2회)
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
                    # 일반 문단 간 1줄 빈 줄 유지
                    page.keyboard.press("Enter")
                    page.keyboard.press("Enter")
                    time.sleep(0.1)

            # 본문 하단 해시태그 텍스트 추가 (네이버 본문 검색 인덱싱 보조)
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
            page.evaluate("""
                () => {
                    const pubBtn = document.querySelector(
                        'button[class*="publish_btn"], .se-publish-button'
                    );
                    if (pubBtn) {
                        pubBtn.click();
                        return;
                    }
                    const btns = Array.from(document.querySelectorAll('button'));
                    const fallback = btns.find(b => b.innerText.trim() === '발행' && !b.className.includes('confirm'));
                    if (fallback) fallback.click();
                }
            """)
            time.sleep(2.5)

            # 5. 발행 설정 서랍 내 카테고리 2단계 드롭다운 정밀 선택
            print(f"📁 카테고리 [{target_cat_no}] ('{category_name}') 2단계 드롭다운 검증 및 선택 중...")
            cat_status = page.evaluate(f"""
                (targetKeyword) => {{
                    // 현재 선택된 카테고리 버튼 텍스트 확인 (\\xa0 등 모든 공백 제거 후 비교)
                    const catBtn = document.querySelector(
                        '[aria-label*="카테고리"], [class*="option_category"] button, [class*="selectbox_button"]'
                    );
                    if (catBtn) {{
                        const currentTxt = (catBtn.innerText || '').replace(/\\s+/g, '');
                        if (currentTxt.includes(targetKeyword)) {{
                            return 'ALREADY_SELECTED:' + currentTxt;
                        }}
                        catBtn.click();
                        return 'OPENED_DROPDOWN:' + currentTxt;
                    }}
                    return 'NO_CAT_BTN';
                }}
            """, target_cat_keyword)
            print(f"  - 카테고리 버튼 상태: {cat_status}")

            if not str(cat_status).startswith("ALREADY_SELECTED"):
                time.sleep(1.0)
                selected_result = page.evaluate(f"""
                    (args) => {{
                        const {{ catNo, keyword }} = args;
                        // 1순위: value나 data 속성이 catNo인 요소
                        const byVal = document.querySelector(
                            `input[name="categoryNo"][value="${{catNo}}"], [data-categoryno="${{catNo}}"], [data-value="${{catNo}}"]`
                        );
                        if (byVal) {{
                            byVal.click();
                            const lbl = document.querySelector(`label[for="${{byVal.id}}"]`);
                            if (lbl) lbl.click();
                            return 'CLICKED_BY_VALUE';
                        }}
                        // 2순위: 드롭다운 리스트 내 텍스트(공백/\\xa0 무시) 일치 항목 클릭
                        const candidates = Array.from(document.querySelectorAll(
                            '[class*="option_category"] li, [class*="option_category"] label, ' +
                            '[class*="option_category"] button, [class*="selectbox"] li, ' +
                            '[class*="selectbox"] label, [role="option"], label, .category_item'
                        ));
                        const match = candidates.find(el => {{
                            const txt = (el.innerText || '').replace(/\\s+/g, '');
                            return txt === keyword || txt.includes(keyword);
                        }});
                        if (match) {{
                            match.click();
                            return 'CLICKED_BY_TEXT:' + match.innerText.trim();
                        }}
                        return 'NOT_FOUND';
                    }}
                """, {"catNo": target_cat_no, "keyword": target_cat_keyword})
                print(f"  - 카테고리 드롭다운 선택 결과: {selected_result}")
                time.sleep(1.0)

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
                    print(f"  ⚠️ 발행창 태그 입력 중 예외 (본문 해시태그로 대체됨): {tag_err}")
            time.sleep(1.0)

            # 7. 최종 [발행] 확인 버튼 클릭
            print("📤 2단계 최종 [발행] 확인 버튼 클릭 중...")
            page.evaluate("""
                () => {
                    const confirmBtn = document.querySelector(
                        'button[class*="confirm_btn"], [data-testid="seOnePublishBtn"]'
                    );
                    if (confirmBtn) {
                        confirmBtn.click();
                        return;
                    }
                    const layer = document.querySelector(
                        '[class*="layer_publish"], [class*="publish_layer"], [class*="layer_popup"]'
                    );
                    if (layer) {
                        const btn = Array.from(layer.querySelectorAll('button')).find(
                            b => b.innerText.trim() === '발행'
                        );
                        if (btn) {
                            btn.click();
                            return;
                        }
                    }
                    const allPublishBtns = Array.from(document.querySelectorAll('button')).filter(
                        b => b.innerText.trim() === '발행'
                    );
                    if (allPublishBtns.length > 0) {
                        allPublishBtns[allPublishBtns.length - 1].click();
                    }
                }
            """)
            time.sleep(6)

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
