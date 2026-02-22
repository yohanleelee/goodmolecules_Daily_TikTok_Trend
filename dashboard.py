import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# 페이지 설정
st.set_page_config(page_title="GM Viral vs Stock Analysis", layout="wide")

st.title("📊 Good Molecules 틱톡 바이럴 & 제조사 주가 분석")
st.markdown("틱톡 바이럴 점수(Bar)와 주요 제조사 주가(Line)의 등락 방향성을 비교합니다.")

file_path = "tiktok_trends_master.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    # Good Molecules 데이터 필터링
    df_gm = df[df["Keyword"] == "goodmolecules"].sort_values(by="Date")

    if not df_gm.empty:
        # --- 섹션 1: 4대 핵심 지표 (바 그래프) ---
        st.subheader("📱 틱톡 개별 지표현황")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.plotly_chart(px.bar(df_gm, x="Date", y="Avg_Views", title="조회수", color_discrete_sequence=['#3498DB']), use_container_width=True)
        with col2:
            st.plotly_chart(px.bar(df_gm, x="Date", y="Avg_Likes", title="좋아요", color_discrete_sequence=['#E74C3C']), use_container_width=True)
        with col3:
            st.plotly_chart(px.bar(df_gm, x="Date", y="Avg_Comments", title="댓글", color_discrete_sequence=['#2ECC71']), use_container_width=True)
        with col4:
            st.plotly_chart(px.bar(df_gm, x="Date", y="Avg_Shares", title="공유", color_discrete_sequence=['#9B59B6']), use_container_width=True)

        st.divider()

        # --- 섹션 2: 바-선 복합 상관관계 차트 ---
        st.subheader("📈 바이럴 점수(Bar) vs 주가 추이(Line) 비교")
        
        # 복합 차트 생성 (이중 축)
        fig_master = make_subplots(specs=[[{"secondary_y": True}]])

        # 1. 틱톡 바이럴 점수 (연한 회색 바 그래프)
        fig_master.add_trace(
            go.Bar(
                x=df_gm["Date"], 
                y=df_gm["Score"], 
                name="틱톡 바이럴 점수",
                marker_color='rgba(200, 200, 200, 0.5)', # 연한 회색
                offsetgroup=1
            ),
            secondary_y=False,
        )

        # 2. 잉글우드랩 주가 추이 (진한 파란색 선 그래프)
        # *실제 데이터 파일에 주가 컬럼이 없다면 시각화를 위해 가상 흐름을 생성합니다. 
        # 실제 주가 컬럼이 있다면 df_gm["Stock_Englewood"] 등으로 변경하세요.
        fig_master.add_trace(
            go.Scatter(
                x=df_gm["Date"], 
                y=[16000 + (i*150) for i in range(len(df_gm))], # 가상 주가 데이터 예시
                name="잉글우드랩 주가",
                line=dict(color="#2980B9", width=4), # 진한 파란색
                mode='lines+markers'
            ),
            secondary_y=True,
        )

        # 3. 코스메카코리아 주가 추이 (진한 주황색 선 그래프)
        fig_master.add_trace(
            go.Scatter(
                x=df_gm["Date"], 
                y=[75000 + (i*450) for i in range(len(df_gm))], # 가상 주가 데이터 예시
                name="코스메카코리아 주가",
                line=dict(color="#E67E22", width=4), # 진한 주황색
                mode='lines+markers'
            ),
            secondary_y=True,
        )

        # 레이아웃 설정
        fig_master.update_layout(
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="white",
            height=600
        )

        fig_master.update_yaxes(title_text="<b>Viral Score (Bar)</b>", secondary_y=False, showgrid=False)
        fig_master.update_yaxes(title_text="<b>Stock Price (Line)</b>", secondary_y=True, showgrid=True, gridcolor='lightgray')

        st.plotly_chart(fig_master, use_container_width=True)

        # --- 섹션 3: 데이터 기록 상세 ---
        with st.expander("📝 상세 데이터 보기"):
            st.dataframe(df_gm.sort_values(by="Date", ascending=False), use_container_width=True)

    else:
        st.info("데이터 파일에 'goodmolecules' 관련 기록이 아직 없습니다.")
else:
    st.error("CSV 파일이 없습니다. 먼저 main.py를 실행하여 데이터를 수집하세요.")
