# pages/1_대시보드_요약.py
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="대시보드 요약", layout="wide")
st.title("📋 대시보드 요약")
st.markdown("#### ‍💻 팀 이름: SMWU Project 6조 | 🔍 프로젝트: 전기 요금 & 탄소 예측 시스템")

# # 보조된 예산 값 (dummy)
# st.metric(label="오늘 총 전력 소비량", value="1,250 kWh", delta="-50 kWh")
# st.metric(label="오늘 총 전기 요금", value="225,000 원", delta="-9,000 원")
# st.metric(label="오늘 총 탄소 배출량", value="530.00 kgCO₂", delta="-21.2 kgCO₂")

st.markdown("""
#### 개요
- 이벤트 공사에서 전력 사용•요금 •탄소 배출량을 예측과 리스트로 보여준 대시보드입니다.
- 모든 값은 예산된 것으로, 복수로 변경됩니다.
""")

# 요약 지표: 5월 10일 ~ 5월 31일 vs 4월 10일 ~ 4월 30일

st.markdown("---")

col1, col2, col3 = st.columns(3)

col1.metric(
    label="🔋 5월 총 전력 소비량",
    value="36,420 kWh",
    delta="+1,200 kWh"
)

col2.metric(
    label="💸 5월 총 전기 요금",
    value="6,555,600 원",
    delta="+216,000 원"
)

col3.metric(
    label="🌱 5월 총 탄소 배출량",
    value="15,415.86 kgCO₂",
    delta="+508.32 kgCO₂"
)

st.markdown("---")

# 더미 총합 데이터
df_summary = pd.DataFrame({
    "항목": ["전력 소비량 (kWh)", "전기 요금 (원)", "탄소 배출량 (kgCO₂)"],
    "실제": [36000, 6480000, 15200],
    "예측": [36750, 6615000, 15540]
})

# 정규화된 비율 계산 (실제값을 100으로 둠)
df_summary["실제_비율"] = 100.0
df_summary["예측_비율"] = (df_summary["예측"] / df_summary["실제"]) * 100

# 시각화용 long-form 변환
bar_data = df_summary.melt(
    id_vars="항목",
    value_vars=["실제_비율", "예측_비율"],
    var_name="데이터종류",
    value_name="비율값"
)

# 보기 좋게 이름 매핑
bar_data["데이터종류"] = bar_data["데이터종류"].map({
    "실제_비율": "실제 (100%)",
    "예측_비율": "예측"
})

# 원하는 항목 순서 지정
desired_order = ["전력 소비량 (kWh)", "전기 요금 (원)", "탄소 배출량 (kgCO₂)"]
bar_data["항목"] = pd.Categorical(bar_data["항목"], categories=desired_order, ordered=True)

# 그래프
bar_chart = alt.Chart(bar_data).mark_bar(size=50).encode(
    x=alt.X("항목:N", title="", sort=desired_order, axis=alt.Axis(labelAngle=0)),
    xOffset="데이터종류:N",
    y=alt.Y("비율값:Q", title="예측 비율 (%)", scale=alt.Scale(domain=[0, 120])),
    color=alt.Color("데이터종류:N", scale=alt.Scale(range=["#cfd8dc", "#90caf9"])),
    tooltip=["항목", "데이터종류", alt.Tooltip("비율값:Q", format=".1f")]
).properties(
    width=650,
    height=350,
)

# 시각화 + MAE 나란히 배치
with st.container():
    col1, col2 = st.columns([1.5, 1])  # 또는 [3, 2]
    with col1:
        st.markdown("### 📊 예측 vs 실제 (정규화된 100% 기준)")
        st.altair_chart(bar_chart, use_container_width=True)
    with col2:
        st.markdown("### 📐 예측 오차 지표 (MAE 기준)")
        st.metric("🔋 전력 소비량", "68.3 kWh")
        st.metric("💸 전기 요금", "12,240 원")
        st.metric("🌱 탄소 배출량", "37.2 kgCO₂")

# 3. 선 그래프 (예측 vs 실제 트렌드)
st.markdown("### 📈 시간대별 예측 vs 실제 비교")

dates = pd.date_range("2025-05-10", "2025-05-31 00:00", freq="D")
actual_power = np.random.uniform(1400, 1700, len(dates))
pred_power = actual_power + np.random.uniform(-100, 100, len(dates))

df_trend = pd.DataFrame({
    "날짜": dates,
    "실제": actual_power,
    "예측": pred_power
}).melt(id_vars="날짜", var_name="구분", value_name="전력 소비량 (kWh)")

line_chart = alt.Chart(df_trend).mark_line(point=True).encode(
    x="날짜:T",
    y="전력 소비량 (kWh):Q",
    color=alt.Color("구분:N", scale=alt.Scale(
        domain=["실제", "예측"],
        range=["#cfd8dc", "#90caf9"] 
    )),
).properties(title="일자별 전력 소비 예측 비교")

st.altair_chart(line_chart, use_container_width=True)

# 4. 평가 요약
st.info("✅ 예측 오차는 전체 사용량 대비 ±2.1% 이내로, 예측 품질이 양호한 편입니다.")