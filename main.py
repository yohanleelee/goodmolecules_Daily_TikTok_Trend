import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Good Molecules x 잉글우드랩 정밀 분석", layout="wide")
st.title("🧪 브랜드 인기도 & 투자 선행 지표 정밀 대시보드")

try:
    # 데이터 로드
    df = pd.read_csv("tiktok_trends_master.csv")
    df['Date'] = pd.to_datetime(df['Date'])

    # 주요 계산 지표 추가
    df['Like_Ratio'] = (df['Avg_Likes'] / df['Avg_Views'] * 100).fillna(0)     # 조회수 대비 좋아요 비율
    df['Comment_Ratio'] = (df['Avg_Comments'] / df['Avg_Views'] * 100).fillna(0) # 조회수 대비 댓글 비율

    # 최신 데이터 추출
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row

    # --- 상단 핵심 지표 (Metrics) ---
    st.subheader("📍 오늘의 핵심 지표")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("종합 Score", f"{last_row['Score']:,}", f"{round(last_row['Score'] - prev_row['Score'], 2)}")
    m2.metric("신규 영상(24h)", f"{int(last_row['New_Clips'])}개", f"{int(last_row['New_Clips'] - prev_row['New_Clips'])}")
    m3.metric("평균 조회수", f"{int(last_row['Avg_Views']):,}")
    m4.metric("좋아요 참여율", f"{last_row['Like_Ratio']:.2f}%")
    m5.metric("댓글 참여율", f"{last_row['Comment_Ratio']:.2f}%")

    st.divider()

    # --- 그래프 섹션 1: 확산성 및 화력 (Score, 조회수, 신규 영상) ---
    st.subheader("🚀 1. 브랜드 확산 및 인지도 지표")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**종합 화력 (Score)**")
        fig1 = px.area(df, x='Date', y='Score', color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.write("**평균 조회수 추이**")
        fig2 = px.line(df, x='Date', y='Avg_Views', markers=True, color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.write("**신규 영상 업로드 수**")
        fig3 = px.bar(df, x='Date', y='New_Clips', color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig3, use_container_width=True)

    # --- 그래프 섹션 2: 참여 및 몰입 (댓글, 공유, 좋아요) ---
    st.subheader("💬 2. 소비자 몰입 및 참여 지표 (Engagement)")
    col4, col5, col6 = st.columns(3)

    with col4:
        st.write("**평균 댓글 수**")
        fig4 = px.line(df, x='Date', y='Avg_Comments', markers=True, color_discrete_sequence=['#AB63FA'])
        st.plotly_chart(fig4, use_container_width=True)

    with col5:
        st.write("**평균 공유 수**")
        fig5 = px.line(df, x='Date', y='Avg_Shares', markers=True, color_discrete_sequence=['#FFA15A'])
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.write("**평균 좋아요 수**")
        fig6 = px.bar(df, x='Date', y='Avg_Likes', color_discrete_sequence=['#EF553B'])
        st.plotly_chart(fig6, use_container_width=True)

    # --- 그래프 섹션 3: 효율성 분석 (참여 비율) ---
    st.subheader("📊 3. 콘텐츠 반응 효율 분석")
    col7, col8 = st.columns(2)

    with col7:
        st.write("**조회수 대비 댓글 비율 (%)**")
        fig7 = px.line(df, x='Date', y='Comment_Ratio', markers=True, color_discrete_sequence=['#19D3F3'])
        st.plotly_chart(fig7, use_container_width=True)

    with col8:
        st.write("**조회수 대비 좋아요 비율 (%)**")
        fig8 = px.line(df, x='Date', y='Like_Ratio', markers=True, color_discrete_sequence=['#FECB52'])
        st.plotly_chart(fig8, use_container_width=True)

except Exception as e:
    st.warning("데이터 파일(CSV)을 읽어오는 중입니다. 잠시만 기다려주세요!")
    st.error(f"Error: {e}")
