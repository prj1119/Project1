import streamlit as st
import numpy as np
import pandas as pd
import requests as req
import json
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

st.set_page_config(
    page_title="2. 뮤지컬 실시간 통계",
    page_icon="💗",
    # layout="wide",
    # initial_sidebar_state="collapsed"
)

st.title("뮤지컬 실시간 통계")

# 1. 수집 코드
st.header("수집 코드")
code1 = '''
import requests as req
import json
from bs4 import BeautifulSoup

#인터파크 url로 자바스크립트 받아와서 json 형식으로 만드는게 반복 되어서 함수로 만들어서 호출 해서 사용함
def fetch_ranking_data(url):
   
  
        # 웹페이지 요청
        response = req.get(url, verify=True)

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # __NEXT_DATA__ script 태그에서 JSON 데이터 추출
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
        
        # JSON 데이터 파싱
        json_data = json.loads(script_tag.string)
        # 랭킹 데이터 반환
        return json_data.get('props', {}).get('pageProps', {}).get('fallback', {})
   
   
#인터파크 스크립트에서 가져온 json 형식 파일로 장르별 정보를 리스트로 변환 하는 함수
def extract_ranking_info(ranking_data, ranking_type):
  
    # ranking_type에 따라 동적으로 랭킹 키를 생성
    # 뮤지컬 키
    if ranking_type == "MUSICAL":
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=MUSICAL",'
    # 콘서트 키
    if ranking_type == "CONCERT":
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=CONCERT",'
    # 클래식 키
    if ranking_type == "CLASSIC":
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=CLASSIC",'
    if ranking_type == "KIDS":
    # 아동 키
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=KIDS",'
    if ranking_type == "DRAMA":
    # 연극 키
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=DRAMA",'
    # 전시 키
    if ranking_type == "EXHIBIT":
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=EXHIBIT",'
    
    
    # 해당 key에 해당하는 데이터가 없을 경우 빈 리스트 반환
    ranking_info = ranking_data.get(ranking_key, [])
    
     # 데이터를 리스트로 변환
    ranking_list = []
    for item in ranking_info:
        ranking_list.append([
            item.get('rank', 'N/A'), 
            item.get('goodsName', 'N/A'), 
            item.get('placeName', 'N/A'), 
            item.get('playStartDate', 'N/A'), 
            item.get('playEndDate', 'N/A'), 
            item.get('bookingPercent', 'N/A')
        ])
    
    return ranking_list

# 티켓링크에서 주는 API를 JSON 형태로 바꾸는 함수

def get_ranking_data_from_url(url):
   
   
        # 웹페이지 요청
        response = req.get(url, verify=True)
        
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # JSON 데이터 추출
        json_data = json.loads(soup.string)
        return json_data
  
# 티켓링크의 랭킹 JSON 데이터에서 필요한 정보를 추출하고, 정렬된 리스트 반환.
  
def parse_ranking_info(ranking_json):
    
    ranking_data = ranking_json.get('data', {}).get('rankingList', [])
    
    ranking_list = []
    for item in ranking_data:
        reserve_rate_int = int(item['reserveRate'])
        
        # previousRanking이 None일 경우, '무한대'로 처리하여 마지막에 배치
        previous_ranking = item['previousRanking'] if item['previousRanking'] is not None else float('inf')
        
        # 필요한 정보 리스트에 추가
        ranking_list.append([
            previous_ranking, 
            item['productName'], 
            item['hallName'], 
            item['startDate'], 
            item['endDate'], 
            reserve_rate_int
        ])
    
    # 데이터가 정렬된 상태로 저장 된게 아니라서 랭킹을 기준으로 정렬
    ranking_list_sorted = sorted(ranking_list, key=lambda x: x[0])
    
    return ranking_list_sorted

# 티켓링크에서 주어진 URL에서 장르별 랭킹 데이터를 가져와 처리하는 함수.
def get_genre_ranking(url):
   
    ranking_json = get_ranking_data_from_url(url)

    sorted_ranking_list = parse_ranking_info(ranking_json)
    return sorted_ranking_list





# 인터파크 에서 주어진 URL에서 데이터 가져오기
# 티켓링크 뮤지컬 url
musical_url = "https://tickets.interpark.com/contents/ranking?genre=MUSICAL"
# 티켓링크 콘서트 url
concert_url = "https://tickets.interpark.com/contents/ranking?genre=CONCERT"
# 티켓링크 클래식 url
classic_url = "https://tickets.interpark.com/contents/ranking?genre=CLASSIC"
# 티켓링크 아동 url
kids_url = "https://tickets.interpark.com/contents/ranking?genre=KIDS"
# 티켓링크 연극 url
drama_url = "https://tickets.interpark.com/contents/ranking?genre=DRAMA"
# 티켓링크 전시 url
exhibit_url = "https://tickets.interpark.com/contents/ranking?genre=EXHIBIT"

# 인터파크 랭킹 데이터 가져오기
# 인터파크 뮤지컬 JSON 데이터
musical_ranking_data = fetch_ranking_data(musical_url)
# 인터파크 콘서트 JSON 데이터
concert_ranking_data = fetch_ranking_data(concert_url)
# 인터파크 클래식 JSON 데이터
classic_ranking_data = fetch_ranking_data(classic_url)
# 인터파크 아동 JSON 데이터
kids_ranking_data = fetch_ranking_data(kids_url)
# 인터파크 연극 JSON 데이터
drama_ranking_data = fetch_ranking_data(drama_url)
# 인터파크전시 JSON 데이터
exhibit_ranking_data = fetch_ranking_data(exhibit_url)


# 티켓링크 URL 설정
# 티켓링크 뮤지컬 URL
musical_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=16&categoryId3=0&menu=RANKING"
# 티켓링크 콘서트 URL
concert_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=14&categoryId3=0&menu=RANKING"
# 티켓링크 클래식 URL
classic_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=18&categoryId3=0&menu=RANKING"
# 티켓링크 아동 URL
kids_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=85&categoryId3=0&menu=RANKING"
# 티켓링크 연극 URL
drama_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=15&categoryId3=0&menu=RANKING"
# 티켓링크 전시 URL
exhibit_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=11&categoryId2=24&categoryId3=0&menu=RANKING"

# 티켓링크 랭킹 데이터 가져오기
# 티켓링크 뮤지컬 데이터
musical_ranking = get_genre_ranking(musical_url)
# 티켓링크 콘서트 데이터
concert_ranking = get_genre_ranking(concert_url)
# 티켓링크 클래식 데이터
classic_ranking = get_genre_ranking(classic_url)
# 티켓링크 아동 데이터
kids_ranking = get_genre_ranking(kids_url)
# 티켓링크 연극 데이터
drama_ranking = get_genre_ranking(drama_url)
# 티켓링크 전시 데이터
exhibit_ranking = get_genre_ranking(exhibit_url)
# 인터파크 랭킹 데이터 가져오기
# 인터파크 뮤지컬 데이터
musical_list = extract_ranking_info(musical_ranking_data, ranking_type="MUSICAL")


# 인터파크 콘서트 데이터
concert_list = extract_ranking_info(concert_ranking_data, ranking_type="CONCERT")

# 인터파크 클래식 데이터
classic_list = extract_ranking_info(classic_ranking_data, ranking_type="CLASSIC")

# 인터파크 아동 데이터
kids_list = extract_ranking_info(kids_ranking_data, ranking_type="KIDS")

# 인터파크 연극 데이터
drama_list = extract_ranking_info(drama_ranking_data, ranking_type="DRAMA")

# 인터파크 전시 데이터
exhibit_list = extract_ranking_info(exhibit_ranking_data, ranking_type="EXHIBIT")




'''
st.code(code1, language="python")


import requests as req
import json
from bs4 import BeautifulSoup

#인터파크 url로 자바스크립트 받아와서 json 형식으로 만드는게 반복 되어서 함수로 만들어서 호출 해서 사용함
def fetch_ranking_data(url):
   
  
        # 웹페이지 요청
        response = req.get(url, verify=True)

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # __NEXT_DATA__ script 태그에서 JSON 데이터 추출
        script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
        
        # JSON 데이터 파싱
        json_data = json.loads(script_tag.string)
        # 랭킹 데이터 반환
        return json_data.get('props', {}).get('pageProps', {}).get('fallback', {})
   
   
#인터파크 스크립트에서 가져온 json 형식 파일로 장르별 정보를 리스트로 변환 하는 함수
def extract_ranking_info(ranking_data, ranking_type):
  
    # ranking_type에 따라 동적으로 랭킹 키를 생성
    # 뮤지컬 키
    if ranking_type == "MUSICAL":
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=MUSICAL",'
    # 콘서트 키
    if ranking_type == "CONCERT":
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=CONCERT",'
    # 클래식 키
    if ranking_type == "CLASSIC":
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=CLASSIC",'
    if ranking_type == "KIDS":
    # 아동 키
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=KIDS",'
    if ranking_type == "DRAMA":
    # 연극 키
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=DRAMA",'
    # 전시 키
    if ranking_type == "EXHIBIT":
        ranking_key = '@"/ranking","?period=D&page=1&pageSize=50&rankingTypes=EXHIBIT",'
    
    
    # 해당 key에 해당하는 데이터가 없을 경우 빈 리스트 반환
    ranking_info = ranking_data.get(ranking_key, [])
    
     # 데이터를 리스트로 변환
    ranking_list = []
    for item in ranking_info:
        ranking_list.append([
            item.get('rank', 'N/A'), 
            item.get('goodsName', 'N/A'), 
            item.get('placeName', 'N/A'), 
            item.get('playStartDate', 'N/A'), 
            item.get('playEndDate', 'N/A'), 
            item.get('bookingPercent', 'N/A')
        ])
    
    return ranking_list

# 티켓링크에서 주는 API를 JSON 형태로 바꾸는 함수

def get_ranking_data_from_url(url):
   
   
        # 웹페이지 요청
        response = req.get(url, verify=True)
        
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # JSON 데이터 추출
        json_data = json.loads(soup.string)
        return json_data
  
# 티켓링크의 랭킹 JSON 데이터에서 필요한 정보를 추출하고, 정렬된 리스트 반환.
  
def parse_ranking_info(ranking_json):
    
    ranking_data = ranking_json.get('data', {}).get('rankingList', [])
    
    ranking_list = []
    for item in ranking_data:
        reserve_rate_int = int(item['reserveRate'])
        
        # previousRanking이 None일 경우, '무한대'로 처리하여 마지막에 배치
        previous_ranking = item['previousRanking'] if item['previousRanking'] is not None else float('inf')
        
        # 필요한 정보 리스트에 추가
        ranking_list.append([
            previous_ranking, 
            item['productName'], 
            item['hallName'], 
            item['startDate'], 
            item['endDate'], 
            reserve_rate_int
        ])
    
    # 데이터가 정렬된 상태로 저장 된게 아니라서 랭킹을 기준으로 정렬
    ranking_list_sorted = sorted(ranking_list, key=lambda x: x[0])
    
    return ranking_list_sorted

# 티켓링크에서 주어진 URL에서 장르별 랭킹 데이터를 가져와 처리하는 함수.
def get_genre_ranking(url):
   
    ranking_json = get_ranking_data_from_url(url)

    sorted_ranking_list = parse_ranking_info(ranking_json)
    return sorted_ranking_list





# 인터파크 에서 주어진 URL에서 데이터 가져오기
# 티켓링크 뮤지컬 url
musical_url = "https://tickets.interpark.com/contents/ranking?genre=MUSICAL"
# 티켓링크 콘서트 url
concert_url = "https://tickets.interpark.com/contents/ranking?genre=CONCERT"
# 티켓링크 클래식 url
classic_url = "https://tickets.interpark.com/contents/ranking?genre=CLASSIC"
# 티켓링크 아동 url
kids_url = "https://tickets.interpark.com/contents/ranking?genre=KIDS"
# 티켓링크 연극 url
drama_url = "https://tickets.interpark.com/contents/ranking?genre=DRAMA"
# 티켓링크 전시 url
exhibit_url = "https://tickets.interpark.com/contents/ranking?genre=EXHIBIT"

# 인터파크 랭킹 데이터 가져오기
# 인터파크 뮤지컬 JSON 데이터
musical_ranking_data = fetch_ranking_data(musical_url)
# 인터파크 콘서트 JSON 데이터
concert_ranking_data = fetch_ranking_data(concert_url)
# 인터파크 클래식 JSON 데이터
classic_ranking_data = fetch_ranking_data(classic_url)
# 인터파크 아동 JSON 데이터
kids_ranking_data = fetch_ranking_data(kids_url)
# 인터파크 연극 JSON 데이터
drama_ranking_data = fetch_ranking_data(drama_url)
# 인터파크전시 JSON 데이터
exhibit_ranking_data = fetch_ranking_data(exhibit_url)


# 티켓링크 URL 설정
# 티켓링크 뮤지컬 URL
musical_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=16&categoryId3=0&menu=RANKING"
# 티켓링크 콘서트 URL
concert_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=14&categoryId3=0&menu=RANKING"
# 티켓링크 클래식 URL
classic_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=18&categoryId3=0&menu=RANKING"
# 티켓링크 아동 URL
kids_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=85&categoryId3=0&menu=RANKING"
# 티켓링크 연극 URL
drama_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=10&categoryId2=15&categoryId3=0&menu=RANKING"
# 티켓링크 전시 URL
exhibit_url = "https://mapi.ticketlink.co.kr/mapi/ranking/genre/daily?categoryId=11&categoryId2=24&categoryId3=0&menu=RANKING"

# 티켓링크 랭킹 데이터 가져오기
# 티켓링크 뮤지컬 데이터
musical_ranking = get_genre_ranking(musical_url)
# 티켓링크 콘서트 데이터
concert_ranking = get_genre_ranking(concert_url)
# 티켓링크 클래식 데이터
classic_ranking = get_genre_ranking(classic_url)
# 티켓링크 아동 데이터
kids_ranking = get_genre_ranking(kids_url)
# 티켓링크 연극 데이터
drama_ranking = get_genre_ranking(drama_url)
# 티켓링크 전시 데이터
exhibit_ranking = get_genre_ranking(exhibit_url)
# 인터파크 랭킹 데이터 가져오기
# 인터파크 뮤지컬 데이터
musical_list = extract_ranking_info(musical_ranking_data, ranking_type="MUSICAL")


# 인터파크 콘서트 데이터
concert_list = extract_ranking_info(concert_ranking_data, ranking_type="CONCERT")

# 인터파크 클래식 데이터
classic_list = extract_ranking_info(classic_ranking_data, ranking_type="CLASSIC")

# 인터파크 아동 데이터
kids_list = extract_ranking_info(kids_ranking_data, ranking_type="KIDS")

# 인터파크 연극 데이터
drama_list = extract_ranking_info(drama_ranking_data, ranking_type="DRAMA")

# 인터파크 전시 데이터
exhibit_list = extract_ranking_info(exhibit_ranking_data, ranking_type="EXHIBIT")



# # 인터파크 데이터 출력
# print("인터파크 뮤지컬 랭킹 데이터:", musical_list)
# # 티켓링크 데이터 출력
# print("티켓링크 뮤지컬 랭킹 데이터:", musical_ranking)

# # 인터파크 데이터 출력
# print("인터파크 콘서트 랭킹 데이터:", concert_list)
# # 티켓링크 데이터 출력
# print("티켓링크 콘서트 랭킹 데이터:", concert_ranking)

# # 인터파크 데이터 출력
# print("인터파크 클래식 랭킹 데이터:", classic_list)
# # 티켓링크 데이터 출력
# print("티켓링크 클래식 랭킹 데이터:", classic_ranking)

# # 인터파크 데이터 출력
# print("인터파크 아동 랭킹 데이터:", kids_list)
# # 티켓링크 데이터 출력
# print("티켓링크 아동 랭킹 데이터:", kids_ranking)

# # 인터파크 데이터 출력
# print("인터파크 연극 랭킹 데이터:", drama_list)
# # 티켓링크 데이터 출력
# print("티켓링크 연극 랭킹 데이터:", drama_ranking)

# # 인터파크 데이터 출력
# print("인터파크 전시 랭킹 데이터:", exhibit_list)
# # 티켓링크 데이터 출력
# print("티켓링크 전시 랭킹 데이터:", exhibit_ranking)

# 2. 데이터 전처리 과정
st.header("데이터 전처리 과정")
code2 = '''
# 한글 깨짐 처리 설정
font_path = "C:\\Windows\\Fonts\\malgun.ttf"  # Linux 시스템의 경우 예시
# Windows에서는 "C:\\Windows\\Fonts\\malgun.ttf"로 수정
font_prop = font_manager.FontProperties(fname=font_path)
rc('font', family=font_prop.get_name())
similarity_threshold = 80

# 결과를 담을 리스트
result = []

# musical_list와 musical_ranking 비교
for m_list_item in musical_list:
    for m_ranking_item in musical_ranking:
        # fuzzywuzzy를 사용하여 제목 유사도 계산
        similarity_score = fuzz.ratio(m_list_item[1], m_ranking_item[1])

        # 유사도가 threshold 이상이면 결과 리스트에 추가
        if similarity_score >= similarity_threshold:
            result.append([
                m_list_item[1],  # 뮤지컬 제목
                m_list_item[5],  # musical_list의 인기 지표
                m_ranking_item[5]  # musical_ranking의 순위 지표
            ])

# 결과 리스트에서 제목, 인터파크 예매율, 티켓링크 예매율 추출
titles = [item[0] for item in result]  # 뮤지컬 제목
interpark_sales = [float(item[1]) for item in result]  # 인터파크 예매율 (float형으로 변환)
ticketlink_sales = [float(item[2]) for item in result]  # 티켓링크 예매율 (float형으로 변환)

# X축 위치 설정 (뮤지컬 제목 수만큼 x 위치 생성)
x = np.arange(len(titles))

# 차트 크기 설정
fig, ax = plt.subplots(figsize=(10, 6))  # Streamlit에 맞는 크기 설정

# 바 차트 그리기
bar_width = 0.35  # 바 너비 설정
ax.bar(x - bar_width / 2, interpark_sales, bar_width, label='인터파크 예매율', color='blue')  # 인터파크 예매율
ax.bar(x + bar_width / 2, ticketlink_sales, bar_width, label='티켓링크 예매율', color='green')  # 티켓링크 예매율

# 제목, 축 라벨 설정
ax.set_xlabel('뮤지컬 제목')  # x축 레이블
ax.set_ylabel('예매율 (%)')  # y축 레이블
ax.set_title('인터파크 예매율 vs 티켓링크 예매율 비교')  # 차트 제목
ax.set_xticks(x)  # x축 위치 설정
ax.set_xticklabels(titles, rotation=90)  # x축 레이블(제목)을 90도 회전하여 표시
ax.legend()  # 범례 추가

# 레이아웃을 최적화하여 레이블이 잘리지 않게 설정
plt.tight_layout()

# Streamlit에서 차트 출력
st.pyplot(fig)
'''


st.code(code2, language="python")

# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")
# 라인 차트를 생성하는 함수
def create_line_chart(musical_list, musical_ranking, similarity_threshold=80, chart_title='예매율 비교', x_label='뮤지컬 제목', y_label='예매율 (%)'):
      # 한글 폰트 설정

    # 결과를 담을 리스트
    result = []

    # inter_list와 ticket_ranking 비교
    for m_list_item in musical_list:
        for m_ranking_item in musical_ranking:
            # fuzzywuzzy를 사용하여 제목 유사도 계산
            similarity_score = fuzz.ratio(m_list_item[1], m_ranking_item[1])

            # 유사도가 threshold 이상이면 결과 리스트에 추가
            if similarity_score >= similarity_threshold:
                result.append([ 
                    m_list_item[1],  # 뮤지컬 제목
                    m_list_item[5],  # inter_list의 인기 지표
                    m_ranking_item[5]  # ticket_ranking의 순위 지표
                ])

    # 결과 리스트에서 제목, 인터파크 예매율, 티켓링크 예매율 추출
    titles = [item[0] for item in result]  # 뮤지컬 제목
    interpark_sales = [float(item[1]) for item in result]  # 인터파크 예매율 (float형으로 변환)
    ticketlink_sales = [float(item[2]) for item in result]  # 티켓링크 예매율 (float형으로 변환)

    # 제목 길이 제한 (15자 이하로 자르기)
    titles = [title if len(title) <= 15 else title[:8] + '...' for title in titles]

    # 라인 차트 그리기
    fig, ax = plt.subplots(figsize=(12, 6))  # 동일한 크기로 설정 (12x6 인치)
    ax.plot(titles, interpark_sales, label='인터파크 예매율', color='blue', marker='o')  # 인터파크 예매율
    ax.plot(titles, ticketlink_sales, label='티켓링크 예매율', color='green', marker='s')  # 티켓링크 예매율

    # 제목, 축 라벨 설정
    ax.set_xlabel(x_label)  # x축 레이블 (변경 가능)
    ax.set_ylabel(y_label)  # y축 레이블 (변경 가능)

    # 제목을 보기 좋게 수정: 카테고리명 + " 예매율 비교"
    chart_title = f"{chart_title} 예매율 비교 (인터파크 vs 티켓링크)"
    ax.set_title(chart_title)  # 차트 제목 (변경 가능)
    ax.legend()  # 범례 추가

    # x축 레이블 회전 및 간격 조정
    plt.xticks(rotation=45, ha='right', fontsize=10)  # 제목이 겹치지 않도록 회전 및 정렬

    # 레이아웃을 최적화하여 레이블이 잘리지 않게 설정
    plt.tight_layout()

    # Streamlit에서 차트 출력
    st.pyplot(fig)

# 사용 예시
create_line_chart(musical_list, musical_ranking, similarity_threshold=80, chart_title='뮤지컬', x_label='뮤지컬 제목', y_label='예매율 (%)')
create_line_chart(concert_list, concert_ranking, similarity_threshold=80, chart_title='콘서트', x_label='콘서트 제목', y_label='예매율 (%)')
create_line_chart(classic_list, classic_ranking, similarity_threshold=80, chart_title='클래식', x_label='클래식 제목', y_label='예매율 (%)')
create_line_chart(kids_list, kids_ranking, similarity_threshold=80, chart_title='아동/가족', x_label='아동/가족 제목', y_label='예매율 (%)')
create_line_chart(drama_list, drama_ranking, similarity_threshold=80, chart_title='연극', x_label='연극 제목', y_label='예매율 (%)')
create_line_chart(exhibit_list, exhibit_ranking, similarity_threshold=80, chart_title='전시', x_label='전시 제목', y_label='예매율 (%)')