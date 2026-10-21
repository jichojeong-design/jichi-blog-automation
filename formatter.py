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


def compose_thumbnail(inner_image_path: str, output_path: str, template_path: str = "썸네일_원본첨부.png") -> str:
    """
    사장님의 1691x930 썸네일 원본 좌측 둥근 카드 영역에 AI 이미지를 정확하게 맞춤 합성
    좌측 카드 정확한 영역:
    x: 62 ~ 789 (w: 728)
    y: 52 ~ 853 (h: 802)  <-- 상단 52부터 시작하여 흰 여백 완전 제거!
    radius: 68
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"썸네일 원본 템플릿을 찾을 수 없습니다: {template_path}")
    if not os.path.exists(inner_image_path):
        raise FileNotFoundError(f"합성할 AI 이미지를 찾을 수 없습니다: {inner_image_path}")
        
    template = Image.open(template_path).convert("RGBA")
    inner_img = Image.open(inner_image_path).convert("RGBA")
    
    # 수정된 정확한 좌표: 상단 흰 여백 완전 밀착 커버
    box_x = 62
    box_y = 52
    box_w = 728
    box_h = 802
    radius = 68
    
    # 비율 유지하며 중앙 채우기 (Fit & Crop)
    inner_resized = ImageOps.fit(inner_img, (box_w, box_h), Image.Resampling.LANCZOS)
    
    # 둥근 모서리 마스크 적용
    mask = create_rounded_mask((box_w, box_h), radius=radius)
    
    # 템플릿 위에 마스크를 활용해 합성
    template.paste(inner_resized, (box_x, box_y), mask)
    
    template.save(output_path, "PNG")
    return output_path
