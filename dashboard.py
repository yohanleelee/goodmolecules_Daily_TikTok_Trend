import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Beauty Brand TikTok Trend Tracker", layout="wide")

st.title("📈 뷰티 브랜드 틱톡 바이럴 분석 대시보드")
st.sidebar.header("설정")

file_path = "tiktok_trends_master.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    
    # 1. 상단 요약 지표 (가장 최근 날짜 기준)
    recent_date = df["Date"].max()
    st.subheader(f"📅 최근 분석 일자: {recent_date}")
    
    cols = st.columns(len(df["Keyword"].unique()))
    for i, kw in enumerate(df["Keyword"].unique()):
        kw_data = df[(df["Keyword"] == kw) & (df["Date"] == recent_date)]
        if not kw_data.empty:
            cols[i].metric(label=f"🚀 {kw} Score", value=kw_data["Score"].values[0])

    st.divider()

    # 2. 트렌드 그래프
    st.subheader("📊 브랜드별 바이럴 스코어 추이")
    fig = px.line(df, x="Date", y="Score", color="Keyword", markers=True,
                 title="일별 틱톡 통합 점수 추이")
    st.plotly_chart(fig, use_container_width=True)

    # 3. 상세 데이터 테이블
    st.subheader("📋 상세 통계 데이터")
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)

else:
    st.warning("데이터 파일(tiktok_trends_master.csv)이 아직 없습니다. main.py를 먼저 실행해 주세요.")
