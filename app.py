import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="My Health Focus", page_icon="💊")

st.title("💊 My Health Focus")
st.write("오늘의 건강 상태를 기록하고 분석해보세요.")

# 데이터 파일 이름
DATA_FILE = "health_data.csv"

# 1. 입력 폼 섹션
with st.form("health_form", clear_on_submit=True):
    vitamin = st.checkbox("비타민 C 먹음")
    food = st.text_input("오늘 먹은 음식")
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

# 2. 데이터 분석 및 시각화 섹션
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    st.divider()
    st.subheader("📊 나의 건강 리포트")
    
    # 통계 수치
    col1, col2 = st.columns(2)
    vitamin_count = df["영양제"].sum()
    col1.metric("총 비타민 섭취 횟수", f"{vitamin_count}회")
    col2.metric("총 기록 횟수", f"{len(df)}회")
    
    # 섭취 패턴 그래프
    st.write("### 📅 섭취 패턴")
    df['날짜_일자'] = df['날짜'].dt.date
    daily_stats = df.groupby('날짜_일자')['영양제'].sum()
    st.bar_chart(daily_stats)
    
    # 전체 기록 펼쳐보기
    with st.expander("📝 전체 기록 보기"):
        st.dataframe(df.sort_values(by='날짜', ascending=False))
else:
    st.info("아직 기록된 데이터가 없습니다. 먼저 기록을 시작해 보세요!")
