import requests
import datetime
import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
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

TARGET_TIMES = [
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


def send_email(date, start, price, link):

    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]

    subject = "🎾 Padel court vrij!"

    html = f"""
    <html>
    <body style="font-family: Arial">

    <h2>🎾 Padel court vrij!</h2>

    <p><b>Datum:</b> {date}</p>
    <p><b>Tijd:</b> {start}</p>
    <p><b>Prijs:</b> {price}</p>

    <p>
    <a href="{link}" 
       style="background:#28a745;color:white;padding:12px 18px;
       text-decoration:none;border-radius:6px;">
       Boek nu op Playtomic
    </a>
    </p>

    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender

    msg.attach(MIMEText(html, "html"))

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

    for slot in court.get("slots", []):

        start = slot.get("start_time")
        duration = slot.get("duration")
        price = slot.get("price")

        if not price:
            continue

        if start not in TARGET_TIMES:
            continue

        if duration != 90:
            continue

        slot_id = f"{target_date}_{start}_{court['resource_id']}"

        if slot_id in seen_slots:
            continue

        booking_link = f"https://playtomic.com/en/book/club/{tenant_id}?date={target_date}"

        print("Court gevonden:", start)

        send_email(target_date, start, price, booking_link)

        seen_slots.add(slot_id)

save_seen(seen_slots)
