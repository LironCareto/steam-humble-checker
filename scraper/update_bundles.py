# scraper/update_bundles.py

import requests
from bs4 import BeautifulSoup
import json
import os
import unicodedata
from datetime import datetime
import re

APPWS_URL = "https://appsolutelywonderful.com/humblechoice"
HUMBLE_URL = "https://www.humblebundle.com/membership"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "humble_bundles.json")
HEADERS = {"User-Agent": "Mozilla/5.0"}

print("🔍 Scraping Humble Choice bundles from AppsolutelyWonderful and Humble.com...")

# Load existing data if available
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        bundle_data = json.load(f)
else:
    bundle_data = {}

found = 0

# --- Extract historical data from AppsolutelyWonderful ---
try:
    response = requests.get(APPWS_URL, headers=HEADERS, timeout=10)
    response.encoding = response.apparent_encoding
    if response.status_code != 200:
        raise Exception(f"Failed to load source page: status {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    headers = soup.find_all("h2")

    for header in headers:
        raw_name = header.text.strip()
        ul = header.find_next("ul")
        if not ul:
            continue

        games = []
        for li in ul.find_all("li"):
            text = li.get_text(strip=True)
            text = unicodedata.normalize("NFKC", text)
            text = text.replace("\uFFFD", "").replace("™", "").replace("®", "").strip()
            steam_tag = li.find("a", href=True)
            steam_url = steam_tag["href"] if steam_tag else None
            if text:
                games.append({"title": text, "humble_url": steam_url})

        if games:
            try:
                normalized_date = datetime.strptime(raw_name, "%B %Y").strftime("%Y-%m")
                bundle_key = normalized_date
                bundle_type = "monthly"
            except ValueError:
                bundle_key = raw_name
                bundle_type = "special"

            bundle_data[bundle_key] = {
                "type": bundle_type,
                "games": games
            }
            found += 1

except Exception as e:
    print(f"❌ Error scraping historical bundles: {e}")

# --- Attempt to get current month's bundle from Humble ---
try:
    from datetime import UTC
    now = datetime.now(UTC)
    current_key = now.strftime("%Y-%m")

    if current_key not in bundle_data:
        print(f"🌐 Attempting to extract current bundle from Humble.com ({current_key})...")
        r = requests.get(HUMBLE_URL, headers=HEADERS, timeout=10)
        r.encoding = r.apparent_encoding
        match = re.search(r"window\.__REACT_QUERY_STATE__\s*=\s*({.*?})\s*;</script>", r.text, re.DOTALL)

        if match:
            react_state = json.loads(match.group(1))
            entries = [v for k, v in react_state.items() if "subscription_products" in k]
            if entries:
                products = entries[0].get("state", {}).get("data", {}).get("content_items", [])
                if products:
                    games = []
                    for item in products:
                        title = item.get("title", "").strip()
                        slug = item.get("url", "")
                        url = f"https://www.humblebundle.com{subslug}" if (subslug := slug) else None
                        if title:
                            games.append({"title": title, "humble_url": url})

                    if games:
                        bundle_data[current_key] = {
                            "type": "monthly",
                            "games": games
                        }
                        print(f"✅ Added current bundle: {current_key} ({len(games)} games)")
                        found += 1

except Exception as e:
    print(f"⚠️ Could not fetch current bundle from Humble.com: {e}")

print(f"✅ Extracted {found} bundles")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(bundle_data, f, indent=2, ensure_ascii=False)

print(f"📄 Saved to {OUTPUT_FILE}")
