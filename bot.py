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
    requests.post(url, data=payload)

def check_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, timeout=20, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # Zoek alle <div> elementen met de class van jouw target prijs
    # Vervang "some-class" door de class die je in Inspect hebt gezien
    divs = soup.find_all("div", class_= "mb-4 mx-0 p-4 search-result bg-white rounded border row")

    for div in divs:
        strong_tag = div.find("strong")
        if strong_tag:
            try:
                target_price = float(strong_tag.get_text(strip=True))
                # Als het onder TARGET_PRICE valt, stuur Telegram
                if target_price <= TARGET_PRICE:
                    return target_price, url
            except ValueError:
                continue  # negeer niet-numerieke inhoud


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
