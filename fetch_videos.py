"""Fetch all videos from a YouTube channel and write videos.json.

Usage:
  1. Get a YouTube Data API v3 key: https://console.cloud.google.com/apis/credentials
  2. Find your channel ID (starts with "UC..."): https://www.youtube.com/account_advanced
  3. Run:
       set YT_API_KEY=your_key_here          (Windows cmd)
       $env:YT_API_KEY="your_key_here"       (PowerShell)
       python fetch_videos.py --channel-id UCxxxxxxxxxxxxxxxx

  Or pass the key directly:
       python fetch_videos.py --channel-id UCxxxx --api-key YOUR_KEY

This uses only the public "uploads" playlist, so it needs nothing more than a
read-only API key (no OAuth / YouTube Studio login required). Quota cost is
tiny: ~1 unit per 50 videos.
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

from categorize import enrich, CATEGORY_LABELS

API = "https://www.googleapis.com/youtube/v3"


def _get(path, params):
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as r:
        return json.load(r)


def get_uploads_playlist(channel_id, key):
    data = _get("channels", {"part": "contentDetails", "id": channel_id, "key": key})
    items = data.get("items")
    if not items:
        sys.exit(f"No channel found for id '{channel_id}'. Check the ID and API key.")
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_all_videos(playlist_id, key):
    videos, page = [], None
    while True:
        params = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": 50,
            "key": key,
        }
        if page:
            params["pageToken"] = page
        data = _get("playlistItems", params)
        for it in data.get("items", []):
            sn = it["snippet"]
            vid = it["contentDetails"]["videoId"]
            videos.append({
                "id": vid,
                "title": sn.get("title", ""),
                "description": sn.get("description", ""),
                "publishedAt": sn.get("publishedAt", ""),
                "thumbnail": (sn.get("thumbnails", {}).get("medium", {}) or {}).get("url", ""),
                "url": f"https://www.youtube.com/watch?v={vid}",
            })
        page = data.get("nextPageToken")
        print(f"  fetched {len(videos)} videos...", file=sys.stderr)
        if not page:
            break
    return videos


def main():
    ap = argparse.ArgumentParser(description="Fetch & categorize YouTube channel videos.")
    ap.add_argument("--channel-id", required=True, help="Channel ID starting with UC...")
    ap.add_argument("--api-key", default=os.environ.get("YT_API_KEY"),
                    help="YouTube Data API v3 key (or set YT_API_KEY env var).")
    ap.add_argument("--out", default="videos.json", help="Output file (default videos.json).")
    args = ap.parse_args()

    if not args.api_key:
        sys.exit("Missing API key. Pass --api-key or set the YT_API_KEY env var.")

    print("Resolving uploads playlist...", file=sys.stderr)
    pl = get_uploads_playlist(args.channel_id, args.api_key)
    print("Fetching videos...", file=sys.stderr)
    videos = get_all_videos(pl, args.api_key)

    counts = {c: 0 for c in CATEGORY_LABELS}
    for v in videos:
        # Enrich (category, companies, difficulty, topics) using the FULL
        # description, then trim the stored description to keep the JSON small.
        enrich(v)
        v["description"] = (v["description"] or "")[:300]
        counts[v["category"]] += 1

    payload = {"channelId": args.channel_id, "count": len(videos), "videos": videos}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"\nWrote {len(videos)} videos to {args.out}", file=sys.stderr)
    for c, n in counts.items():
        print(f"  {CATEGORY_LABELS[c]:16s}: {n}", file=sys.stderr)


if __name__ == "__main__":
    main()
