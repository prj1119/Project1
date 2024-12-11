import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="3. 암환자수 통계",
    page_icon="💗",
    layout="wide",
    # initial_sidebar_state="collapsed"
)

if 'slider_value' not in st.session_state:
    st.session_state.slider_value = (2017, 2022)

if 'line_chart_value' not in st.session_state:
    st.session_state.line_chart_value = pd.DataFrame([])

def makeData():
    url = "https://www.index.go.kr/unity/potal/eNara/sub/showStblGams3.do?stts_cd=277002&idx_cd=2770&freq=Y&period=N"
    df = pd.read_html(url)[0].drop(0)
    df = df.drop('Unnamed: 1', axis=1)
    data1 = df.iloc[::2,:].set_index(keys="Unnamed: 0")
    st.session_state.line_chart_value = data1.filter(items=makeCol(data1)).transpose()

def makeCol(data1):
    point = []
    target = st.session_state.slider_value
    for i in range(target[0], target[1]+1):
        point.append(str(i))
    if len(point) == 0:
        point = list(data1.columns)
    return point




# 접속한 아이프레임에서 돌아오기 
# driver.switch_to.default_content()

# 단독으로 수집 할 경우 종료 함수
# driver.quit()
# 1. 수집 코드
st.header("수집 코드")
code1 = '''
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="3. 암환자수 통계",
    page_icon="💗",
    layout="wide",
    # initial_sidebar_state="collapsed"
)

if 'slider_value' not in st.session_state:
    st.session_state.slider_value = (2017, 2022)

if 'line_chart_value' not in st.session_state:
    st.session_state.line_chart_value = pd.DataFrame([])

def makeData():
    url = "https://www.index.go.kr/unity/potal/eNara/sub/showStblGams3.do?stts_cd=277002&idx_cd=2770&freq=Y&period=N"
    df = pd.read_html(url)[0].drop(0)
    df = df.drop('Unnamed: 1', axis=1)
    data1 = df.iloc[::2,:].set_index(keys="Unnamed: 0")
    st.session_state.line_chart_value = data1.filter(items=makeCol(data1)).transpose()


'''
st.code(code1, language="python")

# 2. 데이터 전처리 과정
st.header("데이터 전처리 과정")
code2 = '''

def makeCol(data1):
    point = []
    target = st.session_state.slider_value
    for i in range(target[0], target[1]+1):
        point.append(str(i))
    if len(point) == 0:
        point = list(data1.columns)
    return point

sl = st.slider(
    label="년도 범위를 변경하세요", min_value=1989, max_value=2023, value=st.session_state.slider_value, step=1
)

# st.write(st.session_state.slider_value)
if st.button("선택한 범위 확인"):
    st.session_state.slider_value = sl
    makeData()

if st.session_state.line_chart_value.empty:
    st.markdown("<h4 style='text-align: center;'>출력할 내용이 없습니다.</h4>", unsafe_allow_html=True)
else:
    st.dataframe(st.session_state.line_chart_value, use_container_width=True)
    st.line_chart(st.session_state.line_chart_value)

'''
st.code(code2, language="python")

# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")

sl = st.slider(
    label="년도 범위를 변경하세요", min_value=1989, max_value=2023, value=st.session_state.slider_value, step=1
)

# st.write(st.session_state.slider_value)
if st.button("선택한 범위 확인"):
    st.session_state.slider_value = sl
    makeData()


if st.session_state.line_chart_value.empty:
    st.markdown("<h4 style='text-align: center;'>출력할 내용이 없습니다.</h4>", unsafe_allow_html=True)
else:
    st.dataframe(st.session_state.line_chart_value, use_container_width=True)
    st.line_chart(st.session_state.line_chart_value)