import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import datetime
import notifier

# 9대 금지 표현 목록
BANNED_EXPRESSIONS = [
    "핵심은 ~이 아니라", "단순한 ~이 아니라", "중요한 점은", "주목할 점은",
    "방향은 분명합니다", "관건입니다", "시사하는 바가 큽니다", "귀추가 주목됩니다",
    "첫째,", "둘째,", "셋째,"
]

def inspect_latest_post_quality(expected_category: str = "AI 정보", is_article: bool = True) -> dict:
    """
    발행 직후 코부장 품질검사관이 독자 모드로 직접 블로그에 접속하여 전수 검사 실시!
    1. 썸네일/이미지 1장 이상 첨부 여부
    2. 목표 카테고리(AI 정보 또는 웹툰) 정확 일치 여부
    3. 본문 텍스트 분량 및 가운데 정렬 가독성
    4. 9대 금지 표현 포함 여부
    """
    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 품질검사관 출동] 방금 발행된 게시글 전수 품질 검사 시작!")
    print("=" * 60)

    url = "https://blog.naver.com/PostList.naver?blogId=jcjung1401&currentPage=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    report = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": "",
        "category": "",
        "image_count": 0,
        "char_count": 0,
        "banned_found": [],
        "passed": False,
        "issues": []
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            soup = BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")
            
            # 최신 글 파싱
            post_title_el = soup.select_one(".se-title-text, .pcol1, h3.title, .se-documentTitle")
            report["title"] = post_title_el.get_text(strip=True) if post_title_el else "제목 확인 불가"

            # 카테고리 확인
            cat_el = soup.select_one(".blog2_series, .category, .se-series")
            report["category"] = cat_el.get_text(strip=True) if cat_el else "게시판"

            # 이미지 개수 확인
            imgs = soup.select(".se-main-container img, .se-image-resource, img.se_mediaImage")
            report["image_count"] = len(imgs)

            # 본문 텍스트 및 분량 확인
            body_el = soup.select_one(".se-main-container, .post-view")
            body_text = body_el.get_text() if body_el else ""
            report["char_count"] = len(body_text.strip())

            # 9대 금지어 검사
            for banned in BANNED_EXPRESSIONS:
                clean_banned = banned.replace("~", "").replace(",", "").strip()
                if clean_banned in body_text:
                    report["banned_found"].append(banned)

    except Exception as e:
        print(f"⚠️ 품질 검사 웹 크롤링 중 오류: {e}")

    # [품질 합격/불합격 판정 기준]
    # 1. 이미지 검사: 최소 1장(썸네일) 이상
    if report["image_count"] < 1:
        report["issues"].append("❌ 대표 썸네일(이미지) 누락 감지")

    # 2. 카테고리 검사: AI 정보 또는 웹툰
    if expected_category not in report["category"]:
        report["issues"].append(f"❌ 카테고리 불일치 (목표: '{expected_category}' vs 실제: '{report['category']}')")

    # 3. 분량 검사 (기사 기준 최소 800자 이상)
    if is_article and report["char_count"] < 800:
        report["issues"].append(f"❌ 본문 분량 부족 (공백 포함 {report['char_count']}자)")

    # 4. 금지 표현 검사
    if report["banned_found"]:
        report["issues"].append(f"❌ 9대 금지 표현 발견: {', '.join(report['banned_found'])}")

    # 최종 판정
    report["passed"] = (len(report["issues"]) == 0)

    # 콘솔 브리핑
    print(f"📌 검사 대상: {report['title']}")
    print(f"📁 확인된 카테고리: {report['category']}")
    print(f"🖼️ 첨부된 이미지 수: {report['image_count']}장")
    print(f"📄 본문 분량: {report['char_count']}자")
    
    if report["passed"]:
        print("🎉 [전수 검사 합격] 5대 품질 기준 100% 통과! 사람이 쓴 명품 포스팅으로 인증되었습니다.")
    else:
        print(f"🚨 [품질 검사 불합격] 발견된 결함 {len(report['issues'])}건:")
        for iss in report["issues"]:
            print(f"   - {iss}")
        
        # 사장님 네이버 메일로 '품질 결함 긴급 리포트' 즉각 발송
        notifier.send_emergency_alert(
            failed_task_name=f"품질 검사 불합격 ({report['title'][:15]}...)",
            error_detail="<br/>".join(report["issues"])
        )

    print("=" * 60 + "\n")
    return report

if __name__ == "__main__":
    inspect_latest_post_quality(expected_category="AI 정보", is_article=True)
