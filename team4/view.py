import streamlit as st

def show(df, target):
    # Streamlit 제목
    # st.title("책 정보 검색")
    st.dataframe(df, use_container_width=True)

    # 사용자 입력 선택
    option = st.selectbox(f"{target} 검색 옵션을 선택하세요:", ["순위로 검색(1 ~ 30)", "책 제목으로 검색", "작가로 검색"])

    if option == "순위로 검색(1 ~ 30)":
        rank = st.number_input(f"{target} 순위를 입력하세요:", min_value=1, max_value=len(df), step=1)
        
        if st.button(f"{target} 검색"):
            if rank in df.index:
                book = df.iloc[int(rank) -1]
                st.write(f"### {target} 순위 {rank} 정보")
                st.write(f"**제목:** {book['제목']}")
                st.write(f"**작가:** {book['작가']}")
                st.write(f"**장르:** {book['장르']}")
                st.write(f"[책 링크 보기]({book['링크']})")
            else:
                st.write(f"{target} 해당 순위의 책 정보를 찾을 수 없습니다.")

    elif option == "책 제목으로 검색":
        title = st.text_input(f"{target} 책 제목을 입력하세요:")
        
        if st.button(f"{target} 검색"):
            result = df[df['제목'].str.contains(title, case=False)]
            if not result.empty:
                st.write(f"### '{title}'에 대한 검색 결과")
                for idx, book in result.iterrows():
                    st.write(f"**순위:** {idx}")
                    st.write(f"**제목:** {book['제목']}")
                    st.write(f"**작가:** {book['작가']}")
                    st.write(f"**장르:** {book['장르']}")
                    st.write(f"[책 링크 보기]({book['링크']})")
            else:
                st.write(f"{target}에서 해당 제목의 책 정보를 찾을 수 없습니다.")

    elif option == "작가로 검색":
        author = st.text_input("작가 이름을 입력하세요:")
        
        if st.button("검색"):
            result = df[df['작가'].str.contains(author, case=False)]
            if not result.empty:
                st.write(f"### '{author}' 작가의 책 검색 결과")
                st.write(f"총 {len(result)}건의 책이 순위 내에 있습니다.")
                for idx, book in result.iterrows():
                    st.write(f"**순위:** {idx}")
                    st.write(f"**제목:** {book['제목']}")
                    st.write(f"**작가:** {book['작가']}")
                    st.write(f"**장르:** {book['장르']}")
                    st.write(f"[책 링크 보기]({book['링크']})")
            else:
                st.write("해당 작가의 책 정보를 찾을 수 없습니다.")