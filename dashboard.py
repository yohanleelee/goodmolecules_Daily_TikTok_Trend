import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="Good Molecules x 제조사 통합 분석", layout="wide")
st.title("📈 브랜드 트렌드 vs 제조사(코스메카/잉글우드) 주가 상관관계")

try:
    # 1. 틱톡 데이터 로드
    df = pd.read_csv("tiktok_trends_master.csv")
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    # 2. 주가 데이터 로드 (잉글우드랩 & 코스메카코리아)
    start_date = df['Date'].min().strftime('%Y-%m-%d')
    # 950140: 잉글우드랩, 240810: 코스메카코리아
    stocks = yf.download(["950140.KQ", "240810.KS"], start=start_date)
    
    # 멀티 인덱스 컬럼 해결
    if isinstance(stocks.columns, pd.MultiIndex):
        close_prices = stocks['Close']
    else:
        close_prices = stocks[['Close']]

    close_prices = close_prices.reset_index()
    close_prices['Date'] = pd.to_datetime(close_prices['Date']).dt.date

    # 3. 데이터 통합
    merged_df = pd.merge(df, close_prices, on='Date', how='left')
    merged_df = merged_df.ffill() # 주말 데이터 보간

    # 지표 계산
    merged_df['Comment_Ratio'] = (merged_df['Avg_Comments'] / merged_df['Avg_Views'] * 100).fillna(0)
    last_row = merged_df.iloc[-1]

    # --- 상단 핵심 지표 ---
    st.info("💡 틱톡 트렌드가 코스메카코리아와 잉글우드랩 주가에 미치는 영향을 분석합니다.")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("종합 Score", f"{last_row['Score']:,}")
    m2.metric("코스메카 현재가", f"{last_row['240810.KS']:,.0f}원")
    m3.metric("잉글우드 현재가", f"{last_row['950140.KQ']:,.0f}원")
    m4.metric("댓글 참여율", f"{last_row['Comment_Ratio']:.2f}%")

    st.divider()

    # --- 메인 분석: 주가 vs 틱톡 Score (삼중축 형태의 시각화) ---
    st.subheader("🔗 제조사 주가 그룹 vs 틱톡 종합 화력")
    
    fig_combined = go.Figure()
    # 틱톡 Score (막대)
    fig_combined.add_trace(go.Bar(
        x=merged_df['Date'], y=merged_df['Score'], name="틱톡 Score",
        marker_color='rgba(255, 75, 75, 0.4)', yaxis='y1'
    ))
    # 코스메카코리아 주가 (선)
    fig_combined.add_trace(go.Scatter(
        x=merged_df['Date'], y=merged_df['240810.KS'], name="코스메카코리아",
        line=dict(color='#FF7F0E', width=3), yaxis='y2'
    ))
    # 잉글우드랩 주가 (선)
    fig_combined.add_trace(go.Scatter(
        x=merged_df['Date'], y=merged_df['950140.KQ'], name="잉글우드랩",
        line=dict(color='#1F77B4', width=3), yaxis='y2'
    ))

    fig_combined.update_layout(
        yaxis=dict(title="틱톡 Score", side="left"),
        yaxis2=dict(title="주가 (원)", side="right", overlaying="y", showgrid=False),
        legend=dict(x=0, y=1.1, orientation="h")
    )
    st.plotly_chart(fig_combined, use_container_width=True)

    # --- 세부 지표 분석 ---
    st.subheader("💬 소비자 반응 및 효율성 지표")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**댓글 및 공유 수 추이**")
        st.plotly_chart(px.line(merged_df, x='Date', y=['Avg_Comments', 'Avg_Shares'], markers=True), use_container_width=True)
    with c2:
        st.write("**참여율 추이 (조회수 대비 %)**")
        merged_df['Like_Ratio'] = (merged_df['Avg_Likes'] / merged_df['Avg_Views'] * 100).fillna(0)
        st.plotly_chart(px.line(merged_df, x='Date', y=['Comment_Ratio', 'Like_Ratio'], markers=True), use_container_width=True)

except Exception as e:
    st.warning("데이터 통합 중입니다.")
    st.error(f"에러 내용: {e}")
