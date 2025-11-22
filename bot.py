import requests
from bs4 import BeautifulSoup

URLS = [
    httpstorreshike.comensearchfrom=2026-01-12&to=2026-01-20&currency=USD&persons=2&tab_id=custom&itinerary=%5B%5B5%5D%5D,
    httpstorreshike.comensearchfrom=2026-01-12&to=2026-01-20&currency=USD&persons=2&tab_id=custom&itinerary=%5B%5B4%5D%5D
]

TARGET_PRICE = 200
TARGET_DATE = February 14

TELEGRAM_BOT_TOKEN = "8577775344:AAGAIEcrMhB1zbDNskBcprtwR5AEiVhoQ78"
TELEGRAM_CHAT_ID = "8208296891"

def send_telegram(message)
    url = fhttpsapi.telegram.orgbot{TELEGRAM_BOT_TOKEN}sendMessage
    payload = {chat_id TELEGRAM_CHAT_ID, text message}
    requests.post(url, data=payload)

def check_price(url)
    r = requests.get(url, timeout=20)
    soup = BeautifulSoup(r.text, html.parser)

    # Zoek alles wat tekst bevat
    all_text = soup.get_text( , strip=True)

    # Vind prijzen (ruw, maar werkt voor de meeste sites)
    import re
    prices = re.findall(r$(d+)sUSD, all_text)

    for p in prices
        p = float(p)
        if p = TARGET_PRICE
            # Check ook of 14 feb ergens staat
            if 14 in all_text or Feb in all_text or February in all_text
                return p, url

    return None

def main()
    for url in URLS
        result = check_price(url)
        if result
            price, link = result
            send_telegram(f🔥 TORRES ALERT!nPrijs {price} USDnURL {link})

if __name__ == __main__
    main()
