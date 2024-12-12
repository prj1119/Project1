import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

#yes24 데이터 수집
def getYes24Data(size):
    url = "https://www.yes24.com/Product/Category/MonthWeekBestSeller?categoryNumber=001&pageNumber=1&pageSize=40&type=month&saleYear=2024&saleMonth=11"
    res = req.get(url)

    bookData_yes24 = []
    if res.status_code == 200:
        soup = bs(res.text, "html.parser")
        trs = soup.select("#yesBestList .itemUnit")
        rank = 1
        for item in trs:
            if rank > size:
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
    books_yes24_df.set_index("순위", inplace=True)
    return books_yes24_df

if __name__ == "__main__":
    print( getYes24Data(10) )