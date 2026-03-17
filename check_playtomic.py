import requests
import datetime
import smtplib
import os
import json
from email.mime.text import MIMEText

tenant_id = "2b0af113-70a9-4ad2-a54c-b0bcf20f596b"

url = "https://playtomic.com/api/clubs/availability"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Origin": "https://playtomic.com",
    "Referer": "https://playtomic.com/"
}

STATE_FILE = "seen_slots.json"


def load_seen():

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f))

    return set()


def save_seen(seen):

    with open(STATE_FILE, "w") as f:
        json.dump(list(seen), f)


def send_email(msg):

    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]

    message = MIMEText(msg)

    message["Subject"] = "⚠ Padel court vrij!"
    message["From"] = sender
    message["To"] = sender

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, sender, message.as_string())


seen_slots = load_seen()

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

    data = response.json()

    for court in data:

        for slot in court.get("slots", []):

            start = slot.get("start_time")
            price = slot.get("price")

            if not price:
                continue

            hour = int(start.split(":")[0])

            if hour < 18 or hour > 22:
                continue

            slot_id = f"{date}_{start}_{court['resource_id']}"

            if slot_id not in seen_slots:

                msg = f"""
Padel court vrij!

Datum: {date}
Tijd: {start}
Prijs: {price}
"""

                print(msg)

                send_email(msg)

                seen_slots.add(slot_id)

save_seen(seen_slots)
