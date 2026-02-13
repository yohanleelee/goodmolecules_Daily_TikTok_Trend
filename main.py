import requests
import pandas as pd
from datetime import datetime
import time
import os

# 1. 설정 정보
API_TOKEN = "apify_api_C2b8c0NEP4XXOVzqF7KTnaY7OMXYx926RYYD"
ACTOR_ID = "GdWCkxBtKWOsKjdch" 

def run_and_get_report(keyword):
    print(f"🚀 [{keyword}] 트렌드 데이터 수집 시작 (최신 24시간 기준)...")
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}"
    
    # 💡 신규 영상 수와 실시간 트렌드 반영을 위한 설정 변경
    # resultsPerPage를 50으로 늘려 더 넓은 범위를 체크합니다.
    payload = {
        "searchQueries": [keyword],
        "resultsPerPage": 50,           
        "searchType": "video",
        "searchDateFilter": "past-24h", # 최근 24시간 데이터만 타겟팅 (신규 업로드 확인용)
        "searchSort": "latest"          # 가장 최신 영상부터 수집
    }
    
    response = requests.post(run_url, json=payload)
    run_res = response.json()
    
    if "data" not in run_res:
        print(f"❌ 실행 실패: {run_res}")
        return None
        
    dataset_id = run_res["data"]["defaultDatasetId"]
    
    print(f"✅ 실행 성공! 데이터 수집 대기 중 (50초)...")
    time.sleep(50) 
    
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}"
    items = requests.get(items_url).json()
    
    if not items: 
        print(f"ℹ️ 지난 24시간 동안 [{keyword}] 관련 신규 영상이 없습니다.")
        # 데이터가 없을 경우 0으로 기록하여 트렌드 하락을 표시합니다.
        items = []

    df = pd.DataFrame(items)
    
    # --- 데이터 계산 (세분화 지표) ---
    if not df.empty:
        plays = df['playCount'].mean() if 'playCount' in df.columns else 0
        likes = df['diggCount'].mean() if 'diggCount' in df.columns else 0
        comments = df['commentCount'].mean() if 'commentCount' in df.columns else 0
        shares = df['shareCount'].mean() if 'shareCount' in df.columns else 0
        new_clips = len(df) # 50개 한도 내에서 실제 검색된 영상 수
    else:
        plays = likes = comments = shares = new_clips = 0

    report_data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Keyword": keyword,
        "Score": round((plays * 0.01) + (likes * 0.5) + (comments * 2), 2),
        "Avg_Views": int(plays),
        "Avg_Likes": int(likes),
        "Avg_Comments": int(comments),
        "Avg_Shares": int(shares),
        "New_Clips": new_clips
    }
    
    # 💾 CSV 파일에 누적 저장
    file_name = "tiktok_trends_master.csv"
    df_new = pd.DataFrame([report_data])
    
    if not os.path.exists(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"✅ 새 파일 {file_name} 생성 및 첫 데이터 저장 완료.")
    else:
        df_old = pd.read_csv(file_name)
        # 오늘 날짜 중복 체크 (문자열 변환 후 비교)
        if str(report_data["Date"]) not in df_old["Date"].astype(str).values:
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.to_csv(file_name, index=False, encoding='utf-8-sig')
            print(f"✅ {report_data['Date']} 트렌드 데이터가 업데이트되었습니다.")
        else:
            # 중복 데이터가 있을 경우 기존 행을 업데이트하거나 건너뜁니다.
            print(f"ℹ️ {report_data['Date']} 데이터가 이미 존재합니다. (업데이트 생략)")
            
    return report_data

# 실행
report = run_and_get_report("goodmolecules")
