import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Good Molecules x 잉글우드랩 통합 분석", layout="wide")
st.title("📈 브랜드 트렌드 vs 잉글우드랩(950140) 주가 상관관계")

try:
    # 1. 틱톡 데이터 로드
    df = pd.read_csv("tiktok_trends_master.csv")
    df['Date'] = pd.to_datetime(df['Date'])

    # 2. 잉글우드랩 주가 데이터 로드 (yfinance)
    # 틱톡 데이터의 시작일부터 오늘까지의 주가를 가져옵니다.
    start_date = df['Date'].min().strftime('%Y-%m-%d')
    stock_df = yf.download("950140.KQ", start=start_date)
    stock_df = stock_df.reset_index()
    stock_df['Date'] = pd.to_datetime(stock_df['Date'])

    # 3. 데이터 통합 (날짜 기준)
    merged_df = pd.merge(df, stock_df[['Date', 'Close']], on='Date', how='left')
    merged_df['Comment_Ratio'] = (merged_df['Avg_Comments'] / merged_df['Avg_Views'] * 100).fillna(0)

    # 최신 데이터 추출
    last_row = merged_df.iloc[-1]
    current_price = last_row['Close'] if not pd.isna(last_row['Close']) else "데이터 없음"

    # --- 상단 핵심 지표 ---
    st.info(f"💡 잉글우드랩 현재가: {current_price}원 (종가 기준)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("종합 Score", f"{last_row['Score']:,}")
    m2.metric("댓글 참여율", f"{last_row['Comment_Ratio']:.2f}%")
    m3.metric("평균 댓글수", f"{int(last_row['Avg_Comments']):,}")
    m4.metric("평균 공유수", f"{int(last_row['Avg_Shares']):,}")

    st.divider()

    # --- 메인 분석: 주가 vs 틱톡 Score (이중축 그래프) ---
    st.subheader("🔗 주가 vs 틱톡 종합 화력 (상관관계 분석)")
    
    fig_combined = go.Figure()
    # 틱톡 Score (막대)
    fig_combined.add_trace(go.Bar(
        x=merged_df['Date'], y=merged_df['Score'], name="틱톡 Score",
        marker_color='rgba(255, 75, 75, 0.6)', yaxis='y1'
    ))
    # 잉글우드랩 주가 (선)
    fig_combined.add_trace(go.Scatter(
        x=merged_df['Date'], y=merged_df['Close'], name="잉글우드랩 주가",
        line=dict(color='#1f77b4', width=3), yaxis='y2'
    ))

    fig_combined.update_layout(
        yaxis=dict(title="틱톡 Score", side="left"),
        yaxis2=dict(title="주가 (원)", side="right", overlaying="y", showgrid=False),
        legend=dict(x=0, y=1.1, orientation="h")
    )
    st.plotly_chart(fig_combined, use_container_width=True)

    # --- 세부 지표 섹션 ---
    st.subheader("💬 세부 참여 지표 추이")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.write("**댓글 참여율 (%)**")
        st.plotly_chart(px.line(merged_df, x='Date', y='Comment_Ratio', markers=True), use_container_width=True)
    with c2:
        st.write("**평균 공유수**")
        st.plotly_chart(px.bar(merged_df, x='Date', y='Avg_Shares', color_discrete_sequence=['#FFA15A']), use_container_width=True)
    with c3:
        st.write("**조회수 대비 좋아요 비율 (%)**")
        merged_df['Like_Ratio'] = (merged_df['Avg_Likes'] / merged_df['Avg_Views'] * 100).fillna(0)
        st.plotly_chart(px.line(merged_df, x='Date', y='Like_Ratio', markers=True, color_discrete_sequence=['#FECB52']), use_container_width=True)

except Exception as e:
    st.warning("데이터 수집 및 통합 중입니다. 첫 데이터가 생성되면 주가와 함께 표시됩니다.")
    st.error(f"상세 에러: {e}")
