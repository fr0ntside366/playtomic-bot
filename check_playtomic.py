import requests
import datetime

club_id = 1  # tijdelijk test-id
date = datetime.date.today().isoformat()

url = "https://api.playtomic.io/v1/availability"

params = {
    "date": date,
    "sport_id": 2
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

try:
    r = requests.get(url, params=params, headers=headers)

    print("Status:", r.status_code)

    if "application/json" in r.headers.get("Content-Type",""):
        print("JSON data gevonden")
        print(r.text[:800])
    else:
        print("Geen JSON ontvangen")

except Exception as e:
    print("Error:", e)
