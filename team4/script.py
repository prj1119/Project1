code1 = '''
#교보 데이터 수집

options = Options()
# options.add_argument('--headless')
options.add_argument("--start-maximized")
options.add_experimental_option("detach", True)

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
for i in range(0,30):
#     title = li[i].find_element(By.CSS_SELECTOR, "a.font-weight-medium").text
    link_kb = li_kb[i].find_element(By.CSS_SELECTOR, "a.font-weight-medium").get_attribute("href")
    links_kb.append(link_kb)

for j in links_kb:
    driver.get(j)
    time.sleep(2)
    title_kb = driver.find_element(By.CSS_SELECTOR, "span.prod_title").text
    author_kb = driver.find_element(By.CSS_SELECTOR, ".author > a").text
    genre_kb = driver.find_elements(By.CSS_SELECTOR, '.btn_sub_depth')[1].text
    titles_kb.append(title_kb)
    authors_kb.append(author_kb)
    genres_kb.append(genre_kb)
driver.quit()

# print(titles_kb)
# print(authors_kb)
# print(genres_kb)

for i in range(len(genres_kb)):
    if genres_kb[i] == '소설':
        genres_kb[i] = '소설/시/희곡/에세이'
    elif genres_kb[i] == '시/에세이':
        genres_kb[i] = '소설/시/희곡/에세이'
print(genres_kb)

bookData_kb = []
for k in range(0,30):
    bookData_kb.append({
            "순위": k+1,
            "제목": titles_kb[k],
            "작가": authors_kb[k],
            "장르": genres_kb[k]
    })
print(bookData_kb)

books_kb_df = pd.DataFrame(bookData_kb)
books_kb_df
'''

code2 = '''
#yes24 데이터 수집

url = "https://www.yes24.com/Product/Category/MonthWeekBestSeller?categoryNumber=001&pageNumber=1&pageSize=40&type=month&saleYear=2024&saleMonth=11"
res = req.get(url)

bookData_yes24 = []

if res.status_code == 200:
    soup = bs(res.text, "html.parser")
    trs = soup.select("#yesBestList .itemUnit")
    
    rank = 1
    for item in trs:
        if rank > 30:
            break
        title_yes24 = item.select_one(".gd_name").get_text(strip=True)
        href = item.find("a")["href"]
        author_yes24 = item.select('span.authPub.info_auth > a')[0].text.strip()
        
        url2 = "https://www.yes24.com" + href
        res2 = req.get(url2)    
        if res2.status_code == 200:
            book_soup = bs(res2.text, "html.parser")
            links = book_soup.select(".infoSetCont_wrap > dl > dd > ul > li > a")
            if links:
                genre_yes24 = links[1].get_text(strip=True)
                genre_yes24 = genre_yes24.replace("에세이", "소설/시/희곡")
                genre_yes24 = genre_yes24.replace("소설/시/희곡", "소설/시/희곡/에세이")
                genre_yes24 = genre_yes24.replace("경제 경영", "경제/경영")
        

        bookData_yes24.append({
            "순위": rank,
            "제목": title_yes24,
            "작가": author_yes24,
            "장르": genre_yes24,
            "링크": "https://www.yes24.com" + href
        })
                   
        rank += 1

books_yes24_df = pd.DataFrame(bookData_yes24)
books_yes24_df
'''

code3 = '''
#교보 데이터 전처리 코드
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
                "장르": genres_kb[k],
                "링크": links_kb[k]
        })

    print("Step Stop >>> Data End!!")
    books_kb_df = pd.DataFrame(bookData_kb)

#yes24 데이터 전처리 코드
                if links:
                    genre_yes24 = links[1].get_text(strip=True)
                    genre_yes24 = genre_yes24.replace("에세이", "소설/시/희곡")
                    genre_yes24 = genre_yes24.replace("소설/시/희곡", "소설/시/희곡/에세이")
                    genre_yes24 = genre_yes24.replace("경제 경영", "경제/경영")
            

            bookData_yes24.append({
                "순위": rank,
                "제목": title_yes24,
                "작가": author_yes24,
                "장르": genre_yes24,
                "링크": "https://www.yes24.com" + href
            })
                    
            rank += 1

    books_yes24_df = pd.DataFrame(bookData_yes24)
    books_yes24_df.set_index("순위", inplace=True)
    return books_yes24_df
'''