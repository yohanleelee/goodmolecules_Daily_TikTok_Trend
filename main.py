import requests
import pandas as pd
from datetime import datetime
import time
import os

# 1. 설정 정보
API_TOKEN = "apify_api_C2b8c0NEP4XXOVzqF7KTnaY7OMXYx926RYYD"
ACTOR_ID = "GdWCkxBtKWOsKjdch" 

def run_and_get_report(keyword):
    print(f"🚀 [{keyword}] 상세 트렌드 분석 시작...")
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}"
    
    # 💡 충분한 데이터를 가져오기 위해 resultsPerPage를 100으로 설정
    payload = {
        "searchQueries": [keyword],
        "resultsPerPage": 100,           
        "searchType": "video",
        "searchDateFilter": "past-24h",
        "searchSort": "latest"
    }
    
    response = requests.post(run_url, json=payload)
    run_res = response.json()
    dataset_id = run_res["data"]["defaultDatasetId"]
    
    print(f"✅ 실행 성공! 정밀 분석을 위해 60초 대기 중...")
    time.sleep(60) 
    
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}"
    items = requests.get(items_url).json()
    
    if not items: 
        print(f"ℹ️ 지난 24시간 동안 신규 영상이 없습니다.")
        items = []

    df = pd.DataFrame(items)
    
    # --- 데이터 정밀 계산 로직 ---
    if not df.empty:
        # 1. 신규 영상 수: 검색된 전체 결과 개수 (최대 100개 내에서 실제 수치)
        total_new_clips = len(df)
        
        # 2. 상위 50개 추출: 지표 분석용 (데이터가 50개 미만이면 전체 사용)
        analysis_df = df.head(50)
        
        plays = analysis_df['playCount'].mean() if 'playCount' in analysis_df.columns else 0
        likes = analysis_df['diggCount'].mean() if 'diggCount' in analysis_df.columns else 0
        comments = analysis_df['commentCount'].mean() if 'commentCount' in analysis_df.columns else 0
        shares = analysis_df['shareCount'].mean() if 'shareCount' in analysis_df.columns else 0
    else:
        total_new_clips = plays = likes = comments = shares = 0

    report_data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Keyword": keyword,
        "Score": round((plays * 0.01) + (likes * 0.5) + (comments * 2), 2),
        "Avg_Views": int(plays),
        "Avg_Likes": int(likes),
        "Avg_Comments": int(comments),
        "Avg_Shares": int(shares),
        "New_Clips": total_new_clips  # 24시간 내 실제 발견된 모든 영상 수
    }
    
    # 💾 CSV 파일 저장 로직
    file_name = "tiktok_trends_master.csv"
    df_new = pd.DataFrame([report_data])
    
    if not os.path.exists(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df_old = pd.read_csv(file_name)
        if str(report_data["Date"]) not in df_old["Date"].astype(str).values:
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.to_csv(file_name, index=False, encoding='utf-8-sig')
            print(f"✅ {report_data['Date']} 데이터가 저장되었습니다. (전체 신규: {total_new_clips}개 / 분석: {len(analysis_df)}개)")
        else:
            print(f"ℹ️ {report_data['Date']} 데이터가 이미 존재합니다.")
            
    return report_data

# 실행
report = run_and_get_report("goodmolecules")
