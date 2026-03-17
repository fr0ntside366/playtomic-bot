import requests

url = "https://playtomic.com/clubs/tc-ranst"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if "Book" in response.text:
    print("Er is mogelijk een court beschikbaar!")
else:
    print("Geen courts gevonden.")
