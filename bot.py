import os
import requests
from bs4 import BeautifulSoup
import re

# URLs van de zoekpagina's
URLS = [
    "https://torreshike.com/en/search?from=2026-01-12&to=2026-01-20&currency=USD&persons=2&tab_id=custom&itinerary=%5B%5B5%5D%5D",
    "https://torreshike.com/en/search?from=2026-01-12&to=2026-01-20&currency=USD&persons=2&tab_id=custom&itinerary=%5B%5B4%5D%5D"
]

TARGET_PRICE = 700
TARGET_DATE = "February 14"

# Haal secrets uit GitHub Actions
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

def check_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}  # voorkomt blokkades door website
    r = requests.get(url, timeout=20, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Alle tekst uit de pagina
    all_text = soup.get_text(" ", strip=True)

    # Vind alle prijzen in USD
    prices = re.findall(r"\$?(\d+)\s?USD", all_text)

    for p in prices:
        p = float(p)
        if p <= TARGET_PRICE:
            # Check ook of de target datum ergens staat
            if TARGET_DATE in all_text:
                return p, url

    return None

def main():
    for url in URLS:
        result = check_price(url)
        if result:
            price, link = result
            send_telegram(f"🔥 TORRES ALERT!\nPrijs: {price} USD\nURL: {link}")

if __name__ == "__main__":
    main()
