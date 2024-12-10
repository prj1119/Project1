import streamlit as st

st.set_page_config(
    page_title="1차 프로젝트",
    page_icon="💗",
    layout="wide",
    # initial_sidebar_state="collapsed"
)

# st.title("프로젝트 목록")
st.markdown("<h1 style='text-align: center;'>프로젝트 목록</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

col1.header("1. 가구원수 비교")
col1.page_link(page="./pages/1_가구원수 통계.py", label="[그래프 보기]", icon="🔗")

col1.header("2. 뮤지컬 실시간 통계 차트")
col1.page_link(page="./pages/2_뮤지컬 실시간 통계.py", label="[차트 보기]", icon="🔗")

col1.header("3. 암환자수 통계 그래프")
col1.page_link(page="./pages/3_암환자수 통계.py", label="[그래프 보기]", icon="🔗")

col2.header("4. 베스트셀러 비교")
col2.page_link(page="./pages/4_베스트셀러 통계.py", label="[그래프 보기]", icon="🔗")

col2.header("5. 티켓 비교 그래프")
col2.page_link(page="./pages/5_티켓 통계.py", label="[그래프 보기]", icon="🔗")

col2.header("6. 음악사이트 장르별인기 차트 그래프")
col2.page_link(page="./pages/6_음악사이트 장르별 인기 통계.py", label="[차트, 그래프 보기]", icon="🔗")
