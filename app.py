import streamlit as st
import duckdb
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="마당 서점 관리", layout="wide")

# 2. DB 연결 함수
@st.cache_resource
def get_connection():
    try:
        conn = duckdb.connect('madang.db', read_only=True)
        return conn
    except Exception as e:
        st.error(f"DB 연결 오류: {e}")
        return None

conn = get_connection()

# 3. 상단 탭 메뉴 만들기 (보여준 이미지대로!)
tab1, tab2, tab3 = st.tabs(["고객조회", "거래 입력", "고객 등록"])

# --- [첫 번째 탭: 고객 조회] ---
with tab1:
    st.subheader("고객명")
    
    # 텍스트 입력창 (placeholder 없이 깔끔하게)
    search_name = st.text_input("검색할 이름을 입력하세요", label_visibility="collapsed")

    # 이름을 입력했을 때만 조회 실행
    if search_name:
        if conn:
            # 쿼리 마법: 고객(Customer) + 주문(Orders) + 책(Book) 테이블을 합쳐서 가져옴
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
                    # 데이터가 있으면 표 보여주기
                    st.dataframe(df, use_container_width=True)
                    # 건수 알려주기
                    st.success(f"🔎 '{search_name}' 고객님의 구매 내역: 총 {len(df)}건 검색되었습니다.")
                else:
                    # 데이터가 없으면 안내
                    st.warning(f"⚠ '{search_name}' 고객님의 주문 내역이 없거나, 등록되지 않은 고객입니다.")
            except Exception as e:
                st.error(f"오류 발생: {e}")

# --- [두 번째 탭: 거래 입력 (껍데기)] ---
with tab2:
    st.info("🛠 거래 입력 기능은 준비 중입니다.")

# --- [세 번째 탭: 고객 등록 (껍데기)] ---
with tab3:
    st.info("🛠 고객 등록 기능은 준비 중입니다.")
    