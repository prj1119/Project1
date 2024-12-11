import streamlit as st
import ast
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

st.set_page_config(
    page_title="5. 티켓 통계",
    page_icon="💗",
    layout="wide",
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
        # 제목, 기간, 장소 예매율, 상세 페이지 링크 순
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

# 열 순서가 제목, 기간, 장소, 예매율, 가격, 상세 페이지 주소인 콘서트 데이터 csv 파일 생성
df.to_csv("concert_data.csv", columns=["title", "period", "place", "rate", "price", "link"], encoding="utf-8-sig")
'''
with st.expander("데이터 수집 코드"):
    st.code(code1, language="python")


# 2. 데이터 전처리 과정
st.header("데이터 전처리 과정")
code2 = '''
import pandas as pd
import ast

# CSV 파일 읽기
df = pd.read_csv('concert_data.csv')

# 'place' 열에서 '해당 없음'이 아닌 데이터만 필터링
df = df[df['place'] != '해당 없음']

def 중복제거(price_list):
    # 문자열 형태의 리스트를 실제 리스트로 변환
    if isinstance(price_list, str):
        price_list = ast.literal_eval(price_list)
    # 중복 제거 후 정렬
    return sorted(set(price_list), reverse=True)

# 'price' 열에 중복 제거 함수 적용
if 'price' in df.columns:
    df['price'] = df['price'].apply(중복제거)

df = df.drop(columns=['Unnamed: 0'])

# 정렬된 데이터프레임을 새로운 CSV 파일로 저장
df.to_csv('concert_data_sort.csv', index=False, encoding="utf-8-sig")

# 정렬된 데이터프레임에 남은 행 개수 출력
filter = len(df)
print(f"최종 콘서트 개수: {filter}")
'''
with st.expander("데이터 전처리 과정"):
    st.code(code2, language="python")


# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")

# 데이터프레임 시각화
st.subheader("2024 연간 콘서트 랭킹 TOP50")

# CSV 파일 읽기
df = pd.read_csv('./ticketdata/concert_data_sort.csv')

# 인덱스를 1부터 다시 지정
df.index = range(1, len(df) + 1)

# df의 문자열을 리스트로 변환하는 함수
def 리스트변환(price_list):
    if isinstance(price_list, str):
        return ast.literal_eval(price_list)
    return price_list

# 'price' 문자열을 리스트로 변환
if 'price' in df.columns:
    df['price'] = df['price'].apply(리스트변환)

# Streamlit 화면에 표시
with st.expander("MD 구매 등 콘서트가 아닌 항목 필터링"):
    st.dataframe(df)

# 'period' 열에서 시작 날짜 추출
df['start_date'] = df['period'].str.split(' - ').str[0]
# 시작 날짜를 datetime 형식으로 변환
df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
df['year_month'] = df['start_date'].dt.to_period('M')


# 글꼴 설정
font_path = "./ticketdata/NanumGothic.ttf"
font_prop = font_manager.FontProperties(fname=font_path)

# 몇 월에 콘서트가 가장 많이 열렸는지 그래프
# 어디에서 콘서트가 가장 많이 열렸는지 순위표
# 최고가와 최저가 그래프
# 시기별 콘서트 출력 슬라이드

# 통계
select = st.selectbox(
    label = "통계",
    options = ("---SELECT---", "월별 콘서트 횟수", "콘서트 장소", "각 콘서트 최고가 및 최저가", "시기별 콘서트 데이터"),
    index = 0
)

if select == "월별 콘서트 횟수":
    # 연도-월별 콘서트 횟수 집계
    monthly_counts = df['year_month'].value_counts().sort_index()

    # 가능한 연월 범위 생성
    full_range = pd.period_range(
        start=df['year_month'].min(),
        end=df['year_month'].max(),
        freq='M'
    )

    # 데이터프레임 변환 및 누락 값 0 처리
    full_range_df = pd.DataFrame({'Year-Month': full_range})
    monthly_counts_df = monthly_counts.reset_index()
    monthly_counts_df.columns = ['year_month', 'Concert_Counts']
    monthly_counts_df = full_range_df.merge(
        monthly_counts_df,
        left_on='Year-Month',
        right_on='year_month',
        how='left'
    ).fillna(0)

    # 최종 열 조정
    monthly_counts_df = monthly_counts_df[['Year-Month', 'Concert_Counts']]  # 필요한 열만 유지
    monthly_counts_df['Concert_Counts'] = monthly_counts_df['Concert_Counts'].astype(int)

    # 그래프 생성 및 출력
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.plot(monthly_counts_df['Year-Month'].astype(str),
            monthly_counts_df['Concert_Counts'],
            marker='o', label='Concert Counts')

    # 기본 폰트 설정, 그래프 제목과 축 레이블 설정
    plt.rcParams['font.family'] = 'NanumGothic'
    ax.set_title("월별 콘서트 횟수", fontproperties=font_prop, fontsize=16)
    ax.set_xlabel("연-월"[2:], fontproperties=font_prop, fontsize=12)
    ax.set_ylabel("콘서트 횟수", fontproperties=font_prop, fontsize=12)
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.2)
    ax.legend()

    # Streamlit에서 그래프 출력
    st.pyplot(fig)


elif select == "콘서트 장소":
    # 장소별 콘서트 횟수 세기
    place_counts = df['place'].value_counts()

    # 데이터프레임으로 변환
    place_counts_df = place_counts.reset_index()
    place_counts_df.columns = ['Place', 'Counts']

    # 횟수가 1인 장소 필터링
    one_places = place_counts_df[place_counts_df['Counts'] == 1]
    # 횟수가 2회 이상인 장소
    fplace_counts_df = place_counts_df[place_counts_df['Counts'] > 1]
    # fplace_counts_df['Place'] = fplace_counts_df['Place'].str[:7] + "..."

    st.write("콘서트가 다회 열린 장소")
    if not one_places.empty:
        st.table(fplace_counts_df)
    else:
        st.write("")

    st.write("콘서트가 1회만 열린 장소")
    if not one_places.empty:
        st.table(one_places[['Place']])  # Place 열만 출력
    else:
        st.write("")

elif select == "각 콘서트 최고가 및 최저가":
    
    price_data = df[['title', 'price']].copy()

    # 최고가와 최저가 열 생성
    price_data['Highest Price'] = price_data['price'].apply(lambda x: max(x) if x else None)
    price_data['Lowest Price'] = price_data['price'].apply(lambda x: min(x) if x else None)

    # 선그래프 생성
    fig, ax = plt.subplots(figsize=(15, 8))
    x = range(1,len(price_data)+1)
    highest = price_data['Highest Price']
    lowest = price_data['Lowest Price']

    ax.plot(x, highest, color='red', marker='o', label='최고가')
    ax.plot(x, lowest, color='blue', marker='o', label='최저가')

    # 그래프 설정
    ax.set_title("콘서트 최고가 및 최저가", fontproperties=font_prop, fontsize=16)
    # ax.set_xlabel("콘서트 제목", fontproperties=font_prop, fontsize=12)
    ax.set_ylabel("가격 (원)", fontproperties=font_prop, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.legend(prop=font_prop)

    st.pyplot(fig)


elif select == "시기별 콘서트 데이터":

    # Session State 초기화
    if 'slider_value' not in st.session_state:
        st.session_state.slider_value = (datetime(2024, 7, 1), datetime(2025, 1, 1))

    if 'filtered_data' not in st.session_state:
        st.session_state.filtered_data = pd.DataFrame([])

    # 슬라이더: 연도-월 범위 선택
    sl = st.slider(
        "연도-월 범위를 선택하세요",
        min_value=datetime(2024, 1, 1),
        max_value=datetime(2025, 5, 31),
        value=st.session_state.slider_value,
        format="YYYY-MM",
    )

    # 필터링된 데이터
    start_date, end_date = sl
    filtered_df = df[(df['start_date'] >= start_date) & (df['start_date'] <= end_date)]
    filtered_df = filtered_df.drop(columns=['start_date', 'year_month'], errors='ignore')

    # 버튼 클릭 시 데이터 필터링
    if st.button("선택한 범위 확인"):
        st.session_state.slider_value = sl
        st.session_state.filtered_data = filtered_df
    
    # 데이터 출력
    if st.session_state.filtered_data.empty:
        st.write("해당 기간에 진행된 콘서트가 없습니다.")
    else:
        st.write("시기별 콘서트 데이터")
        st.dataframe(st.session_state.filtered_data, use_container_width=True)
    
else:
    st.write("")