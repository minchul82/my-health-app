import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

# 1. 민트색 테마 적용 (필라이즈 스타일)
st.set_page_config(page_title="My Health Focus", page_icon="💊", layout="wide")

st.markdown("""
    <style>
    :root { --mint-color: #00d2b4; }
    .stApp {background-color: #f7f9f9;}
    h1 {color: #00b89e !important; text-align: center; font-weight: 800;}
    h2 {color: #00b89e; font-size: 1.2rem;}
    .stButton>button {background-color: #00d2b4; color: white; border-radius: 20px; border: none; font-weight: bold;}
    div[data-testid="stMetricValue"] {color: #00b89e;}
    .css-1r6slp0 {background-color: white; border-radius: 20px; padding: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);}
    </style>
    """, unsafe_allow_html=True)

st.title("💊 My Health Focus")

DATA_FILE = "health_data.csv"

# 2. 메인 대시보드 레이아웃
with st.container():
    st.subheader("💡 오늘의 건강 기록")
    with st.form("input_form", clear_on_submit=True):
        col1, col2, col3 = st.columns([1, 4, 1])
        is_vitamin = col1.checkbox("비타민")
        food_input = col2.text_input("식단 입력", placeholder="오늘 먹은 음식을 기록하세요")
        submit_btn = col3.form_submit_button("저장")

if submit_btn:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({"날짜": [now], "영양제": [1 if is_vitamin else 0], "식단": [food_input]})
    df = pd.concat([pd.read_csv(DATA_FILE), new_data], ignore_index=True) if os.path.exists(DATA_FILE) else new_data
    df.to_csv(DATA_FILE, index=False)
    st.rerun()

# 3. 데이터 시각화
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    # 상단 지표 (민트 강조)
    m1, m2 = st.columns(2)
    m1.metric("총 섭취 횟수", f"{df['영양제'].sum()}회")
    m2.metric("최근 식단", df['식단'].iloc[-1])

    # 그래프 (민트색 영역 차트)
    st.subheader("📊 섭취 추이")
    stats = df.groupby(df['날짜'].dt.date)['영양제'].sum().reset_index()
    fig = px.area(stats, x='날짜', y='영양제', color_discrete_sequence=['#00d2b4'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    
    # 기록 관리
    with st.expander("🛠 기록 상세 관리"):
        del_idx = st.selectbox("삭제할 기록 선택", df.index)
        if st.button("선택 기록 삭제"):
            df.drop(del_idx).to_csv(DATA_FILE, index=False)
            st.rerun()
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)
else:
    st.info("첫 기록을 남겨보세요! 민트색 건강 리포트가 생성됩니다.")
