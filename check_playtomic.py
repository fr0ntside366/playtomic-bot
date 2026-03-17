import requests
import datetime

tenant_id = "2b0af113-70a9-4ad2-a54c-b0bcf20f596b"

date = datetime.date.today().isoformat()

url = "https://playtomic.com/api/clubs/availability"

params = {
    "tenant_id": tenant_id,
    "date": date,
    "sport_id": "PADEL"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Origin": "https://playtomic.com",
    "Referer": "https://playtomic.com/"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()

for court in data:
    for slot in court.get("slots", []):

        start = slot.get("start_time")

        if slot.get("available") and start >= "19:00" and start <= "22:00":
            print("⚠ Court vrij:", court.get("name"), start)
