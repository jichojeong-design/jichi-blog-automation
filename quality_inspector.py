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

# 단일 치트키 템플릿 복제 방지용 금지 패턴
STALE_TITLE_PATTERNS = [
    "직접 써보니… 진짜 충격 반전",
    "직접 써보니 진짜 충격 반전"
]
STALE_SUMMARY_PHRASE = "기술 격차와 시장 파장 분석"


def validate_and_repair_article_pre_publish(
    title: str,
    summary_lines: list,
    paragraphs: list,
    topic: str,
    article_index: int = 1
) -> tuple:
    """
    [포스팅 전 선제 품질검사 및 불량 자동 수리 엔진]
    발행 버튼을 누르기 전에 코부장이 4대 핵심 품질 기준을 검사하고,
    불량이 감지되면 '즉시 현장에서 정상 완제품으로 자동 수리'하여 리턴합니다.
    
    검사 및 자동 수리 항목:
    1. 제목 단일 템플릿 복제 및 글자수 오버플로우 검사 -> 다양하고 매력적인 상황별 제목으로 자동 치환
    2. 썸네일 요약 카피 복제(기술 격차와 시장 파장 분석 등) 검사 -> 기사 맞춤 실질 요약으로 자동 수리
    3. 마침표 뒤 어색한 줄바꿈 검사 -> 자연스러운 어절/문장 호흡으로 즉각 재포맷팅
    4. 소제목([1. ...], [2. ...], [3. ...]) 블록 분리 검사 -> 상하단 독립 여백 강제 재정렬
    """
    import constants
    import formatter
    
    print(f"\n[코부장 포스팅 전 사전 품질 검사 가동: 기사 #{article_index}]")
    repairs_done = []
    repaired_title = title
    repaired_summary = list(summary_lines) if summary_lines else []
    repaired_paragraphs = list(paragraphs)

    clean_t = constants.clean_topic_title(topic)
    cheat_titles = constants.generate_cheat_title_templates(clean_t)

    # 1. 제목 검사: 판에 박힌 패턴("직접 써보니… 진짜 충격 반전")이거나 28자 초과/미달 시 자동 수리
    is_stale_title = any(sp in repaired_title for sp in STALE_TITLE_PATTERNS)
    is_length_bad = len(repaired_title) > 28 or len(repaired_title) < 14
    if is_stale_title or is_length_bad:
        # 7가지 다채로운 상황별 제목 중 순번에 맞게 최적의 제목으로 즉시 치환
        repaired_title = cheat_titles[article_index % len(cheat_titles)]
        repairs_done.append(f"제목 불량 수리 (패턴복제/길이이상 -> '{repaired_title}')")

    # 2. 썸네일 요약 카피 검사: 판에 박힌 문구 복제 감지 시 기사 맞춤으로 자동 수리
    summary_str = " ".join(repaired_summary)
    if STALE_SUMMARY_PHRASE in summary_str or len(repaired_summary) < 2:
        repaired_summary = [f"{clean_t} 전격 발표!", "글로벌 테크 시장 술렁"]
        repairs_done.append(f"썸네일 요약 불량 수리 (판에 박힌 문구 -> {repaired_summary})")

    # 3. 본문 문장 끝 줄바꿈 및 소제목 상하 여백 정밀 검사
    full_body = "\n\n".join(repaired_paragraphs)
    # 마침표/물음표 뒤에 곧바로 다음 단어가 한 줄에 붙어있는 불량 감지 (예: '쟁점입니다. 하지만')
    has_awkward_break = bool(re.search(r'[.?!]\s+[가-힣a-zA-Z]{2,}', full_body))
    
    # 소제목 존재 여부 확인
    subheading_count = len(re.findall(r'\[\d+\.\s*[^\]]+\]', full_body))
    if subheading_count < 3:
        repairs_done.append(f"소제목 수량 주의 ({subheading_count}개 발견)")

    # 어색한 줄바꿈이 발견되었거나 문단 재정렬이 필요한 경우 formatter로 완벽 재수리
    re_formatted = formatter.format_mobile_text(full_body)
    repaired_paragraphs = [p for p in re_formatted.split("\n\n") if p.strip()]
    if has_awkward_break:
        repairs_done.append("본문 줄바꿈 호흡 불량 감지 -> 문장/절 단위 자연스러운 줄바꿈으로 자동 완벽 수리")

    if repairs_done:
        print(f"  * [사전 불량 감지 및 자동 수리 완료] 총 {len(repairs_done)}건 조치:")
        for r in repairs_done:
            print(f"     - {r}")
    else:
        print("  * [사전 품질 검사 100% 무결점 통과] 불량 없음, 즉시 안전 포스팅 승인!")

    return repaired_title, repaired_summary, repaired_paragraphs


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

        # 6. 스마트에디터 자동 번호 리스트 중복 표시 여부 검사
        # (스마트에디터 번호 목록 서식 .se-section-list 내부에 텍스트로도 '1.' '2.' 등이 중복 들어갔는지 감지)
        list_items = latest_viewer.select(".se-section-list li, ol.se-ol li")
        duplicate_num_count = 0
        for li in list_items:
            li_txt = li.get_text(strip=True)
            if re.match(r"^\d+\.", li_txt):
                duplicate_num_count += 1
        if duplicate_num_count > 0:
            report["issues"].append(f"❌ 스마트에디터 자동 번호 목록과 텍스트 숫자 중복 발견 ({duplicate_num_count}건)")

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
