import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import yfinance as yf
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="GM x 실시간 주가 분석", layout="wide")

st.title("📊 Good Molecules 틱톡 지표 & 실시간 주가 상관관계")
st.markdown("Good Molecules의 틱톡 바이럴 지표와 제조사의 실제 주가(잉글우드랩, 코스메카코리아)를 비교 분석합니다.")

# --- 주가 데이터 가져오기 함수 ---
@st.cache_data(ttl=3600)  # 1시간마다 캐시 갱신
def get_stock_data(tickers, start_date):
    stock_df = pd.DataFrame()
    for name, ticker in tickers.items():
        data = yf.download(ticker, start=start_date)
        if not data.empty:
            data = data[['Close']].rename(columns={'Close': name})
            if stock_df.empty:
                stock_df = data
            else:
                stock_df = stock_df.join(data)
    return stock_df.reset_index()

file_path = "tiktok_trends_master.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df_gm = df[df["Keyword"] == "goodmolecules"].sort_values(by="Date")

    if not df_gm.empty:
        # 1. 주가 데이터 준비 (수집된 데이터의 첫 날짜부터 오늘까지)
        start_date = df_gm["Date"].min()
        tickers = {
            "잉글우드랩": "182400.KQ",
            "코스메카코리아": "241710.KQ"
        }
        stock_data = get_stock_data(tickers, start_date)

        # --- 섹션 1: 4대 틱톡 지표 (바 그래프) ---
        st.subheader("📱 틱톡 핵심 지표 (Daily Bar Charts)")
        r1_c1, r1_c2 = st.columns(2)
        r2_c1, r2_c2 = st.columns(2)
        
        with r1_c1:
            st.plotly_chart(px.bar(df_gm, x="Date", y="Avg_Views", title="평균 조회수(Views)", color_discrete_sequence=['#3498DB']), use_container_width=True)
        with r1_c2:
            st.plotly_chart(px.bar(df_gm, x="Date", y="Avg_Likes", title="평균 좋아요(Likes)", color_discrete_sequence=['#E74C3C']), use_container_width=True)
        with r2_c1:
            st.plotly_chart(px.bar(df_gm, x="Date", y="Avg_Comments", title="평균 댓글수(Comments)", color_discrete_sequence=['#2ECC71']), use_container_width=True)
        with r2_c2:
            st.plotly_chart(px.bar(df_gm, x="Date", y="Avg_Shares", title="평균 공유수(Shares)", color_discrete_sequence=['#9B59B6']), use_container_width=True)

        st.divider()

        # --- 섹션 2: 주가 상관관계 마스터 차트 ---
        st.subheader("📉 바이럴 스코어 vs 실제 주가 동향")
        
        fig_master = make_subplots(specs=[[{"secondary_y": True}]])

        # 바이럴 스코어 (바 그래프)
        fig_master.add_trace(
            go.Bar(x=df_gm["Date"], y=df_gm["Score"], name="GM 바이럴 점수", 
                   marker_color='rgba(180, 180, 180, 0.4)', offsetgroup=1),
            secondary_y=False,
        )

        # 실제 주가 (선 그래프)
        if not stock_data.empty:
            # 잉글우드랩
            fig_master.add_trace(
                go.Scatter(x=stock_data["Date"], y=stock_data["잉글우드랩"], 
                           name="잉글우드랩(실시간)", line=dict(color="#2980B9", width=3)),
                secondary_y=True,
            )
            # 코스메카코리아
            fig_master.add_trace(
                go.Scatter(x=stock_data["Date"], y=stock_data["코스메카코리아"], 
                           name="코스메카코리아(실시간)", line=dict(color="#E67E22", width=3)),
                secondary_y=True,
            )

        fig_master.update_layout(
            title_text="[바이럴 점수(Bar) vs 실제 시장 주가(Line)]",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="white"
        )

        fig_master.update_yaxes(title_text="Viral Score", secondary_y=False, showgrid=False)
        fig_master.update_yaxes(title_text="Stock Price (KRW)", secondary_y=True, showgrid=True, gridcolor='lightgray')

        st.plotly_chart(fig_master, use_container_width=True)

        # --- 섹션 3: 데이터 상세 정보 ---
        with st.expander("📝 데이터 원본 및 상세 기록"):
            st.write("틱톡 통계 데이터")
            st.dataframe(df_gm.sort_values(by="Date", ascending=False), use_container_width=True)
            st.write("최근 주가 데이터")
            st.dataframe(stock_data.sort_values(by="Date", ascending=False).head(10), use_container_width=True)

    else:
        st.warning("Good Molecules 데이터가 부족합니다.")
else:
    st.error("CSV 파일이 없습니다. main.py를 실행하여 데이터를 수집해 주세요.")
