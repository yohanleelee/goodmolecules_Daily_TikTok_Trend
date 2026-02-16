import requests
import pandas as pd
from datetime import datetime
import time
import os

# 설정 정보
API_TOKEN = "apify_api_C2b8c0NEP4XXOVzqF7KTnaY7OMXYx926RYYD"
ACTOR_ID = "GdWCkxBtKWOsKjdch" 

def run_and_get_report(keyword):
    print(f"🚀 [{keyword}] 투자 분석 데이터 수집 시작...")
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}"
    
    payload = {
        "searchQueries": [keyword],
        "resultsPerPage": 50,           
        "searchType": "video",
        "searchDateFilter": "past-24h",
        "searchSort": "latest"
    }
    
    response = requests.post(run_url, json=payload)
    run_res = response.json()
    dataset_id = run_res["data"]["defaultDatasetId"]
    
    time.sleep(50) 
    
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}"
    items = requests.get(items_url).json()
    
    if not items: return None

    df = pd.DataFrame(items)
    
    # 지표 계산 (상위 50개 샘플 기반)
    plays = df['playCount'].mean() if 'playCount' in df.columns else 0
    likes = df['diggCount'].mean() if 'diggCount' in df.columns else 0
    comments = df['commentCount'].mean() if 'commentCount' in df.columns else 0
    shares = df['shareCount'].mean() if 'shareCount' in df.columns else 0

    report_data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Keyword": keyword,
        "Score": round((plays * 0.01) + (likes * 0.5) + (comments * 2), 2),
        "Avg_Views": int(plays),
        "Avg_Likes": int(likes),
        "Avg_Comments": int(comments),
        "Avg_Shares": int(shares)
        # New_Clips(신규 영상 수) 제외
    }
    
    file_name = "tiktok_trends_master.csv"
    df_new = pd.DataFrame([report_data])
    
    if not os.path.exists(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df_old = pd.read_csv(file_name)
        if str(report_data["Date"]) not in df_old["Date"].astype(str).values:
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.to_csv(file_name, index=False, encoding='utf-8-sig')
            
    return report_data

run_and_get_report("goodmolecules")
