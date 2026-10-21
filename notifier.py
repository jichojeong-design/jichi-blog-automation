import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os

def send_emergency_alert(failed_task_name: str, error_detail: str):
    """
    네이버 메일 SMTP를 사용하여 사장님 네이버 메일(jcjung1401@naver.com)로 즉시 긴급 알림 발송
    네이버 앱 푸시 알림으로 스마트폰에 즉각 팝업 유도!
    """
    naver_id = os.environ.get("NAVER_ID", "jcjung1401")
    naver_pw = os.environ.get("NAVER_PW", "")
    
    if not naver_pw:
        print("⚠️ NAVER_PW가 설정되지 않아 알림 메일을 건너뜁니다.")
        return False

    sender_email = f"{naver_id}@naver.com"
    receiver_email = f"{naver_id}@naver.com" # 사장님 본인에게 즉시 발송
    
    subject = f"🚨 [지치 블로그 긴급 알림] {failed_task_name} 미발행 감지! 비상 가동 필요"
    
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_content = f"""
    <div style="font-family: 'Apple SD Gothic Neo', sans-serif; max-width: 600px; margin: 0 auto; border: 2px solid #E53935; border-radius: 12px; padding: 25px; background-color: #FFF8F8;">
        <h2 style="color: #D32F2F; margin-top: 0;">🚨 [지치 블로그 긴급 알림] 포스팅 이상 감지</h2>
        <p style="font-size: 15px; color: #333; line-height: 1.6;">
            사장님, <b>{now_str}</b> 기준 <b>[{failed_task_name}]</b> 자동 발행 과정에서 이상이 감지되었습니다.
        </p>
        
        <div style="background-color: #FFFFFF; border: 1px solid #FFCDD2; border-radius: 8px; padding: 15px; margin: 20px 0;">
            <b style="color: #C62828;">상세 에러 내용:</b><br/>
            <code style="color: #555; font-size: 13px; display: block; margin-top: 8px;">{error_detail}</code>
        </div>
        
        <p style="font-size: 14px; color: #444; line-height: 1.6;">
            아침 황금 시간대 방문객 선점을 위해 <b>아래 버튼을 눌러 비상 가동</b>을 진행해 주세요!
        </p>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="https://github.com/jichojeong-design/jichi-blog-automation/actions/workflows/daily_blog.yml" 
               style="background-color: #E53935; color: #FFFFFF; text-decoration: none; padding: 14px 28px; font-size: 16px; font-weight: bold; border-radius: 8px; display: inline-block; box-shadow: 0 4px 6px rgba(229,57,53,0.3);">
               🚨 [원클릭] 비상 자동 발행 즉시 재가동하기
            </a>
        </div>
        
        <hr style="border: 0; border-top: 1px solid #FFCDD2; margin: 20px 0;">
        <p style="font-size: 12px; color: #888; text-align: center;">
            지치 블로그 무인 자동화 관제 센터 (코다리부장 24H 모니터링 시스템)
        </p>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        # 네이버 SMTP SSL 연결 (포트 465)
        with smtplib.SMTP_SSL("smtp.naver.com", 465, timeout=10) as server:
            server.login(naver_id, naver_pw)
            server.sendmail(sender_email, [receiver_email], msg.as_string())
        print(f"📧 사장님 네이버 메일({receiver_email})로 긴급 알림 발송 완료!")
        return True
    except Exception as e:
        print(f"❌ 네이버 메일 발송 실패: {e}")
        return False

if __name__ == "__main__":
    send_emergency_alert("09:00 AI 트렌드 기사 1편", "테스트 에러: 스마트에디터 타임아웃 발생")
