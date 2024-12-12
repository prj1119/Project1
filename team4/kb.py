from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

options = Options()
if __name__ == "__main__":
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
else:    
    options.add_argument('--headless')
    
#교보 데이터 수집
def getKbData(size):
    driver = webdriver.Chrome(options=options)
    driver.get("https://store.kyobobook.co.kr/bestseller/total/monthly?page=1&per=50")
    time.sleep(3)

    ol = driver.find_element(By.CSS_SELECTOR, "ol.grid.border-t.border-gray-400.grid-cols-1.pt-9")
    li10_kb = ol.find_elements(By.XPATH, '/html/body/div[1]/main/section/div/div/section/ol[1]/li')
    li40_kb = ol.find_elements(By.XPATH, '/html/body/div[1]/main/section/div/div/section/ol[2]/li')
    li_kb = li10_kb + li40_kb

    links_kb = []
    titles_kb = []
    authors_kb = []
    genres_kb = []
    print("Step1 Start!!")
    for i in range(0,size):
    #     title = li[i].find_element(By.CSS_SELECTOR, "a.font-weight-medium").text
        link_kb = li_kb[i].find_element(By.CSS_SELECTOR, "a.font-weight-medium").get_attribute("href")
        links_kb.append(link_kb)

    print("Step2 Start!!")
    for j in links_kb:
        driver.get(j)
        print("Step2 Go >>", j)
        time.sleep(2)
        title_kb = driver.find_element(By.CSS_SELECTOR, "span.prod_title").text
        author_kb = driver.find_element(By.CSS_SELECTOR, ".author > a").text
        genre_kb = driver.find_elements(By.CSS_SELECTOR, '.btn_sub_depth')[1].text
        titles_kb.append(title_kb)
        authors_kb.append(author_kb)
        genres_kb.append(genre_kb)

    print("Step3 Start!!")
    for i in range(len(genres_kb)):
        if genres_kb[i] == '소설':
            genres_kb[i] = '소설/시/희곡/에세이'
        elif genres_kb[i] == '시/에세이':
            genres_kb[i] = '소설/시/희곡/에세이'

    print("Step4 Start!!")
    bookData_kb = []
    for k in range(0,size):
        bookData_kb.append({
                "순위": k+1,
                "제목": titles_kb[k],
                "작가": authors_kb[k],
                "장르": genres_kb[k]
        })

    print("Step Stop >>> Data End!!")
    books_kb_df = pd.DataFrame(bookData_kb)
    return books_kb_df

if __name__ == "__main__":
    print( getKbData(10) )