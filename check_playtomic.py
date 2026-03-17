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
    "Accept": "application/json"
}

response = requests.get(url, params=params, headers=headers)

print("Status:", response.status_code)
print("Response:", response.text[:1000])
