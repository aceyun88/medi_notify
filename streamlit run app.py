import streamlit as st
import sqlite3
from datetime import datetime

# 데이터베이스 초기화
conn = sqlite3.connect('supplements.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS intake (date TEXT, quantity INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS stock (start_date TEXT, initial_quantity INTEGER, current_quantity INTEGER, daily_intake INTEGER)''')
conn.commit()

# 초기 재고 설정
def set_initial_stock(start_date, initial_quantity, daily_intake):
    c.execute("INSERT INTO stock (start_date, initial_quantity, current_quantity, daily_intake) VALUES (?, ?, ?, ?)", 
              (start_date, initial_quantity, initial_quantity, daily_intake))
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
    c.execute("SELECT current_quantity, daily_intake FROM stock")
    stock_info = c.fetchone()
    current_quantity = stock_info[0]
    daily_intake = stock_info[1]
    return current_quantity, daily_intake

# Streamlit UI 구성
st.title("건강식품 섭취 관리 앱")

# 초기 재고 설정
st.header("초기 재고 설정")
start_date = st.date_input("시작 날짜")
initial_quantity = st.number_input("초기 수량", min_value=1)
daily_intake = st.number_input("주기적 섭취량 (예: 매일 두 알)", min_value=1)

if st.button("재고 설정"):
    set_initial_stock(start_date, initial_quantity, daily_intake)
    st.success("재고가 설정되었습니다.")

# 섭취 기록 추가
st.header("섭취 기록 추가")
intake_date = st.date_input("섭취 날짜", datetime.now())

# 주기적 섭취량을 기본값으로 설정
current_quantity, default_daily_intake = check_stock()
intake_quantity = st.number_input("섭취 수량", min_value=1, value=default_daily_intake)

if st.button("섭취 기록 추가"):
    add_intake(intake_date, intake_quantity)
    st.success("섭취 기록이 추가되었습니다.")

# 재고 확인
st.header("재고 확인")
if st.button("재고 확인"):
    current_quantity, daily_intake = check_stock()
    days_left = current_quantity // daily_intake
    st.write(f"현재 남은 수량: {current_quantity} 알")
    st.write(f"주기적 섭취량: {daily_intake} 알")
    st.write(f"남은 일수: {days_left} 일")
    
    if days_left <= 5:
        st.warning(f"알림: 재고가 {days_left} 일분 ({current_quantity} 알) 남아 있습니다. 보충이 필요합니다.")

# Streamlit 앱 실행
if __name__ == "__main__":
    st.run()
