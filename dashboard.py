import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="Good Molecules 트렌드", layout="wide")
st.title("🔥 Good Molecules 틱톡 인기도 실시간 추세")

# 데이터 불러오기
try:
    df = pd.read_csv("tiktok_trends_master.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # 1. 상단 요약 지표 (Metrics)
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row
    
    col1, col2, col3 = st.columns(3)
    col1.metric("오늘의 불꽃 점수", f"{last_row['Score']:,}", f"{last_row['Score'] - prev_row['Score']:.2f}")
    col2.metric("평균 조회수", f"{last_row['Avg_Views']:,}회")
    col3.metric("수집된 영상 수", f"{last_row['New_Clips']}개")

    # 2. 인기도 추세 그래프 (Plotly 사용)
    st.subheader("📈 날짜별 인기도(Score) 변화")
    fig = px.line(df, x='Date', y='Score', markers=True, 
                  title="Good Molecules Trend Score Over Time",
                  line_shape="spline", render_mode="svg")
    st.plotly_chart(fig, use_container_width=True)

    # 3. 상세 데이터 테이블
    with st.expander("전체 데이터 보기"):
        st.write(df)

except FileNotFoundError:
    st.warning("아직 데이터 파일(tiktok_trends_master.csv)이 없습니다. main.py를 먼저 실행해 주세요!")
