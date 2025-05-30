import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
from utils.sagemaker_util import query_sagemaker

st.set_page_config(page_title="탄소배출량 소비 예측", layout="wide")
st.title("🔌 날짜별 탄소배출량 소비 예측")
st.markdown("기간별 탄소배출량을 예측하여 시각화합니다.")

# 날짜 선택
selected_range = st.date_input("📆 예측 날짜 범위 선택", [datetime(2025, 5, 10), datetime(2025, 5, 17)])
if len(selected_range) != 2:
    st.warning("시작일과 종료일을 모두 선택해주세요.")
    st.stop()

start_date, end_date = selected_range
horizon = (end_date - start_date).days + 1

# 더미 입력 데이터
date_range = pd.date_range(end=start_date - timedelta(days=1), periods=30, freq="D")
dummy_data = [{"timestamp": d.strftime("%Y-%m-%d"), "value": 40000 + np.sin(i / 5) * 500} for i, d in enumerate(date_range)]

payload = {
    "data": dummy_data,
    "horizon": horizon
}

# 예측 결과 처리
try:
    result = query_sagemaker("carbon-lstm2", payload)
    predictions = result["values"]
    timestamps = result["timestamps"]

    df = pd.DataFrame({
        "날짜": pd.to_datetime(timestamps),
        "예측 탄소배출량": [max(v[0], 0) for v in predictions]  # 음수 방지
    })
    df["예측 탄소배출량 (kgCO₂)"] = df["예측 전력량 (kWh)"] * 0.424
    df["누적 전력량"] = df["예측 전력량 (kWh)"].cumsum()
    df["누적 탄소배출"] = df["예측 탄소배출량 (kgCO₂)"].cumsum()

    # 그래프
    chart = alt.Chart(df).transform_fold(
        ["예측 전력량 (kWh)", "예측 탄소배출량 (kgCO₂)"],
        as_=["항목", "값"]
    ).mark_line(point=True).encode(
        x="날짜:T",
        y="값:Q",
        color=alt.Color("항목:N", scale=alt.Scale(
            domain=["예측 전력량 (kWh)", "예측 탄소배출량 (kgCO₂)"],
            range=["#42a5f5", "#66bb6a"]
        )),
        tooltip=["날짜:T", "항목:N", "값:Q"]
    ).properties(
        title="📈 날짜별 전력 및 탄소 예측 추이",
        width=850,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    # 누적 지표 요약
    col1, col2, col3 = st.columns(3)
    col1.metric("🔋 총 전력 소비량", f"{df['예측 전력량 (kWh)'].sum():,.2f} kWh")
    col2.metric("🌱 총 탄소배출량", f"{df['예측 탄소배출량 (kgCO₂)'].sum():,.2f} kgCO₂")
    col3.metric("📐 탄소 배출 예측 MAE", "65.68 g")

    # 예측 테이블
    st.markdown("### 📋 예측 상세 결과")
    st.dataframe(df[["날짜", "예측 전력량 (kWh)", "예측 탄소배출량 (kgCO₂)"]].style.format({
        "예측 전력량 (kWh)": "{:.2f}",
        "예측 탄소배출량 (kgCO₂)": "{:.2f}"
    }), use_container_width=True)

    st.info("※ 탄소배출량은 `전력량 × 0.424`로 계산되었으며, LSTM 예측 모델의 MAE는 65.68g입니다.")

except Exception as e:
    st.error(f"❌ 예측 실패: {e}")