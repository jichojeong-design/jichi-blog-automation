import random

def clean_topic_title(topic: str) -> str:
    """기사 제목에서 단어가 중간에 잘리지 않도록 온전한 단어 단위로 14자 이내 추출"""
    if not topic:
        return "AI 신기술"
    cleaned = topic.split("...")[0].split("…")[0].split(":")[0].split("｜")[0].strip()
    words = cleaned.split()
    
    # 글자 수를 세어가며 단어가 통째로 들어가는 것만 추가 (단어 쪼개짐 원천 차단)
    selected = []
    current_len = 0
    for w in words:
        if current_len + len(w) + (1 if selected else 0) <= 14:
            selected.append(w)
            current_len += len(w) + 1
        else:
            break
            
    result = " ".join(selected) if selected else (words[0] if words else "AI 트렌드")
    return result.strip()

def generate_cheat_title_templates(core_topic: str) -> list:
    """
    치트키 조합을 다채롭게 랜덤 변형하여 28자 이내로 완결된 고클릭률 제목 5종 생성
    (문장 중간 뚝 잘림 현상 완전 방지)
    """
    topic = clean_topic_title(core_topic)
    
    # 28자 이내로 딱 맞게 완성된 문장 패턴들 (글자수 20~27자)
    patterns = [
        f'"{topic}" 몰랐는데 결국 터졌다',           # ~22자
        f'{topic} 믿었는데 아니었다? 충격 반전',       # ~23자
        f'한때는 최고라더니 {topic} 써본 후기',        # ~24자
        f'{topic} 비상 걸렸다… 다들 싹 다 후회',      # ~25자
        f'"{topic} 된다고?" 직접 봤더니 기가막힌 근황',  # ~26자
        f'{topic} 이렇게 바뀔 줄이야… 판도 뒤집혔다',   # ~27자
        f'조용하던 {topic} 결국 일냈다! 숨겨진 진실',   # ~27자
        f'{topic} 모르면 손해? 직접 해보니 소름돋네',   # ~26자
        f'다들 {topic} 난리 났는데… 막상 써보니'      # ~24자
    ]
    
    # 28자 이내의 패턴 중에서 랜덤 5개 추출
    valid_titles = [p for p in patterns if len(p) <= 28]
    if len(valid_titles) >= 5:
        return random.sample(valid_titles, 5)
    return valid_titles
