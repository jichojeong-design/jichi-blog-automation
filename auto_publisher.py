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
    (사장님의 평소 로그인된 실제 크롬 브라우저와 100% 동일한 프로필 사용)
    """
    chrome_user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")

    with sync_playwright() as p:
        try:
            # 사장님의 크롬 프로필을 그대로 활용 (별도 로그인 필요 없음!)
            context = p.chromium.launch_persistent_context(
                user_data_dir=chrome_user_data,
                channel="chrome",
                headless=False, # 동작하는 모습을 눈으로 확인할 수도 있음
                viewport={"width": 1400, "height": 950},
                args=["--disable-blink-features=AutomationControlled"]
            )
        except Exception as e:
            # 크롬 창이 이미 켜져 있어 lock이 걸렸을 경우를 대비한 복제 프로필 처리
            print(f"⚠️ 크롬 실행 중: {e}")
            return False

        page = context.pages[0] if context.pages else context.new_page()
        
        try:
            print(f"🚀 블로그 글쓰기 진입 중... ({title[:15]}...)")
            page.goto("https://blog.naver.com/jcjung1401/postwrite", wait_until="networkidle")
            time.sleep(2)
            
            # 작성 중인 글 취소 팝업
            try:
                cancel_btn = page.locator("button.se-popup-button-cancel")
                if cancel_btn.is_visible(timeout=3000):
                    cancel_btn.click()
                    time.sleep(1)
            except Exception:
                pass

            # 도움말 팝업 닫기
            try:
                help_close = page.locator("button.se-help-panel-close-button")
                if help_close.is_visible(timeout=2000):
                    help_close.click()
            except Exception:
                pass

            # 제목 입력
            print("📝 제목 입력 중...")
            title_input = page.locator(".se-documentTitle .se-ff-nanumgothic, .se-documentTitle [contenteditable='true']")
            title_input.click()
            title_input.fill(title)
            time.sleep(1)

            # 본문 작성 및 이미지 첨부
            print("📄 본문 및 이미지 업로드 중...")
            body_area = page.locator(".se-main-container [contenteditable='true']").first
            body_area.click()
            
            if image_paths:
                for img_path in image_paths:
                    if os.path.exists(img_path):
                        file_input = page.locator("input[type='file'][accept*='image']")
                        if file_input.count() > 0:
                            file_input.first.set_input_files(img_path)
                            time.sleep(3)

            for p in content_paragraphs:
                page.keyboard.type(p)
                page.keyboard.press("Enter")
                page.keyboard.press("Enter")
                time.sleep(0.2)

            time.sleep(2)

            # 발행 버튼 클릭
            print("📤 발행 준비 중...")
            publish_open_btn = page.locator("button.publish_btn__m9nHH, button[data-action='publish'], button:has-text('발행')").first
            publish_open_btn.click()
            time.sleep(1.5)

            confirm_publish_btn = page.locator("button.confirm_btn__DAeXZ, button:has-text('발행')").last
            confirm_publish_btn.click()
            time.sleep(4)
            
            print(f"✅ 포스팅 완료: {title}")
            context.close()
            return True

        except Exception as e:
            print(f"❌ 포스팅 실패: {e}")
            context.close()
            return False

if __name__ == "__main__":
    print("스마트에디터 포스팅 모듈 준비 완료")
