import requests
import json

# 🔐 তোমার JWT টোকেন (Toffee থেকে নেওয়া)
JWT_TOKEN = "eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwczovL3RvZmZlZWxpdmUuY29tIiwiY291bnRyeSI6IkJEIiwiZF9pZCI6IjFhNGJiOTAzLWY5MjAtNDZmYS04ZTQyLTExNDVkOTYyMDg4YiIsImV4cCI6MTc2NDQ2MzYwOCwiaWF0IjoxNzYxODMzODA4LCJpc3MiOiJ0b2ZmZWVsaXZlLmNvbSIsImp0aSI6ImU3YTI5OThkLTM4YjctNGI5My05ZmMwLTQ5NzliYzM4MzYzNF8xNzYxODMzODA4IiwicHJvdmlkZXIiOiJ0b2ZmZWUiLCJyX2lkIjoiMWE0YmI5MDMtZjkyMC00NmZhLThlNDItMTE0NWQ5NjIwODhiIiwic19pZCI6IjFhNGJiOTAzLWY5MjAtNDZmYS04ZTQyLTExNDVkOTYyMDg4YiIsInRva2VuIjoiYWNjZXNzIiwidHlwZSI6ImRldmljZSJ9.YqGvOdawMelRRej_Cb9ZdvtaypgWkgaabXd8lGnrLbi0VKvwzw1csEr3CIYkyqeu-ARUVoYIR_Cr8F1cVN-b_w"

# 🔹 channels.json ফাইল থেকে ডেটা লোড করা
with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

# 🔸 প্রতিটি চ্যানেল চেক করা
for ch in channels:
    url = ch["api_url"]
    headers = {
        "Authorization": f"Bearer {JWT_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            playback_url = data.get("playback", {}).get("hls", "")
            if playback_url:
                print(f"✅ {ch['name']} → {playback_url}")
            else:
                print(f"⚠️ {ch['name']} – HLS link not found")
        except Exception as e:
            print(f"⚠️ {ch['name']} – Error parsing JSON: {e}")
    else:
        print(f"❌ {ch['name']} – HTTP Error {response.status_code}")
