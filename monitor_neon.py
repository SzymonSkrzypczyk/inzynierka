import os
import requests
import sys
from datetime import datetime, timedelta

API_KEY = os.getenv("NEON_API_KEY")
PROJECT_ID = os.getenv("NEON_PROJECT_ID")
THRESHOLD = 0.8
LIMIT_CU = 100
LIMIT_STORAGE = 0.5


def check_resources():
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    url = "https://console.neon.tech/api/v2/consumption_history/projects"
    headers = {
        "authorization": f"Bearer {API_KEY}",
        "accept": "application/json"
    }
    params = {
        "project_id": PROJECT_ID, 
        "from": start_date,
        "metrics": "compute_time_seconds,synthetic_storage_size_bytes"
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"API Error {response.status_code}: {response.text}")
        sys.exit(1)

    data = response.json()
    usage = data.get('usage', [])
    
    current_cu = sum(item.get('compute_time_seconds', 0) for item in usage) / 3600

    current_storage = (usage[-1].get('synthetic_storage_size_bytes', 0) / (1024**3)) if usage else 0
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"cu_used={current_cu:.2f}\n")
            f.write(f"storage_used={current_storage:.4f}\n")

    print(f"Usage: {current_cu:.2f} CU-h / {current_storage:.4f} GB")

    if current_cu > (LIMIT_CU * THRESHOLD) or current_storage > (LIMIT_STORAGE * THRESHOLD):
        print("CRITICAL: Resource threshold exceeded.")
        sys.exit(1)


if __name__ == "__main__":
    check_resources()
