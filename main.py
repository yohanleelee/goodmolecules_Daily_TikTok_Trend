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
    
    payload = {
        "searchQueries": [keyword],
        "resultsPerPage": 20,
        "searchType": "video",
        "searchDateFilter": "this-month",
        "searchSort": "latest"           
    }
    
    response = requests.post(run_url, json=payload)
    run_res = response.json()
    dataset_id = run_res["data"]["defaultDatasetId"]
    
    print(f"✅ 실행 성공! 50초 대기 중...")
    time.sleep(50) 
    
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}"
    items = requests.get(items_url).json()
    
    if not items: 
        print("❌ 수집된 데이터가 없습니다.")
        return None

    df = pd.DataFrame(items)
    
    # --- 데이터 계산 (세분화 지표 추가) ---
    plays = df['playCount'].mean() if 'playCount' in df.columns else 0
    likes = df['diggCount'].mean() if 'diggCount' in df.columns else 0
    comments = df['commentCount'].mean() if 'commentCount' in df.columns else 0 # 댓글수 추가
    shares = df['shareCount'].mean() if 'shareCount' in df.columns else 0     # 공유수 추가
    new_clips = len(df)

    report_data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Keyword": keyword,
        "Score": round((plays * 0.01) + (likes * 0.5) + (comments * 2), 2), # 댓글 가중치 추가
        "Avg_Views": int(plays),
        "Avg_Likes": int(likes),      # 추가된 지표
        "Avg_Comments": int(comments), # 추가된 지표
        "Avg_Shares": int(shares),     # 추가된 지표
        "New_Clips": new_clips
    }
    
    # 💾 CSV 파일에 누적 저장
    file_name = "tiktok_trends_master.csv"
    df_new = pd.DataFrame([report_data])
    
    if not os.path.exists(file_name):
        # 파일이 없으면 새로 생성 (헤더 포함)
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"✅ 새 파일 {file_name}이 생성되었습니다.")
    else:
        # 기존 파일 로드
        df_old = pd.read_csv(file_name)
        
        # 오늘 날짜 데이터 중복 체크
        if report_data["Date"] not in df_old["Date"].astype(str).values:
            # 기존 데이터에 새로운 열(컬럼)이 없을 경우를 대비해 합치는 방식 권장
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.to_csv(file_name, index=False, encoding='utf-8-sig')
            print(f"✅ {report_data['Date']} 세부 데이터가 추가되었습니다.")
        else:
            print(f"ℹ️ {report_data['Date']} 데이터가 이미 존재합니다.")
            
    return report_data

# 실행
report = run_and_get_report("goodmolecules")
