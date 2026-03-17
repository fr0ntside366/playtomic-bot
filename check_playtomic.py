import requests

url = "https://playtomic.io/api/v1/availability"

params = {
    "sport_id": 2
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, params=params, headers=headers)
    print("Status:", response.status_code)
    print("Data:", response.text[:800])

except Exception as e:
    print("Error:", e)
