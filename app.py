import streamlit as st
import os
import glob
import random
from PIL import Image
import formatter
import constants
import collector
import prompt_engine
import snack_trends

st.set_page_config(page_title="지치 블로그 올인원 자동화 센터", page_icon="🌿", layout="wide")

st.markdown("""
<style>
    .main-header { font-size: 26px; font-weight: bold; color: #2E7D32; margin-bottom: 5px; }
    .sub-header { font-size: 14px; color: #666; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; font-size: 16px; font-weight: bold; }
    .card-box { background-color: #F1F8E9; padding: 15px; border-radius: 10px; border-left: 5px solid #7CB342; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌿 지치 블로그 올인원 자동화 센터 (코다리부장 Ver 1.3)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI 기사와 웹툰을 완벽 분업하여 토큰 낭비를 없애고 퀄리티를 극대화합니다.</div>', unsafe_allow_html=True)

# 🚨 긴급 비상 안전 가동 센터 (Fail-Safe 배너)
col_alert1, col_alert2 = st.columns([3, 1])
with col_alert1:
    st.markdown("""
    <div style="background-color: #FFF3E0; border: 2px solid #FF9800; padding: 12px 18px; border-radius: 10px; margin-bottom: 15px;">
        <span style="font-size: 15px; font-weight: bold; color: #E65100;">🚨 [아침 9시 무인 발행 안전 관제 시스템 가동 중]</span><br/>
        <span style="font-size: 13px; color: #5D4037;">
            기사 1편이 09:03까지 발행되지 않으면 <b>네이버 메일로 긴급 알림</b>이 즉시 발송됩니다. 출근길 이상 감지 시 오른쪽 비상 버튼을 눌러주세요!
        </span>
    </div>
    """, unsafe_allow_html=True)
with col_alert2:
    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    st.link_button(
        "🚨 비상 포스팅 즉시 가동",
        "https://github.com/jichojeong-design/jichi-blog-automation/actions/workflows/daily_blog.yml",
        use_container_width=True,
        help="스마트폰에서 터치 1번으로 클라우드 로봇을 즉시 비상 가동시킵니다."
    )

tab_news, tab_webtoon, tab_chars = st.tabs(["📰 AI 트렌드 기사", "🎨 AI 웹툰", "👥 캐릭터 레퍼런스 시트"])

# ==========================================
# 탭 1: AI 트렌드 기사
# ==========================================
with tab_news:
    st.subheader("1. 소재 발굴 & 최신 기사 수집")
    
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        if st.button("🔄 허용 출처 6곳 실시간 뉴스 수집", use_container_width=True):
            with st.spinner("AI타임스, TechCrunch 등 최신 소식 수집 중..."):
                st.session_state["news_items"] = collector.get_all_sources()
                st.success(f"{len(st.session_state.get('news_items', []))}건 수집 완료!")
    with col_info:
        news_list = st.session_state.get("news_items", [])
        if news_list:
            st.info(f"현재 총 {len(news_list)}개의 최신 기사가 수집되었습니다. 아래에서 기사를 선택하면 상세 정보가 자동 입력됩니다.")
        else:
            st.write("👈 버튼을 눌러 AI타임스, TechCrunch 등 최신 뉴스를 불러오세요.")

    news_list = st.session_state.get("news_items", [])
    selected_news = None
    
    if news_list:
        st.markdown("**📋 수집된 기사 목록 (원하는 기사를 클릭하세요):**")
        news_options = [f"【{item['slot']}】 {item['source']} ｜ {item['title']}" for item in news_list]
        chosen_idx = st.radio(
            "기사 선택",
            range(len(news_options)),
            format_func=lambda x: news_options[x],
            label_visibility="collapsed"
        )
        selected_news = news_list[chosen_idx]
        st.caption(f"🔗 원문 링크: {selected_news['url']}")
        st.markdown("---")

    col_topic1, col_topic2 = st.columns([2, 1])
    with col_topic1:
        custom_topic = st.text_input("기사 제목 / 핵심 주제:", value=selected_news['title'] if selected_news else "OpenAI 차세대 추론 모델 발표와 시장 반응")
        custom_url = st.text_input("출처 URL:", value=selected_news['url'] if selected_news else "https://openai.com/news/")
    with col_topic2:
        custom_facts = st.text_area("보강할 핵심 팩트 / 수치 (선택):", placeholder="공식 출시일, 가격, 모델 성능 수치 등", height=115)

    st.markdown("---")
    st.subheader("2. 트렌드 키워드 & 치트키 제목 추천")
    
    col_k1, col_k2 = st.columns(2)
    clean_k = constants.clean_topic_title(custom_topic)
    with col_k1:
        st.markdown("**🎯 SEMrush 기준 추천 상위 노출 키워드**")
        st.code(f"1. {clean_k} 사용법\n2. {clean_k} 가격 비교\n3. {clean_k} 장단점", language="text")
    with col_k2:
        st.markdown("**🔥 비밀 치트키 조합 추천 제목 (28자 이내)**")
        titles = constants.generate_cheat_title_templates(clean_k)
        for t in titles:
            st.write(f"- `{t}`")

    st.markdown("---")
    st.subheader("3. 10년 차 기자 문체 프롬프트 생성 (Gemini Pro / 대화용)")
    prompt_text = prompt_engine.generate_ai_news_prompt(custom_topic, custom_url, custom_facts)
    st.text_area("아래 프롬프트를 복사하여 Gemini Pro에 넣으면 최고 품질의 원고가 나옵니다:", value=prompt_text, height=180)

    st.markdown("---")
    st.subheader("4. 모바일 줄바꿈 가공 & 1691×930 썸네일 자동 합성")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        raw_article = st.text_area("Gemini가 작성해준 원문 본문을 붙여넣으세요:", height=250, placeholder="여기에 원고 텍스트를 붙여넣으면 공백 포함 25자 이내로 정밀 자동 줄바꿈됩니다.")
        if st.button("📱 모바일 최적화 25자 줄바꿈 실행", use_container_width=True):
            formatted_art = formatter.format_mobile_text(raw_article)
            st.session_state["formatted_art"] = formatted_art
            
        if "formatted_art" in st.session_state:
            st.success("✅ 25자 줄바꿈 완료! 네이버 블로그 스마트에디터에 바로 붙여넣으세요:")
            st.text_area("완성된 모바일 원고:", value=st.session_state["formatted_art"], height=200)

    with col_t2:
        st.markdown("**🖼️ 1691×930 썸네일 합성 (지치와 친구들)**")
        uploaded_ai_img = st.file_uploader("ChatGPT(DALL-E)가 생성한 좌측 알맹이 이미지 업로드:", type=["png", "jpg", "jpeg"])
        
        if uploaded_ai_img is not None:
            temp_path = "temp_uploaded_inner.png"
            with open(temp_path, "wb") as f:
                f.write(uploaded_ai_img.getbuffer())
                
            out_thumb = "완성_썸네일_1691x930.png"
            formatter.compose_thumbnail(temp_path, out_thumb, template_path="썸네일_원본첨부.png")
            st.image(out_thumb, caption="🎉 합성 완성된 1691×930 썸네일", use_container_width=True)
            with open(out_thumb, "rb") as file:
                st.download_button(label="📥 완성된 썸네일 다운로드", data=file, file_name="지치_썸네일_완성본.png", mime="image/png", use_container_width=True)


# ==========================================
# 탭 2: AI 웹툰
# ==========================================
with tab_webtoon:
    st.subheader("🎨 AI 웹툰 3단계 제작 프로세스")
    
    st.markdown("### 1단계: 실시간 핫이슈 발굴 ➡️ 1~5위 랭킹 ➡️ 시식후기 검증 Best 2종 자동 선별")
    
    col_yt_btn, col_yt_info = st.columns([1, 3])
    with col_yt_btn:
        if st.button("🚀 5단계 알고리즘 실시간 분석 가동", use_container_width=True):
            with st.spinner("1~5위 랭킹 산출 및 네이버/유튜브 시식 후기 검증 중... (0.5초 소요)"):
                st.session_state["ranked_snacks"] = snack_trends.get_realtime_ranked_trends()
                st.success("1~5위 랭킹 분석 및 시식 후기 검증 Best 2종 선별 완료!")
                
    ranked_snacks = st.session_state.get("ranked_snacks", snack_trends.get_realtime_ranked_trends())
    
    # 1~5위 랭킹 테이블 및 시식 후기 + 기발행 중복 검증 뱃지 표시
    st.markdown("**📊 실시간 화제성 1~5위 랭킹 및 [기발행 중복 / 시식후기 검증] 현황:**")
    
    r_cols = st.columns(5)
    for idx, r_item in enumerate(ranked_snacks[:5]):
        with r_cols[idx]:
            if r_item.get("is_duplicate"):
                is_best = "🚫 [기발행 제외]"
                badge_color = "#FFEBEE"
                border_color = "#E57373"
                header_color = "#C62828"
                status_text = f"<span style='font-size: 11px; color: #C62828; font-weight: bold;'>{r_item.get('dup_msg', '이미 발행됨')}</span>"
            elif r_item.get("is_selected_best"):
                best_num = 1 if r_item == [x for x in ranked_snacks if x.get("is_selected_best")][0] else 2
                is_best = f"⭐ [추천 {best_num}위]"
                badge_color = "#E8F5E9"
                border_color = "#2E7D32"
                header_color = "#1B5E20"
                status_text = "<span style='font-size: 11px; color: #0D47A1; font-weight: bold;'>✅ 미발행 신규 / 후기완벽</span>"
            else:
                is_best = f"후보 {r_item['rank']}위"
                badge_color = "#F8F9FA"
                border_color = "#9E9E9E"
                header_color = "#424242"
                status_text = "<span style='font-size: 11px; color: #2E7D32;'>✅ 시식 후기 검증</span>"
            
            st.markdown(f"""
            <div style="background-color: {badge_color}; border: 2px solid {border_color}; padding: 10px; border-radius: 8px; text-align: center; min-height: 145px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <b style="color: {header_color}; font-size: 13px;">{is_best}</b><br/>
                <span style="font-size: 12px; font-weight: bold; color: #111111; display: block; margin: 4px 0;">{r_item['keyword']}</span>
                <span style="font-size: 10px; color: #424242; display: block; margin-bottom: 4px;">{r_item['tag']}</span>
                {status_text}
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    st.markdown("**👇 작업할 웹툰 소재 선택 (기발행 건은 제외되고 신규 Best 2종이 기본 선별됩니다):**")
    
    snack_options = []
    for item in ranked_snacks:
        if item.get("is_duplicate"):
            snack_options.append(f"🚫 [기발행] {item['keyword']} (10/18~10/19 이미 포스팅됨)")
        elif item.get("is_selected_best"):
            snack_options.append(f"⭐ [신규 추천] {item['keyword']} ｜ {item['tag']}")
        else:
            snack_options.append(f"[{item['rank']}위] {item['keyword']} ｜ {item['tag']}")
    chosen_snack_idx = st.radio(
        "신상 선택",
        range(len(snack_options)),
        format_func=lambda x: snack_options[x],
        label_visibility="collapsed"
    )
    current_snack = ranked_snacks[chosen_snack_idx]
    
    col_rev1, col_rev2 = st.columns(2)
    with col_rev1:
        st.markdown(f"**🎬 유튜브 실시간 트렌드 요약:**\n{current_snack['youtube']}")
    with col_rev2:
        st.markdown(f"**📝 네이버 블로그 내돈내산 시식 후기 (검증 완료):**\n{current_snack['naver']}")
        
    st.info(f"📸 **공식 제품 사진 활용 팁**: 공식 패키지 사진 및 포스터를 캐릭터 뒤쪽 자료 판넬로 배치하면 현장감 극대화!")
    
    combined_reviews = f"1. 유튜브 트렌드: {current_snack['youtube']}\n2. 네이버 블로그 내돈내산 후기: {current_snack['naver']}"
    
    col_w1, col_w2 = st.columns(2)
    with col_w1:
        snack_name = st.text_input("선택된 상품명:", value=current_snack['keyword'])
        prop_twist = st.text_input("소품 반전 1개:", value="에어프라이어 (또는 반쪽 빵, 포크, 얼음잔 등)")
    with col_w2:
        snack_reviews = st.text_area("종합 후기 내용 (수정 가능):", value=combined_reviews, height=100)

    st.markdown("---")
    st.markdown("### 2단계: 웹툰 통합 패키지 생성 (웹툰 1편 & 2편 각각 분리 운영)")
    
    # 사장님 요청: 하루 2편 웹툰의 등장인물이 서로 겹치지 않고 다채롭게 바뀌도록 탭/선택 분리
    subtab_wt1, subtab_wt2 = st.tabs(["🎨 [웹툰 1편] 대본 & 프롬프트", "🎨 [웹툰 2편] 대본 & 프롬프트"])
    
    other_pool = ["송이 (삼색 고양이)", "초코 (턱시도 고양이)", "AI 로봇 (도우미)"]
    
    # --- 웹툰 1편 ---
    with subtab_wt1:
        col_c1_btn, col_c1_info = st.columns([1, 2])
        with col_c1_btn:
            if st.button("🎲 [1편] 파트너 캐릭터 셔플"):
                p1_pick = ["지치 (새싹 요정)"] + random.sample(other_pool, random.choice([1, 2]))
                st.session_state["wt1_chars"] = p1_pick
        
        wt1_chars = st.session_state.get("wt1_chars", ["지치 (새싹 요정)", "송이 (삼색 고양이)"])
        with col_c1_info:
            st.write(f"**1편 출연진**: `{' + '.join(wt1_chars)}` (주인공 '지치' 중심)")
            
        p1_prompt = prompt_engine.generate_webtoon_script_prompt(snack_name, snack_reviews, prop_twist, wt1_chars)
        st.text_area("👉 [웹툰 1편] 복사용 프롬프트 (제목 + 대본 + DALL-E 영문 세트):", value=p1_prompt, height=200, key="prompt_wt1")

    # --- 웹툰 2편 ---
    with subtab_wt2:
        col_c2_btn, col_c2_info = st.columns([1, 2])
        with col_c2_btn:
            if st.button("🎲 [2편] 파트너 캐릭터 셔플"):
                # 1편과 다른 캐릭터를 우선 선발
                p2_pool = [c for c in other_pool if c not in wt1_chars] or other_pool
                p2_pick = ["지치 (새싹 요정)"] + random.sample(p2_pool, min(len(p2_pool), random.choice([1, 2])))
                st.session_state["wt2_chars"] = p2_pick
                
        wt2_chars = st.session_state.get("wt2_chars", ["지치 (새싹 요정)", "초코 (턱시도 고양이)"])
        with col_c2_info:
            st.write(f"**2편 출연진**: `{' + '.join(wt2_chars)}` (1편과 차별화된 새로운 조합)")
            
        p2_prompt = prompt_engine.generate_webtoon_script_prompt(f"{snack_name} 후속/다른맛", snack_reviews, "다른 꿀팁 소품", wt2_chars)
        st.text_area("👉 [웹툰 2편] 복사용 프롬프트 (제목 + 대본 + DALL-E 영문 세트):", value=p2_prompt, height=200, key="prompt_wt2")

    st.markdown("---")
    st.markdown("### 3단계: ChatGPT Plus로 컷 만화 그리기 (대본과 100% 연동)")
    st.warning("""
    **⚠️ [발행 전 필수 검증 원칙] 한글 깨짐 유무 확인 & 검증 필수!**
    
    이미지 생성 후 말풍선 속 한글이 깨지거나 외계어로 뭉개지지 않았는지 반드시 확인하세요.
    - **한글이 또렷하면**: 그대로 블로그에 등록!
    - **한글이 뭉개졌다면**: "말풍선 속 글자를 '우와!', '대박!' 같은 2글자 단어로 바꿔서 다시 그려줘"라고 1회 재생성하거나, 대사를 본문 텍스트로 보완 후 안전하게 발행합니다.
    """)
    
    st.markdown("""
    💡 **초간단 3단계 이용법**:
    1. Gemini가 2단계에서 만들어준 **`[이미지 1 DALL-E 3 영문 프롬프트]`**를 복사합니다.
    2. ChatGPT 창에 **아래 출연 캐릭터 시트 사진들을 첨부**하고 프롬프트를 넣어 **컷 1~3 만화**를 생성합니다!
    3. 이어서 Gemini가 준 **`[이미지 2 DALL-E 3 영문 프롬프트]`**를 넣어 **컷 4~6 만화**를 생성하면 끝!
    """)
    
    # 4개 캐릭터 시트 표시
    c_cols = st.columns(4)
    with c_cols[0]:
        st.image("assets/characters/지치_시트.jpg", caption="지치 (새싹 요정 - 주인공)", use_container_width=True)
    with c_cols[1]:
        st.image("assets/characters/송이_시트.jpg", caption="송이 (깨끗한 삼색묘)", use_container_width=True)
    with c_cols[2]:
        st.image("assets/characters/초코_시트.jpg", caption="초코 (턱시도 고양이)", use_container_width=True)
    with c_cols[3]:
        st.image("assets/characters/AI로봇_시트.jpg", caption="AI 로봇 (도우미)", use_container_width=True)



# ==========================================
# 탭 3: 캐릭터 레퍼런스 시트
# ==========================================
with tab_chars:
    st.subheader("👥 지치 블로그 공식 캐릭터 4종 공식 시트")
    st.markdown("지치, 송이, 초코, AI 로봇의 턴어라운드 및 표정 시트입니다. ChatGPT에 첨부할 때 원본 파일로 활용하세요.")
    
    char_files = glob.glob("assets/characters/*.jpg")
    cols = st.columns(2)
    for i, cf in enumerate(char_files):
        with cols[i % 2]:
            st.image(cf, caption=os.path.basename(cf).replace("_시트.jpg", ""), use_container_width=True)
