# scraper/update_bundles.py

import requests
from bs4 import BeautifulSoup
import json

SOURCE_URL = "https://appsolutelywonderful.com/humblechoice"
OUTPUT_FILE = "../humble_bundles.json"
HEADERS = {"User-Agent": "Mozilla/5.0"}

print("🔍 Scraping Humble Choice bundles from AppsolutelyWonderful...")

bundle_data = {}
found = 0

try:
    response = requests.get(SOURCE_URL, headers=HEADERS, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to load source page: status {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    headers = soup.find_all("h2")

    for header in headers:
        bundle_name = header.text.strip()
        ul = header.find_next("ul")
        if not ul:
            continue

        games = []
        for li in ul.find_all("li"):
            text = li.get_text(strip=True)
            steam_tag = li.find("a", href=True)
            steam_url = steam_tag["href"] if steam_tag else None
            if text:
                games.append({"title": text, "steam_url": steam_url})

        if games:
            bundle_data[bundle_name] = games
            found += 1

except Exception as e:
    print(f"❌ Error scraping source: {e}")

print(f"✅ Extracted {found} bundles")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(bundle_data, f, indent=2, ensure_ascii=False)

print(f"📄 Saved to {OUTPUT_FILE}")