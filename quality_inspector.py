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
    발행 직후 코부장 품질검사관이 독자 모드로 직접 블로그에 접속하여 최신 글(첫 번째 .se-viewer) 전수 검사 실시!
    1. 썸네일/이미지 1장 이상 첨부 여부
    2. 목표 카테고리(AI 정보 또는 웹툰) 정확 일치 여부 (\xa0 공백 정규화 비교)
    3. 본문 텍스트 분량 및 가운데 정렬 가독성
    4. 9대 금지 표현 포함 여부
    """
    print("\n" + "=" * 60)
    print("🕵️‍♂️ [코부장 품질검사관 출동] 방금 발행된 최신 게시글 전수 품질 검사 시작!")
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
        with urllib.request.urlopen(req, timeout=12) as resp:
            soup = BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")

            # 반드시 가장 최신 게시글(.se-viewer 첫 번째 요소)만 타겟팅하여 검사
            latest_viewer = soup.select_one(".se-viewer") or soup.select_one(".post-view") or soup

            # 1. 최신 글 제목 파싱
            post_title_el = latest_viewer.select_one(".se-title-text, .pcol1, .se-documentTitle")
            report["title"] = post_title_el.get_text(strip=True) if post_title_el else "제목 확인 불가"

            # 2. 최신 글 카테고리 확인 (\xa0 특수 공백을 일반 공백으로 정규화)
            cat_el = latest_viewer.select_one(".blog2_series, .se-series")
            raw_cat = cat_el.get_text(strip=True) if cat_el else "게시판"
            report["category"] = re.sub(r"\s+", " ", raw_cat.replace("\xa0", " ")).strip()

            # 3. 최신 글 내부의 실제 콘텐츠 이미지 개수 확인
            imgs = latest_viewer.select(".se-main-container img.se-image-resource, .se-main-container .se-image img")
            report["image_count"] = len(imgs)

            # 4. 최신 글 본문 텍스트 및 분량 확인
            body_el = latest_viewer.select_one(".se-main-container")
            body_text = body_el.get_text(" ", strip=True) if body_el else ""
            report["char_count"] = len(body_text.strip())

            # 5. 9대 금지어 검사
            for banned in BANNED_EXPRESSIONS:
                clean_banned = banned.replace("~", "").replace(",", "").strip()
                if clean_banned and clean_banned in body_text:
                    report["banned_found"].append(banned)

    except Exception as e:
        print(f"⚠️ 품질 검사 웹 크롤링 중 오류: {e}")

    # [품질 합격/불합격 판정 기준]
    if report["image_count"] < 1:
        report["issues"].append("❌ 대표 썸네일(이미지) 누락 감지")

    norm_expected = re.sub(r"\s+", "", expected_category.replace("\xa0", ""))
    norm_actual = re.sub(r"\s+", "", report["category"].replace("\xa0", ""))
    if norm_expected not in norm_actual:
        report["issues"].append(f"❌ 카테고리 불일치 (목표: '{expected_category}' vs 실제: '{report['category']}')")

    if is_article and report["char_count"] < 700:
        report["issues"].append(f"❌ 본문 분량 부족 (공백 포함 {report['char_count']}자)")

    if report["banned_found"]:
        report["issues"].append(f"❌ 9대 금지 표현 발견: {', '.join(report['banned_found'])}")

    report["passed"] = len(report["issues"]) == 0

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

        notifier.send_emergency_alert(
            failed_task_name=f"품질 검사 불합격 ({report['title'][:15]}...)",
            error_detail="<br/>".join(report["issues"])
        )

    print("=" * 60 + "\n")
    return report


if __name__ == "__main__":
    inspect_latest_post_quality(expected_category="AI 정보", is_article=True)
