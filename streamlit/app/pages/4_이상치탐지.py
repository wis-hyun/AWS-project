import streamlit as st
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="이상치 탐지", layout="wide")

# 제목 (기본 스타일, 흰색 배경에서 이모지 포함)
st.title("🚨 이상치 탐지 결과")

# 사이드바에 날짜 및 모듈 선택 UI 배치
st.sidebar.header("설정")

date_range = st.sidebar.date_input(
    "이상치 분석 기간",
    [datetime(2024, 12, 1), datetime(2025, 4, 30)],
    min_value=datetime(2024, 12, 1),
    max_value=datetime(2025, 4, 30)
)

module_img_map = {
    "모듈11": "모듈 11 이상치 탐지 결과.png",
    "모듈1": "모듈1 이상치 탐지결과.png"
}

selected_module = st.sidebar.selectbox("모듈 선택", options=list(module_img_map.keys()))

# 선택된 기간 표시
if len(date_range) == 2:
    start_date = date_range[0].strftime("%Y-%m-%d")
    end_date = date_range[1].strftime("%Y-%m-%d")
    st.sidebar.markdown(f"**선택된 기간:** `{start_date}` ~ `{end_date}`")

# 본문은 2개 컬럼으로 나누기 (Voltage S / 선택 모듈)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Voltage S 이상치 탐지 시각화 결과")
    try:
        voltage_img_path = "./pages/voltage S 이상치 탐지 결과.png"
        voltage_image = Image.open(voltage_img_path)
        st.image(voltage_image, use_container_width=True)
    except FileNotFoundError:
        st.warning(f"Voltage S 이미지 파일을 찾을 수 없습니다: {voltage_img_path}")
    except Exception as e:
        st.error(f"Voltage S 이미지를 불러오는 중 오류 발생: {e}")

with col2:
    st.subheader(f"🧩 {selected_module} 이상치 탐지 시각화 결과")
    try:
        module_img_path = f"./pages/{module_img_map[selected_module]}"
        module_image = Image.open(module_img_path)
        st.image(module_image, use_container_width=True)
    except FileNotFoundError:
        st.warning(f"{selected_module} 이미지 파일을 찾을 수 없습니다: {module_img_path}")
    except Exception as e:
        st.error(f"{selected_module} 이미지를 불러오는 중 오류 발생: {e}")

# 하단 여백
st.markdown("<br>", unsafe_allow_html=True)
