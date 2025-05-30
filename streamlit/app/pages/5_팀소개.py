import streamlit as st
from PIL import Image

st.set_page_config(page_title="팀 소개", layout="wide")
st.title("👥 팀 소개 및 역할")

st.markdown("---")

# 팀원 정보 카드
st.subheader("🧑‍💻 팀 구성원 역할")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👩 김예은")
    st.markdown("""
    - 💼 팀장  
    - 📊 모델링  
    - 🧹 데이터 전처리  
    """)

    st.markdown("### 👩 조해수")
    st.markdown("""
    - 📈 모델링  
    - 🚨 이상치 탐지  
    """)

with col2:
    st.markdown("### 👩 임수연")
    st.markdown("""
    - ☁️ AWS SageMaker 배포  
    - 🔌 Streamlit 연동  
    """)

    st.markdown("### 👩 김성현")
    st.markdown("""
    - ☁️ AWS SageMaker 배포  
    - 🎨 UI/UX 개발  
    """)

st.markdown("---")
st.success("우리는 전기 요금과 탄소 배출 예측을 위해 협업한 SMWU AI 팀입니다! 🔥")