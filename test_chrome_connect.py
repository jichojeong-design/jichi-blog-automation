import os
from playwright.sync_api import sync_playwright

def test_login_with_chrome_profile():
    # 사장님의 실제 크롬 사용자 데이터 폴더 직접 연결!
    chrome_user_data = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
    
    with sync_playwright() as p:
        # 사장님의 평소 크롬 브라우저를 그대로 연결 실행
        context = p.chromium.launch_persistent_context(
            user_data_dir=chrome_user_data,
            channel="chrome",
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://blog.naver.com/jcjung1401")
        print(">>> 사장님의 기존 크롬 로그인으로 블로그 접속 성공 여부를 확인합니다.")
        page.wait_for_timeout(5000)
        context.close()

if __name__ == "__main__":
    test_login_with_chrome_profile()
