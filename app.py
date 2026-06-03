import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="My Health Focus", page_icon="💊", layout="wide")
st.title("💊 My Health Focus")

DATA_FILE = "health_data.csv"

# 1. 기록 폼
with st.form("health_form", clear_on_submit=True):
    col_a, col_b = st.columns([1, 3])
    vitamin = col_a.checkbox("비타민 C")
    food = col_b.text_input("오늘 먹은 음식")
    submit = st.form_submit_button("기록 저장하기")

if submit:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({"날짜": [now], "영양제": [1 if vitamin else 0], "식단": [food]})
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(DATA_FILE, index=False)
    st.success("기록 완료!")
    st.rerun()

# 2. 데이터 시각화 및 AI 분석
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    st.divider()
    
    # 2개 열로 나누어 보기
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📊 섭취 패턴")
        df['날짜_일자'] = df['날짜'].dt.date
        stats = df.groupby('날짜_일자')['영양제'].sum().reset_index()
        fig = px.bar(stats, x='날짜_일자', y='영양제', title="날짜별 비타민 섭취 횟수")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("🤖 AI 건강 코칭")
        if st.button("AI 분석 요청하기"):
            if "OPENAI_API_KEY" in st.secrets:
                client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                summary = df.tail(5).to_string()
                with st.spinner("분석 중..."):
                    res = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": f"기록: {summary}. 조언해줘."}]
                    )
                    st.info(res.choices[0].message.content)
            else:
                st.error("API 키가 없습니다.")

    st.divider()
    
    # 3. 데이터 관리
    st.subheader("🛠 데이터 관리")
    row_to_delete = st.selectbox("삭제할 기록 선택:", df.index)
    if st.button("선택한 기록 삭제"):
        df = df.drop(row_to_delete)
        df.to_csv(DATA_FILE, index=False)
        st.rerun()
        
    st.write("### 📝 전체 기록")
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)

else:
    st.info("아직 데이터가 없습니다. 첫 기록을 남겨보세요!")
