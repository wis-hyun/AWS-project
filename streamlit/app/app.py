import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="스마트팩토리 에너지 시스템",
    page_icon="⚡",
    layout="wide"
)

# 제목 영역
st.markdown("<h1 style='text-align: center;'>⚙️ 스마트팩토리 에너지 예측 시스템</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>전력 소비량 · 요금 · 탄소 배출량을 한눈에 예측하고 모니터링하세요.</h4>", unsafe_allow_html=True)
st.markdown("---")


# 소개 카드
st.markdown("## 🔍 프로젝트 개요")
st.markdown("""
- 본 시스템은 **공장 이벤트/작업 시간 동안의 전력 소비, 요금, 탄소배출량을 예측**하는 대시보드입니다.
- AI 기반의 시계열 예측 모델(LSTM, RNN 등)을 활용해 실시간 또는 일별 트렌드 비교가 가능합니다.
- 이상치 탐지 기능을 통해 비정상적인 소비 패턴도 식별할 수 있습니다.
""")

# 팀 정보
st.markdown("## 👥 팀 정보")
st.markdown("""
- 팀 이름: **SMWU Project 6조**
- 소속: 숙명여자대학교 인공지능공학부, 소프트웨어학부
- 개발 도구: Streamlit, AWS SageMaker, PyTorch, Altair
""")

# 기능 안내
st.markdown("## 🧭 주요 기능")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🔌 전력 예측", "일/시간별 소비량")
    st.caption("AI가 학습한 결과를 통해 소비량 예측")
with col2:
    st.metric("💰 요금 예측", "실시간 비용 계산")
    st.caption("단가 입력을 통해 요금 변동 확인")
with col3:
    st.metric("🌱 탄소 배출량", "환경 영향 추정")
    st.caption("지속 가능한 에너지 관리 지원")

st.markdown("---")
st.success("📊 좌측 메뉴에서 대시보드 기능을 시작해보세요!")