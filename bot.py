import os
import requests
from bs4 import BeautifulSoup
import re

# URLs van de zoekpagina's
URLS = [
    "https://torreshike.com/en/search?from=2026-01-14&to=2026-01-14&currency=USD&persons=2&tab_id=custom&itinerary=%5B%5B5%5D%5D",
    "https://torreshike.com/en/search?from=2026-01-14&to=2026-01-14&currency=USD&persons=2&tab_id=custom&itinerary=%5B%5B4%5D%5D"
]

TARGET_PRICE = 700
TARGET_DATE = "February 14"

# Haal secrets uit GitHub Actions
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    response = requests.post(url, data=payload)
    print("TELEGRAM RESPONSE:", response.text)


def check_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, timeout=20, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    print("DEBUG HTML:", r.text[:2000])

    # Selecteer alle strong tags binnen de knop
    strong_tags = soup.select("a.btn.btn-primary.btn-sm strong")

    for tag in strong_tags:
        text = tag.get_text(strip=True)
        # text is bv "540.00USD" → eerst de cijfers eruit halen
        match = re.search(r"\d+(\.\d+)?", text)
        if match:
            price = float(match.group())
            print("DEBUG gevonden prijs:", price)

            if price <= TARGET_PRICE:
                return price, url

    return None


def main():
    send_telegram("Testbericht: Telegram werkt!")
    
    for url in URLS:
        result = check_price(url)
        print("DEBUG result:", result)
        if result:
            price, link = result
            send_telegram(f"🔥 TORRES ALERT!\nPrijs: {price} USD\nURL: {link}")

if __name__ == "__main__":
    main()
