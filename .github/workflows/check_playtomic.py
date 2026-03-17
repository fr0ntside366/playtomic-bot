import requests
from bs4 import BeautifulSoup

url = "https://playtomic.io"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

if "Book" in soup.text:
    print("Court mogelijk beschikbaar!")
else:
    print("Geen courts gevonden.")
