import streamlit as st
import ast
import datetime as dt
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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from requests import get
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

# 데이터를 추출할 티켓링크 콘서트 연간 랭킹 페이지 주소
url1 = "https://www.ticketlink.co.kr/ranking?ranking=genre&categoryId=10&category2Id=14&category3Id=14&period=yearly"

# 위 티켓링크의 데이터를 반환하는 API 엔드포인트 주소
url2 = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/yearly?categoryId=10&categoryId2=14&categoryId3=0&menu=RANKING"


# Selenium 옵션 설정
options = Options()
# 브라우저를 백그라운드에서 실행
options.add_argument('--headless')

# Selenium WebDriver 초기화, 페이지 로드
driver = webdriver.Chrome(options=options)
driver.get(url1)

# 페이지 로드 대기
time.sleep(1)
# 콘서트 탭 클릭 (XPath로 버튼 선택)
driver.find_element(By.XPATH, '//*[@id="content"]/section[2]/div[2]/div/ul/li[2]/button').click()
driver.find_element(By.XPATH, '//*[@id="content"]/section[2]/div[3]/div[3]/div/ul/li[4]/button').click()

# API를 통해 각 콘서트의 상세 페이지 URL 목록을 가져오는 함수
def 상세화면주소():
    arr = []
    # API 호출, JSON 데이터 가져오기
    data = json.loads(get(url2).text)
    for row in data["data"]["rankingList"]:
        # 각 콘서트의 상세 페이지 URL 생성
        arr.append(f'https://www.ticketlink.co.kr/product/{row["productId"]}')
    return arr

# 콘서트 데이터 저장 리스트 초기화
items = []

# 메인 페이지 콘서트 데이터 추출 및 생성 함수
def 데이터생성():
    links = 상세화면주소()
    time.sleep(1)

    # 콘서트 랭킹의 각 행 데이터 가져오기
    trs = driver.find_elements(By.CSS_SELECTOR, "table.ranking_product_table > tbody > tr")

    # 각 행의 콘서트 데이터 크롤링
    for i in range(len(links)):
        # 제목, 예매율, 상세 페이지 링크 순
        title = trs[i].find_element(By.CSS_SELECTOR, "span.ranking_product_title").text
        period = trs[i].find_element(By.CSS_SELECTOR, "span.ranking_product_period").text
        place = trs[i].find_element(By.CSS_SELECTOR, "span.ranking_product_place").text
        rate = trs[i].find_element(By.CSS_SELECTOR, "span.rate_percent").text
        link = links[i]

        # 콘서트 데이터를 딕셔너리에 추가
        items.append({
            "title": title,
            "period": period,
            "place": place,
            "rate": rate,
            "link": link
        })
    return items

# 메인 페이지에서 추출한 데이터로 데이터프레임 생성
df = pd.DataFrame(데이터생성())
# 데이터프레임에 상세 페이지에서 가져올 가격 정보 열 추가 생성
df["price"] = None

# 상세 페이지에서 가격 정보 추출
for j in range(len(df)):
    # 상세 페이지 로드 및 대기
    driver.get(df.loc[j, "link"])
    time.sleep(1)
    # BeautifulSoup으로 HTML 파싱
    detail = bs(driver.page_source, 'html.parser')
    # '할인' 관련 정보를 제외하고 가격 정보 추출
    price_elements = [
    price for price in detail.select("ul.product_info_sublist > li.product_info_subitem > em.text_emphasis")
    if "할인" not in price.find_parent("ul").text
]

    # 텍스트에서 기타 요소를 제거하고 숫자로 변환
    price = [int(price.text.replace(",", "").replace("원", "").strip()) for price in price_elements]
    # 데이터프레임에 가격 정보 추가
    df.at[j, "price"] = price

# 열 순서가 제목, 예매율, 가격, 상세 페이지 주소인 콘서트 데이터 csv 파일 생성
df.to_csv("concert_data.csv", columns=["title", "period", "place", "rate", "price", "link"], encoding="utf-8-sig")
'''
with st.expander("데이터 수집 코드"):
    st.code(code1, language="python")


# 2. 데이터 전처리 과정
st.header("데이터 전처리 과정")
code2 = '''
import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('concert_data.csv')

# 'place' 열에서 '해당 없음'이 아닌 데이터만 필터링
df = df[df['place'] != '해당 없음']

# 'period' 열에서 시작 날짜만 추출
df['start_date'] = df['period'].str.split(' - ').str[0]

# 시작 날짜를 datetime 형식으로 변환
df['start_date'] = pd.to_datetime(df['start_date'], format='%Y.%m.%d')

# 시작 날짜 기준으로 정렬
df_sorted = df.sort_values(by='start_date', ascending=True)

# 정렬된 데이터프레임에서 정렬에 사용한 열을 제거
df_sorted = df_sorted.drop(columns=['start_date'])

# 정렬된 데이터프레임을 새로운 CSV 파일로 저장
df_sorted.to_csv('concert_data_sort.csv', index=False, encoding="utf-8-sig")

# 정렬된 데이터프레임에 남은 행 개수 출력
filter = len(df_sorted)
print(f"최종 콘서트 개수: {filter}")
'''
with st.expander("데이터 전처리 과정"):
    st.code(code2, language="python")


# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")

# 데이터프레임 시각화
st.subheader("2024 연간 콘서트 랭킹 TOP50")

# CSV 파일 읽기
df = pd.read_csv('concert_data.csv')

# 'place' 열에서 '해당 없음'이 아닌 데이터만 필터링
filtered_df = df[df['place'] != '해당 없음']

# 'Unnamed: 0' 열 제거
if 'Unnamed: 0' in filtered_df.columns:
    filtered_df = filtered_df.drop(columns=['Unnamed: 0'])

# 인덱스를 1부터 다시 지정
filtered_df.index = range(1, len(filtered_df) + 1)

# 'price' 열의 중복 제거 및 정렬 함수 정의
def 중복제거(price_list):
    # 문자열 형태 리스트를 실제 리스트로 변환
    if isinstance(price_list, str):
        price_list = ast.literal_eval(price_list)
    # 중복 제거, 내림차순 정렬
    return sorted(set(price_list), reverse=True)

# 'price' 열의 중복 요소 제거
if 'price' in filtered_df.columns:
    filtered_df['price'] = filtered_df['price'].apply(중복제거)

# Streamlit 화면에 표시
with st.expander("MD 구매 등 콘서트가 아닌 항목 필터링"):
    st.dataframe(filtered_df)


# 몇 월에 콘서트가 가장 많이 열렸는지 그래프
# 어디에서 콘서트가 가장 많이 열렸는지 순위표
# 최고가와 최저가 그래프
# 시기별 콘서트 출력 슬라이드


select = st.selectbox(
    label = "한식 메뉴",
    options = ("김치찌개", "된장찌개", "불백"),
    index = 0
)
