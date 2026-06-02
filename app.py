import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("My Health Focus")

# 데이터 파일 이름
DATA_FILE = "health_data.csv"

# 입력 폼
with st.form("health_form"):
    vitamin = st.checkbox("비타민 C 먹음")
    food = st.text_input("오늘 먹은 음식")
    submit = st.form_submit_button("기록 저장하기")

if submit:
    # 현재 시간 가져오기
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({"날짜": [now], "영양제": [vitamin], "식단": [food]})
    
    # 파일이 있으면 불러오고, 없으면 새로 만들기
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
        
    df.to_csv(DATA_FILE, index=False)
    st.success("기록 완료!")

# 데이터 확인하기
if os.path.exists(DATA_FILE):
    st.subheader("기록된 데이터")
    st.write(pd.read_csv(DATA_FILE))
