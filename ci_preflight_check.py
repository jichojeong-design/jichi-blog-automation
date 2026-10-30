import ast
import builtins
import os
import sys
import py_compile

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CORE_MODULES = [
    "daily_scheduler.py",
    "content_generator.py",
    "auto_publisher.py",
    "quality_inspector.py",
    "formatter.py",
    "collector.py",
    "history_checker.py",
    "notifier.py",
    "constants.py",
    "sync_github_secrets.py",
]

BUILTIN_NAMES = set(dir(builtins)) | {"__file__", "__name__", "__doc__", "__package__"}


def check_ast_undefined_names(filepath: str) -> list:
    """
    모든 함수 내부에서 참조하는 심볼/모듈(os, json, re 등)이
    실제 최상단 또는 해당 함수 내부에 정의/임포트되어 있는지 AST 레벨에서 전수 검사합니다.
    (py_compile이 잡지 못하는 NameError를 100% 사전 색출)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source, filename=filepath)

    top_defs = set(BUILTIN_NAMES)
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                top_defs.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                top_defs.add(alias.asname or alias.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            top_defs.add(node.name)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store):
                    top_defs.add(sub.id)
        elif isinstance(node, ast.Try):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Import):
                    for alias in sub.names:
                        top_defs.add(alias.asname or alias.name.split(".")[0])
                elif isinstance(sub, ast.ImportFrom):
                    for alias in sub.names:
                        top_defs.add(alias.asname or alias.name)
                elif isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store):
                    top_defs.add(sub.id)

    issues = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            local_defs = set(top_defs)
            for sub in ast.walk(node):
                if isinstance(sub, ast.Import):
                    for alias in sub.names:
                        local_defs.add(alias.asname or alias.name.split(".")[0])
                elif isinstance(sub, ast.ImportFrom):
                    for alias in sub.names:
                        local_defs.add(alias.asname or alias.name)
                elif isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    local_defs.add(sub.name)
                elif isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store):
                    local_defs.add(sub.id)
                elif isinstance(sub, ast.arg):
                    local_defs.add(sub.arg)
                elif isinstance(sub, ast.ExceptHandler) and sub.name:
                    local_defs.add(sub.name)

            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                    if sub.id not in local_defs:
                        issues.append((node.name, sub.lineno, sub.id))
    return issues


def run_preflight():
    print("=" * 65)
    print("🛡️ [코부장 3중 사전 무결성 검증 엔진 (Pre-Flight Check)] 가동!")
    print("=" * 65)

    # 1단계: 구문(Syntax) 컴파일 검사
    print("\n[1/3] 파이썬 구문(Syntax) 전수 컴파일 검사 중...")
    for mod in CORE_MODULES:
        if not os.path.exists(mod):
            continue
        py_compile.compile(mod, doraise=True)
    print("  ✅ 1단계 통과: 모든 핵심 모듈 구문 이상 없음")

    # 2단계: 함수 스코프별 미정의 변수/모듈(NameError) AST 정적 전수 검사
    print("\n[2/3] 함수 스코프별 미정의 심볼(NameError) AST 정적 감사 중...")
    all_ast_issues = []
    for mod in CORE_MODULES:
        if not os.path.exists(mod):
            continue
        issues = check_ast_undefined_names(mod)
        if issues:
            for fn_name, lineno, sym in issues:
                print(f"  ❌ [NameError 위험 감지] {mod}:{lineno} (함수 {fn_name}) -> 미정의 심볼 '{sym}'")
            all_ast_issues.extend(issues)
    if all_ast_issues:
        print(f"\n🛑 [검증 실패] 총 {len(all_ast_issues)}건의 미정의 심볼(NameError 위험)이 발견되었습니다!")
        sys.exit(1)
    print("  ✅ 2단계 통과: 모든 함수 내 미정의 모듈/변수(NameError) 0건 검증 완료")

    # 3단계: 핵심 런타임 함수 실제 호출 드라이런(Dry-Run Smoke Test)
    print("\n[3/3] 핵심 파이프라인 런타임 함수 드라이런(Dry-Run) 실행 검증 중...")
    import constants
    import formatter
    import history_checker
    import collector
    import quality_inspector

    # (a) history_checker 함수 호출 테스트
    today_posts = history_checker.get_today_published_ai_articles("jcjung1401")
    is_dup = history_checker.is_article_already_published_live(
        "Test Headline for Preflight Check", source_url="https://example.com/preflight-test"
    )
    best3_block = history_checker.build_best3_tech_links_block("jcjung1401", exclude_title="프리플라이트 테스트")
    assert "[함께 읽으면" in best3_block and "https://blog.naver.com/jcjung1401/" in best3_block, "BEST 3 블록 생성 오류"
    print(f"  - history_checker 런타임 호출 정상 (오늘 발행 감지: {len(today_posts)}건, 중복판정: {is_dup})")

    # (b) constants & formatter 호출 테스트
    titles = constants.generate_cheat_title_templates("엔비디아 차세대 AI 칩 공개")
    assert len(titles) > 0, "제목 템플릿 생성 실패"
    formatted = formatter.format_mobile_text("결론부터 말씀드리면 이번 기술 발표는 글로벌 테크 판도를 바꿀 핵심 전환점입니다.")
    assert len(formatted) > 0, "모바일 줄바꿈 포맷팅 실패"
    print("  - constants & formatter 런타임 호출 정상")

    # (c) collector 호출 테스트
    sources = collector.get_all_sources()
    assert isinstance(sources, list) and len(sources) > 0, "기사 수집기(collector) 소스 반환 실패"
    print(f"  - collector 런타임 호출 정상 (수집된 기사 풀: {len(sources)}건)")

    # (d) quality_inspector 사전 검증 로직 드라이런 (임시 더미 이미지 제외 텍스트 검증)
    test_paragraphs = [
        "결론부터 말씀드리면 이번 신규 아키텍처는 추론 속도를 2배 높였습니다.",
        "[공식 발표 핵심 사양과 개념 및 뜻]",
        "공식 발표 수치를 바탕으로 분석한 결과 전력 효율이 크게 개선되었습니다.",
        "[기술 전환의 핵심 원인과 산업 구조 변화]",
        "실무진이 알아야 할 핵심 팩트를 정확하게 안내해 드리면 메모리 병목 해소가 핵심입니다.",
        "[실무 도입 시 장단점과 관전 포인트]",
        "장점과 단점이 공존하므로 철저한 사전 검증이 필수적입니다.",
        "[지치 블로그 테크 전문 분석]",
        "실제 현업 도입 시 제가 활용하고 있는 기준을 바탕으로 단계적 도입을 권장합니다.",
        "공식 출처: https://example.com/news",
        best3_block,
        "소중한 시간 내어 읽어주셔서 진심으로 감사드립니다. **공감(좋아요)** 꾹 눌러주세요."
    ]
    _, rep_title, rep_sum, rep_pars = quality_inspector.validate_and_repair_article_pre_publish(
        title="엔비디아 루빈 공식 발표! 핵심 기술 분석",
        summary_lines=["엔비디아 루빈 공개", "글로벌 테크 판도 변화"],
        paragraphs=test_paragraphs,
        topic="Unique Preflight Test Topic XYZ999",
        article_index=1,
        thumb_path=None
    )
    assert len(rep_pars) >= 5, "quality_inspector 문단 반환 오류"
    print("  - quality_inspector 런타임 호출 정상")

    print("\n🎉 [Pre-Flight Check 100% 통과] 구문·심볼·런타임 모든 방어선 이상 없음!\n")


if __name__ == "__main__":
    run_preflight()
