import streamlit as st
import sqlite3
from datetime import datetime

# 데이터베이스 초기화
conn = sqlite3.connect('supplements.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS intake (date TEXT, quantity INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS stock (start_date TEXT, initial_quantity INTEGER, current_quantity INTEGER)''')
conn.commit()

# 초기 재고 설정
def set_initial_stock(start_date, initial_quantity):
    c.execute("INSERT INTO stock (start_date, initial_quantity, current_quantity) VALUES (?, ?, ?)", (start_date, initial_quantity, initial_quantity))
    conn.commit()

# 섭취 기록 추가
def add_intake(date, quantity):
    c.execute("INSERT INTO intake (date, quantity) VALUES (?, ?)", (date, quantity))
    conn.commit()
    update_stock(quantity)

# 남은 재고 업데이트
def update_stock(quantity):
    c.execute("UPDATE stock SET current_quantity = current_quantity - ?", (quantity,))
    conn.commit()

# 재고 확인 및 알림
def check_stock():
    c.execute("SELECT current_quantity FROM stock")
    current_quantity = c.fetchone()[0]
    return current_quantity

# Streamlit UI 구성
st.title("건강식품 섭취 관리 앱")

# 초기 재고 설정
st.header("초기 재고 설정")
start_date = st.date_input("시작 날짜")
initial_quantity = st.number_input("초기 수량", min_value=1)

if st.button("재고 설정"):
    set_initial_stock(start_date, initial_quantity)
    st.success("재고가 설정되었습니다.")

# 섭취 기록 추가
st.header("섭취 기록 추가")
intake_date = st.date_input("섭취 날짜", datetime.now())
intake_quantity = st.number_input("섭취 수량", min_value=1)

if st.button("섭취 기록 추가"):
    add_intake(intake_date, intake_quantity)
    st.success("섭취 기록이 추가되었습니다.")

# 재고 확인
st.header("재고 확인")
if st.button("재고 확인"):
    current_quantity = check_stock()
    st.write(f"현재 남은 수량: {current_quantity}")
    if current_quantity <= 5:
        st.warning("알림: 재고가 부족합니다. 보충이 필요합니다.")

# Streamlit 앱 실행
if __name__ == "__main__":
    st.run()
