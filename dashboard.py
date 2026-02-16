import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Good Molecules x 잉글우드랩 분석", layout="wide")
st.title("📈 브랜드 인기도 vs 잉글우드랩 주가 선행 분석")

try:
    df = pd.read_csv("tiktok_trends_master.csv")
    df['Date'] = pd.to_datetime(df['Date'])

    # 투자 분석용 비율 지표 계산
    df['Comment_Ratio'] = (df['Avg_Comments'] / df['Avg_Views'] * 100).fillna(0)
    df['Like_Ratio'] = (df['Avg_Likes'] / df['Avg_Views'] * 100).fillna(0)

    last_row = df.iloc[-1]
    
    # --- 상단 핵심 지표 ---
    st.info("💡 잉글우드랩(950140) 주가와 비교해 보세요. 트렌드 점수가 주가에 선행하는 경우가 많습니다.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("종합 화력(Score)", f"{last_row['Score']:,}")
    c2.metric("댓글 참여율", f"{last_row['Comment_Ratio']:.2f}%")
    c3.metric("평균 공유수", f"{int(last_row['Avg_Shares'])}회")
    c4.metric("평균 조회수", f"{int(last_row['Avg_Views']):,}")

    st.divider()

    # --- 주가 반영 확인용 그래프 섹션 ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📊 실구매 전환 선행 지표 (댓글/공유)")
        # 댓글과 공유는 단순 조회보다 실제 매출과 상관관계가 높습니다.
        fig_engagement = px.line(df, x='Date', y=['Avg_Comments', 'Avg_Shares'], 
                                 markers=True, title="관심도 밀도 추이")
        st.plotly_chart(fig_engagement, use_container_width=True)

    with col_right:
        st.subheader("🔥 종합 트렌드 점수 (Score)")
        # 종합 점수가 며칠 후 주가에 반영되는지 확인하는 용도입니다.
        fig_score = px.area(df, x='Date', y='Score', 
                            color_discrete_sequence=['#FF4B4B'], title="종합 브랜드 파워")
        st.plotly_chart(fig_score, use_container_width=True)

    # 참여율 분석 (몰입도)
    st.subheader("🎯 소비자 몰입도 분석 (조회수 대비 비율)")
    fig_ratios = px.line(df, x='Date', y=['Comment_Ratio', 'Like_Ratio'], 
                         markers=True, title="조회수 대비 좋아요 및 댓글 비율 (%)")
    st.plotly_chart(fig_ratios, use_container_width=True)

except Exception as e:
    st.warning("데이터가 쌓이기를 기다리고 있습니다.")
