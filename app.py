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

st.set_page_config(page_title="지치 컴퍼니 올인원 통합 관제 센터", page_icon="🏢", layout="wide")

st.markdown("""
<style>
    /* JICHI COMPANY — Midnight Neon Tech UI Theme */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Noto+Sans+KR:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans KR', sans-serif;
    }
    .stApp {
        background-color: #080a0d !important;
        color: #f1f5f9 !important;
    }
    .main-header { 
        font-size: 28px; 
        font-weight: 800; 
        color: #ffffff; 
        letter-spacing: -0.5px;
        margin-bottom: 4px; 
    }
    .main-header span {
        color: #a3e635;
    }
    .sub-header { 
        font-size: 14px; 
        color: #94a3b8; 
        margin-bottom: 24px; 
    }
    .stTabs [data-baseweb="tab-list"] { 
        gap: 8px; 
        background-color: #12161f;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .stTabs [data-baseweb="tab"] { 
        height: 48px; 
        white-space: pre-wrap; 
        font-size: 14px; 
        font-weight: 700; 
        color: #94a3b8 !important;
        border-radius: 8px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1c222d !important;
        color: #a3e635 !important;
        border-bottom: 2px solid #a3e635 !important;
    }
    
    /* 부서/에이전트 다크 네온 카드 */
    .dept-card {
        background: linear-gradient(145deg, #12161f, #0d1117) !important;
        color: #f1f5f9 !important;
        padding: 20px !important;
        border-radius: 16px !important;
        border-left: 5px solid #a3e635 !important;
        border-top: 1px solid rgba(255,255,255,0.08) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
        border-bottom: 1px solid rgba(255,255,255,0.08) !important;
        margin-bottom: 16px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5) !important;
    }
    .dept-card h4, .dept-card h5 {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin-bottom: 8px !important;
    }
    .dept-card b, .dept-card strong {
        color: #a3e635 !important;
    }
    .dept-card p, .dept-card span, .dept-card li {
        color: #cbd5e1 !important;
        line-height: 1.6 !important;
    }
    
    /* Aside 탭 박스 */
    .aside-box {
        background: #12161f !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        padding: 18px !important;
        margin-bottom: 16px !important;
    }
    .aside-box h5 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .aside-box b, .aside-box strong {
        color: #38bdf8 !important;
    }
    .aside-box span, .aside-box p, .aside-box li {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🏢 지치 컴퍼니(Jichi Company) 올인원 웹 관제 센터 (Ver 2.0)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">👑 사장님의 비전 아래, 전 부서(코부장·코서치·코디터·코자이너·코리티·Aside)가 완벽 분업화된 공식 워크스페이스입니다.</div>', unsafe_allow_html=True)

# 🚨 긴급 비상 안전 가동 센터 (Fail-Safe 배너)
col_alert1, col_alert2 = st.columns([3, 1])
with col_alert1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1a0f12, #241419); border: 2px solid #e32652; padding: 14px 20px; border-radius: 14px; margin-bottom: 16px; box-shadow: 0 0 25px rgba(227,38,82,0.25);">
        <span style="font-size: 15px; font-weight: 800; color: #ff4d6d;">🚨 [아침 9시 무인 발행 안전 관제 시스템 가동 중 — Fail-Safe]</span><br/>
        <span style="font-size: 13px; color: #fecdd3; line-height: 1.5;">
            AI 기사 3편 및 웹툰이 09:03까지 발행되지 않으면 <b>네이버 메일로 긴급 알림</b>이 즉시 발송됩니다. 출근길 이상 감지 시 오른쪽 비상 버튼을 눌러주세요!
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

tab_org, tab_news, tab_webtoon, tab_aside, tab_chars = st.tabs([
    "🏢 1. 지치컴퍼니 조직도 & R&R", 
    "📰 2. 코서치 & 코부장의 AI 뉴스실", 
    "🎨 3. 코서치·코디터·코자이너 웹툰 제작실", 
    "🤖 4. Aside RPA 무인자동화실", 
    "👥 5. 전속 스타 캐릭터 시트"
])

# ==========================================
# 탭 1: 지치컴퍼니 조직도 & R&R
# ==========================================
with tab_org:
    st.subheader("🏢 지치 컴퍼니 공식 조직 체계 및 6대 부서 R&R")
    st.markdown("사장님(CEO)의 지휘 아래 각 부서 전용 폴더와 고유 역할이 100% 분업화되어 운영됩니다.")

    col_ceo, col_coo = st.columns(2)
    with col_ceo:
        st.markdown("""
        <div class="dept-card">
            <h4>👑 사장님 (CEO & 총괄 프로듀서)</h4>
            <ul>
                <li><b>핵심 역할</b>: 전사 사업 방향 수립, 최종 포스팅 승인</li>
                <li><b>최근 특급 성과</b>: 
                    <ul>
                        <li><b>캐릭터 붕괴 제로 황금 공식</b> 직접 발견 (텍스트 배제 + 시트 사진 위임)</li>
                        <li><b>리센느 '원이대로' 마산대 축제</b> 킬러 콘텐츠 기획 및 직접 집필</li>
                    </ul>
                </li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_coo:
        st.markdown("""
        <div class="dept-card">
            <h4>🌱 코부장 (COO & 총괄 본부장)</h4>
            <ul>
                <li><b>전용 폴더</b>: <code>01_코부장_총괄/</code></li>
                <li><b>핵심 역할</b>: 전체 자동화 프로세스 관리, 스크립트 개발 총괄</li>
                <li><b>주요 업무</b>: 데일리 무인 스케줄러, 모바일 포맷터, 자산 원장 관리, Aside 연동 총괄</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 👥 5대 실무 부서별 전용 폴더 및 업무 분담")
    
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.markdown("""
        <div class="dept-card" style="border-left-color: #29B6F6;">
            <h5>🔎 코서치 (Scout 자료실)</h5>
            <b>폴더</b>: <code>02_코서치_자료/</code><br/>
            • 편의점 매대/패키지/단면 실사 발굴<br/>
            • 상하단 텍스트 및 워터마크 정밀 도려내기 (크롭 정제)<br/>
            • 저작권 100% 무결점 팩트 컷 전달
        </div>
        """, unsafe_allow_html=True)
    with col_d2:
        st.markdown("""
        <div class="dept-card" style="border-left-color: #AB47BC;">
            <h5>✍️ 코디터 (Editor 집필실)</h5>
            <b>폴더</b>: <code>03_코디터_원고/</code><br/>
            • 상반부(1~4)+하반부(5~8) 8컷 콘티 집필<br/>
            • <b>대사 1~2문장 슬림화 및 숏폼 티키타카</b><br/>
            • 친근한 구어체 7대 원칙 준수
        </div>
        """, unsafe_allow_html=True)
    with col_d3:
        st.markdown("""
        <div class="dept-card" style="border-left-color: #FF7043;">
            <h5>🎨 코자이너 (Designer 디자인실)</h5>
            <b>폴더</b>: <code>04_코자이너_프롬프트/</code><br/>
            • ChatGPT 4분할 3D Pixar 프롬프트 작성<br/>
            • <b>캐릭터 외형 설명 완전 배제</b> (시트 위임)<br/>
            • <code>[CHATGPT 컷 복사...]</code> 태그 명시<br/>
            • 엔딩 <code>좋아요 & 구독 ❤️</code> 팻말 설계
        </div>
        """, unsafe_allow_html=True)

    col_d4, col_d5 = st.columns(2)
    with col_d4:
        st.markdown("""
        <div class="dept-card" style="border-left-color: #26A69A;">
            <h5>🔍 코리티 (QA Inspector 검사실)</h5>
            <b>폴더</b>: <code>05_코리티_검수/</code><br/>
            • 스마트에디터 불릿 점(•) 및 번호 리스트 트리거 차단<br/>
            • 모바일 18~22자 줄바꿈 및 카드 링크 검증<br/>
            • <b>[사장님 지침] 코부장 검사 항목과 중복되더라도 철저한 교차 검증 수행</b>
        </div>
        """, unsafe_allow_html=True)
    with col_d5:
        st.markdown("""
        <div class="dept-card" style="border-left-color: #FFA726;">
            <h5>🤖 Aside RPA 봇 (무인자동화실)</h5>
            <b>폴더</b>: <code>06_Aside_자동화/</code><br/>
            • 네이버 블로그 임시저장함 진입 및 프롬프트 1·2세트 일괄 추출<br/>
            • ChatGPT 2장 연속 생성 및 다운로드 (V3 원스톱 배치)<br/>
            • 블로그 사진 업로드 및 최종 원클릭 발행
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 탭 2: AI 트렌드 기사 (코서치 & 코부장)
# ==========================================
with tab_news:
    st.subheader("📰 AI 트렌드 기사 수집 & 발행 관제 (코서치 & 코부장)")
    
    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        if st.button("🔄 허용 출처 6곳 실시간 뉴스 수집", use_container_width=True):
            with st.spinner("AI타임스, TechCrunch 등 최신 소식 수집 중..."):
                st.session_state["news_items"] = collector.get_all_sources()
                st.success(f"{len(st.session_state.get('news_items', []))}건 수집 완료!")
    with col_info:
        news_list = st.session_state.get("news_items", [])
        if news_list:
            st.info(f"현재 총 {len(news_list)}개의 최신 기사가 수집되었습니다.")
        else:
            st.write("👈 버튼을 눌러 글로벌 빅테크 및 IT 뉴스를 실시간 수집하세요.")

    if news_list:
        st.markdown("**📋 수집된 기사 목록:**")
        news_options = [f"【{item['slot']}】 {item['source']} ｜ {item['title']}" for item in news_list]
        chosen_idx = st.radio(
            "기사 선택",
            range(len(news_options)),
            format_func=lambda x: news_options[x],
            label_visibility="collapsed"
        )
        selected_news = news_list[chosen_idx]
        if selected_news:
            st.text_input("선택된 기사 제목", value=selected_news.get('title', ''))
            st.text_input("출처 URL", value=selected_news.get('url', ''))

# ==========================================
# 탭 3: 웹툰 제작실 (코서치·코디터·코자이너)
# ==========================================
with tab_webtoon:
    st.subheader("🎨 웹툰 기획 & 프롬프트 제작실 (코서치 · 코디터 · 코자이너)")
    
    st.markdown("""
    <div class="rule-card">
        <b>💡 [사장님 확정 웹툰 제작 3대 황금 공식]</b><br/>
        1. <b>캐릭터 외형 텍스트 일체 금지</b>: 챗GPT 프롬프트에 외형 텍스트를 빼고 캐릭터 시트 사진에 100% 위임하여 비주얼 붕괴 0% 달성!<br/>
        2. <b>대화 텍스트 1~2문장 슬림화</b>: 이미지가 풍부한 비주얼을 전달하므로 대본은 모바일 숏폼에 맞게 경쾌한 티키타카 유지!<br/>
        3. <b>[CHATGPT 컷 복사 시작/끝]</b>: 사장님께서 한 번에 복사-붙여넣기 하실 수 있도록 규격화된 태그 제공!
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📸 최근 발행 웹툰 현황 (실사 팩트 & 웹툰 컷)")
    w_cols = st.columns(3)
    with w_cols[0]:
        st.image("02_코서치_자료/rescene_wonidaero_meme.png", caption="[코서치] 리센느 원이대로 밈 실사", use_container_width=True)
    with w_cols[1]:
        st.image("02_코서치_자료/masan_univ_stage.png", caption="[코서치] 마산대학교 축제 무대 실사", use_container_width=True)
    with w_cols[2]:
        st.image("02_코서치_자료/wonidaero_road_real.png", caption="[코서치] 창원 원이대로 표지판 도로", use_container_width=True)

# ==========================================
# 탭 4: Aside RPA 무인자동화실
# ==========================================
with tab_aside:
    st.subheader("🤖 Aside 브라우저 RPA 무인자동화 가이드 (V3 원스톱 배치)")
    st.markdown("브라우저 탭 간의 불필요한 왕복을 완전히 없앤 최신 자동화 시나리오입니다.")

    st.markdown("""
    <div class="aside-box">
        <h4>🚀 Aside 3단 원스톱(Batch) 실행 플로우</h4>
        <ol>
            <li><b>Phase 1 (블로그)</b>: 임시저장함 진입 ➜ 최신 웹툰 글 로드 ➜ <code>PROMPT_1</code>과 <code>PROMPT_2</code> 일괄 추출!</li>
            <li><b>Phase 2 (ChatGPT)</b>: 'AI웹툰' 스레드 접속 ➜ 프롬프트 1·2 연속 전송 및 <b>[다운로드(↓)] 클릭으로 PC 저장</b>!</li>
            <li><b>Phase 3 (블로그)</b>: 블로그 복귀 ➜ 1번·2번 사진 자리에 다운로드 파일 정식 업로드 ➜ <b>우측 상단 [발행] 2회 클릭 끝!</b></li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.info("💡 **임시저장 글 식별 팁**: 글쓰기 진입 시 '작성 중인 글이 있습니다' 팝업의 [확인]을 누르면 가장 최신 글이 즉시 로드됩니다.")
    with col_a2:
        st.success("✅ **에러 차단 팁**: 우클릭 복사 대신 챗GPT [다운로드] 버튼을 이용해 네이버 [사진] 버튼으로 업로드하므로 100% 무결점!")

# ==========================================
# 탭 5: 전속 스타 캐릭터 시트
# ==========================================
with tab_chars:
    st.subheader("👥 지치 컴퍼니 공식 전속 스타 4총사 시트")
    st.markdown("ChatGPT에 첨부할 때 사용하는 고해상도 공식 턴어라운드 시트입니다.")
    
    char_files = glob.glob("assets/characters/*.jpg")
    cols = st.columns(4)
    for i, cf in enumerate(sorted(char_files)):
        with cols[i % 4]:
            c_name = os.path.basename(cf).replace("_시트.jpg", "")
            st.image(cf, caption=c_name, use_container_width=True)
