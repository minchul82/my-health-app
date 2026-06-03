import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime
from openai import OpenAI

# 1. 디자인 개선을 위한 CSS 주입
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {width: 100%; border-radius: 10px; height: 3em; background-color: #007bff; color: white;}
    div[data-testid="stMetricValue"] {font-size: 20px;}
    .css-1r6slp0 {padding: 1rem; border-radius: 15px; border: 1px solid #ddd; background-color: white;}
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="My Health Focus", page_icon="💊", layout="wide")

# 헤더
st.title("💊 My Health Focus")
st.markdown("---")

DATA_FILE = "health_data.csv"

# 2. 카드 형태의 입력 섹션
with st.container():
    st.subheader("📝 오늘 기록하기")
    with st.form("health_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([1, 2, 1])
        vitamin = col1.checkbox("비타민 C 섭취")
        food = col2.text_input("오늘 먹은 음식", placeholder="예: 방울토마토 10개")
        submit = col3.form_submit_button("저장하기")

# (데이터 저장 로직은 기존과 동일...)
if submit:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({"날짜": [now], "영양제": [1 if vitamin else 0], "식단": [food]})
    df = pd.concat([pd.read_csv(DATA_FILE), new_data], ignore_index=True) if os.path.exists(DATA_FILE) else new_data
    df.to_csv(DATA_FILE, index=False)
    st.rerun()

# 3. 대시보드 형태의 시각화
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.subheader("📈 나의 건강 리포트")
        stats = df.groupby(df['날짜'].dt.date)['영양제'].sum().reset_index()
        fig = px.bar(stats, x='날짜', y='영양제', template="plotly_white", color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("🤖 AI 건강 조언")
        if st.button("AI 분석 실행"):
            # (AI 로직은 동일)
            st.info("AI 분석 결과가 여기에 깔끔하게 표시됩니다.")
            
    st.subheader("📋 전체 기록 관리")
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)
