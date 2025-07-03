import os
import requests
from dotenv import load_dotenv

# .env'i yükle (aynı klasörde ise otomatik bulur)
load_dotenv()

USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASS")
QB_URL = "http://qbittorrent:8080"  # Sabit

session = requests.Session()

print("➡️ Logging in to qBittorrent Web UI...")

login = session.post(f"{QB_URL}/api/v2/auth/login", data={"username": USERNAME, "password": PASSWORD})
if login.text != "Ok.":
    print("❌ Login failed!")
    exit()

print("✅ Logged in successfully.")

try:
    torrents = session.get(f"{QB_URL}/api/v2/torrents/info").json()
    print(f"📦 Fetched {len(torrents)} torrents from qBittorrent.")
except Exception as e:
    print("❌ Failed to fetch torrents:", str(e))
    exit()

stalled_count = 0

for torrent in torrents:
    if torrent["state"] == "stalledDL":
        print(f"🔁 Force rechecking: {torrent['name']}")
        session.post(f"{QB_URL}/api/v2/torrents/recheck", data={"hashes": torrent["hash"]})
        stalled_count += 1

if stalled_count == 0:
    print("ℹ️ No stalled downloads found.")
else:
    print(f"✅ Rechecked {stalled_count} stalled torrents.")
