import streamlit as st
import pandas as pd
from team4.script import code1
from team4.script import code2
from team4.script import code3
from team4.kb import getKbData
from team4.yes24 import getYes24Data
from team4.view import show

st.set_page_config(
    page_title="4. 베스트셀러 통계",
    page_icon=":books:",
    # layout="wide"
    # initial_sidebar_state="collapsed"
)

if 'books_kb_df' not in st.session_state:
    st.session_state.books_kb_df = pd.DataFrame([])

if 'books_yes24_df' not in st.session_state:
    st.session_state.books_yes24_df = pd.DataFrame([])

st.title("베스트셀러 통계")

# 1. 수집 코드
# st.header("수집 코드1")
with st.expander("수집 코드1"):
    st.code(code1, language="python")

# st.header("수집 코드2")
with st.expander("수집 코드2"):
    st.code(code2, language="python")

# 2. 데이터 전처리 과정
# st.header("데이터 전처리 과정")
with st.expander("데이터 전처리 과정"):
    st.code(code3, language="python")

# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")
col1, col2 = st.columns(2)
with col1:
    st.subheader("교보문고 순위 리스트")
    if st.button("교보문고 수집하기"):
        st.session_state.books_kb_df = getKbData(10)

with col2:
    st.subheader("yes24 순위 리스트")
    if st.button("yes24 수집하기"):
        st.session_state.books_yes24_df = getYes24Data(30)

if st.session_state.books_kb_df.empty:
    pass
else:
    st.subheader("교보문고 수집 데이터")
    st.dataframe(st.session_state.books_kb_df)

if st.session_state.books_yes24_df.empty:
    pass
else:
    show(st.session_state.books_yes24_df)
