import requests

url = "https://playtomic.io/api/v1/availability"

params = {
    "sport_id": 2
}

try:
    r = requests.get(url, params=params)
    print("Status:", r.status_code)
    print("Response:", r.text[:500])
except Exception as e:
    print("Error:", e)
