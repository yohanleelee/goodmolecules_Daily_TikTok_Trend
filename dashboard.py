import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(page_title="GM & Englewood Lab Analysis", layout="wide")

st.title("🧪 Good Molecules 바이럴 - 제조사 주가 상관관계 분석")
st.markdown("Good Molecules의 틱톡 지표와 잉글우드랩/코스메카코리아의 주가 동향을 비교합니다.")

file_path = "tiktok_trends_master.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df_gm = df[df["Keyword"] == "goodmolecules"].sort_values(by="Date")

    if not df_gm.empty:
        # --- 섹션 1: 4대 지표 개별 그래프 ---
        st.subheader("📊 틱톡 개별 지표 트렌드")
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(px.line(df_gm, x="Date", y="Avg_Views", title="평균 조회수(Views) 추이", line_shape="spline", color_discrete_sequence=['#636EFA']), use_container_width=True)
            st.plotly_chart(px.line(df_gm, x="Date", y="Avg_Comments", title="평균 댓글수(Comments) 추이", line_shape="spline", color_discrete_sequence=['#00CC96']), use_container_width=True)
        
        with col2:
            st.plotly_chart(px.line(df_gm, x="Date", y="Avg_Likes", title="평균 좋아요(Likes) 추이", line_shape="spline", color_discrete_sequence=['#EF553B']), use_container_width=True)
            st.plotly_chart(px.line(df_gm, x="Date", y="Avg_Shares", title="평균 공유수(Shares) 추이", line_shape="spline", color_discrete_sequence=['#AB63FA']), use_container_width=True)

        st.divider()

        # --- 섹션 2: 주가 상관관계 분석 (이중 축 그래프) ---
        st.subheader("📈 브랜드 바이럴 점수 vs 제조사 주가")
        st.info("※ 주가 데이터는 분석을 위해 연동된 예시이며, 실제 증권사 API 연결 시 실시간 반영됩니다.")

        # 가상의 주가 데이터 생성 (실제 주가 데이터를 넣으려면 yfinance 등을 사용)
        # 여기서는 바이럴 점수와 비교하기 위해 샘플 데이터를 매칭합니다.
        fig_stock = make_subplots(specs=[[{"secondary_y": True}]])

        # 바이럴 점수 (막대 그래프)
        fig_stock.add_trace(
            go.Bar(x=df_gm["Date"], y=df_gm["Score"], name="GM 바이럴 점수", opacity=0.3, marker_color="gray"),
            secondary_y=False,
        )

        # 잉글우드랩 주가 추이 (선 그래프)
        fig_stock.add_trace(
            go.Scatter(x=df_gm["Date"], y=[15000 + (i*100) for i in range(len(df_gm))], name="잉글우드랩(예시)", line=dict(color="#1f77b4", width=3)),
            secondary_y=True,
        )

        # 코스메카코리아 주가 추이 (선 그래프)
        fig_stock.add_trace(
            go.Scatter(x=df_gm["Date"], y=[70000 + (i*500) for i in range(len(df_gm))], name="코스메카코리아(예시)", line=dict(color="#ff7f0e", width=3)),
            secondary_y=True,
        )

        fig_stock.update_layout(title_text="바이럴 점수와 주가 추이 비교 (상관관계 분석)")
        fig_stock.update_yaxes(title_text="<b>Viral Score</b>", secondary_y=False)
        fig_stock.update_yaxes(title_text="<b>Stock Price (KRW)</b>", secondary_y=True)
        
        st.plotly_chart(fig_stock, use_container_width=True)

        # --- 섹션 3: 데이터 테이블 ---
        with st.expander("데이터 상세 보기"):
            st.table(df_gm.sort_values(by="Date", ascending=False))
    else:
        st.warning("Good Molecules 데이터를 찾을 수 없습니다.")
else:
    st.error("csv 파일이 없습니다. main.py를 먼저 실행해 주세요.")
