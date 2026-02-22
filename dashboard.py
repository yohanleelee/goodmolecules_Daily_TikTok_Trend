import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 페이지 설정
st.set_page_config(page_title="Good Molecules Tracker", layout="wide")

# 이전 스타일의 헤더
st.title("✨ Good Molecules TikTok Trend Analysis")
st.markdown("틱톡 바이럴 지표를 기반으로 한 일일 투자 분석 대시보드")
st.divider()

file_path = "tiktok_trends_master.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    # 데이터 필터링 (Good Molecules 전용)
    df_gm = df[df["Keyword"] == "goodmolecules"].sort_values(by="Date")

    if not df_gm.empty:
        # 1. 상단 요약 지표 (최신 데이터 기반)
        latest = df_gm.iloc[-1]
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📊 Viral Score", f"{latest['Score']}")
        m2.metric("👀 Avg Views", f"{latest['Avg_Views']:,}")
        m3.metric("❤️ Avg Likes", f"{latest['Avg_Likes']:,}")
        m4.metric("💬 Avg Comments", f"{latest['Avg_Comments']:,}")

        st.divider()

        # 2. 메인 추이 차트 (이전 스타일)
        st.subheader("📈 Viral Score Trend")
        fig = px.area(df_gm, x="Date", y="Score", 
                      title="Good Molecules 바이럴 점수 추이",
                      line_shape="spline", 
                      color_discrete_sequence=['#2E86C1'])
        fig.update_layout(plot_bgcolor="white", xaxis_title="날짜", yaxis_title="점수")
        st.plotly_chart(fig, use_container_width=True)

        # 3. 상세 내역 테이블
        st.subheader("📋 상세 통계 기록")
        st.table(df_gm.sort_values(by="Date", ascending=False))
    else:
        st.info("데이터 파일에 'goodmolecules' 데이터가 없습니다.")
else:
    st.error("데이터 파일을 찾을 수 없습니다. main.py를 먼저 실행해 주세요.")
