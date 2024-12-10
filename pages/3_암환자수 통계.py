import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="3. 암환자수 통계",
    page_icon="💗",
    # layout="wide",
    # initial_sidebar_state="collapsed"
)

st.title("암환자수 통계")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import streamlit as st

url = "https://www.index.go.kr/unity/potal/main/EachDtlPageDetail.do?idx_cd=2770"

options = Options()
options.add_argument('--headless')
# options.add_argument("--start-maximized") # 전체 화면 창으로 설정
# options.add_experimental_option("detach", True) # 창이 자동 닫기 무효화

driver = webdriver.Chrome(options=options)
driver.get(url)

step1 = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe#showStblGams")
    )
)

ths = driver.find_elements(By.CSS_SELECTOR, "table#t_Table_277002 > thead > tr#trHeader277002_1 > th")
trs = driver.find_elements(By.CSS_SELECTOR, "table#t_Table_277002 > tbody > tr")

#열생성
def makeCol():
    cols = []
    del ths[0]
    for col in ths:
        cols.append(col.text)
    return cols



def makeData():
    data = []
    index = []
    for i in range(len(trs)):
        if i % 2 != 0:
            continue
        arr = []
        for td in trs[i].find_elements(By.CSS_SELECTOR, "td"):
            arr.append(int(td.text.replace(",","")))
        #data.append(arr)
        data.append(arr)
        index.append(trs[i].find_elements(By.CSS_SELECTOR, "th")[0].text)
    return pd.DataFrame(data=data, index=index, columns=makeCol())


df = makeData()
df = df.transpose()


# 접속한 아이프레임에서 돌아오기 
# driver.switch_to.default_content()

# 단독으로 수집 할 경우 종료 함수
# driver.quit()
# 1. 수집 코드
st.header("수집 코드")
code1 = '''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import streamlit as st

url = "https://www.index.go.kr/unity/potal/main/EachDtlPageDetail.do?idx_cd=2770"

options = Options()
options.add_argument('--headless')
# options.add_argument("--start-maximized") # 전체 화면 창으로 설정
# options.add_experimental_option("detach", True) # 창이 자동 닫기 무효화

driver = webdriver.Chrome(options=options)
driver.get(url)

step1 = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe#showStblGams")
    )
)

ths = driver.find_elements(By.CSS_SELECTOR, "table#t_Table_277002 > thead > tr#trHeader277002_1 > th")
trs = driver.find_elements(By.CSS_SELECTOR, "table#t_Table_277002 > tbody > tr")

#열생성
def makeCol():
    cols = []
    del ths[0]
    for col in ths:
        cols.append(col.text)
    return cols



def makeData():
    data = []
    index = []
    for i in range(len(trs)):
        if i % 2 != 0:
            continue
        arr = []
        for td in trs[i].find_elements(By.CSS_SELECTOR, "td"):
            arr.append(int(td.text.replace(",","")))
        #data.append(arr)
        data.append(arr)
        index.append(trs[i].find_elements(By.CSS_SELECTOR, "th")[0].text)
    return pd.DataFrame(data=data, index=index, columns=makeCol())


df = makeData()
'''
st.code(code1, language="python")

# 2. 데이터 전처리 과정
st.header("데이터 전처리 과정")
code2 = '''
df = df.transpose()
'''
st.code(code2, language="python")

# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")

sl = st.slider(
    "여기라벨내용",1989.0,2023.0,(2000.0,2020.0),step=1.0
)

st.write(sl)
#연도 시작~ 끝, 보일위치

st.line_chart(df)