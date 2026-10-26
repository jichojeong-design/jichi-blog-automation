import os
import sys

# 세션 환경변수 즉시 주입
os.environ['NAVER_NID_AUT'] = 'BvZFJBlsvl6Uld9m/W99QBF8tBE9xVDdFPnONTPn6kRKnBC69SLeN+CDGa2FGWhF'
os.environ['NAVER_NID_SES'] = 'AAABygWJEGoJ+kwLmHZNcpxCA6eg2tyMgUwqxRX4kjohUIEVN32lNrdOGe1bqsojK9MTcED7ImhfCY+4o3Cvpuoqt2hUs+gVzOi9+mbp+o5VR/EuROGfzYuzWwNwMEQK5vJ0UDzjSSjk1VR+PqEJ/2KWQbqQgJk8Pf7iYN2CuijVtcQYdPzpQNUFPbfF7hdXygbSgAAlWwRRkXJRjcQHbIknQxqcDOjDg3mzP5xTrpEq7+HCH0UwgO+98xEddhS4aYt9bPZ7VaTRKfcqxd6bXOJS/OLa8MImYmFtMPYv0xtQ1FPa+VPsvgchay+/r4yDoTVZuYIspCsb3pO9HDt+640kkDYGly8rnY7ZgGsGDvsCz4GqgA6lS6jZlrrMuonpqpc3GNm64G4aZNsRja7d/kXlt+465ZaFiMGhq3l3V9XlaLvy9TTeJD529qmOUtH7XeCTyfQ7L/T98iEB/Hh/IG3KBq4s/B8tWXrkKwrSrAKtnDW1jgIdFIcLOSuJ3cV8Nzg1Tqtjq8TK0dq1WhIgDM3X1g1FHwppV71E0N9WNaksNnv33VXRRAFwpt6JZRuuwV0/ShIcj2Bcv01UYnhzN2OmYRb0az99JhSg3Aj/23bMSS6g'
os.environ['CLOUD_MODE'] = 'true'

import daily_scheduler

print("\n" + "=" * 65)
print("🚀 [지치컴퍼니 긴급 출격] 오늘의 9시 AI 기사 3편 로컬 직통 순차 발행 시작!")
print("=================================================================")

for idx in range(1, 4):
    print(f"\n📰 [기사 #{idx}/3] 발행 프로세스 가동 중...")
    success = daily_scheduler.run_ai_article_routine(idx)
    if success:
        print(f"✅ 기사 #{idx} 네이버 블로그에 라이브 발행 성공!")
    else:
        print(f"❌ 기사 #{idx} 발행 실패!")
    
    if idx < 3:
        print("⏳ [네이버 알고리즘 및 블로그 최적화 보호] 대표님 특명: 다음 글 발행 전 무조건 10분(600초) 대기합니다...")
        import time
        for remaining in range(600, 0, -60):
            print(f"  - 다음 기사 발행까지 남은 시간: {remaining // 60}분...")
            time.sleep(60)

print("\n" + "=" * 65)
print("🎉🎉 [전원 임무 완수] 오늘의 AI 기사 3편 라이브 발행이 모두 완료되었습니다!")
print("=================================================================")
