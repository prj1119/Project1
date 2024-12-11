import streamlit as st

st.set_page_config(
    page_title="1차 프로젝트",
    page_icon="💗",
    layout="wide",
    # initial_sidebar_state="collapsed"
)

# st.title("프로젝트 목록")
st.markdown("<h1 style='text-align: center;'>프로젝트 목록</h1>", unsafe_allow_html=True)

st.subheader("1. 가구원수 비교")
with st.expander("시연 영상 보기"):
    st.video("./mp4/team5.mp4")
    st.page_link(page="./pages/1_가구원수 통계.py", label="[그래프 보기]", icon="🔗")

st.subheader("2. 뮤지컬 실시간 통계 차트")
with st.expander("시연 영상 보기"):
    st.video("./mp4/team5.mp4")
    st.page_link(page="./pages/2_뮤지컬 실시간 통계.py", label="[차트 보기]", icon="🔗")

st.subheader("3. 암환자수 통계 그래프")
with st.expander("시연 영상 보기"):
    st.video("./mp4/team5.mp4")
    st.page_link(page="./pages/3_암환자수 통계.py", label="[그래프 보기]", icon="🔗")

st.subheader("4. 베스트셀러 비교")
with st.expander("시연 영상 보기"):
    st.video("./mp4/team5.mp4")
    st.page_link(page="./pages/4_베스트셀러 통계.py", label="[그래프 보기]", icon="🔗")

st.subheader("5. 티켓 비교 그래프")
with st.expander("시연 영상 보기"):
    st.video("./mp4/team5.mp4")
    st.page_link(page="./pages/5_티켓 통계.py", label="[그래프 보기]", icon="🔗")

st.subheader("6. 음악사이트 장르별인기 차트 그래프")
with st.expander("시연 영상 보기"):
    st.video("./mp4/team5.mp4")
    st.page_link(page="./pages/6_음악사이트 장르별 인기 통계.py", label="[차트, 그래프 보기]", icon="🔗")
