import requests
import pandas as pd
from datetime import datetime
import time
import os

# 1. 설정 정보
API_TOKEN = "apify_api_C2b8c0NEP4XXOVzqF7KTnaY7OMXYx926RYYD"
ACTOR_ID = "GdWCkxBtKWOsKjdch" 

def run_and_get_report(keyword):
    print(f"🚀 [{keyword}] 트렌드 데이터 수집 시작...")
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}"
    
    # 💡 추세 파악을 위해 최신순(latest) 필터 적용 권장
    payload = {
        "searchQueries": [keyword],
        "resultsPerPage": 20,
        "searchType": "video",
        "searchDateFilter": "this-month", # 이번 달 영상 위주로
        "searchSort": "latest"           # 최신순
    }
    
    response = requests.post(run_url, json=payload)
    run_res = response.json()
    dataset_id = run_res["data"]["defaultDatasetId"]
    
    print(f"✅ 실행 성공! 50초 대기 중...")
    time.sleep(50) 
    
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}"
    items = requests.get(items_url).json()
    
    if not items: return None

    df = pd.DataFrame(items)
    plays = df['playCount'].mean() if 'playCount' in df.columns else 0
    likes = df['diggCount'].mean() if 'diggCount' in df.columns else 0
    
    # 신규 영상 수 (데이터 개수)
    new_clips = len(df)

    report_data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Keyword": keyword,
        "Score": round((plays * 0.01) + (likes * 0.5), 2),
        "Avg_Views": int(plays),
        "New_Clips": new_clips
    }
    
    # 💾 CSV 파일에 누적 저장
    file_name = "tiktok_trends_master.csv"
    df_new = pd.DataFrame([report_data])
    
    if not os.path.exists(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        # 기존 파일 로드 후 오늘 날짜 데이터가 있는지 확인 (중복 방지)
        df_old = pd.read_csv(file_name)
        if report_data["Date"] not in df_old["Date"].values:
            df_new.to_csv(file_name, index=False, mode='a', header=False, encoding='utf-8-sig')
            print(f"✅ {report_data['Date']} 데이터가 추가되었습니다.")
        else:
            print(f"ℹ️ {report_data['Date']} 데이터가 이미 존재합니다.")
            
    return report_data

report = run_and_get_report("goodmolecules")
