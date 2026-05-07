import os
import requests
from datetime import datetime, timezone


def log_call_to_airtable(phone: str, duration: int, transcript: str) -> bool:
    api_key = os.environ["AIRTABLE_API_KEY"]
    base_id = os.environ["AIRTABLE_BASE_ID"]
    table_name = os.environ["AIRTABLE_TABLE_NAME"]

    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "fields": {
            "Phone": phone,
            "Duration": duration,
            "Transcript": transcript,
            "Timestamp": datetime.now(timezone.utc).isoformat(),
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return True

    print(f"[Airtable] Error {response.status_code}: {response.text}")
    return False
