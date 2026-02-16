import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Good Molecules 트렌드 분석기", layout="wide")
st.title("📊 브랜드 트렌드 vs 주가 선행 지표 대시보드")

try:
    df = pd.read_csv("tiktok_trends_master.csv")
    df['Date'] = pd.to_datetime(df['Date'])

    # 주요 지표 계산
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2] if len(df) > 1 else last_row
    
    # 댓글 참여율 (Comment-to-View Ratio)
    comment_ratio = (last_row['Avg_Comments'] / last_row['Avg_Views'] * 100) if last_row['Avg_Views'] > 0 else 0
    prev_ratio = (prev_row['Avg_Comments'] / prev_row['Avg_Views'] * 100) if prev_row['Avg_Views'] > 0 else 0

    # --- 상단 메트릭 ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("종합 화력 점수", f"{last_row['Score']:,}", f"{round(last_row['Score'] - prev_row['Score'], 2)}")
    col2.metric("실제 신규 영상 (24h)", f"{int(last_row['New_Clips'])}개", f"{int(last_row['New_Clips'] - prev_row['New_Clips'])}")
    col3.metric("댓글 참여율 (%)", f"{comment_ratio:.2f}%", f"{round(comment_ratio - prev_ratio, 2)}%")
    col4.metric("평균 댓글 수", f"{int(last_row['Avg_Comments']):,}")

    st.divider()

    # --- 분석 그래프 ---
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("💡 구매 의사 선행 지표 (댓글 참여율)")
        # 주가와 가장 상관관계가 높을 것으로 예상되는 지표
        df['Comment_Ratio'] = (df['Avg_Comments'] / df['Avg_Views'] * 100).fillna(0)
        fig1 = px.line(df, x='Date', y='Comment_Ratio', markers=True, color_discrete_sequence=['#AB63FA'])
        st.plotly_chart(fig1, use_container_width=True)

    with row1_col2:
        st.subheader("🚀 인지도 확산 지표 (신규 영상 수)")
        fig2 = px.bar(df, x='Date', y='New_Clips', color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig2, use_container_width=True)

    # 전체 추이 섹션
    st.subheader("📈 전체 점수(Score) 추이")
    fig3 = px.area(df, x='Date', y='Score', color_discrete_sequence=['#FF4B4B'])
    st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.info("데이터를 불러오는 중입니다. 첫 수집이 완료되면 대시보드가 활성화됩니다.")
