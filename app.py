import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 라이브러리 체크를 위한 시도
try:
    from openai import OpenAI
    openai_available = True
except ImportError:
    openai_available = False

st.title("My Health Focus")

# 데이터 파일 이름
DATA_FILE = "health_data.csv"

# 입력 폼
with st.form("health_form"):
    vitamin = st.checkbox("비타민 C 먹음")
    food = st.text_input("오늘 먹은 음식")
    submit = st.form_submit_button("기록 저장하기")

if submit:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({"날짜": [now], "영양제": [vitamin], "식단": [food]})
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(DATA_FILE, index=False)
    st.success("기록 완료!")

# AI 기능
if st.button("AI 건강 분석 요청하기"):
    if not openai_available:
        st.error("openai 라이브러리가 설치되지 않았습니다. requirements.txt를 확인하세요.")
    elif "OPENAI_API_KEY" not in st.secrets:
        st.error("Streamlit Secrets에 OPENAI_API_KEY가 설정되지 않았습니다.")
    elif os.path.exists(DATA_FILE):
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        data = pd.read_csv(DATA_FILE).tail(3)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"다음 기록을 분석해줘: {data.to_string()}"}]
        )
        st.info(response.choices[0].message.content)
    else:
        st.warning("분석할 데이터가 없습니다.")
