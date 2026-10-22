import re
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

def format_mobile_text(text: str, max_chars: int = 25) -> str:
    """
    모바일 가독성 최적화:
    1. 각 줄을 공백/부호 포함 max_chars(기본 25자) 이내로 줄바꿈
    2. 소제목([1. ...], [2. ...], [3. ...]) 앞뒤에는 2줄 공백을 두어 문단 간격을 시원하게 분리!
    3. 일반 문단 사이에는 단 1줄 빈 줄 유지
    """
    if not text:
        return ""
    
    # 소제목 태그 앞뒤에 강제로 명확한 구분자 삽입
    text = re.sub(r'(\[\d+\.\s*[^\]]+\])', r'\n\n\1\n\n', text)
    
    paragraphs = re.split(r'\n\s*\n', text.strip())
    formatted_paragraphs = []
    
    for para in paragraphs:
        para_clean = para.strip()
        if not para_clean:
            continue
            
        # 소제목인 경우 줄바꿈 없이 깔끔하게 단독 문단으로 유지
        if re.match(r'^\[\d+\.\s*[^\]]+\]$', para_clean):
            formatted_paragraphs.append(para_clean)
            continue
            
        cleaned_para = " ".join(para_clean.split())
        words = cleaned_para.split()
        
        lines = []
        current_line = ""
        
        for word in words:
            is_url = word.startswith(("http://", "https://", "www."))
            if not current_line:
                if len(word) > max_chars and not is_url:
                    for i in range(0, len(word), max_chars):
                        lines.append(word[i:i+max_chars])
                else:
                    current_line = word
            else:
                if len(current_line) + 1 + len(word) <= max_chars:
                    current_line += " " + word
                else:
                    lines.append(current_line)
                    if len(word) > max_chars and not is_url:
                        for i in range(0, len(word), max_chars):
                            if i + max_chars < len(word):
                                lines.append(word[i:i+max_chars])
                            else:
                                current_line = word[i:]
                    else:
                        current_line = word
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
    
    # [1] 좌측 카드 영역 맞춤 합성 (상단 52부터 여백 밀착)
    box_x = 62
    box_y = 52
    box_w = 728
    box_h = 802
    radius = 68
    
    inner_resized = ImageOps.fit(inner_img, (box_w, box_h), Image.Resampling.LANCZOS)
    mask = create_rounded_mask((box_w, box_h), radius=radius)
    template.paste(inner_resized, (box_x, box_y), mask)
    
    # [2] 우측 상단 핵심 요약 1~2줄 동적 마킹
    if summary_lines and len(summary_lines) >= 1:
        draw = ImageDraw.Draw(template)
        # 상단 '기사 중점 요약 내용:' 라벨 아래부터 지치 새싹 머리 위까지 깔끔 커버
        bg_box = (760, 155, 1560, 415)
        draw.rounded_rectangle(bg_box, radius=24, fill=(255, 254, 245, 255), outline=(215, 225, 200, 255), width=3)
        
        # 폰트 로드 (동봉된 나눔고딕볼드 또는 윈도우 맑은고딕)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        local_font = os.path.join(base_dir, "NanumGothicBold.ttf")
        win_font = "C:/Windows/Fonts/malgunbd.ttf"
        
        font = None
        for fp in [local_font, win_font]:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, 48)
                    break
                except Exception:
                    pass
        if not font:
            font = ImageFont.load_default()
            
        text_color = (25, 75, 35, 255) # 고급스러운 딥 포레스트 그린
        
        l1 = str(summary_lines[0]).strip()
        l2 = str(summary_lines[1]).strip() if len(summary_lines) > 1 else ""
        
        if l2:
            draw.text((1160, 230), l1, fill=text_color, font=font, anchor="mm")
            draw.text((1160, 335), l2, fill=text_color, font=font, anchor="mm")
        else:
            draw.text((1160, 285), l1, fill=text_color, font=font, anchor="mm")
            
    template.save(output_path, "PNG")
    return output_path
