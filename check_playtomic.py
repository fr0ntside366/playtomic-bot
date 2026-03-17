import requests
import datetime

tenant_id = "2b0af113-70a9-4ad2-a54c-b0bcf20f596b"
sport_id = 2

date = datetime.date.today().isoformat()

url = "https://api.playtomic.io/v1/availability"

params = {
    "tenant_id": tenant_id,
    "sport_id": sport_id,
    "date": date
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

r = requests.get(url, params=params, headers=headers)

print("Status:", r.status_code)
print("Response:", r.text[:1000])
