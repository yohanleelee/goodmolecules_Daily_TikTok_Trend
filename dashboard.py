import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Good Molecules x 잉글우드랩 분석", layout="wide")
st.title("🧪 브랜드 인기도 & 투자 선행 지표 정밀 대시보드")

try:
    # 데이터 로드
    df = pd.read_csv("tiktok_trends_master.csv")
    df['Date'] = pd.to_datetime(df['Date'])

    # 추가 비율 지표 계산
    df['Like_Ratio'] = (df['Avg_Likes'] / df['Avg_Views'] * 100).fillna(0)     # 조회수 대비 좋아요 비율
    df['Comment_Ratio'] = (df['Avg_Comments'] / df['Avg_Views'] * 100).fillna(0) # 조회수 대비 댓글 비율

    # 최신 데이터 추출
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row

    # --- 상단 핵심 지표 (Metrics) ---
    st.info("💡 잉글우드랩(950140) 주가와 비교 분석을 위한 실시간 지표입니다.")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("종합 Score", f"{last_row['Score']:,}", f"{round(last_row['Score'] - prev_row['Score'], 2)}")
    m2.metric("평균 조회수", f"{int(last_row['Avg_Views']):,}")
    m3.metric("평균 댓글수", f"{int(last_row['Avg_Comments']):,}")
    m4.metric("좋아요 비율", f"{last_row['Like_Ratio']:.2f}%")
    m5.metric("댓글 참여율", f"{last_row['Comment_Ratio']:.2f}%")

    st.divider()

    # --- 섹션 1: 브랜드 파워 및 확산 (Score & 조회수) ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔥 종합 브랜드 화력 (Score)")
        fig1 = px.area(df, x='Date', y='Score', color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.subheader("👁️ 평균 조회수 추이")
        fig2 = px.line(df, x='Date', y='Avg_Views', markers=True, color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig2, use_container_width=True)

    # --- 섹션 2: 소비자 참여 (댓글 & 공유 & 좋아요) ---
    st.subheader("💬 소비자 직접 반응 지표 (Engagement)")
    col3, col4, col5 = st.columns(3)
    with col3:
        st.write("**평균 댓글 수**")
        fig3 = px.line(df, x='Date', y='Avg_Comments', markers=True, color_discrete_sequence=['#AB63FA'])
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.write("**평균 공유 수**")
        fig4 = px.bar(df, x='Date', y='Avg_Shares', color_discrete_sequence=['#FFA15A'])
        st.plotly_chart(fig4, use_container_width=True)
    with col5:
        st.write("**평균 좋아요 수**")
        fig5 = px.line(df, x='Date', y='Avg_Likes', markers=True, color_discrete_sequence=['#EF553B'])
        st.plotly_chart(fig5, use_container_width=True)

    # --- 섹션 3: 효율성 분석 (참여 비율) ---
    st.subheader("📊 콘텐츠 몰입도 분석 (조회수 대비 비율)")
    col6, col7 = st.columns(2)
    with col6:
        st.write("**조회수 대비 댓글 비율 (%)**")
        fig6 = px.line(df, x='Date', y='Comment_Ratio', markers=True, color_discrete_sequence=['#19D3F3'])
        st.plotly_chart(fig6, use_container_width=True)
    with col7:
        st.write("**조회수 대비 좋아요 비율 (%)**")
        fig7 = px.line(df, x='Date', y='Like_Ratio', markers=True, color_discrete_sequence=['#FECB52'])
        st.plotly_chart(fig7, use_container_width=True)

except Exception as e:
    st.warning("데이터 수집 중입니다. 첫 번째 데이터가 저장되면 대시보드가 활성화됩니다.")
