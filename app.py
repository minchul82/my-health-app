import streamlit as st

st.title("My Health Focus")

# 영양제 복용 체크
if st.checkbox("비타민 C 먹음"):
    st.write("잘하셨어요! 건강을 챙겼네요. ✅")
else:
    st.write("아직 안 드셨나요?")

# 식단 기록
food = st.text_input("오늘 무엇을 드셨나요?")
if food:
    st.write(f"기록 완료: {food}")

st.info("AI 분석 기능은 설정 중입니다.")
