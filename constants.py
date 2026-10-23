import re
import random

def clean_topic_title(topic: str) -> str:
    """기사 제목에서 말머리, 괄호, 쉼표, 특수부호 및 불필요한 조사를 제거하고 핵심 명사 추출 (최대 11자)"""
    if not topic:
        return "AI 신기술"
    
    # 1. 말머리 대괄호/소괄호 완전 제거
    cleaned = re.sub(r'\[[^\]]*\]', '', topic)
    cleaned = re.sub(r'\([^\)]*\)', '', cleaned)
    
    # 2. 특수문자 및 기호 공백 치환
    for ch in ['"', "'", "“", "”", "‘", "’", ",", "…", "...", "·", ":", "|", "｜", "-", "–"]:
        cleaned = cleaned.replace(ch, " ")
    
    # 3. 불필요한 행동어 및 중복 단어 제거
    junk_words = ["직접", "써보니", "읽고", "보니", "공개", "출시", "관련", "논문"]
    for jw in junk_words:
        cleaned = re.sub(r'\b' + re.escape(jw) + r'\b', ' ', cleaned)

    words = [w.strip() for w in cleaned.split() if w.strip()]
    if not words:
        return "AI 신기술"
        
    # 끝에 붙은 조사(도, 는, 은, 가, 이, 의, 를, 을, 로, 에서) 제거
    cleaned_words = []
    for w in words[:3]:
        w_cleaned = re.sub(r'(에도|에서|으로|까지|부터|과는|와의|도|는|은|가|이|의|를|을|로)$', '', w)
        cleaned_words.append(w_cleaned if len(w_cleaned) >= 2 else w)

    selected = []
    curr_len = 0
    for w in cleaned_words:
        if curr_len + len(w) + (1 if selected else 0) <= 11:
            selected.append(w)
            curr_len += len(w) + 1
        else:
            break
            
    result = " ".join(selected) if selected else words[0][:10]
    return result.strip()

def generate_cheat_title_templates(core_topic: str) -> list:
    """
    28자 이내로 완결된 상황별 다채로운 고클릭률 제목 5종 생성 (무작위 셔플 보장)
    """
    topic = clean_topic_title(core_topic)
    
    patterns = [
        f'"{topic}" 베일 벗었다! 실제 성능 분석',      # ~24자 (신기술 발표/성능)
        f'{topic} 결국 일냈다! 판도 바뀔까',          # ~22자 (시장 파장/혁신)
        f'{topic} 논란 속 진짜 실체… 업계 발칵',       # ~23자 (이슈/반전)
        f'다들 {topic} 주목하는 진짜 이유 총정리',      # ~24자 (트렌드/분석)
        f'{topic} 아직도 모르면 손해… 핵심 팩트',       # ~23자 (정보/가이드)
        f'조용하던 {topic} 초강수… 승부수 통할까',      # ~24자 (기업 전략)
        f'{topic} 기대 이상일까? 솔직 심층 분석'       # ~23자 (리뷰/평가)
    ]
    
    valid_titles = [p for p in patterns if len(p) <= 28]
    if not valid_titles:
        valid_titles = [f'{topic} 전격 공개! 심층 분석']
    random.shuffle(valid_titles)
    return valid_titles
