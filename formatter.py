import re
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

def format_mobile_text(text: str, max_chars: int = 18) -> str:
    """
    모바일 최적화 및 자연스러운 한국어 문맥 줄바꿈 (파워블로그 16~18자 가독성 규격):
    [사장님 엄격 규정 3대 원칙]
    1. 소제목 번호매김 절대 금지! ([1. 소제목] -> [소제목]으로 자동 정제)
    2. 스마트에디터 dot(•) 및 번호 리스트 트리거 문자(-, *, 1. 2.) 원천 차단!
    3. 온점(.), 물음표(?), 느낌표(!) 기준으로 자연스러운 호흡 부여
    """
    if not text:
        return ""
    
    # 1. 소제목 내 번호 매김 완전 제거 ([1. ...] -> [...])
    text = re.sub(r'\[\s*\d+[\.\)]\s*', '[', text)
    # 소제목 태그 앞뒤에 명확한 문단 구분자 삽입
    text = re.sub(r'(\[[^\]]+\])', r'\n\n\1\n\n', text)

    # [사장님 특명: 주소 끝난 후 및 '소중한 시간' 앞뒤 확실한 독립 문단/빈 줄 분리]
    # 출처 레이블 앞뒤 분리
    text = re.sub(r'([^\n])\s*(공식\s*출처:|출처:)', r'\1\n\n\2', text)
    # 출처 콜론과 URL 사이 줄바꿈 분리
    text = re.sub(r'(공식\s*출처:|출처:)\s*(https?://[^\s]+)', r'\1\n\2', text)
    # 단독 URL 앞 문단 분리
    text = re.sub(r'([^\n])\s*(https?://[^\s\n]+)', r'\1\n\n\2', text)
    # URL 주소가 끝난 직후 어떤 텍스트가 오든 반드시 빈 줄 2개(\n\n)로 완전히 분리
    text = re.sub(r'(https?://[^\s\n]+)\s*([^\s\n])', r'\1\n\n\2', text)
    # '소중한 시간' 독자 감사 인사말 블록 앞뒤 무조건 빈 줄 2개(\n\n)로 확실한 독립 문단 보장
    text = re.sub(r'([^\n])\s*(소중한\s*시간)', r'\1\n\n\2', text)
    
    paragraphs = re.split(r'\n\s*\n', text.strip())
    formatted_paragraphs = []
    
    for para in paragraphs:
        para_clean = para.strip()
        if not para_clean:
            continue
            
        # 대괄호 소제목인 경우 줄바꿈 없이 깔끔하게 단독 문단으로 유지 (내부 번호 완전 제거)
        if re.match(r'^\[[^\]]+\]$', para_clean):
            clean_sub = re.sub(r'\[\s*\d+[\.\)]\s*', '[', para_clean)
            formatted_paragraphs.append(clean_sub)
            continue

        # [스마트에디터 dot 및 번호 리스트 원천 차단]
        # 문단 내부의 각 줄마다 대시(-), 불릿(*, •, ·), 숫자(1. 2. 3.) 완전 박멸
        cleaned_lines = []
        for raw_line in para_clean.split('\n'):
            line_s = raw_line.strip()
            if not line_s:
                continue
            line_s = re.sub(r'^[\-\*•·]\s*', '', line_s)
            line_s = re.sub(r'^\d+[\.\)]\s*', '', line_s)
            line_s = line_s.strip()
            if line_s:
                cleaned_lines.append(line_s)
        
        if not cleaned_lines:
            continue
            
        para_clean = " ".join(cleaned_lines)
            
        # 1. 문장 단위로 분리 (. ? !)
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
                
            # 18자 이내의 짧은 문장은 줄바꿈 없이 한 호흡으로 유지
            clean_len = len(re.sub(r'\*\*', '', s_clean))
            if clean_len <= max_chars + 2:
                lines.append(s_clean)
                continue
                
            # 긴 문장은 쉼표(,) 단위 절 분리 후 어절 맞춤 줄바꿈
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
                    word_len = len(re.sub(r'\*\*', '', word))
                    cur_clean_len = len(re.sub(r'\*\*', '', current_line))
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
                # 쉼표 뒤에서 줄 길이가 12자 이상이면 자연스러운 호흡으로 줄바꿈
                cur_clean_len = len(re.sub(r'\*\*', '', current_line))
                if c.endswith(",") and cur_clean_len >= 12:
                    lines.append(current_line)
                    current_line = ""
            if current_line:
                lines.append(current_line)
                
        formatted_paragraphs.append("\n".join(lines))
        
    return "\n\n".join(formatted_paragraphs)


def create_rounded_mask(size, radius):
    """지정된 크기와 반경의 둥근 모서리 마스크 생성"""
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), size], radius=radius, fill=255)
    return mask


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
