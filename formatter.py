import re
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import os


def format_mobile_text(text: str, max_chars: int = 18) -> str:
    """
    [웹툰 전용] 모바일 최적화 및 자연스러운 한국어 문맥 줄바꿈 (파워블로그 16~18자 가독성 규격):
    [사장님 엄격 규정 3대 원칙]
    1. 소제목 번호매김 절대 금지! ([1. 소제목] -> [소제목]으로 자동 정제)
    2. 스마트에디터 dot(•) 및 번호 리스트 트리거 문자(-, *, 1. 2.) 원천 차단!
    3. 온점(.), 물음표(?), 느낌표(!) 기준으로 자연스러운 호흡 부여
    4. [RED], [BLUE], [MINT], [PURPLE], [HL_SKY], [HL_YELLOW] 등 컬러/형광펜 강조 태그 완벽 보존
    """
    if not text:
        return ""

    # 이미 매거진 전용 마커([HOOK], [SUMMARY_BOX], [QUOTE], [SUB])가 포함된 AI 기사 원고인 경우
    # 18자 강제 절단(영수증 현상)을 하지 않고 매거진 포맷터로 자동 위임합니다!
    if any(m in text for m in ["[HOOK]", "[SUMMARY_BOX]", "[QUOTE]", "[SUB]", "▎"]):
        return format_magazine_article_text(text)

    # 0. 컬러 태그들을 임시 플레이스홀더로 보호 (소제목 대괄호 정규식에 걸리지 않도록 방지)
    color_names = ["RED", "BLUE", "MINT", "PURPLE", "HL_SKY", "HL_YELLOW"]
    for cname in color_names:
        text = re.sub(rf'\[{cname}\](.*?)\[/{cname}\]', rf'⟪{cname}⟫\1⟪/{cname}⟫', text, flags=re.DOTALL)

    # 1. 소제목 내 번호 매김 완전 제거 ([1. ...] -> [...])
    text = re.sub(r'\[\s*\d+[\.\)]\s*', '[', text)
    # 소제목 태그 앞뒤에 명확한 문단 구분자 삽입
    text = re.sub(r'(\[[^\]]+\])', r'\n\n\1\n\n', text)

    # [사장님 특명: 주소 끝난 후 및 '소중한 시간' 앞뒤 확실한 독립 문단/빈 줄 분리]
    text = re.sub(r'공식\s*\n+\s*출처:', '공식 출처:', text)
    text = re.sub(r'([^\n])\s*(?<!공식\s)(?<!공식)(공식\s*출처:|출처:)', r'\1\n\n\2', text)
    text = re.sub(r'(공식\s*출처:|출처:)\s*(https?://[^\s\n]+)', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])\s*(https?://[a-zA-Z0-9./?=&_%#\-+:=~]+)', r'\1\n\n\2', text)
    text = re.sub(r'(https?://[a-zA-Z0-9./?=&_%#\-+:=~]+)\s*([^\s\na-zA-Z0-9./?=&_%#\-+:=~])', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])\s*(소중한\s*시간)', r'\1\n\n\2', text)

    paragraphs = re.split(r'\n\s*\n', text.strip())
    formatted_paragraphs = []

    for para in paragraphs:
        para_clean = para.strip()
        if not para_clean:
            continue

        if para_clean.startswith("__IMAGE__:"):
            formatted_paragraphs.append(para_clean)
            continue

        # 대괄호 소제목인 경우 줄바꿈 없이 깔끔하게 단독 문단으로 유지
        if re.match(r'^\[[^\]]+\]$', para_clean):
            clean_sub = re.sub(r'\[\s*\d+[\.\)]\s*', '[', para_clean)
            formatted_paragraphs.append(clean_sub)
            continue

        # 단독 출처 레이블이나 URL은 원형 그대로 보존
        if para_clean in ("공식 출처:", "출처:") or re.match(r'^https?://\S+$', para_clean):
            formatted_paragraphs.append(para_clean)
            continue

        cleaned_lines = []
        for raw_line in para_clean.split('\n'):
            line_s = raw_line.strip()
            if not line_s:
                continue
            line_s = re.sub(r'^(?:[\-•·]\s*|\*(?!\*)\s+)', '', line_s)
            line_s = re.sub(r'^\d+[\.\)]\s*', '', line_s)
            line_s = line_s.strip()
            if line_s:
                cleaned_lines.append(line_s)

        if not cleaned_lines:
            continue

        para_clean = " ".join(cleaned_lines)

        # 볼드 마크다운(**) 짝맞춤 정제
        para_clean = re.sub(r'\*\*([^\*\n]+?)\*\*', r'⟪B⟫\1⟪/B⟫', para_clean)
        para_clean = para_clean.replace('*', '')
        para_clean = para_clean.replace('⟪B⟫', '**').replace('⟪/B⟫', '**')

        # 문장 단위 분리 (. ? !)
        raw_sentences = re.split(r'((?<!\d)[.?!]\s+)', para_clean)
        sentences = []
        for i in range(0, len(raw_sentences) - 1, 2):
            sentences.append(raw_sentences[i] + raw_sentences[i+1].rstrip())
        if len(raw_sentences) % 2 == 1 and raw_sentences[-1]:
            sentences.append(raw_sentences[-1])

        lines = []
        for s in sentences:
            s_clean = " ".join(s.split())
            if not s_clean:
                continue

            clean_len = len(re.sub(r'\*\*|⟪/?(?:RED|BLUE|MINT|PURPLE|HL_SKY|HL_YELLOW)⟫', '', s_clean))
            if clean_len <= max_chars + 2:
                lines.append(s_clean)
                continue

            clauses = re.split(r'(,\s+)', s_clean)
            clause_list = []
            for j in range(0, len(clauses) - 1, 2):
                clause_list.append(clauses[j] + clauses[j+1].rstrip())
            if len(clauses) % 2 == 1 and clauses[-1]:
                clause_list.append(clauses[-1])

            current_line = ""
            for c in clause_list:
                words = c.split()
                for word in words:
                    is_url = word.startswith(("http://", "https://", "www."))
                    word_len = len(re.sub(r'\*\*|⟪/?(?:RED|BLUE|MINT|PURPLE|HL_SKY|HL_YELLOW)⟫', '', word))
                    cur_clean_len = len(re.sub(r'\*\*|⟪/?(?:RED|BLUE|MINT|PURPLE|HL_SKY|HL_YELLOW)⟫', '', current_line))
                    if not current_line:
                        if word_len > max_chars and not is_url:
                            for k in range(0, len(word), max_chars):
                                lines.append(word[k:k+max_chars])
                        else:
                            current_line = word
                    else:
                        if cur_clean_len + 1 + word_len <= max_chars:
                            current_line += " " + word
                        else:
                            lines.append(current_line)
                            current_line = word
                cur_clean_len = len(re.sub(r'\*\*|⟪/?(?:RED|BLUE|MINT|PURPLE|HL_SKY|HL_YELLOW)⟫', '', current_line))
                if c.endswith(",") and cur_clean_len >= 12:
                    lines.append(current_line)
                    current_line = ""
            if current_line:
                lines.append(current_line)

        # [줄바꿈으로 인해 **볼드** 및 컬러 태그 구간이 나뉜 경우 각 줄마다 완벽 짝맞춤]
        balanced_lines = []
        in_bold = False
        active_color = None
        for ln in lines:
            if in_bold:
                ln = "**" + ln
            if active_color:
                ln = f"⟪{active_color}⟫" + ln

            for cname in color_names:
                c_opens = ln.count(f"⟪{cname}⟫")
                c_closes = ln.count(f"⟪/{cname}⟫")
                if active_color == cname:
                    if c_closes > c_opens - 1:
                        active_color = None
                    else:
                        ln = ln + f"⟪/{cname}⟫"
                        active_color = cname
                else:
                    if c_opens > c_closes:
                        ln = ln + f"⟪/{cname}⟫"
                        active_color = cname

            if ln.count("**") % 2 == 1:
                ln = ln + "**"
                in_bold = True
            else:
                in_bold = False

            balanced_lines.append(ln)

        formatted_paragraphs.append("\n".join(balanced_lines))

    result_text = "\n\n".join(formatted_paragraphs)
    for cname in color_names:
        result_text = result_text.replace(f"⟪{cname}⟫", f"[{cname}]").replace(f"⟪/{cname}⟫", f"[/{cname}]")
    return result_text


def format_magazine_article_text(text: str) -> str:
    """
    [AI 정보 기사 전용 - ACE ETF급 매거진 에디토리얼 포맷터]
    - 기존의 18자 강제 줄바꿈(세로 영수증 현상)을 전면 폐지!
    - [HOOK], [SUMMARY_BOX], [QUOTE], [SUB], __IMAGE__: 등 매거진 컴포넌트 마커를 그대로 보존합니다.
    - 일반 해설 문단은 표준 가로 문단 폭(왼쪽 정렬용)으로 자연스럽게 유지하되,
      스마트에디터 dot(•) 및 번호 리스트(1. 2.) 트리거만 안전하게 제거합니다.
    """
    if not text:
        return ""

    # 출처 및 URL 앞뒤 독립 문단 보장
    text = re.sub(r'공식\s*\n+\s*출처:', '공식 출처:', text)
    text = re.sub(r'([^\n])\s*(?<!공식\s)(?<!공식)(공식\s*출처:|출처:)', r'\1\n\n\2', text)
    text = re.sub(r'(공식\s*출처:|출처:)\s*(https?://[^\s\n]+)', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])\s*(https?://[a-zA-Z0-9./?=&_%#\-+:=~]+)', r'\1\n\n\2', text)
    text = re.sub(r'(https?://[a-zA-Z0-9./?=&_%#\-+:=~]+)\s*([^\s\na-zA-Z0-9./?=&_%#\-+:=~])', r'\1\n\n\2', text)
    text = re.sub(r'([^\n])\s*(소중한\s*시간)', r'\1\n\n\2', text)

    raw_blocks = re.split(r'\n\s*\n', text.strip())
    out_blocks = []

    for block in raw_blocks:
        b = block.strip()
        if not b:
            continue

        # 1. 이미지 마커, 매거진 구조 마커([HOOK], [SUMMARY_BOX], [QUOTE], [SUB]), 단독 URL은 원형 보존
        if (
            b.startswith("__IMAGE__:")
            or b.startswith("[HOOK]")
            or b.startswith("[SUMMARY_BOX]")
            or b.startswith("[QUOTE]")
            or b.startswith("[SUB]")
            or b.startswith("▎")
            or b in ("공식 출처:", "출처:")
            or re.match(r'^https?://\S+$', b)
        ):
            out_blocks.append(b)
            continue

        # 2. 구형 대괄호 소제목([소제목])이 들어온 경우 매거진 버티컬 바 소제목([SUB]▎ 소제목[/SUB])으로 승격
        if re.match(r'^\[(?!(?:RED|BLUE|MINT|PURPLE|HL_SKY|HL_YELLOW))[^\]]+\]$', b):
            inner_sub = b[1:-1].strip()
            inner_sub = re.sub(r'^\d+[\.\)]\s*', '', inner_sub).strip()
            if inner_sub.startswith("▎"):
                out_blocks.append(f"[SUB]{inner_sub}[/SUB]")
            else:
                out_blocks.append(f"[SUB]▎ {inner_sub}[/SUB]")
            continue

        # 3. 일반 본문 문단: 스마트에디터 리스트 트리거(-, *, 1.) 제거 후 깔끔한 문장 단위 호흡 유지
        cleaned_lines = []
        for raw_ln in b.split("\n"):
            ln = raw_ln.strip()
            if not ln:
                continue
            ln = re.sub(r'^(?:[\-•·]\s*|\*(?!\*)\s+)', '', ln)
            ln = re.sub(r'^\d+[\.\)]\s*', '', ln)
            if ln:
                cleaned_lines.append(ln)

        if not cleaned_lines:
            continue

        # 엔딩 인사말이나 짧은 슬로건처럼 이미 의도적으로 줄바꿈된 블록은 줄바꿈 유지,
        # 긴 해설 문단은 자연스러운 이어쓰기(문단 통일감) 제공
        joined = " ".join(cleaned_lines)
        joined = re.sub(r'\*\*([^\*\n]+?)\*\*', r'⟪B⟫\1⟪/B⟫', joined)
        joined = joined.replace('*', '')
        joined = joined.replace('⟪B⟫', '**').replace('⟪/B⟫', '**')
        out_blocks.append(joined)

    return "\n\n".join(out_blocks)


def create_rounded_mask(size, radius):
    """지정된 크기와 반경의 둥근 모서리 마스크 생성"""
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask


def _get_korean_font(size: int, bold: bool = False):
    """시스템 내 고화질 한글 고딕 폰트 로드"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = []
    if bold:
        candidates = [
            "C:/Windows/Fonts/malgunbd.ttf",
            os.path.join(base_dir, "NanumGothicBold.ttf"),
            "C:/Windows/Fonts/NanumGothicBold.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/malgun.ttf",
            os.path.join(base_dir, "NanumGothicBold.ttf"),
            "C:/Windows/Fonts/malgunbd.ttf",
        ]
    for fp in candidates:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _wrap_text_by_pixel(draw, text: str, font, max_width: int) -> list:
    """지정된 픽셀 폭(max_width) 안에 들어오도록 어절/글자 단위로 깔끔하게 줄바꿈"""
    if not text:
        return [""]
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip() if cur else w
        if draw.textlength(test, font=font) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            # 단어 자체가 max_width보다 긴 경우 글자 단위로 분할
            if draw.textlength(w, font=font) > max_width:
                sub = ""
                for ch in w:
                    if draw.textlength(sub + ch, font=font) <= max_width:
                        sub += ch
                    else:
                        if sub:
                            lines.append(sub)
                        sub = ch
                cur = sub
            else:
                cur = w
    if cur:
        lines.append(cur)
    return lines if lines else [""]


def generate_infographic_table_card(
    card_title: str,
    metric_banner: dict,
    table_headers: list,
    table_rows: list,
    output_path: str = "infographic_card.png",
    source_note: str = "*자료: 공식 발표 및 지치 테크 리서치 종합 분석"
) -> str:
    """
    [ACE ETF 스타일 본문 중간 삽입용 고해상도 인포그래픽 & 비교표 이미지 생성기]
    - 상단: [핵심 분석 타이틀] + 핵심 지표 하이라이트 배너 (Before -> After / 핵심 수치 뱃지)
    - 중단: 3열 구조화 비교표 (구분 | 핵심 사양 및 팩트 | 산업·실무 파장)
    - 하단: 자료 출처 캡션
    """
    width = 1200
    # 행 개수와 줄바꿈 분량에 맞춰 동적으로 높이 계산
    f_title = _get_korean_font(28, bold=True)
    f_banner_lbl = _get_korean_font(20, bold=True)
    f_banner_val = _get_korean_font(26, bold=True)
    f_th = _get_korean_font(21, bold=True)
    f_td_bold = _get_korean_font(20, bold=True)
    f_td = _get_korean_font(19, bold=False)
    f_caption = _get_korean_font(16, bold=False)

    dummy_img = Image.new("RGB", (width, 200))
    dummy_draw = ImageDraw.Draw(dummy_img)

    col_widths = [220, 440, 440]  # 총 1100px (좌우 여백 50px씩)
    table_x = 50

    if not table_headers or len(table_headers) < 3:
        table_headers = ["핵심 구분", "주요 발표 팩트 및 수치", "시장 및 실무 파장"]

    if not table_rows:
        table_rows = [
            ["핵심 배경", "차세대 기술 아키텍처 전환 및 대규모 투자 단행", "글로벌 빅테크 주도권 경쟁 본격화"],
            ["주요 지표", "연산 효율 및 처리 성능 대폭 개선, 비용 구조 혁신", "엔터프라이즈 도입 장벽 완화 기대"],
            ["리스크 요인", "국가별 규제 장벽 및 인프라 전환 초기 비용 존재", "도입 전 실무 PoC 및 규제 점검 필수"],
        ]

    # 각 행의 줄바꿈 및 높이 사전 계산
    processed_rows = []
    total_rows_h = 0
    for r in table_rows[:4]:
        c0 = str(r[0]) if len(r) > 0 else ""
        c1 = str(r[1]) if len(r) > 1 else ""
        c2 = str(r[2]) if len(r) > 2 else ""
        w0 = _wrap_text_by_pixel(dummy_draw, c0, f_td_bold, col_widths[0] - 32)
        w1 = _wrap_text_by_pixel(dummy_draw, c1, f_td, col_widths[1] - 36)
        w2 = _wrap_text_by_pixel(dummy_draw, c2, f_td, col_widths[2] - 36)
        max_lines = max(len(w0), len(w1), len(w2), 1)
        row_h = max(72, max_lines * 30 + 32)
        processed_rows.append((w0, w1, w2, row_h))
        total_rows_h += row_h

    header_h = 58
    banner_h = 118
    top_margin = 40
    title_h = 55
    bottom_margin = 65

    height = top_margin + title_h + banner_h + 28 + header_h + total_rows_h + bottom_margin
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # 외곽 은은한 카드 보더
    draw.rounded_rectangle([(12, 12), (width - 13, height - 13)], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

    # 1. 최상단 [핵심 분석 타이틀] (ACE ETF 스타일 대괄호 센터 타이틀)
    clean_card_title = card_title.strip()
    if not clean_card_title.startswith("["):
        clean_card_title = f"[{clean_card_title}]"
    draw.text((width // 2, top_margin + 18), clean_card_title, fill=(15, 23, 42), font=f_title, anchor="mm")

    # 2. 상단 Key Metric Callout 배너 (연한 아이스 블루 박스 + 로열 블루 핵심 뱃지)
    banner_y = top_margin + title_h
    draw.rounded_rectangle(
        [(table_x, banner_y), (table_x + 1100, banner_y + banner_h)],
        radius=16,
        fill=(240, 246, 255),
        outline=(191, 219, 254),
        width=2
    )

    m_label = (metric_banner or {}).get("label", "핵심 관전 지표")
    m_main = (metric_banner or {}).get("main_value", "글로벌 AI·테크 패러다임 전환")
    m_sub = (metric_banner or {}).get("sub_value", "기술 효율성 극대화 vs 규제·수익성 검증")

    # 좌측 로열 블루 필(Pill) 뱃지
    badge_x1, badge_y1 = table_x + 28, banner_y + 22
    badge_x2, badge_y2 = table_x + 260, banner_y + banner_h - 22
    draw.rounded_rectangle([(badge_x1, badge_y1), (badge_x2, badge_y2)], radius=36, fill=(29, 78, 216))
    draw.text(((badge_x1 + badge_x2) // 2, (badge_y1 + badge_y2) // 2), m_label[:10], fill=(255, 255, 255), font=f_banner_lbl, anchor="mm")

    # 우측 핵심 지표 텍스트 2줄
    draw.text((badge_x2 + 28, banner_y + 38), m_main[:42], fill=(15, 23, 42), font=f_banner_val, anchor="lm")
    draw.text((badge_x2 + 28, banner_y + 80), m_sub[:52], fill=(51, 65, 85), font=f_td, anchor="lm")

    # 3. 3열 비교표(Table) 렌더링
    table_y = banner_y + banner_h + 24

    # 테이블 헤더 배경 (ACE ETF 스타일 소프트 틸/네이비 헤더)
    draw.rounded_rectangle(
        [(table_x, table_y), (table_x + 1100, table_y + header_h)],
        radius=8,
        fill=(30, 58, 138)
    )
    # 상단 모서리만 둥글게 보이도록 하단 절반 직사각형 덮기
    draw.rectangle([(table_x, table_y + header_h - 10), (table_x + 1100, table_y + header_h)], fill=(30, 58, 138))

    cur_x = table_x
    for idx, th_text in enumerate(table_headers[:3]):
        cw = col_widths[idx]
        draw.text((cur_x + cw // 2, table_y + header_h // 2), str(th_text), fill=(255, 255, 255), font=f_th, anchor="mm")
        if idx > 0:
            draw.line([(cur_x, table_y + 10), (cur_x, table_y + header_h - 10)], fill=(96, 165, 250), width=1)
        cur_x += cw

    # 테이블 데이터 행
    cur_y = table_y + header_h
    for r_idx, (w0, w1, w2, row_h) in enumerate(processed_rows):
        bg_color = (255, 255, 255) if r_idx % 2 == 0 else (248, 250, 252)
        draw.rectangle([(table_x, cur_y), (table_x + 1100, cur_y + row_h)], fill=bg_color)

        # 1열(구분)은 은은한 블루그레이 틴트 배경으로 가독성 강화
        draw.rectangle([(table_x, cur_y), (table_x + col_widths[0], cur_y + row_h)], fill=(241, 245, 249))

        # 세로 구분선
        x1 = table_x + col_widths[0]
        x2 = x1 + col_widths[1]
        draw.line([(x1, cur_y), (x1, cur_y + row_h)], fill=(203, 213, 225), width=1)
        draw.line([(x2, cur_y), (x2, cur_y + row_h)], fill=(203, 213, 225), width=1)

        # 가로 하단 구분선
        draw.line([(table_x, cur_y + row_h), (table_x + 1100, cur_y + row_h)], fill=(203, 213, 225), width=1)

        # 텍스트 렌더링 (수직 중앙 정렬)
        def _draw_cell_lines(lines_list, cell_x, cell_w, cell_y, cell_h, font_obj, color, center=False):
            line_step = 28
            total_text_h = len(lines_list) * line_step
            start_y = cell_y + (cell_h - total_text_h) // 2 + line_step // 2
            for l_i, ln_str in enumerate(lines_list):
                if center:
                    draw.text((cell_x + cell_w // 2, start_y + l_i * line_step), ln_str, fill=color, font=font_obj, anchor="mm")
                else:
                    draw.text((cell_x + 20, start_y + l_i * line_step), ln_str, fill=color, font=font_obj, anchor="lm")

        _draw_cell_lines(w0, table_x, col_widths[0], cur_y, row_h, f_td_bold, (30, 58, 138), center=True)
        _draw_cell_lines(w1, x1, col_widths[1], cur_y, row_h, f_td, (15, 23, 42), center=False)
        _draw_cell_lines(w2, x2, col_widths[2], cur_y, row_h, f_td_bold, (29, 78, 216), center=False)

        cur_y += row_h

    # 테이블 외곽 테두리 마감
    draw.rectangle([(table_x, table_y), (table_x + 1100, cur_y)], outline=(148, 163, 184), width=2)

    # 4. 하단 출처 캡션
    draw.text((width // 2, cur_y + 28), source_note, fill=(100, 116, 139), font=f_caption, anchor="mm")

    img.save(output_path, "PNG")
    return output_path


def generate_dynamic_tech_illustration(topic: str, output_path: str, article_index: int = 1) -> str:
    """
    Gemini Image API 일시 지연 시 워터마크나 중복 폴백(파란 소용돌이/지구본)을 쓰지 않고,
    기사 주제 해시 기반으로 고유한 네온 글래스모피즘 3D 스타일 테크 아트워크(1024x1024)를 즉시 생성합니다.
    """
    size = 1024
    seed_val = sum(ord(c) * (i + 1) for i, c in enumerate(topic or "tech")) + article_index * 137

    palettes = [
        ((10, 25, 55), (20, 90, 185), (56, 189, 248), (167, 243, 208)),
        ((22, 16, 52), (88, 28, 135), (192, 132, 252), (56, 189, 248)),
        ((8, 35, 48), (13, 148, 136), (45, 212, 191), (253, 224, 71)),
        ((28, 25, 54), (37, 99, 235), (96, 165, 250), (244, 114, 182)),
    ]
    c_bg1, c_bg2, c_accent1, c_accent2 = palettes[seed_val % len(palettes)]

    img = Image.new("RGBA", (size, size), c_bg1 + (255,))
    draw = ImageDraw.Draw(img)

    # 부드러운 대각선 그라데이션 배경
    for y in range(size):
        ratio = y / float(size)
        r = int(c_bg1[0] * (1 - ratio) + c_bg2[0] * ratio)
        g = int(c_bg1[1] * (1 - ratio) + c_bg2[1] * ratio)
        b = int(c_bg1[2] * (1 - ratio) + c_bg2[2] * ratio)
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # 은은한 미래지향적 그리드 라인
    grid_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grid_layer)
    for x in range(64, size, 96):
        g_draw.line([(x, 0), (x, size)], fill=c_accent1 + (28,), width=1)
    for y in range(64, size, 96):
        g_draw.line([(0, y), (size, y)], fill=c_accent1 + (28,), width=1)

    # 발광 오브(Glowing Orbs) & 네트워크 노드
    orb_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(orb_layer)
    nodes = []
    for idx in range(7):
        angle = (seed_val + idx * 52) * math.pi / 180.0
        dist = 180 + (idx % 3) * 95
        nx = int(size // 2 + math.cos(angle) * dist)
        ny = int(size // 2 + math.sin(angle) * dist)
        nodes.append((nx, ny))
        rad = 55 + (idx % 3) * 28
        col = c_accent1 if idx % 2 == 0 else c_accent2
        o_draw.ellipse([(nx - rad, ny - rad), (nx + rad, ny + rad)], fill=col + (95,))

    orb_layer = orb_layer.filter(ImageFilter.GaussianBlur(radius=32))
    img = Image.alpha_composite(img, grid_layer)
    img = Image.alpha_composite(img, orb_layer)

    # 노드 연결 신경망 라인 & 크리스탈 코어
    net_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    n_draw = ImageDraw.Draw(net_layer)
    center_pt = (size // 2, size // 2)
    for nx, ny in nodes:
        n_draw.line([center_pt, (nx, ny)], fill=c_accent1 + (160,), width=4)
        n_draw.ellipse([(nx - 18, ny - 18), (nx + 18, ny + 18)], fill=(255, 255, 255, 230), outline=c_accent1 + (255,), width=5)

    # 중앙 아이소메트릭 글래스 플랫폼
    n_draw.rounded_rectangle(
        [(290, 290), (734, 734)],
        radius=72,
        fill=(255, 255, 255, 38),
        outline=c_accent2 + (210,),
        width=4
    )
    n_draw.rounded_rectangle(
        [(360, 360), (664, 664)],
        radius=54,
        fill=c_bg2 + (190,),
        outline=c_accent1 + (255,),
        width=5
    )
    # 코어 링
    n_draw.ellipse([(420, 420), (604, 604)], fill=c_accent1 + (80,), outline=(255, 255, 255, 240), width=6)
    n_draw.ellipse([(468, 468), (556, 556)], fill=(255, 255, 255, 245))

    img = Image.alpha_composite(img, net_layer)
    img.convert("RGB").save(output_path, "PNG")
    return output_path


def compose_thumbnail(
    inner_image_path: str,
    output_path: str,
    template_path: str = "썸네일_원본첨부.png",
    summary_lines: list = None
) -> str:
    """
    사장님의 1691x930 썸네일 원본 템플릿에:
    1. 좌측 둥근 카드(x:62~789, y:52~853, radius:68)에 기사 맞춤 1:1 AI 일러스트 합성
    2. 우측 상단 '기사 중점 요약 내용:' 영역에 기사 핵심 요약 1~2줄을 동적으로 정밀 마킹
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"썸네일 원본 템플릿을 찾을 수 없습니다: {template_path}")
    if not os.path.exists(inner_image_path):
        raise FileNotFoundError(f"합성할 AI 이미지를 찾을 수 없습니다: {inner_image_path}")

    template = Image.open(template_path).convert("RGBA")
    inner_img = Image.open(inner_image_path).convert("RGBA")

    # [1] 좌측 카드 영역 맞춤 합성 (외곽 그린 테두리 안쪽에 여백 없이 100% 정밀 밀착)
    box_x = 58
    box_y = 57
    box_w = 740
    box_h = 791
    radius = 64

    inner_resized = ImageOps.fit(inner_img, (box_w, box_h), Image.Resampling.LANCZOS)
    mask = create_rounded_mask((box_w, box_h), radius=radius)
    template.paste(inner_resized, (box_x, box_y), mask)

    # [2] 우측 상단 요약 박스 내부(점선 테두리·새싹 아이콘·우측 하단 잎사귀 보존)에 1~2줄 정밀 배치
    if summary_lines and len(summary_lines) >= 1:
        draw = ImageDraw.Draw(template)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        local_font = os.path.join(base_dir, "NanumGothicBold.ttf")
        win_font = "C:/Windows/Fonts/malgunbd.ttf"
        font_path = local_font if os.path.exists(local_font) else (win_font if os.path.exists(win_font) else None)

        def _get_fitted_font(text_str: str, max_width: int = 472, start_size: int = 34):
            if not font_path:
                return ImageFont.load_default()
            sz = start_size
            while sz > 20:
                try:
                    f = ImageFont.truetype(font_path, sz)
                    if draw.textlength(text_str, font=f) <= max_width:
                        return f
                except Exception:
                    break
                sz -= 1
            return ImageFont.truetype(font_path, 22)

        text_color = (25, 75, 35, 255)  # 딥 포레스트 그린

        l1 = str(summary_lines[0]).strip()
        l2 = str(summary_lines[1]).strip() if len(summary_lines) > 1 else ""

        if l2:
            f1 = _get_fitted_font(l1, max_width=472, start_size=34)
            f2 = _get_fitted_font(l2, max_width=472, start_size=34)
            draw.text((920, 232), l1, fill=text_color, font=f1, anchor="lm")
            draw.text((920, 284), l2, fill=text_color, font=f2, anchor="lm")
        else:
            f1 = _get_fitted_font(l1, max_width=472, start_size=35)
            draw.text((920, 256), l1, fill=text_color, font=f1, anchor="lm")

    template.save(output_path, "PNG")
    return output_path
