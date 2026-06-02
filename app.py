import streamlit as st
from PIL import Image
import os
from openai import OpenAI  # OpenAI API를 활용한다고 가정합니다.

# --- 환경 설정 (API 키) ---
# 실제 사용 시에는 환경 변수나 secrets.toml에 안전하게 저장해야 합니다.
os.environ["OPENAI_API_API_KEY"] = "YOUR_API_KEY_HERE"  # 실제 키로 변경하세요!
client = OpenAI()

st.title("My Health Focus: 식단 분석 테스트")

# --- 1. 사진 업로드 탭 ---
st.subheader("1. 오늘 드신 식단 사진을 올려주세요")
uploaded_file = st.file_uploader("사진 선택...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 업로드된 이미지를 화면에 표시
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드한 식단', use_column_width=True)
    
    st.write("")
    
    # --- 2. AI 분석 요청 (테스트 실행) ---
    if st.button("AI에게 영양 성분 분석 요청하기"):
        with st.spinner('AI가 식단을 분석 중입니다... 잠시만 기다려주세요.'):
            # 실제 구현 시에는 이미지를 base64로 인코딩하여 OpenAI Vision API에 전송하는 로직이 들어갑니다.
            # 이 부분은 API 연결 설정이 필요하므로, 테스트에서는 '결과 예시'를 보여줍니다.
            
            # (API 연동 완료 시 아래와 같은 결과를 AI가 반환합니다)
            # mock data (테스트용 예시 데이터)
            ai_analysis_result = {
                "meal_name": "비빔밥과 계란후라이",
                "calories": "약 650 kcal",
                "carbs": "85g",
                "protein": "22g",
                "fat": "25g",
                "note": "탄수화물 비중이 높지만, 채소가 많아 섬유질이 풍부합니다."
            }
            
            # --- 3. 분석 결과 표시 ---
            st.subheader("2. AI 분석 결과")
            st.success(f"분석 완료! 이 식단은 **{ai_analysis_result['meal_name']}**으로 보입니다.")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("칼로리", ai_analysis_result['calories'])
            col2.metric("탄수화물", ai_analysis_result['carbs'])
            col3.metric("단백질", ai_analysis_result['protein'])
            col4.metric("지방", ai_analysis_result['fat'])
            
            st.info(f"💡 **AI 코치 한줄 평**: {ai_analysis_result['note']}")
