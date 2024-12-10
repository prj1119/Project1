import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="1. 가구원수 통계",
    page_icon="💗",
    # layout="wide",
    # initial_sidebar_state="collapsed"
)

st.title("가구원수 통계")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

options = Options()
# options.add_argument("--start-maximized") # 전체 화면 창으로 설정
# options.add_experimental_option("detach", True) # 창이 자동 닫기 무효화
options.add_argument('--headless') # 백그라운드 실행 옵션
download_dir = "C:\IDE"
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,  # 다운로드 위치
    "download.prompt_for_download": False,  # 다운로드 시 알림 없이 바로 저장
    "download.directory_upgrade": True,  # 디렉토리 경로가 변경되었을 때 자동으로 업데이트
    "safebrowsing.enabled": True  # 안전 브라우징 활성화
})

driver = webdriver.Chrome(options=options)
url = "https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1JC1511&vw_cd=MT_ZTITLE&list_id=&scrId=&seqNo=&lang_mode=ko&obj_var_id=&itm_id=&conn_path=MT_ZTITLE&path=%252Fvisual%252FpopulationKorea%252FPopulationDashBoardDetail.do"
driver.get(url)

time.sleep(10)
# 1단계: 첫 번째 iframe (상위 iframe)으로 전환 : iframe#iframe_rightMenu
step1 = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe#iframe_rightMenu")
    )
)
print(1, step1)
driver.execute_script("fnCloseTab('1');")
driver.switch_to.default_content()

# 데이터 유형 변경 : iframe#iframe_leftMenu
step0 = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe#iframe_leftMenu") 
    )
)
print(0, step0)

driver.execute_script('showStats("101","DT_1JC1501","N","A12_2015_1_10_10","MT_ZTITLE","");')
print("메뉴 선택 이동 완료")
driver.switch_to.default_content()
time.sleep(5)

# 1단계: 첫 번째 iframe (상위 iframe)으로 전환 : iframe#iframe_rightMenu
step1 = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe#iframe_rightMenu")
    )
)
print(1, step1)

# 2단계: 두 번째 iframe (중첩된 iframe)으로 전환 : iframe#iframe_centerMenu1
step2 = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe#iframe_centerMenu1")
    )
)
print(2, step2)

def 다운로드():
    # 1. 다운로드 클릭
    print(3, "5초간 잠시 대기!")
    time.sleep(5)
    driver.execute_script("popupControl('pop_downgrid', 'show', 'modal');") 

    # 2. 다운로드 시작
    driver.execute_script("fn_downGridSubmit();")
    time.sleep(2)

    # 3. 다운로드 창 닫기
    driver.execute_script("popupControl('pop_downgrid', 'hide', 'modal');")  

def 시점변경():
    다운로드()
    print(3, "1초간 잠시 대기!")
    time.sleep(1)
    반복다운로드()

def 반복다운로드():
    driver.execute_script("javascript:fn_timeSet();")
    time.sleep(1)
    list = driver.find_elements(By.CSS_SELECTOR, "#ft-id-4 span.fancytree-title")
    for i in range(1, len(list)):
        list[i - 1].click()
        list[i].click()
        time.sleep(1)
        driver.execute_script("javascript:fn_searchPopPrd('prd');")
        다운로드()
        driver.execute_script("javascript:fn_timeSet();")
    driver.execute_script("javascript:fn_searchPopPrd('prd');")

시점변경()

driver.switch_to.default_content()

print("종료!!")
time.sleep(5)
driver.quit()

# 1. 수집 코드
st.header("수집 코드")
code1 = '''

import os
import pandas as pd

temp_folder = 'C:\IDE\works\pj_temp'

file_list = os.listdir(temp_folder)

excel_arr = []


excel = pd.read_excel(temp_folder + "\\" + file_list[0], sheet_name='데이터', engine='openpyxl', index_col="행정구역별(읍면동)")
print(excel.iloc[0:,0])


###############
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# Streamlit 인터페이스

st.markdown("이 앱은 KOSIS 사이트에서 데이터를 자동으로 다운로드합니다.")

# 사용자로부터 입력 받기
download_dir = st.text_input("다운로드 경로 설정", value="C:\\IDE")
run_script = st.button("스크립트 실행")

if run_script:
    st.write("스크립트를 실행합니다...")

    # Selenium 옵션 설정
    options = Options()
    options.add_argument('--headless')  # 백그라운드 실행
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # 드라이버 시작
    driver = webdriver.Chrome(options=options)
    url = "https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1JC1511&vw_cd=MT_ZTITLE&list_id=&scrId=&seqNo=&lang_mode=ko&obj_var_id=&itm_id=&conn_path=MT_ZTITLE&path=%252Fvisual%252FpopulationKorea%252FPopulationDashBoardDetail.do"
    driver.get(url)

    try:
        # 첫 번째 iframe으로 전환
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe#iframe_rightMenu")
            )
        )
        driver.execute_script("fnCloseTab('1');")
        driver.switch_to.default_content()

        # 두 번째 iframe 전환 및 메뉴 이동
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe#iframe_leftMenu")
            )
        )
        driver.execute_script('showStats("101","DT_1JC1501","N","A12_2015_1_10_10","MT_ZTITLE","");')
        driver.switch_to.default_content()
        time.sleep(5)

        # 데이터 다운로드 함수
        def 다운로드():
            st.write("데이터 다운로드 중...")
            time.sleep(5)
            driver.execute_script("popupControl('pop_downgrid', 'show', 'modal');")
            driver.execute_script("fn_downGridSubmit();")
            time.sleep(2)
            driver.execute_script("popupControl('pop_downgrid', 'hide', 'modal');")

        # 데이터 시점 변경 및 반복 다운로드
        def 반복다운로드():
            driver.execute_script("javascript:fn_timeSet();")
            time.sleep(1)
            list = driver.find_elements(By.CSS_SELECTOR, "#ft-id-4 span.fancytree-title")
            for i in range(1, len(list)):
                list[i - 1].click()
                list[i].click()
                time.sleep(1)
                driver.execute_script("javascript:fn_searchPopPrd('prd');")
                다운로드()
                driver.execute_script("javascript:fn_timeSet();")
            driver.execute_script("javascript:fn_searchPopPrd('prd');")

        # 실행
        다운로드()
        반복다운로드()

        st.success("작업이 완료되었습니다!")
    except Exception as e:
        st.error(f"에러 발생: {e}")
    finally:
        driver.quit()

'''
st.code(code1, language="python")

# 2. 데이터 전처리 과정
st.header("데이터 전처리 과정")
code2 = '''

'''
st.code(code2, language="python")

# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")