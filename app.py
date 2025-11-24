import streamlit as st
import duckdb
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="마당 서점 관리", layout="wide")

# 2. DB 연결 및 초기화 함수 (없으면 만드는 똑똑한 함수)
@st.cache_resource
def get_connection():
    # madang.db에 연결 (없으면 새로 생성됨)
    con = duckdb.connect('madang.db', read_only=False)
    
    # 테이블이 있는지 확인 (없으면 CSV에서 로딩)
    try:
        con.execute("SELECT count(*) FROM Book")
    except:
        # 테이블이 없으면 CSV 파일에서 데이터 가져와서 테이블 만들기
        # (깃허브에 올린 csv 파일들이 여기서 쓰임)
        con.execute("CREATE OR REPLACE TABLE Book AS SELECT * FROM 'Book_madang.csv'")
        con.execute("CREATE OR REPLACE TABLE Customer AS SELECT * FROM 'Customer_madang.csv'")
        con.execute("CREATE OR REPLACE TABLE Orders AS SELECT * FROM 'Orders_madang.csv'")
        
        # [관리자 모드] 박지성을 김민중으로 이름 변경 (자동 적용)
        con.execute("UPDATE Customer SET name = '김민중' WHERE name = '박지성'")
        
    return con

conn = get_connection()

# 3. 상단 탭 메뉴
tab1, tab2, tab3 = st.tabs(["고객조회", "거래 입력", "고객 등록"])

# --- [첫 번째 탭: 고객 조회] ---
with tab1:
    st.subheader("고객명")
    
    # 텍스트 입력창
    search_name = st.text_input("검색할 이름을 입력하세요", label_visibility="collapsed")

    # 이름을 입력했을 때만 조회 실행
    if search_name:
        if conn:
            query = f"""
            SELECT 
                c.custid, 
                c.name, 
                b.bookname, 
                o.orderdate, 
                o.saleprice
            FROM Orders o
            JOIN Customer c ON o.custid = c.custid
            JOIN Book b ON o.bookid = b.bookid
            WHERE c.name = '{search_name}'
            ORDER BY o.orderdate DESC
            """
            
            try:
                df = conn.execute(query).df()
                
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                    st.success(f"🔎 '{search_name}' 고객님의 구매 내역: 총 {len(df)}건 검색되었습니다.")
                else:
                    st.warning(f"⚠ '{search_name}' 고객님의 주문 내역이 없거나, 등록되지 않은 고객입니다.")
            except Exception as e:
                st.error(f"오류 발생: {e}")

with tab2:
    st.info("🛠 거래 입력 기능은 준비 중입니다.")

with tab3:
    st.info("🛠 고객 등록 기능은 준비 중입니다.")
