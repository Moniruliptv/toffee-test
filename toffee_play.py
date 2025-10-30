import os
import json
import requests

# =========================
# CONFIG
# =========================
# Local test: export TOFFEE_JWT="eyJ..." অথবা GitHub secret থেকে সেট হবে
JWT_TOKEN = os.getenv("TOFFEE_JWT") or "PASTE_YOUR_JWT_HERE_IF_LOCAL_TEST"

CHANNELS_FILE = "channels.json"
OUTPUT_FILE = "toffee_channels.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}
if JWT_TOKEN:
    HEADERS["Authorization"] = f"Bearer {JWT_TOKEN}"

# =========================
# helper: try extract stream URL
# =========================
def extract_stream_url(j):
    # common places to look
    if not j:
        return None
    # if top-level has data -> stream_url
    if isinstance(j, dict):
        # common patterns
        for key in ("stream_url", "stream", "playback_url", "play_url", "url", "data"):
            val = j.get(key)
            if isinstance(val, str) and val.startswith("http"):
                return val
            if isinstance(val, dict):
                # nested
                for k2 in ("stream_url", "play_url", "hls", "url"):
                    vv = val.get(k2)
                    if isinstance(vv, str) and vv.startswith("http"):
                        return vv
        # nested shallow search for first http string
        for v in j.values():
            if isinstance(v, str) and v.startswith("http"):
                return v
    return None

# =========================
# main
# =========================
def main():
    if not os.path.exists(CHANNELS_FILE):
        print(f"❌ Missing {CHANNELS_FILE}")
        return

    with open(CHANNELS_FILE, "r", encoding="utf-8") as f:
        channels = json.load(f)

    lines = ["#EXTM3U"]
    for ch in channels:
        name = ch.get("name") or ch.get("id")
        api_url = ch.get("api_url") or ch.get("url")
        if not api_url:
            print(f"⚠️ Skip {name}: no api_url")
            continue

        print(f"🔍 Fetching: {name}")
        try:
            resp = requests.get(api_url, headers=HEADERS, timeout=15)
        except Exception as e:
            print(f"❌ Request failed for {name}: {e}")
            continue

        if resp.status_code != 200:
            print(f"❌ HTTP {resp.status_code} for {name}")
            continue

        stream_url = None
        # try JSON
        try:
            j = resp.json()
            stream_url = extract_stream_url(j)
        except ValueError:
            text = resp.text.strip()
            if text.startswith("http"):
                stream_url = text

        if not stream_url:
            print(f"⚠️ No stream URL found for {name}")
            continue

        # add to m3u
        lines.append(f'#EXTINF:-1 tvg-id="{ch.get("id","")}" tvg-name="{name}" group-title="Toffee",{name}')
        lines.append(stream_url)
        print(f"✅ Added: {name} -> {stream_url}")

    # write file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n🎉 Playlist saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
