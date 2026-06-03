import streamlit as st
import pandas as pd
from openai import OpenAI

# OpenAI API 클라이언트 설정 (반드시 Secrets에 OPENAI_API_KEY 저장 필수)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# AI 분석 버튼 및 로직
if st.button("AI 건강 분석 요청하기"):
    if os.path.exists("health_data.csv"):
        data = pd.read_csv("health_data.csv").tail(5) # 최근 5개 데이터 분석
        
        # AI 프롬프트 구성 (사용자의 기록을 분석하도록 요청)
        prompt = f"다음은 나의 최근 식단과 영양제 기록이야: {data.to_string()} 이 내용을 바탕으로 건강 관리에 대한 조언을 해줘."
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        st.write(response.choices[0].message.content)
    else:
        st.warning("분석할 데이터가 없습니다.")
