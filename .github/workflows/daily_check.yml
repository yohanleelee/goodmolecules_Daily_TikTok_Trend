name: Daily TikTok Trend Check

on:
  schedule:
    - cron: '0 0 * * *' # 매일 한국 시간 오전 9시 (UTC 00:00)
  workflow_dispatch: # 수동 실행 버튼 활성화

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install requests pandas
      - name: Run script
        run: python main.py
      - name: Commit and Push changes
        run: |
          git config --global user.name 'github-actions'
          git config --global user.email 'github-actions@github.com'
          git add tiktok_trends_master.csv
          git commit -m "Add daily trend data" || exit 0
          git push
