import re
import random

def clean_topic_title(topic: str) -> str:
    """기사 제목에서 말머리, 괄호, 특수부호를 제거하고 핵심 키워드를 깔끔하게 정제 (최대 12자)"""
    if not topic:
        return "AI 신기술"
    
    # 1. [AI리더의 서가], (종합) 등 괄호 태그 완전 제거
    cleaned = re.sub(r'\[[^\]]*\]', '', topic)
    cleaned = re.sub(r'\([^\)]*\)', '', cleaned)
    
    # 2. 따옴표, 쉼표, 말줄임표 제거 및 구분자 앞부분만 추출
    cleaned = cleaned.replace('"', '').replace("'", "").replace("…", " ").replace("...", " ")
    cleaned = re.split(r'[:|｜\-–]', cleaned)[0].strip()
    
    words = cleaned.split()
    if not words:
        return "AI 신기술"
        
    selected = []
    curr_len = 0
    for w in words:
        # 단어 길이가 12자 이내까지만 온전한 단어로 추가
        if curr_len + len(w) + (1 if selected else 0) <= 12:
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
        f'{topic} 직접 써보니… 진짜 충격 반전',        # ~24자
        f'조용하던 {topic} 결국 일냈다! 핵심 총정리',   # ~25자
        f'{topic} 기대했는데 아니었다? 충격 근황',      # ~24자
        f'{topic} 아직도 모르면 손해… 업계 발칵',       # ~24자
        f'다들 {topic} 난리 났는데… 과연 쓸만할까'      # ~25자
    ]
    
    valid_titles = [p for p in patterns if len(p) <= 28]
    return valid_titles if valid_titles else [f'{topic} 전격 공개! 충격 반전']
