import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from bs4 import BeautifulSoup as bs
from requests import get
import json
import pandas as pd

def 좋아(url2, head):
    arr = []
    data = json.loads(get(url2, headers=head).text)
    for row in data["contsLike"]:
        arr.append({"SUMMCNT": row["SUMMCNT"], "CONTSID": row["CONTSID"]})
    return arr

def 특수문자삭제(txt):
    return txt.replace("\n", "").strip()

def 멜론_크롤링(url1, url2, head=None):
    if head is None:
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    
    res = get(url1, headers=head)

    if res.status_code == 200:
        likes = 좋아(url2, head)  # 좋아요 수 가져오기
        data = bs(res.text, "html.parser")
        trs = data.select("#frm tbody > tr")  # 곡 리스트

        arr = []

        for i in range(len(trs)):
            song = []
            
            제목 = 특수문자삭제(trs[i].select("td")[4].select_one("div[class='ellipsis rank01']").text)
            song.append(제목)
            
            가수 = 특수문자삭제(trs[i].select("td")[4].select_one("div[class='ellipsis rank02'] a").text)
            song.append(가수)
        
            앨범 = 특수문자삭제(trs[i].select("td")[5].select_one("div[class='ellipsis rank03']").text)
            song.append(앨범)
            
            id = int(trs[i].select("td")[0].select_one("input[type='checkbox']").get("value"))
            
            좋아요 = 0
            for like in likes:
                if like["CONTSID"] == id:
                    좋아요 = like["SUMMCNT"]
                    break
            song.append(좋아요)
            
            arr.append(song)

        return arr  # 결과값 반환
    else:
        return None  # 실패한 경우 None 반환

url1_1 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0100&orderBy=POP"
url2_1 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=38123338%2C4352438%2C38104031%2C37390939%2C32061975%2C37228861%2C37069064%2C37145732%2C38244575%2C4446485%2C36699489%2C37023625%2C34061322%2C36382580%2C37344905%2C34360855%2C34451383%2C30962526%2C33496587%2C37375706%2C34657844%2C34431086%2C36616378%2C34908740%2C3973781%2C37248285%2C37491072%2C36502910%2C35008524%2C37635628%2C33855085%2C37820769%2C35008534%2C38311902%2C38092594%2C30877002%2C30147446%2C30190630%2C30672529%2C418168%2C30985406%2C36595401%2C1085869%2C36334401%2C37064763%2C31726704%2C36404853%2C30781482%2C8203900%2C32156286"

url1_2 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0200&orderBy=POP"
url2_2 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=38120327%2C38123332%2C38077932%2C38087937%2C37524037%2C38195515%2C37884934%2C37563682%2C37138469%2C37140709%2C35945927%2C37347911%2C37737619%2C37524038%2C37693124%2C35454426%2C38161297%2C37098744%2C3053259%2C36356993%2C37463572%2C38048464%2C37464459%2C36617841%2C36956630%2C38123775%2C37640352%2C32872978%2C37491071%2C38095946%2C36635522%2C36855841%2C36110996%2C37900204%2C35454425%2C36717264%2C36599950%2C37667860%2C36416114%2C34847378%2C37497123%2C36430773%2C36910957%2C36713849%2C35985167%2C1698598%2C37943763%2C36930793%2C7979764%2C35931532"

url1_3 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0300&orderBy=POP"
url2_3 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=38242510%2C38164895%2C37657039%2C38068560%2C37460832%2C37248286%2C30244931%2C37248284%2C4232200%2C37973745%2C1913501%2C5719286%2C1698598%2C2511767%2C38229421%2C38289454%2C4226211%2C1765767%2C37937762%2C35299693%2C2314377%2C37225604%2C5719287%2C3853980%2C38247005%2C32698101%2C3906383%2C37222942%2C30613202%2C38223807%2C36695861%2C31295312%2C3726617%2C531840%2C30147445%2C3170749%2C34875621%2C2733249%2C34256568%2C32438894%2C32224272%2C34100776%2C5684826%2C35542908%2C33359725%2C37948123%2C5470838%2C2312253%2C1637914%2C34701816"

url1_4 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0500&orderBy=POP"
url2_4 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=37069064%2C31666417%2C34451383%2C35553933%2C31726704%2C35252996%2C36062335%2C32476250%2C30514366%2C3894276%2C32224166%2C34941788%2C33043504%2C34162394%2C37051616%2C31343875%2C31853557%2C35361345%2C33976677%2C37937762%2C30657311%2C33868791%2C30383949%2C3620493%2C31093710%2C33680289%2C31151836%2C5466962%2C8298724%2C32438894%2C30444778%2C32548758%2C33978183%2C8036156%2C4848555%2C9620469%2C31624517%2C34153819%2C31513458%2C34930368%2C4451155%2C8119658%2C5385974%2C31960759%2C33722789%2C35958308%2C32833766%2C36386455%2C420424%2C30163110"

url1_5 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0600&orderBy=POP"
url2_5 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=37323944%2C38022274%2C38300904%2C37323943%2C31927275%2C36397952%2C37373234%2C30232719%2C37946921%2C37053556%2C31666417%2C37907939%2C37248283%2C38071559%2C34819473%2C7844374%2C38222733%2C37248282%2C35008525%2C35834583%2C35834584%2C34845949%2C38300902%2C36180700%2C38300903%2C32476250%2C1177475%2C32586850%2C33043504%2C534252%2C34162394%2C37524049%2C38300909%2C33480898%2C5760116%2C30383949%2C36877939%2C32183386%2C837567%2C3620493%2C31093710%2C33680289%2C31532656%2C31481700%2C34270805%2C34754292%2C37668675%2C32003395%2C38145736%2C732519"

url1_6 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0700&orderBy=POP"
url2_6 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=32508053%2C35008530%2C38101583%2C32626922%2C38101586%2C38101582%2C38101588%2C38101585%2C1726823%2C32323333%2C32457751%2C33337651%2C38101593%2C38101591%2C38101584%2C31368699%2C38101587%2C38101589%2C38101592%2C38101590%2C37434928%2C37384556%2C32397381%2C2710613%2C32323330%2C37952587%2C36181007%2C38254976%2C30177124%2C844269%2C34388834%2C37434931%2C37434929%2C37434930%2C36754053%2C72689%2C32457750%2C36181011%2C34622658%2C31918235%2C31657932%2C35363881%2C32341095%2C30607447%2C36241810%2C32441451%2C38195942%2C36263286%2C4182990%2C36666511"

url1_7 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0900&orderBy=POP"
url2_7 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=5475060%2C30717645%2C35640751%2C4365842%2C4322520%2C31411041%2C32160237%2C32156032%2C5493429%2C33658563%2C32995675%2C8037843%2C36490426%2C31029291%2C37901626%2C33359309%2C32158103%2C30188113%2C7931286%2C36028588%2C3592400%2C33488229%2C35738070%2C32006701%2C32055419%2C33116142%2C37132313%2C4660794%2C34097020%2C33048662%2C31509376%2C30703067%2C34864406%2C30731442%2C5832034%2C31436696%2C33469725%2C31012145%2C31341518%2C38182712%2C7928705%2C37410631%2C34363553%2C34018465%2C4857981%2C30380953%2C36078596%2C37824232%2C31338899%2C32236965"

url1_8 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN1900&orderBy=POP"
url2_8 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=37659322%2C34165330%2C30952294%2C34256232%2C37639980%2C35535827%2C36297161%2C30633420%2C31802584%2C38256229%2C36355817%2C34431960%2C38256220%2C32632368%2C33020905%2C3557251%2C34501184%2C35708856%2C34243311%2C30024219%2C31236592%2C35806237%2C38195682%2C31724618%2C37704840%2C38256223%2C36872331%2C36591870%2C35457868%2C35603969%2C38256225%2C32602860%2C35825907%2C32039117%2C38256230%2C38256228%2C37824953%2C34436187%2C34884364%2C34501178%2C32226733%2C34755308%2C30024200%2C33455399%2C38256232%2C32889134%2C37093274%2C33172406%2C31932139%2C32039106"

result_1 = 멜론_크롤링(url1_1, url2_1)
result_2 = 멜론_크롤링(url1_2, url2_2)
result_3 = 멜론_크롤링(url1_3, url2_3)
result_4 = 멜론_크롤링(url1_4, url2_4)
result_5 = 멜론_크롤링(url1_5, url2_5)
result_6 = 멜론_크롤링(url1_6, url2_6)
result_7 = 멜론_크롤링(url1_7, url2_7)
result_8 = 멜론_크롤링(url1_8, url2_8)

def 크롤링결과_데이터프레임(result, genre_name):
    df = pd.DataFrame(result, columns=["곡 이름", "가수", "앨범", "좋아요 수"])
    df['순위'] = df.index + 1
    df['장르'] = genre_name
    df = df[["순위", "곡 이름", "가수", "좋아요 수", "장르"]]
    return df.reset_index(drop=True) 

df1 = 크롤링결과_데이터프레임(result_1, "발라드")
df2 = 크롤링결과_데이터프레임(result_2, "댄스")
df3 = 크롤링결과_데이터프레임(result_3, "랩/힙합")
df4 = 크롤링결과_데이터프레임(result_4, "인디음악")
df5 = 크롤링결과_데이터프레임(result_5, "록/메탈")
df6 = 크롤링결과_데이터프레임(result_6, "트로트")
df7 = 크롤링결과_데이터프레임(result_7, "팝송")
df8 = 크롤링결과_데이터프레임(result_8, "J-POP")

top_20_df1 = df1.head(20)
top_20_df2 = df2.head(20)
top_20_df3 = df3.head(20)
top_20_df4 = df4.head(20)
top_20_df5 = df5.head(20)
top_20_df6 = df6.head(20)
top_20_df7 = df7.head(20)
top_20_df8 = df8.head(20)

good1 = top_20_df1["좋아요 수"].sum()
good2 = top_20_df2["좋아요 수"].sum()
good3 = top_20_df3["좋아요 수"].sum()
good4 = top_20_df4["좋아요 수"].sum()
good5 = top_20_df5["좋아요 수"].sum()
good6 = top_20_df6["좋아요 수"].sum()
good7 = top_20_df7["좋아요 수"].sum()
good8 = top_20_df8["좋아요 수"].sum()
gd = [good1, good2, good3, good4, good5, good6, good7, good8]

idx = ("발라드", "댄스", "랩/힙합", "인디음악", "록/메탈", "트로트", "팝송", "J-POP")

dfgood = pd.DataFrame({"좋아요 총합" : gd},
    index=idx)

top_20_df1 = top_20_df1.style.hide(axis='index')
top_20_df2 = top_20_df2.style.hide(axis='index')
top_20_df3 = top_20_df3.style.hide(axis='index')
top_20_df4 = top_20_df4.style.hide(axis='index')
top_20_df5 = top_20_df5.style.hide(axis='index')
top_20_df6 = top_20_df6.style.hide(axis='index')
top_20_df7 = top_20_df7.style.hide(axis='index')
top_20_df8 = top_20_df8.style.hide(axis='index')

### 장르별 제목 가로로 출력 하기로 위한 작업

# DataFrame을 '장르'와 '좋아요 총합'으로 변환
dfgood.reset_index(inplace=True)
dfgood.columns = ['장르', '좋아요 총합']

# Altair로 바 차트를 만들고 x축 레이블을 가로로 표시
chart = alt.Chart(dfgood).mark_bar().encode(
    x=alt.X('장르:N', title='장르', sort=None),  # '장르'를 x축에 표시
    y='좋아요 총합:Q',  # '좋아요 총합'을 y축에 표시
).properties(
    width=600,  # 차트의 너비
    height=400   # 차트의 높이
).configure_axis(
    labelAngle=0  # x축 레이블을 수평으로 설정
)

### 장르별 제목 가로로 출력 하기로 위한 작업

st.set_page_config(
    page_title="음악사이트 장르별 인기 통계",
    page_icon="🎵",
    layout="wide",
    # initial_sidebar_state="collapsed"
)

st.title("6. 음악사이트 장르별 인기 통계")

# 1. 수집 코드
st.header("수집 코드")
code1 = '''
from bs4 import BeautifulSoup as bs
from requests import get
import json
import pandas as pd

def 좋아(url2, head):
    arr = []
    data = json.loads(get(url2, headers=head).text)
    for row in data["contsLike"]:
        arr.append({"SUMMCNT": row["SUMMCNT"], "CONTSID": row["CONTSID"]})
    return arr

def 특수문자삭제(txt):
    return txt.replace("\n", "").strip()

def 멜론_크롤링(url1, url2, head=None):
    if head is None:
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
    
    res = get(url1, headers=head)

    if res.status_code == 200:
        likes = 좋아(url2, head)  # 좋아요 수 가져오기
        data = bs(res.text, "html.parser")
        trs = data.select("#frm tbody > tr")  # 곡 리스트

        arr = []

        for i in range(len(trs)):
            song = []
            
            제목 = 특수문자삭제(trs[i].select("td")[4].select_one("div[class='ellipsis rank01']").text)
            song.append(제목)
            
            가수 = 특수문자삭제(trs[i].select("td")[4].select_one("div[class='ellipsis rank02'] a").text)
            song.append(가수)
        
            앨범 = 특수문자삭제(trs[i].select("td")[5].select_one("div[class='ellipsis rank03']").text)
            song.append(앨범)
            
            id = int(trs[i].select("td")[0].select_one("input[type='checkbox']").get("value"))
            
            좋아요 = 0
            for like in likes:
                if like["CONTSID"] == id:
                    좋아요 = like["SUMMCNT"]
                    break
            song.append(좋아요)
            
            arr.append(song)

        return arr  # 결과값 반환
    else:
        return None  # 실패한 경우 None 반환

url1_1 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0100&orderBy=POP"
url2_1 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=38123338%2C4352438%2C38104031%2C37390939%2C32061975%2C37228861%2C37069064%2C37145732%2C38244575%2C4446485%2C36699489%2C37023625%2C34061322%2C36382580%2C37344905%2C34360855%2C34451383%2C30962526%2C33496587%2C37375706%2C34657844%2C34431086%2C36616378%2C34908740%2C3973781%2C37248285%2C37491072%2C36502910%2C35008524%2C37635628%2C33855085%2C37820769%2C35008534%2C38311902%2C38092594%2C30877002%2C30147446%2C30190630%2C30672529%2C418168%2C30985406%2C36595401%2C1085869%2C36334401%2C37064763%2C31726704%2C36404853%2C30781482%2C8203900%2C32156286"

url1_2 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0200&orderBy=POP"
url2_2 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=38120327%2C38123332%2C38077932%2C38087937%2C37524037%2C38195515%2C37884934%2C37563682%2C37138469%2C37140709%2C35945927%2C37347911%2C37737619%2C37524038%2C37693124%2C35454426%2C38161297%2C37098744%2C3053259%2C36356993%2C37463572%2C38048464%2C37464459%2C36617841%2C36956630%2C38123775%2C37640352%2C32872978%2C37491071%2C38095946%2C36635522%2C36855841%2C36110996%2C37900204%2C35454425%2C36717264%2C36599950%2C37667860%2C36416114%2C34847378%2C37497123%2C36430773%2C36910957%2C36713849%2C35985167%2C1698598%2C37943763%2C36930793%2C7979764%2C35931532"

url1_3 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0300&orderBy=POP"
url2_3 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=38242510%2C38164895%2C37657039%2C38068560%2C37460832%2C37248286%2C30244931%2C37248284%2C4232200%2C37973745%2C1913501%2C5719286%2C1698598%2C2511767%2C38229421%2C38289454%2C4226211%2C1765767%2C37937762%2C35299693%2C2314377%2C37225604%2C5719287%2C3853980%2C38247005%2C32698101%2C3906383%2C37222942%2C30613202%2C38223807%2C36695861%2C31295312%2C3726617%2C531840%2C30147445%2C3170749%2C34875621%2C2733249%2C34256568%2C32438894%2C32224272%2C34100776%2C5684826%2C35542908%2C33359725%2C37948123%2C5470838%2C2312253%2C1637914%2C34701816"

url1_4 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0500&orderBy=POP"
url2_4 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=37069064%2C31666417%2C34451383%2C35553933%2C31726704%2C35252996%2C36062335%2C32476250%2C30514366%2C3894276%2C32224166%2C34941788%2C33043504%2C34162394%2C37051616%2C31343875%2C31853557%2C35361345%2C33976677%2C37937762%2C30657311%2C33868791%2C30383949%2C3620493%2C31093710%2C33680289%2C31151836%2C5466962%2C8298724%2C32438894%2C30444778%2C32548758%2C33978183%2C8036156%2C4848555%2C9620469%2C31624517%2C34153819%2C31513458%2C34930368%2C4451155%2C8119658%2C5385974%2C31960759%2C33722789%2C35958308%2C32833766%2C36386455%2C420424%2C30163110"

url1_5 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0600&orderBy=POP"
url2_5 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=37323944%2C38022274%2C38300904%2C37323943%2C31927275%2C36397952%2C37373234%2C30232719%2C37946921%2C37053556%2C31666417%2C37907939%2C37248283%2C38071559%2C34819473%2C7844374%2C38222733%2C37248282%2C35008525%2C35834583%2C35834584%2C34845949%2C38300902%2C36180700%2C38300903%2C32476250%2C1177475%2C32586850%2C33043504%2C534252%2C34162394%2C37524049%2C38300909%2C33480898%2C5760116%2C30383949%2C36877939%2C32183386%2C837567%2C3620493%2C31093710%2C33680289%2C31532656%2C31481700%2C34270805%2C34754292%2C37668675%2C32003395%2C38145736%2C732519"

url1_6 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0700&orderBy=POP"
url2_6 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=32508053%2C35008530%2C38101583%2C32626922%2C38101586%2C38101582%2C38101588%2C38101585%2C1726823%2C32323333%2C32457751%2C33337651%2C38101593%2C38101591%2C38101584%2C31368699%2C38101587%2C38101589%2C38101592%2C38101590%2C37434928%2C37384556%2C32397381%2C2710613%2C32323330%2C37952587%2C36181007%2C38254976%2C30177124%2C844269%2C34388834%2C37434931%2C37434929%2C37434930%2C36754053%2C72689%2C32457750%2C36181011%2C34622658%2C31918235%2C31657932%2C35363881%2C32341095%2C30607447%2C36241810%2C32441451%2C38195942%2C36263286%2C4182990%2C36666511"

url1_7 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN0900&orderBy=POP"
url2_7 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=5475060%2C30717645%2C35640751%2C4365842%2C4322520%2C31411041%2C32160237%2C32156032%2C5493429%2C33658563%2C32995675%2C8037843%2C36490426%2C31029291%2C37901626%2C33359309%2C32158103%2C30188113%2C7931286%2C36028588%2C3592400%2C33488229%2C35738070%2C32006701%2C32055419%2C33116142%2C37132313%2C4660794%2C34097020%2C33048662%2C31509376%2C30703067%2C34864406%2C30731442%2C5832034%2C31436696%2C33469725%2C31012145%2C31341518%2C38182712%2C7928705%2C37410631%2C34363553%2C34018465%2C4857981%2C30380953%2C36078596%2C37824232%2C31338899%2C32236965"

url1_8 = "https://www.melon.com/genre/song_list.htm?gnrCode=GN1900&orderBy=POP"
url2_8 = "https://www.melon.com/commonlike/getSongLike.json?contsIds=37659322%2C34165330%2C30952294%2C34256232%2C37639980%2C35535827%2C36297161%2C30633420%2C31802584%2C38256229%2C36355817%2C34431960%2C38256220%2C32632368%2C33020905%2C3557251%2C34501184%2C35708856%2C34243311%2C30024219%2C31236592%2C35806237%2C38195682%2C31724618%2C37704840%2C38256223%2C36872331%2C36591870%2C35457868%2C35603969%2C38256225%2C32602860%2C35825907%2C32039117%2C38256230%2C38256228%2C37824953%2C34436187%2C34884364%2C34501178%2C32226733%2C34755308%2C30024200%2C33455399%2C38256232%2C32889134%2C37093274%2C33172406%2C31932139%2C32039106"


result_1 = 멜론_크롤링(url1_1, url2_1)
result_2 = 멜론_크롤링(url1_2, url2_2)
result_3 = 멜론_크롤링(url1_3, url2_3)
result_4 = 멜론_크롤링(url1_4, url2_4)
result_5 = 멜론_크롤링(url1_5, url2_5)
result_6 = 멜론_크롤링(url1_6, url2_6)
result_7 = 멜론_크롤링(url1_7, url2_7)
result_8 = 멜론_크롤링(url1_8, url2_8)

def 크롤링결과_데이터프레임(result, genre_name):
    df = pd.DataFrame(result, columns=["곡 이름", "가수", "앨범", "좋아요 수"])
    df['순위'] = df.index + 1
    df['장르'] = genre_name
    df = df[["순위", "곡 이름", "가수", "좋아요 수", "장르"]]
    return df.reset_index(drop=True) 

df1 = 크롤링결과_데이터프레임(result_1, "발라드")
df2 = 크롤링결과_데이터프레임(result_2, "댄스")
df3 = 크롤링결과_데이터프레임(result_3, "랩/힙합")
df4 = 크롤링결과_데이터프레임(result_4, "인디음악")
df5 = 크롤링결과_데이터프레임(result_5, "록/메탈")
df6 = 크롤링결과_데이터프레임(result_6, "트로트")
df7 = 크롤링결과_데이터프레임(result_7, "팝송")
df8 = 크롤링결과_데이터프레임(result_8, "J-POP")

top_20_df1 = df1.head(20)
top_20_df2 = df2.head(20)
top_20_df3 = df3.head(20)
top_20_df4 = df4.head(20)
top_20_df5 = df5.head(20)
top_20_df6 = df6.head(20)
top_20_df7 = df7.head(20)
top_20_df8 = df8.head(20)

good1 = top_20_df1["좋아요 수"].sum()
good2 = top_20_df2["좋아요 수"].sum()
good3 = top_20_df3["좋아요 수"].sum()
good4 = top_20_df4["좋아요 수"].sum()
good5 = top_20_df5["좋아요 수"].sum()
good6 = top_20_df6["좋아요 수"].sum()
good7 = top_20_df7["좋아요 수"].sum()
good8 = top_20_df8["좋아요 수"].sum()
gd = [good1, good2, good3, good4, good5, good6, good7, good8]

idx = ("발라드", "댄스", "랩/힙합", "인디음악", "록/메탈", "트로트", "팝송", "J-POP")

dfgood = pd.DataFrame({"좋아요 총합" : gd},
    index=idx)
'''
st.code(code1, language="python")

# 2. 데이터 전처리 과정
st.header("데이터 전처리 과정")
code2 = '''
import plotly.express as px

def 크롤링결과_데이터프레임(result, genre_name):
    df = pd.DataFrame(result, columns=["곡 이름", "가수", "앨범", "좋아요 수"])
    df['순위'] = df.index + 1
    df['장르'] = genre_name
    df = df[["순위", "곡 이름", "가수", "좋아요 수", "장르"]]
    return df.reset_index(drop=True) 

df1 = 크롤링결과_데이터프레임(result_1, "발라드")
df2 = 크롤링결과_데이터프레임(result_2, "댄스")
df3 = 크롤링결과_데이터프레임(result_3, "랩/힙합")
df4 = 크롤링결과_데이터프레임(result_4, "인디음악")
df5 = 크롤링결과_데이터프레임(result_5, "록/메탈")
df6 = 크롤링결과_데이터프레임(result_6, "트로트")
df7 = 크롤링결과_데이터프레임(result_7, "팝송")
df8 = 크롤링결과_데이터프레임(result_8, "J-POP")

top_20_df1 = df1.head(20)
top_20_df2 = df2.head(20)
top_20_df3 = df3.head(20)
top_20_df4 = df4.head(20)
top_20_df5 = df5.head(20)
top_20_df6 = df6.head(20)
top_20_df7 = df7.head(20)
top_20_df8 = df8.head(20)

good1 = top_20_df1["좋아요 수"].sum()
good2 = top_20_df2["좋아요 수"].sum()
good3 = top_20_df3["좋아요 수"].sum()
good4 = top_20_df4["좋아요 수"].sum()
good5 = top_20_df5["좋아요 수"].sum()
good6 = top_20_df6["좋아요 수"].sum()
good7 = top_20_df7["좋아요 수"].sum()
good8 = top_20_df8["좋아요 수"].sum()
gd = [good1, good2, good3, good4, good5, good6, good7, good8]

idx = ("발라드", "댄스", "랩/힙합", "인디음악", "록/메탈", "트로트", "팝송", "J-POP")

dfgood = pd.DataFrame({"좋아요 총합" : gd},
    index=idx)

'''
st.code(code2, language="python")

# 3. 수집 데이터를 이용한 시각화
st.header("수집 데이터를 이용한 시각화")

with st.expander("발라드"):
    st.table(top_20_df1)
    st.audio('audio/악동뮤지션(AKMU) - 어떻게 이별까지 사랑하겠어, 널 사랑하는 거지.mp3')

with st.expander("댄스"):
    st.table(top_20_df2)
    st.audio('audio/NewJeans - Hype Boy.mp3')

with st.expander("랩/힙합"):
    st.table(top_20_df3)
    st.audio('audio\BTS (방탄소년단) - Spring Day.mp3')

with st.expander("인디음악"):
    st.table(top_20_df4)
    st.audio('audio\잔나비 - 주저하는 연인들을 위해.mp3')

with st.expander("록/메탈"):
    st.table(top_20_df5)
    st.audio('audio\DAY6 (데이식스) - HAPPY.mp3')

with st.expander("트로트"):
    st.table(top_20_df6)
    st.audio('audio\임영웅 - 이제 나만 믿어요.mp3')

with st.expander("팝송"):
    st.table(top_20_df7)
    st.audio('audio\Ariana Grande - Santa Tell Me.mp3')

with st.expander("J-POP"):
    st.table(top_20_df8)
    st.audio('audio\유우리 - 베텔기우스(BETELGEUSE).mp3')
    


# Streamlit에서 차트 확장 표시
with st.expander("각 장르별 좋아요 총합"):
    st.altair_chart(chart, use_container_width=True)
    # Streamlit에서 차트 확장 표시