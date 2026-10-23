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
    28자 이내로 완결된 상황별 다채로운 고클릭률 제목 생성 (무작위 셔플 보장)
    - 네이버 공식 우수 블로거 선정 기준 준수: 
      실제 사용하지 않은 기술 기사에 '직접 써보니', '충격 반전' 등 과장·허위 낚시성 문구 완전 영구 배제
      (자료 기반 분석, 업계 동향 및 핵심 팩트 중심의 신뢰도 높은 제목 생성)
    """
    topic = clean_topic_title(core_topic)
    
    patterns = [
        f'"{topic}" 전격 발표! 핵심 기술 분석',      # ~24자 (기술 발표/팩트 분석)
        f'{topic} 공식 발표! 글로벌 테크 판도 변화',   # ~25자 (업계 파장/동향)
        f'테크 업계가 {topic} 주목하는 핵심 이유',     # ~24자 (트렌드/전문 분석)
        f'{topic} 상세 공개! 실무 도입 전 체크포인트', # ~26자 (실무자 가이드)
        f'{topic} 공개로 보는 빅테크 차세대 전략',    # ~24자 (기업 전략 분석)
        f'{topic} 발표의 명암! 장점과 한계 분석',     # ~23자 (객관적 팩트/비교)
        f'{topic} 핵심 사양 총정리! 시장 영향은'      # ~23자 (사양 및 시장 분석)
    ]
    
    valid_titles = [p for p in patterns if len(p) <= 28]
    if not valid_titles:
        valid_titles = [f'{topic} 공식 발표! 기술 분석']
    random.shuffle(valid_titles)
    return valid_titles
