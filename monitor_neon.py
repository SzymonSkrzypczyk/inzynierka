import os
import requests
import sys
from datetime import datetime, timedelta

API_KEY = os.getenv("NEON_API_KEY")
PROJECT_ID = os.getenv("NEON_PROJECT_ID")

# Free Tier Limits
LIMIT_CU_HOURS = 100
LIMIT_STORAGE_GB = 0.5

def get_neon_usage():
    start_date = (datetime.now() - timedelta(days=30)).isoformat() + "Z"
    
    url = f"https://console.neon.tech/api/v2/consumption_history/projects"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {API_KEY}"
    }
    params = {
        "project_id": PROJECT_ID,
        "from": start_date,
        "metrics": "compute_time_seconds,synthetic_storage_size_bytes"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def analyze_usage(data):
    # 1 CU-hour = 3600 seconds at 1 CU
    total_seconds = sum(item['compute_time_seconds'] for item in data['usage'])
    cu_hours_used = total_seconds / 3600
    
    # Get latest storage size (bytes to GB)
    latest_storage_bytes = data['usage'][-1]['synthetic_storage_size_bytes'] if data['usage'] else 0
    storage_gb_used = latest_storage_bytes / (1024**3)

    print(f"--- Neon Resource Report ({datetime.now().date()}) ---")
    print(f"Compute: {cu_hours_used:.2f} / {LIMIT_CU_HOURS} CU-hours")
    print(f"Storage: {storage_gb_used:.4f} / {LIMIT_STORAGE_GB} GB")

    if cu_hours_used > (LIMIT_CU_HOURS * 0.8):
        print("⚠️ WARNING: Compute usage exceeds 80%!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        usage_data = get_neon_usage()
        analyze_usage(usage_data)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)