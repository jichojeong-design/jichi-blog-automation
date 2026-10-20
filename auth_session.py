import os
import json
import time
from playwright.sync_api import sync_playwright

SESSION_FILE = "naver_session.json"

def save_login_session():
    """
    네이버 로그인 세션을 1회 저장하는 유틸리티
    브라우저 창이 열리면 사장님께서 네이버 로그인(1회)을 완료하신 후 Enter를 누르시면 됩니다.
    """
    with sync_playwright() as p:
        user_data_dir = os.path.join(os.getcwd(), "naver_playwright_profile")
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://nid.naver.com/nidlogin.login")
        print(">>> 네이버 로그인 창이 열렸습니다. 로그인을 완료해 주세요!")
        input(">>> 로그인을 마치신 후 여기 콘솔에서 Enter 키를 눌러주세요...")
        
        # 블로그 메인으로 이동하여 로그인 유지 확인
        page.goto("https://blog.naver.com/jcjung1401")
        time.sleep(3)
        context.close()
        print(">>> 네이버 세션 저장이 완료되었습니다!")

if __name__ == "__main__":
    save_login_session()
