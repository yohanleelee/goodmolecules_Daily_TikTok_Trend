import requests
import pandas as pd
from datetime import datetime
import time
import os

# 설정 정보
API_TOKEN = "apify_api_C2b8c0NEP4XXOVzqF7KTnaY7OMXYx926RYYD"
ACTOR_ID = "GdWCkxBtKWOsKjdch" 

def run_and_get_report(keyword="goodmolecules"):
    print(f"🚀 [{keyword}] 틱톡 데이터 수집 및 분석 시작...")
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}"
    
    payload = {
        "searchQueries": [keyword],
        "resultsPerPage": 50,           
        "searchType": "video",
        "searchDateFilter": "past-24h",
        "searchSort": "latest"
    }
    
    # API 호출 (Run)
    response = requests.post(run_url, json=payload)
    run_res = response.json()
    
    # Apify 응답 구조 수정 (KeyError 방지)
    dataset_id = run_res.get("defaultDatasetId") or run_res.get("data", {}).get("defaultDatasetId")
    
    if not dataset_id:
        print(f"❌ API 응답 실패: {run_res}")
        return None
    
    print(f"⏳ 데이터 추출 중... (ID: {dataset_id})")
    time.sleep(60) # 데이터 양에 따라 충분히 대기
    
    # 데이터셋 결과 가져오기
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}"
    items = requests.get(items_url).json()
    
    if not items or len(items) == 0:
        print("⚠️ 수집된 새로운 영상 데이터가 없습니다.")
        return None

    df = pd.DataFrame(items)
    
    # 지표 계산
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
    }
    
    # 마스터 CSV 저장 (중복 방지)
    file_name = "tiktok_trends_master.csv"
    df_new = pd.DataFrame([report_data])
    
    if not os.path.exists(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df_old = pd.read_csv(file_name)
        # 중복 체크 (날짜와 키워드 기준)
        if not ((df_old["Date"] == report_data["Date"]) & (df_old["Keyword"] == keyword)).any():
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.to_csv(file_name, index=False, encoding='utf-8-sig')
            
    print(f"✅ 분석 완료: {keyword} (Score: {report_data['Score']})")
    return report_data

if __name__ == "__main__":
    run_and_get_report("goodmolecules")
