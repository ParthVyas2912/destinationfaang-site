"""Audit the LIVE state of every video in seo-suggestions.csv (read-only, no OAuth).

Uses yt-dlp to read each video's current public title + description and reports:
  - title_updated: live title == suggested_title from the CSV
  - live_has_ts:   live description currently contains chapter timestamps
  - suggested_has_ts: our suggested_description already contains timestamps
  - recovered / missed: whether Wayback timestamp recovery has data for it

Output: writes a JSON + CSV audit report so we can see, across all 413 videos,
which are updated, which lost timestamps, and which still need recovery.

This is intentionally dependency-light (only yt-dlp) and safe to re-run; it never
writes to YouTube.
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timestamps_util import has_timestamps  # noqa: E402

SEP = "\x1f"  # unit separator, unlikely to appear in titles/descriptions


def fetch_live(video_id, timeout, client):
    """Return (title, description) or (None, None) on failure."""
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--no-warnings",
        "--extractor-args",
        f"youtube:player_client={client}",
        "--print",
        f"%(title)s{SEP}%(description)s",
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except Exception:  # noqa: BLE001
        return None, None
    text = (out.stdout or b"").decode("utf-8", "replace").strip()
    if SEP not in text:
        return None, None
    title, _, desc = text.partition(SEP)
    return title.strip(), desc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="seo-suggestions.csv")
    ap.add_argument("--out-json", default="youtube-audit.json")
    ap.add_argument("--out-csv", default="youtube-audit.csv")
    ap.add_argument("--recovered", default="recovered-timestamps.json")
    ap.add_argument("--misses", default="recovered-timestamps.misses.json")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--sleep", type=float, default=0.2)
    ap.add_argument("--client", default="android", help="yt-dlp youtube player_client")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.csv, encoding="utf-8-sig")))
    if args.limit:
        rows = rows[: args.limit]

    recovered = set()
    if os.path.exists(args.recovered):
        data = json.load(open(args.recovered, encoding="utf-8"))
        recovered = {r["video_id"] for r in data}
    missed = set()
    if os.path.exists(args.misses):
        missed = set(json.load(open(args.misses, encoding="utf-8")))

    results = []
    for i, r in enumerate(rows, 1):
        vid = r["video_id"].strip()
        title, desc = fetch_live(vid, args.timeout, args.client)
        # one retry with the web client if android extraction failed
        if title is None:
            title, desc = fetch_live(vid, args.timeout, "web")
        ok = title is not None
        rec = {
            "video_id": vid,
            "category": r.get("category", ""),
            "fetch_ok": ok,
            "title_updated": bool(ok and title.strip() == r["suggested_title"].strip()),
            "live_has_ts": bool(ok and has_timestamps(desc)),
            "suggested_has_ts": has_timestamps(r.get("suggested_description", "")),
            "recovered": vid in recovered,
            "missed": vid in missed,
            "live_desc_len": len(desc) if ok else 0,
            "live_title": title if ok else "",
        }
        results.append(rec)
        flag = "" if ok else " FETCH-FAIL"
        print(
            f"[{i}/{len(rows)}] {vid} upd={rec['title_updated']} "
            f"live_ts={rec['live_has_ts']} sug_ts={rec['suggested_has_ts']}{flag}",
            flush=True,
        )
        json.dump(results, open(args.out_json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        time.sleep(args.sleep)

    with open(args.out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[k for k in results[0] if k != "live_title"])
        w.writeheader()
        for rec in results:
            w.writerow({k: v for k, v in rec.items() if k != "live_title"})

    ok = [r for r in results if r["fetch_ok"]]
    print("\n===== AUDIT SUMMARY =====")
    print(f"total={len(results)} fetched_ok={len(ok)} fetch_fail={len(results) - len(ok)}")
    print(f"title_updated={sum(r['title_updated'] for r in ok)}")
    print(f"NOT updated (fetched)={sum(not r['title_updated'] for r in ok)}")
    print(f"live_has_ts={sum(r['live_has_ts'] for r in ok)}")
    upd_no_ts = [r for r in ok if r["title_updated"] and not r["live_has_ts"]]
    print(f"updated_but_no_live_ts={len(upd_no_ts)}")


if __name__ == "__main__":
    main()
