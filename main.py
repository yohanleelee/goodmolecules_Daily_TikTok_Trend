import requests
import pandas as pd
from datetime import datetime
import time
import os

# [주의] API_TOKEN은 가급적 환경변수를 사용하거나 노출에 주의하세요.
API_TOKEN = "apify_api_C2b8c0NEP4XXOVzqF7KTnaY7OMXYx926RYYD"
ACTOR_ID = "GdWCkxBtKWOsKjdch" 

def run_and_get_report(keyword):
    print(f"🚀 [{keyword}] 틱톡 트렌드 데이터 수집 시작...")
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={API_TOKEN}"
    
    payload = {
        "searchQueries": [keyword],
        "resultsPerPage": 50,           
        "searchType": "video",
        "searchDateFilter": "past-24h",
        "searchSort": "latest"
    }
    
    # 1. Actor 실행
    response = requests.post(run_url, json=payload)
    run_res = response.json()
    
    # 에러 체크: 'data' 키가 없는 Apify v2 응답 구조 대응
    dataset_id = run_res.get("defaultDatasetId") or run_res.get("data", {}).get("defaultDatasetId")
    
    if not dataset_id:
        print(f"❌ API 호출 실패: {run_res}")
        return None
    
    print(f"⏳ 데이터 추출 중... (Dataset ID: {dataset_id})")
    time.sleep(60) # 틱톡 스크래핑은 시간이 걸리므로 60초 대기
    
    # 2. 결과 데이터 가져오기
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={API_TOKEN}"
    items_response = requests.get(items_url)
    items = items_response.json()
    
    if not items or len(items) == 0:
        print(f"⚠️ [{keyword}] 수집된 데이터가 없습니다.")
        return None

    df = pd.DataFrame(items)
    
    # 3. 지표 계산 (컬럼 존재 여부 확인)
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
    
    # 4. CSV 저장
    file_name = "tiktok_trends_master.csv"
    df_new = pd.DataFrame([report_data])
    
    if not os.path.exists(file_name):
        df_new.to_csv(file_name, index=False, encoding='utf-8-sig')
    else:
        df_old = pd.read_csv(file_name)
        # 같은 날짜, 같은 키워드 데이터 중복 방지
        condition = (df_old["Date"] == report_data["Date"]) & (df_old["Keyword"] == report_data["Keyword"])
        if not condition.any():
            df_combined = pd.concat([df_old, df_new], ignore_index=True)
            df_combined.to_csv(file_name, index=False, encoding='utf-8-sig')
            
    print(f"✅ [{keyword}] 분석 완료! Score: {report_data['Score']}")
    return report_data

if __name__ == "__main__":
    # 분석할 키워드 리스트
    keywords = ["goodmolecules", "aromatica"]
    for kw in keywords:
        run_and_get_report(kw)
