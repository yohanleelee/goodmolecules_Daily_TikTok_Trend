import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Good Molecules 상세 분석", layout="wide")
st.title("📊 Good Molecules 틱톡 세부 지표 분석")

try:
    df = pd.read_csv("tiktok_trends_master.csv")
    df['Date'] = pd.to_datetime(df['Date'])

    # --- 상단 주요 지표 (Metrics) ---
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("종합 점수", f"{last_row['Score']:,}", f"{round(last_row['Score'] - prev_row['Score'], 2)}")
    col2.metric("평균 조회수", f"{int(last_row['Avg_Views']):,}")
    col3.metric("평균 댓글수", f"{int(last_row.get('Avg_Comments', 0)):,}")
    col4.metric("신규 영상수", f"{last_row['New_Clips']}개")

    st.divider()

    # --- 그래프 영역 (2x2 배치) ---
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    with row1_col1:
        st.subheader("🔥 종합 화력 지수 (Score)")
        fig1 = px.line(df, x='Date', y='Score', markers=True, color_discrete_sequence=['#FF4B4B'])
        st.plotly_chart(fig1, use_container_width=True)

    with row1_col2:
        st.subheader("👁️ 평균 조회수 추이")
        fig2 = px.area(df, x='Date', y='Avg_Views', markers=True, color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig2, use_container_width=True)

    with row2_col1:
        st.subheader("💬 평균 댓글수 추이")
        # 컬럼이 없을 경우를 대비해 get() 사용
        y_col = 'Avg_Comments' if 'Avg_Comments' in df.columns else 'Score'
        fig3 = px.bar(df, x='Date', y=y_col, color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig3, use_container_width=True)

    with row2_col2:
        st.subheader("📅 신규 업로드 영상 수")
        fig4 = px.line(df, x='Date', y='New_Clips', markers=True, line_dash_sequence=['dot'])
        st.plotly_chart(fig4, use_container_width=True)

except Exception as e:
    st.warning("데이터를 불러오는 중입니다. 첫 수집이 완료될 때까지 기다려주세요!")
    st.info(f"상세 에러: {e}")
