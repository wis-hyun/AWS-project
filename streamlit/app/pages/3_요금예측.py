import sys
import os
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import altair as alt
import json
import boto3
from botocore.config import Config

# 🔥 SageMaker endpoint 호출 함수
def query_sagemaker(endpoint_name, payload):
    runtime = boto3.client(
        "sagemaker-runtime",
        region_name="ap-northeast-2",  # 배포 리전에 맞게 변경하세요
        config=Config(connect_timeout=60, read_timeout=180)
    )
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(payload)
    )
    result = json.loads(response["Body"].read().decode())
    return result

# 🔥 Streamlit UI
st.title("💰 요금 예측")

# 날짜 범위 선택
selected_range = st.date_input(
    "예측 날짜 범위 선택",
    [datetime(2025, 5, 10), datetime(2025, 5, 17)]
)
if len(selected_range) != 2:
    st.warning("시작일과 종료일을 모두 선택해주세요.")
    st.stop()

start_date, end_date = selected_range
if start_date >= end_date:
    st.warning("예측 시작일은 종료일보다 이전이어야 합니다.")
    st.stop()

# kWh당 요금 입력
unit_price = st.number_input(
    "kWh당 요금 (원)",
    min_value=0,
    value=180,
    step=10
)

# 🔥 예측 버튼
if st.button("예측하기"):
    with st.spinner("🔍 예측 중입니다... 잠시만 기다려주세요."):
        payload = {
            "start_date": str(start_date),
            "end_date": str(end_date),
            "unit_price": unit_price
        }

        try:
            endpoint_name = "bill-lstm-endpoint-v9"
            result = query_sagemaker(endpoint_name, payload)

            df_result = pd.DataFrame({
                "날짜": pd.to_datetime(result["timestamps"]),
                "예측 전력 사용량 (kWh)": [v[0] for v in result["values"]],
                "예상 요금 (원)": [v[0] for v in result["estimated_bills"]]
            })

            # 📈 Altair 시각화
            chart = alt.Chart(df_result).mark_line(point=True).encode(
                x="날짜:T",
                y="예상 요금 (원):Q",
                tooltip=["날짜", "예측 전력 사용량 (kWh)", "예상 요금 (원)"]
            ).properties(title="📈 하루 단위 요금 예측 결과")

            st.altair_chart(chart, use_container_width=True)
            st.metric("🔋 총 전력 사용량", f"{df_result['예측 전력 사용량 (kWh)'].sum():,.2f} kWh")
            st.metric("💸 총 예상 요금", f"{df_result['예상 요금 (원)'].sum():,.0f} 원")
            st.markdown("📋 예측 상세 결과")
            st.dataframe(df_result)

        except Exception as e:
            st.error(f"❌ 예측 실패: {e}")
