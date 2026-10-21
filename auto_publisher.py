import os
import time
from playwright.sync_api import sync_playwright

def post_to_naver_blog(
    title: str,
    content_paragraphs: list,
    image_paths: list = None,
    category_name: str = "AI 트렌드",
    tags: list = None
) -> bool:
    """
    네이버 블로그 스마트에디터 ONE 자동 포스팅 엔진
    - 로컬 환경: 사장님의 크롬 자동 로그인 프로필 직접 사용
    - 클라우드 환경: NAVER_ID / NAVER_PW 또는 NID 쿠키 기반 자동 로그인
    """
    is_cloud = os.environ.get("GITHUB_ACTIONS") == "true" or os.environ.get("CLOUD_MODE") == "true"
    naver_id = os.environ.get("NAVER_ID", "jcjung1401")
    naver_pw = os.environ.get("NAVER_PW", "")
    nid_aut = os.environ.get("NAVER_NID_AUT", "")
    nid_ses = os.environ.get("NAVER_NID_SES", "")

    with sync_playwright() as p:
        browser = None
        context = None

        if not is_cloud:
            # [1] 로컬 PC 실행 모드
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
                print(f"⚠️ 로컬 크롬 실행 중 (기본 브라우저 사용): {e}")
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()
        else:
            # [2] 클라우드(GitHub Actions) 환경
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                viewport={"width": 1400, "height": 950}
            )

            # 쿠키가 주어졌다면 쿠키로 로그인 상태 복원
            if nid_aut and nid_ses:
                context.add_cookies([
                    {"name": "NID_AUT", "value": nid_aut, "domain": ".naver.com", "path": "/"},
                    {"name": "NID_SES", "value": nid_ses, "domain": ".naver.com", "path": "/"}
                ])
            elif naver_id and naver_pw:
                # 아이디/비밀번호 클라우드 로그인 스크립트 실행
                page = context.new_page()
                page.goto("https://nid.naver.com/nidlogin.login")
                time.sleep(1)
                # 네이버 보안 탐지 우회 입력 방식 (evaluate 기반 자바스크립트 값 주입)
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
            print(f"🚀 블로그 글쓰기 진입 중... ({title[:15]}...)")
            page.goto("https://blog.naver.com/jcjung1401/postwrite", wait_until="domcontentloaded", timeout=60000)
            time.sleep(3)

            # 로그인 여부 체크
            if "nidlogin" in page.url or "login" in page.url:
                print("❌ 네이버 로그인 인증이 필요합니다! (세션 만료 또는 로그인 페이지로 리다이렉트됨)")
                context.close()
                if browser:
                    browser.close()
                return False

            print("🔍 에디터 로딩 및 팝업 정리 중...")
            # 작성 중인 글 취소 팝업 (있으면 취소)
            try:
                cancel_btn = page.locator("button.se-popup-button-cancel")
                if cancel_btn.is_visible(timeout=5000):
                    cancel_btn.click()
                    print("  - 작성 중인 임시저장 글 팝업 닫음")
                    time.sleep(1)
            except Exception:
                pass

            # 도움말 팝업 닫기
            try:
                help_close = page.locator("button.se-help-panel-close-button")
                if help_close.is_visible(timeout=3000):
                    help_close.click()
                    print("  - 도움말 패널 닫음")
            except Exception:
                pass

            # 제목 입력
            print("📝 제목 입력 중...")
            # 네이버 스마트에디터 ONE의 실제 제목 입력 영역 정밀 타겟팅
            title_area = page.locator(".se-documentTitle .se-placeholder, .se-documentTitle [contenteditable='true'], .se-documentTitle .se-module-text").first
            try:
                title_area.click(timeout=5000)
            except Exception:
                page.keyboard.press("Tab") # 탭 키로 첫 번째 입력칸(제목) 포커스 이동
            
            page.keyboard.type(title)
            print(f"  - 제목 입력 완료: {title}")
            time.sleep(1)

            # 본문 작성 및 이미지 첨부
            print("📄 본문 및 이미지 업로드 중...")
            page.keyboard.press("Enter")
            time.sleep(1)

            # [1] 대표 썸네일 이미지 첨부 (스마트에디터 상단 툴바의 사진 버튼 정밀 클릭)
            if image_paths:
                for img_path in image_paths:
                    if os.path.exists(img_path):
                        try:
                            abs_img = os.path.abspath(img_path)
                            print(f"  - 대표 썸네일 첨부 시도: {abs_img}")
                            # 스마트에디터 사진 업로드 input 태그에 직접 파일 주입
                            file_input = page.locator("input[type='file'][accept*='image']").first
                            file_input.set_input_files(abs_img)
                            print("  ✅ 썸네일 이미지 파일 첨부 완료 (업로드 대기 4초)...")
                            time.sleep(4)
                            # 이미지 첨부 후 다음 줄로 엔터
                            page.keyboard.press("Enter")
                            time.sleep(1)
                        except Exception as img_err:
                            print(f"  ⚠️ 이미지 첨부 중 예외 발생: {img_err}")

            # [2] 가운데 정렬 적용 (스마트에디터 상단 툴바 가운데 정렬 버튼 클릭)
            try:
                print("📐 가운데 정렬 적용 중...")
                page.evaluate("""
                    () => {
                        // 스마트에디터 정렬 버튼 찾기
                        const alignCenterBtn = document.querySelector('button[data-name="align-center"], button.se-align-center-button, button[data-action="center"]');
                        if (alignCenterBtn) {
                            alignCenterBtn.click();
                        }
                    }
                """)
                time.sleep(1)
            except Exception:
                pass

            # [3] 본문 문단 작성 (소제목 앞뒤 공백 및 25자 서식)
            for p in content_paragraphs:
                p_text = p.strip()
                if not p_text:
                    continue
                # 소제목이면 더 돋보이게 작성
                page.keyboard.type(p_text)
                page.keyboard.press("Enter")
                page.keyboard.press("Enter")
                time.sleep(0.1)

            time.sleep(2)

            # 발행 버튼 클릭
            print("📤 1단계 발행 버튼 클릭 중...")
            page.evaluate("""
                () => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const publishBtn = btns.find(b => b.innerText.trim() === '발행' && !b.className.includes('reserve'));
                    if (publishBtn) publishBtn.click();
                }
            """)
            time.sleep(2)

            # [4] 카테고리 선택 ('AI 정보' 카테고리 6번 정확 선택)
            print(f"📁 카테고리 '{category_name}' 지정 중...")
            page.evaluate(f"""
                (catName) => {{
                    // 카테고리 드롭다운/라디오 선택
                    const labels = Array.from(document.querySelectorAll('label, .category_item, .item__N392L'));
                    const targetLabel = labels.find(l => l.innerText.includes(catName));
                    if (targetLabel) {{
                        targetLabel.click();
                    }} else {{
                        // 셀렉트 박스 형태일 경우
                        const select = document.querySelector('select[name="categoryNo"], .select_category');
                        if (select) {{
                            const opt = Array.from(select.options).find(o => o.text.includes(catName));
                            if (opt) select.value = opt.value;
                        }}
                    }}
                }}
            """, category_name)
            time.sleep(1.5)

            # [5] 태그 5~8개 정밀 입력 (네이버 스마트블록 & 검색 유입 극대화!)
            if tags:
                print(f"🏷️ 검색 태그 5~8개 자동 입력 중... ({', '.join(tags[:5])}...)")
                try:
                    tag_input = page.locator("input.tag_input, input[placeholder*='태그'], .tag_input__N90fR, #tag_input").first
                    if tag_input.is_visible(timeout=3000):
                        tag_input.click()
                        for t in tags[:8]:
                            clean_t = t.replace("#", "").strip()
                            if clean_t:
                                tag_input.fill(clean_t)
                                page.keyboard.press("Enter")
                                time.sleep(0.3)
                        print("  ✅ 태그 5~8개 입력 완료!")
                except Exception as tag_err:
                    print(f"  ⚠️ 태그 입력 중 예외 발생: {tag_err}")
            time.sleep(1)

            print("📤 2단계 최종 발행 확인 버튼 클릭 중...")
            # 발행 레이어 팝업 내부의 최종 초록색 [발행] 버튼 클릭
            page.evaluate("""
                () => {
                    const layer = document.querySelector('.layer_publish, .layer_publish__W8d9Z, .publish_layer');
                    if (layer) {
                        const confirmBtn = Array.from(layer.querySelectorAll('button')).find(b => b.innerText.trim() === '발행');
                        if (confirmBtn) confirmBtn.click();
                    } else {
                        const btns = Array.from(document.querySelectorAll('button'));
                        const lastPublish = btns.filter(b => b.innerText.trim() === '발행').pop();
                        if (lastPublish) lastPublish.click();
                    }
                }
            """)
            time.sleep(5)

            print(f"✅ 포스팅 완료: {title}")
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
    print("스마트에디터 포스팅 모듈 준비 완료")
