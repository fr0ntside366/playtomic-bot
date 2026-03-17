import requests
import datetime

tenant_id = "2b0af113-70a9-4ad2-a54c-b0bcf20f596b"

url = "https://playtomic.com/api/clubs/availability"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Origin": "https://playtomic.com",
    "Referer": "https://playtomic.com/"
}

today = datetime.date.today()

for i in range(7):

    date = (today + datetime.timedelta(days=i)).isoformat()

    params = {
        "tenant_id": tenant_id,
        "date": date,
        "sport_id": "PADEL"
    }

    response = requests.get(url, params=params, headers=headers)

    print("Checking date:", date)
    print("Status:", response.status_code)

    data = response.json()

    courts_found = False

    for court in data:
        for slot in court.get("slots", []):

            start = slot.get("start_time")

            if slot.get("available") and start >= "18:00" and start <= "22:00":
                courts_found = True
                print("⚠ Court vrij:", date, court.get("name"), start)

    if not courts_found:
        print("Geen vrije courts gevonden op", date)

    print("-------------")
