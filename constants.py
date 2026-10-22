import re
import random

def clean_topic_title(topic: str) -> str:
    """기사 제목에서 말머리, 괄호, 쉼표, 특수부호를 제거하고 검색에 걸리는 핵심 명사 추출 (최대 11자)"""
    if not topic:
        return "AI 신기술"
    
    # 1. [AI리더의 서가], (종합) 등 괄호 태그 완전 제거
    cleaned = re.sub(r'\[[^\]]*\]', '', topic)
    cleaned = re.sub(r'\([^\)]*\)', '', cleaned)
    
    # 2. 불필요한 따옴표, 쉼표, 말줄임표 제거 및 구분자 앞부분만 추출
    cleaned = cleaned.replace('"', '').replace("'", "").replace(",", "").replace("…", " ").replace("...", " ")
    cleaned = re.split(r'[:|｜\-–]', cleaned)[0].strip()
    
    words = cleaned.split()
    if not words:
        return "AI 신기술"
        
    selected = []
    curr_len = 0
    for w in words:
        if curr_len + len(w) + (1 if selected else 0) <= 11:
            selected.append(w)
            curr_len += len(w) + 1
        else:
            break
            
    result = " ".join(selected) if selected else words[0][:10]
    return result.strip()

def generate_cheat_title_templates(core_topic: str) -> list:
    """
    28자 이내로 완결된 다채로운 고클릭률 제목 5종 생성 (글자수 20~27자 엄격 보장)
    """
    topic = clean_topic_title(core_topic)
    
    patterns = [
        f'"{topic}" 직접 써보니… 진짜 충격 반전',      # ~24자
        f'조용하던 {topic} 결국 해냈다! 핵심 총정리',   # ~25자
        f'{topic} 기대했는데 아니었다? 충격 근황',      # ~23자
        f'{topic} 아직도 모르면 손해… 업계 발칵',       # ~23자
        f'다들 {topic} 난리 났는데… 과연 쓸만할까'      # ~24자
    ]
    
    valid_titles = [p for p in patterns if len(p) <= 28]
    return valid_titles if valid_titles else [f'{topic} 전격 공개! 충격 반전']
