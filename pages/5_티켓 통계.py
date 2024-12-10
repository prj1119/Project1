import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="5. 티켓 통계",
    page_icon="💗",
    # layout="wide",
    # initial_sidebar_state="collapsed"
)

st.title("티켓 통계")

# 1. 수집 코드
st.header("수집 코드")
code1 = '''

'''
st.code(code1, language="python")

# 2. 데이터 전처리 과정
st.header("데이터 전처리 과정")
code2 = '''

'''
st.code(code2, language="python")

# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")
