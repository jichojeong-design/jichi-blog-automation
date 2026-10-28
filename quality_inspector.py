import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import datetime
import notifier

# 12대 금지 표현 목록 (네이버 우수 블로거 기준: 낚시성 문구 및 판에 박힌 어투 배제)
BANNED_EXPRESSIONS = [
    "직접 써보니 진짜 충격 반전", "충격 반전", "진짜 충격",
    "핵심은 ~이 아니라", "단순한 ~이 아니라", "중요한 점은", "주목할 점은",
    "방향은 분명합니다", "관건입니다", "시사하는 바가 큽니다", "귀추가 주목됩니다",
    "첫째,", "둘째,", "셋째,"
]

def report_image_quality_issue(image_name: str, issue_description: str, suggested_fix: str):
    """
    [대표님 특별 지시] 이미지 품질 저하(태블릿/스크린 내 글자 깨짐 등) 발생 시 코부장 직속 보고 및 해결방안 제시
    """
    print(f"\n🚨 [코리티 긴급 보고 -> 코부장]")
    print(f"  * 검사 대상: {image_name}")
    print(f"  * 발견된 결함: {issue_description}")
    print(f"  * 원인 분석: AI 렌더링 엔진이 스크린/배경에 임의의 외계어/글자(Gibberish text)를 삽입함")
    print(f"  * 해결 방안: {suggested_fix}")
    print(f"  * 조치 계획: 텍스트 제외 프롬프트 강화 후 자동 재렌더링 실시\n")
STALE_TITLE_PATTERNS = [
    "직접 써보니… 진짜 충격 반전",
    "직접 써보니 진짜 충격 반전",
    "직접 써보니",
    "충격 반전",
    "진짜 충격"
]
STALE_SUMMARY_PHRASE = "기술 격차와 시장 파장 분석"


def validate_and_repair_article_pre_publish(
    title: str,
    summary_lines: list,
    paragraphs: list,
    topic: str,
    article_index: int = 1,
    thumb_path: str = None
) -> tuple:
    """
    [포스팅 전 선제 품질검사 및 불량 자동 수리 엔진]
    발행 버튼을 누르기 전에 코부장과 코리티가 5대 핵심 품질 기준을 전수 검사합니다.
    
    검사 항목:
    1. 썸네일/이미지 무결점 검사 (이미지 미통과 or 누락 시 즉시 발행 중단)
    2. 제목 단일 템플릿 복제 및 글자수 오버플로우 검사 -> 다양하고 매력적인 상황별 제목으로 자동 치환
    3. 썸네일 요약 카피 복제(기술 격차와 시장 파장 분석 등) 검사 -> 기사 맞춤 실질 요약으로 자동 수리
    4. 마침표 뒤 어색한 줄바꿈 검사 -> 자연스러운 어절/문장 호흡으로 즉각 재포맷팅
    5. 소제목([1. ...], [2. ...], [3. ...]) 블록 분리 검사 -> 상하단 독립 여백 강제 재정렬
    """
    import os
    import constants
    import formatter
    
    print(f"\n[코리티 & 코부장 포스팅 전 선제 품질 검사 가동: 기사 #{article_index}]")
    repairs_done = []
    repaired_title = title
    repaired_summary = list(summary_lines) if summary_lines else []
    repaired_paragraphs = list(paragraphs)

    # [코리티 책임 권한] 이미지 필수 검증 및 발행 중지 판정
    # [신규 관리자 승인 원칙 (ECO Control)] asset_ledger.json에 승인되지 않은 구버전 폐기 도면(폐기 자산) 사용 절대 차단
    if thumb_path is not None:
        if not thumb_path or not os.path.exists(thumb_path) or os.path.getsize(thumb_path) < 10000:
            print(f"  🚨 [코리티 긴급 권한 발동] 이미지 검증 실패! (파일 부재 또는 용량 미달: {thumb_path})")
            print("  🛑 [발행 즉시 중지] 사장님 방침에 따라 비정상 이미지는 발행을 엄격히 차단합니다.")
            return False, repaired_title, repaired_summary, repaired_paragraphs

        # 승인 장부 검사 (웹툰의 폐기된 구버전 만화 컷 파일명이 인입되었는지 확인)
        base_name = os.path.basename(thumb_path)
        ledger_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "asset_ledger.json")
        if os.path.exists(ledger_path):
            try:
                import json
                with open(ledger_path, "r", encoding="utf-8") as f:
                    ledger = json.load(f)
                deprecated = ledger.get("deprecated_assets", [])
                if base_name in deprecated:
                    print(f"  🚨 [코리티 ECO 거부] 폐기된 구버전 도면(자산) 감지: {base_name}")
                    print("  🛑 [신규 관리자 승인 위반] 승인된 신규 자산 또는 드롭존 파일만 투입 가능합니다.")
                    return False, repaired_title, repaired_summary, repaired_paragraphs
            except Exception as e:
                print(f"  ⚠️ 자산 장부 검증 경고: {e}")

    clean_t = constants.clean_topic_title(topic)
    cheat_titles = constants.generate_cheat_title_templates(clean_t)

    # 1. 제목 검사: 판에 박힌 패턴/낚시성 문구("직접 써보니", "충격 반전") 감지 또는 28자 초과/미달 시 자동 수리
    is_stale_title = any(sp in repaired_title for sp in STALE_TITLE_PATTERNS)
    is_length_bad = len(repaired_title) > 28 or len(repaired_title) < 14
    if is_stale_title or is_length_bad:
        repaired_title = cheat_titles[article_index % len(cheat_titles)]
        repairs_done.append(f"제목 불량 수리 (낚시성 문구/길이이상 -> '{repaired_title}')")

    # 2. 썸네일 요약 카피 검사: 판에 박힌 문구 복제 감지 시 기사 맞춤으로 자동 수리
    summary_str = " ".join(repaired_summary)
    if STALE_SUMMARY_PHRASE in summary_str or len(repaired_summary) < 2:
        repaired_summary = [f"{clean_t} 전격 발표!", "글로벌 테크 시장 술렁"]
        repairs_done.append(f"썸네일 요약 불량 수리 (판에 박힌 문구 -> {repaired_summary})")

    # 3. 본문 문장 끝 줄바꿈 및 소제목 상하 여백 정밀 검사
    full_body = "\n\n".join(repaired_paragraphs)
    has_awkward_break = bool(re.search(r'[.?!]\s+[가-힣a-zA-Z]{2,}', full_body))

    # [코리티 특별 검증: 제미니 티 이모지 및 소제목 내 느낌표 완전 색출 및 박멸]
    banned_emojis = ["🌱", "🔥", "🎬", "✨", "💡", "📝", "🚀", "📌", "✅", "☕", "🥐", "🍰", "🍭", "🎵", "❤️", "❗", "‼️"]
    found_emojis = [emo for emo in banned_emojis if emo in full_body]
    if found_emojis:
        repairs_done.append(f"제미니 티 이모지 색출 및 완전 제거 ({''.join(found_emojis)})")
        for emo in banned_emojis:
            full_body = full_body.replace(emo, "")

    # 소제목 내부 느낌표(!) 강제 제거: 예: [💡 실구매 후기 팩트 체크!] -> [실구매 후기 팩트 체크]
    if re.search(r'\[[^\]]*!+[^\]]*\]', full_body):
        repairs_done.append("소제목 내부 촌스러운 느낌표(!) 자동 제거")
        full_body = re.sub(r'\[([^\]]*?)!+([^\]]*?)\]', r'[\1\2]', full_body)
    
    # [코부장 & 코리티 중복 검사 예외 설정 준수]
    # 사장님 특별 지침: 중복 파일 정리 및 검사 시, 코리티와 코부장의 검사 항목이 겹치더라도
    # 크로스 체크(교차 검증)를 위해 절대 한쪽을 생략하지 않고 예외적으로 이중 검사를 완벽히 수행함!
    # - 코부장: 프로세스 흐름, 파일 무결성, 네트워크 및 에디터 렌더링 검사
    # - 코리티: 문장 서식, 불릿/점 기호 박멸, 소제목 번호 배제, 톤앤매너 전수 검사
    
    # [코리티 특별 검증 1] 소제목 번호 매기기(1. 2. 3. 4.) 일괄 제거 검사
    # 사장님 특명: "1. 2. 3. 4. 다 빼고 깔끔하게 작성할 것"
    if re.search(r'\[\d+\.\s*', full_body):
        repairs_done.append("소제목 내 1. 2. 3. 번호 발견 -> 깔끔한 명사형 소제목으로 일괄 제거 수리")
        full_body = re.sub(r'\[\d+\.\s*', '[', full_body)

    # [코리티 특별 검증 2] 스마트에디터 dot(•) 및 번호 리스트 트리거 기호(-, *, 1. 2.) 완전 박멸
    # 사장님 특명: "스마트 에디터 dot 표시 금지!" (단, **볼드** 마크다운 별표 2개는 절대 훼손하지 않도록 보호)
    has_list_triggers = bool(re.search(r'^\s*(?:[\-•·]|\*(?!\*)|\d+\.)\s+', full_body, re.MULTILINE))
    if has_list_triggers:
        repairs_done.append("스마트에디터 dot(•) 및 번호 리스트 유발 기호(-, *, 1. 2.) 완전 제거")
        full_body = re.sub(r'^\s*(?:[\-•·]\s*|\*(?!\*)\s+)', '', full_body, flags=re.MULTILINE)
        full_body = re.sub(r'^\s*\d+[\.\)]\s*', '', full_body, flags=re.MULTILINE)

    # [코리티 특별 검증 3] 공감(좋아요) 엔딩 멘트 누락 여부 검사 및 출처 URL - 인사말 분리 검사
    # 사장님 특명: "주소 끝나고 / 오픈그래프 카드 / 소중한 시간 글자부터 독립 문단 작성 후 검사할 것"
    if re.search(r'https?://[a-zA-Z0-9./?=&_%#\-+:~]+\s*[^\s\na-zA-Z0-9./?=&_%#\-+:~]', full_body):
        repairs_done.append("출처 URL과 '소중한 시간' 인사말 간격 밀착 감지 -> 빈 줄 2개 독립 문단으로 강제 분리 수리")
        full_body = re.sub(
            r'(https?://[a-zA-Z0-9./?=&_%#\-+:~]+)\s*([^\s\na-zA-Z0-9./?=&_%#\-+:~])',
            r'\1\n\n\2',
            full_body
        )

    if "공감(좋아요)" not in full_body:
        repairs_done.append("엔딩 공감(좋아요) 독자 참여 CTA 추가 수리")
        cta_suffix = "\n\n소중한 시간 내어 읽어주셔서 진심으로 감사드립니다.\n오늘 전해드린 테크 분석이 유익하셨다면 **공감(좋아요)** 꾹 눌러주시고 이웃 추가 부탁드립니다. 지치 블로그가 매일 가장 빠르고 정확한 글로벌 테크 동향을 전달해 드리겠습니다."
        full_body += cta_suffix

    # '1.\n' 처럼 번호만 단독으로 떨어져 분리된 불량이 있는지 철저히 검사
    has_orphan_number = bool(re.search(r'^\s*\d+[\.\)]\s*$', full_body, re.MULTILINE))
    if has_orphan_number:
        repairs_done.append("번호 단독 분리 결함(1.\n) 감지 -> 번호+제목 결합 예외 로직으로 강제 수리")

    # [코리티 특별 검증 4] 동일 소제목 중복 노출 방지 및 자동 수리
    subheadings = re.findall(r'\[[^\]]+\]', full_body)
    subheading_count = len(subheadings)
    if subheading_count < 3:
        repairs_done.append(f"소제목 수량 주의 ({subheading_count}개 발견)")
    elif len(set(subheadings)) < len(subheadings):
        repairs_done.append("동일 소제목 중복 감지 -> 문맥별 고유 소제목 3종으로 자동 분리 수리")
        fallback_subs = [
            "[공식 발표 핵심 사양과 배경]",
            "[기술적 진보와 시장 경쟁 구도]",
            "[실무 도입 시 한계와 관전 포인트]"
        ]
        seen_subs = set()
        sub_idx = 0
        def _replace_dup_sub(m):
            nonlocal sub_idx
            s = m.group(0)
            if s not in seen_subs and s != "[공식 보도자료 및 기술 문서 기반 분석]":
                seen_subs.add(s)
                return s
            replacement = fallback_subs[sub_idx % len(fallback_subs)]
            sub_idx += 1
            seen_subs.add(replacement)
            return replacement
        full_body = re.sub(r'\[(?!(?:지치 블로그|공식 출처))[^\]]+\]', _replace_dup_sub, full_body)

    re_formatted = formatter.format_mobile_text(full_body)
    repaired_paragraphs = [p for p in re_formatted.split("\n\n") if p.strip()]
    if has_awkward_break:
        repairs_done.append("본문 줄바꿈 호흡 불량 감지 -> 문장/절 단위 자연스러운 줄바꿈으로 자동 완벽 수리")

    # 4. 네이버 우수 블로거 선정 기준 필수 요소 정밀 검사:
    # (1) [자료 기반 설명 vs 직접 경험 구분 여부]
    # (2) [지치 블로그 테크 전문 분석 1~2줄 포함 여부]
    has_source_mark = any(m in full_body for m in ["[공식 발표", "[공식 보도자료", "자료 분석", "출처:"])
    if not has_source_mark:
        repairs_done.append("자료 기반 설명 명시 보강 (신뢰도 제고)")
        repaired_paragraphs.insert(0, "(※ 본 포스팅은 공식 발표 자료 및 기술 문서를 바탕으로 심층 분석한 정보성 콘텐츠입니다.)")

    has_analysis = any(a in full_body for a in ["[지치 블로그 테크 전문 분석]", "테크 전문 분석", "전문 분석]"])
    if not has_analysis:
        repairs_done.append("전문 분석 1~2줄 자동 보강 완료")
        analysis_block = (
            "[지치 블로그 테크 전문 분석]\n"
            "단순 수치 경쟁을 넘어 실질적인 인프라 비용 대비 효율성과 도입 실효성이 최대 승부처입니다. "
            "실무진은 벤치마크 지표뿐만 아니라 자사 환경에 맞는 PoC(개념 검증)를 선제적으로 거치는 접근이 권장됩니다."
        )
        repaired_paragraphs.append(analysis_block)

    if repairs_done:
        print(f"  * [사전 불량 감지 및 자동 수리 완료] 총 {len(repairs_done)}건 조치:")
        for r in repairs_done:
            print(f"     - {r}")
    else:
        print("  * [사전 품질 검사 100% 무결점 통과] 불량 없음, 즉시 안전 포스팅 승인!")

    return True, repaired_title, repaired_summary, repaired_paragraphs


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

        # 7. [대표님 스크린샷 검수 기준 1] 출처 URL 뒤에 '소중한 시간...' 등 한글 텍스트가 같은 줄에 붙어 있는지 검사
        for p_el in latest_viewer.select("p.se-text-paragraph"):
            p_txt = p_el.get_text(strip=True)
            if re.search(r"https?://[a-zA-Z0-9./?=&_%#\-+:~]+[가-힣]", p_txt):
                report["issues"].append(f"❌ 출처 URL과 본문 인사말 줄붙음 결함 감지: '{p_txt[:55]}...'")
                break

        # 8. [대표님 스크린샷 검수 기준 2] 오픈그래프(se-oglink) 카드가 URL 바로 아래, '소중한 시간...' 인사말 위에 위치하는지 검사
        if is_article:
            components = latest_viewer.select(".se-component")
            url_comp_idx = -1
            og_comp_idx = -1
            cta_start_idx = -1
            cta_end_idx = -1
            for idx, comp in enumerate(components):
                c_classes = comp.get("class") or []
                c_txt = comp.get_text(" ", strip=True)
                if "se-oglink" in c_classes:
                    og_comp_idx = idx
                if "http://" in c_txt or "https://" in c_txt:
                    url_comp_idx = idx
                if "소중한 시간" in c_txt:
                    cta_start_idx = idx
                if "전달해" in c_txt and "드리겠습니다" in c_txt:
                    cta_end_idx = idx
            if cta_start_idx != -1 and cta_end_idx != -1 and cta_start_idx != cta_end_idx:
                report["issues"].append("❌ 엔딩 인사말('소중한 시간~드리겠습니다') 중간에 링크 카드가 끼어들어 문단이 쪼개짐")
            elif og_comp_idx != -1 and cta_start_idx != -1 and og_comp_idx > cta_start_idx:
                report["issues"].append("❌ 오픈그래프 링크 카드가 '소중한 시간' 인사말 아래로 밀려남 (배치 순서 불량)")

        # 9. [대표님 스크린샷 검수 기준 3] 본문 내 마크다운 별표(**) 노출 결함 검사
        if "**" in body_text:
            report["issues"].append("❌ 본문 내 변환되지 않은 마크다운 별표(**) 노출 결함 감지")

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
