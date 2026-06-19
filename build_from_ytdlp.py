"""Convert a yt-dlp flat-playlist JSON dump into our videos.json format.

Usage:
    python build_from_ytdlp.py channel_raw.json videos.json

This lets you populate the site WITHOUT a YouTube Data API key, by using
yt-dlp's channel listing. Categorization uses the video title (flat dumps
don't include descriptions).
"""

import json
import sys
from datetime import datetime, timezone

from categorize import enrich, CATEGORY_LABELS


def thumb_for(entry):
    thumbs = entry.get("thumbnails") or []
    if thumbs:
        # yt-dlp orders thumbnails small -> large; pick a mid/large one.
        return thumbs[-1].get("url", "")
    vid = entry.get("id", "")
    return f"https://i.ytimg.com/vi/{vid}/mqdefault.jpg"


def iso_from_ts(ts):
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    except (ValueError, OSError, OverflowError):
        return ""


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "channel_raw.json"
    out = sys.argv[2] if len(sys.argv) > 2 else "videos.json"

    with open(src, encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("entries") or []
    videos = []
    counts = {c: 0 for c in CATEGORY_LABELS}
    for e in entries:
        if not e.get("id"):
            continue
        title = e.get("title", "")
        v = {
            "id": e["id"],
            "title": title,
            "description": "",
            "publishedAt": iso_from_ts(e.get("timestamp")),
            "thumbnail": thumb_for(e),
            "url": f"https://www.youtube.com/watch?v={e['id']}",
        }
        enrich(v)
        counts[v["category"]] += 1
        videos.append(v)

    payload = {
        "channelId": data.get("channel_id") or data.get("id", ""),
        "channelTitle": data.get("title", "") or data.get("channel", ""),
        "count": len(videos),
        "videos": videos,
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(videos)} videos to {out}")
    for c, n in counts.items():
        print(f"  {CATEGORY_LABELS[c]:16s}: {n}")


if __name__ == "__main__":
    main()
