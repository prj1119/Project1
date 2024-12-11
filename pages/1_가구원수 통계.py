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

# 1. 수집 코드
st.header("수집 코드")
code1 = '''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import streamlit as st
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator, FuncFormatter
from matplotlib.ticker import ScalarFormatter
import shutil # 기본 폴더 삭제

import openpyxl #시트 이름 출력

# 데이터 파일 다운로드 기본 경로 
global temp_folder 
global font_path
global font_prop

# 한글 폰트 설정 (예: 'NanumGothic' 폰트 사용)
font_path = "./NanumGothic.ttf"  # 시스템에 따라 경로가 다를 수 있음
font_prop = font_manager.FontProperties(fname=font_path)

temp_folder = r'C:\IDE\works\pj_temp'


def 셀리니엄데이터수집():

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


    shutil.rmtree(temp_folder, ignore_errors=True)

    if not os.path.isdir(temp_folder):                                                           
        os.mkdir(temp_folder)

    options = Options()
    # options.add_argument("--start-maximized") # 전체 화면 창으로 설정
    # options.add_experimental_option("detach", True) # 창이 자동 닫기 무효화
    options.add_argument('--headless') # 백그라운드 실행 옵션
    options.add_experimental_option("prefs", {
        "download.default_directory": temp_folder,  # 다운로드 위치
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

    시점변경()

    driver.switch_to.default_content()

    print("종료!!")
    time.sleep(5)
    driver.quit()




def 데이터전처리():   


    # List all files in the folder
    file_list = os.listdir(temp_folder)

    # Y축 값을 10,000 단위로 설정
    def y_axis_formatter(y, pos):
        return f'{int(y / 10000)}'  # 10,000으로 나누고 '만'을 추가


    def 데이터수집(file_list):

        # 사용 값 선언 및 초기화
        col = []
        idx = []
        values = []
        seet_name = ""

        for i in range(len(file_list)):
            #print(file_list[i])        
            
            # Load the first Excel file
            excel = pd.read_excel(
                os.path.join(temp_folder, file_list[i]),
                sheet_name="데이터",
                engine='openpyxl',
                index_col="행정구역별(읍면동)",  # '행정구역별(읍면동)'을 인덱스로 설정
                usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 20]
            )

            # 시트 이름 (ex:2023)
            seet_name = excel.columns.to_list()[0]

            # 컬럼 리스트 (1차원 배열)
            col = excel.iloc[0].to_list()

            # 인덱스 (1차원 배열)
            idx = excel.iloc[1:, :0].index.to_list()

            # 값 리스트 (2차원 배열)
            values = excel.iloc[1:, 0:].values

            if len(idx) == values.shape[0] and len(col) == values.shape[1]:
                df = pd.DataFrame(values, index=idx, columns=col)
            else:
                raise ValueError("Mismatch in dimensions between idx, col, and values.")

            print(df)

            if i == 0:
                with pd.ExcelWriter('읍면동_가구형태별_DATA.xlsx', mode='w', engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=seet_name, index=True)
            else:
                with pd.ExcelWriter('읍면동_가구형태별_DATA.xlsx', mode='a', engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=seet_name, index=True)
            
    # 데이터 전처리 함수 실행
    데이터수집(file_list)



'''
st.code(code1, language="python")

# 2. 데이터 전처리 과정
st.header("데이터 전처리 과정")
code2 = '''

def 데이터전처리시작():   


    # List all files in the folder
    file_list = os.listdir(temp_folder)

    # Y축 값을 10,000 단위로 설정
    def y_axis_formatter(y, pos):
        return f'{int(y / 10000)}'  # 10,000으로 나누고 '만'을 추가


    def 데이터전처리(file_list):

        # 사용 값 선언 및 초기화
        col = []
        idx = []
        values = []
        seet_name = ""

        for i in range(len(file_list)):
            #print(file_list[i])        
            
            # Load the first Excel file
            excel = pd.read_excel(
                os.path.join(temp_folder, file_list[i]),
                sheet_name="데이터",
                engine='openpyxl',
                index_col="행정구역별(읍면동)",  # '행정구역별(읍면동)'을 인덱스로 설정
                usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 20]
            )

            # 시트 이름 (ex:2023)
            seet_name = excel.columns.to_list()[0]

            # 컬럼 리스트 (1차원 배열)
            col = excel.iloc[0].to_list()

            # 인덱스 (1차원 배열)
            idx = excel.iloc[1:, :0].index.to_list()

            # 값 리스트 (2차원 배열)
            values = excel.iloc[1:, 0:].values

            if len(idx) == values.shape[0] and len(col) == values.shape[1]:
                df = pd.DataFrame(values, index=idx, columns=col)
            else:
                raise ValueError("Mismatch in dimensions between idx, col, and values.")

            print(df)

            if i == 0:
                with pd.ExcelWriter('읍면동_가구형태별_DATA.xlsx', mode='w', engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=seet_name, index=True)
            else:
                with pd.ExcelWriter('읍면동_가구형태별_DATA.xlsx', mode='a', engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name=seet_name, index=True)
            
    # 데이터 전처리 함수 실행
    데이터전처리(file_list)


'''
st.code(code2, language="python")

# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")

import openpyxl #시트 이름 출력
from matplotlib import font_manager
from matplotlib.ticker import MaxNLocator, FuncFormatter
import matplotlib.pyplot as plt

# 데이터 파일 다운로드 기본 경로 
global temp_folder 
global font_path
global font_prop

# 한글 폰트 설정 (예: 'NanumGothic' 폰트 사용)
font_path = "./NanumGothic.ttf"  # 시스템에 따라 경로가 다를 수 있음
font_prop = font_manager.FontProperties(fname=font_path)

temp_folder = r'C:\IDE\works\pj_temp'

def 그래프시각화시작():    
    
    # 시트 가져오기
    fileName = r'./읍면동_가구형태별_DATA.xlsx'
    wb = openpyxl.load_workbook(fileName)
    sheet_names = wb.sheetnames

    st.sidebar.header("시트 선택")
    selected_sheet = st.sidebar.selectbox("시트를 선택하세요", sheet_names)

    # Load the first Excel file
    excel = pd.read_excel(fileName,  sheet_name=selected_sheet, engine='openpyxl', index_col=0)


    # Y축 값을 10,000 단위로 설정
    def y_axis_formatter(y, pos):
        return f'{int(y / 10000)}'  # 10,000으로 나누고 '만'을 추가

    # matplotlib로 선 그래프 그리기
    fig, ax = plt.subplots(figsize=(15, 6))  # 그래프 크기 설정
    for column in excel.columns:
        ax.plot(excel.index, excel[column], label=column)  # 각 컬럼에 대해 선 그래프를 그립니다.

    # 한글 폰트 설정
    ax.set_title(selected_sheet+"년도 가구수 표시 (단위 : 만)", fontproperties=font_prop)  # 제목 설정
    ax.set_xlabel("(지역별)", fontproperties=font_prop)  # X축 레이블 설정
    ax.set_ylabel("(Value)", fontproperties=font_prop)  # Y축 레이블 설정
    plt.xticks(rotation=90, ha='center', fontproperties=font_prop)  # X축 레이블 회전

    # Y축 값을 정수로 설정
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Y축의 값을 10,000 단위로 설정하고 '만' 단위로 표시
    ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

    # y축의 지수 표시를 일반 숫자로 바꿔줍니다.
    #ax.yaxis.set_major_formatter(ScalarFormatter())

    # 범례 추가
    ax.legend(title="Title", prop=font_prop)

    # Streamlit에 matplotlib 차트 표시
    st.pyplot(fig)

그래프시각화시작()