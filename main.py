import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os

# 설정 정보
API_TOKEN = "apify_api_C2b8c0NEP4XXOVzqF7KTnaY7OMXYx926RYYD"
ACTOR_ID = "GdWCkxBtKWOsKjdch" 

def run_and_get_report(keyword):
    print(f"🚀 [{keyword}] 정밀 데이터 수집 시작...")
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}"
    
    # 충분한 샘플 확보를 위해 100개 요청 (이 중 24시간 이내 것만 골라냄)
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
    
    print(f"✅ 실행 성공! 정밀 필터링을 위해 60초 대기...")
    time.sleep(60) 
    
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}"
    items = requests.get(items_url).json()
    
    if not items: 
        print("ℹ️ 수집된 데이터가 없습니다.")
        return None

    df = pd.DataFrame(items)
    
    # --- 24시간 이내 신규 영상 '진짜' 개수 계산 ---
    now_ts = time.time()
    one_day_ago_ts = now_ts - (24 * 60 * 60)
    
    # createTime(유닉스 타임스탬프) 기준 필터링
    if 'createTime' in df.columns:
        real_new_videos = df[df['createTime'] >= one_day_ago_ts]
        new_clips_count = len(real_new_videos)
    else:
        # 필드가 없을 경우 기존 방식 유지
        new_clips_count = len(df)

    # --- 지표 계산 (상위 50개 샘플 기반) ---
    analysis_df = df.head(50)
    plays = analysis_df['playCount'].mean() if 'playCount' in analysis_df.columns else 0
    likes = analysis_df['diggCount'].mean() if 'diggCount' in analysis_df.columns else 0
    comments = analysis_df['commentCount'].mean() if 'commentCount' in analysis_df.columns else 0
    shares = analysis_df['shareCount'].mean() if 'shareCount' in analysis_df.columns else 0

    report_data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Keyword": keyword,
        "Score": round((plays * 0.01) + (likes * 0.5) + (comments * 2), 2),
        "Avg_Views": int(plays),
        "Avg_Likes": int(likes),
        "Avg_Comments": int(comments),
        "Avg_Shares": int(shares),
        "New_Clips": new_clips_count  # 진짜 24시간 내 개수
    }
    
    # 💾 CSV 저장
    file_name = "tiktok_trends_master.csv"
    df_new = pd.DataFrame([report_data])
    
    if not os.path.exists(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df_old = pd.read_csv(file_name)
        if str(report_data["Date"]) not in df_old["Date"].astype(str).values:
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.to_csv(file_name, index=False, encoding='utf-8-sig')
            print(f"✅ {report_data['Date']} 데이터 업데이트 완료 (신규: {new_clips_count}개)")
        else:
            print(f"ℹ️ {report_data['Date']} 데이터가 이미 존재합니다.")
            
    return report_data

run_and_get_report("goodmolecules")
