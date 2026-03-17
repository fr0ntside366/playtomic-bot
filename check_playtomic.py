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

ALLOWED_TIMES = [
    "19:00:00",
    "19:30:00",
    "20:00:00",
    "20:30:00"
]


def load_seen():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(list(seen), f)


def send_email(subject, html):

    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]

    msg = MIMEText(html, "html")

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, sender, msg.as_string())


seen_slots = load_seen()

today = datetime.date.today()

target_date = (today + datetime.timedelta(days=7)).isoformat()

params = {
    "tenant_id": tenant_id,
    "date": target_date,
    "sport_id": "PADEL"
}

response = requests.get(url, params=params, headers=headers)

print("Checking:", target_date)

data = response.json()

for court in data:

    court_id = court.get("resource_id")
    court_name = court.get("name", "Onbekend veld")

    for slot in court.get("slots", []):

        start = slot.get("start_time")
        price = slot.get("price")
        duration = slot.get("duration")
        slot_uuid = slot.get("uuid")

        if not price:
            continue

        if duration != 90:
            continue

        if start not in ALLOWED_TIMES:
            continue

        slot_id = f"{target_date}_{start}_{court_id}"

        if slot_id in seen_slots:
            continue

        # DIRECTE BOOKING LINK
        booking_link = f"https://playtomic.com/en/book/club/{tenant_id}/slot/{slot_uuid}"

        html = f"""
        <h2>🎾 Padel court vrij!</h2>

        <b>Court:</b> {court_name}<br>
        <b>Datum:</b> {target_date}<br>
        <b>Tijd:</b> {start}<br>
        <b>Duur:</b> 90 minuten<br>
        <b>Prijs:</b> {price}<br><br>

        <a href="{booking_link}" 
        style="
        background:#28a745;
        padding:14px 22px;
        color:white;
        text-decoration:none;
        border-radius:6px;
        font-size:16px;
        ">
        👉 Direct boeken
        </a>
        """

        print("Court gevonden:", court_name, start)

        send_email(
            "🎾 Padel court beschikbaar!",
            html
        )

        seen_slots.add(slot_id)

save_seen(seen_slots)
