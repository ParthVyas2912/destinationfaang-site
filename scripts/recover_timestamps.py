"""Recover original YouTube descriptions (with timestamps) from the Wayback Machine.

Strategy per video_id (from seo-suggestions.csv):
  1. Query the Wayback CDX API for archived snapshots of the watch page.
  2. Fetch archived snapshots (raw, gzip-decoded) newest-first.
  3. Extract the full description from ytInitialData.attributedDescription.content
     (or the ytInitialPlayerResponse shortDescription fallback).
  4. Keep the first snapshot whose description actually contains timestamps.

Output: recovered-timestamps.json — [{"video_id", "description", "wayback_ts"}]
This file is directly consumable by youtube_bulk_update_from_csv.py via
  --timestamps-source-json recovered-timestamps.json

The run is resumable: already-recovered ids (and confirmed misses) are skipped.
Read-only against YouTube; only writes the local JSON files.
"""

import argparse
import csv
import gzip
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from youtube_bulk_update_from_csv import has_timestamps, extract_timestamp_lines  # noqa: E402

CDX = "https://web.archive.org/cdx/search/cdx"
ATTR_DESC_RE = re.compile(r'"attributedDescription":\{"content":"((?:[^"\\]|\\.)*)"')
SHORT_DESC_RE = re.compile(r'"shortDescription":"((?:[^"\\]|\\.)*)"')
OVERWRITE_CUTOFF = "20260703"  # my metadata edits landed on/after this date (UTC).


def http_get(url, timeout, retries=3, backoff=2.0):
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(backoff * (attempt + 1))
    raise last


def list_snapshots(video_id, timeout):
    watch = f"https://www.youtube.com/watch?v={video_id}"
    q = urllib.parse.urlencode({
        "url": watch,
        "output": "json",
        "fl": "timestamp,statuscode",
        "filter": "statuscode:200",
        "collapse": "digest",
    })
    try:
        raw = http_get(f"{CDX}?{q}", timeout=timeout)
    except Exception:  # noqa: BLE001
        return None  # network error — unknown, retry later
    try:
        data = json.loads(raw.decode("utf-8", "replace"))
    except Exception:  # noqa: BLE001
        return []
    if not data or len(data) < 2:
        return []
    stamps = [row[0] for row in data[1:] if row and row[0]]
    # Prefer snapshots taken BEFORE my overwrite (they still hold timestamps),
    # newest-first; then fall back to any remaining snapshots newest-first.
    before = sorted((s for s in stamps if s < OVERWRITE_CUTOFF), reverse=True)
    after = sorted((s for s in stamps if s >= OVERWRITE_CUTOFF), reverse=True)
    return before + after


def extract_description(html):
    m = ATTR_DESC_RE.search(html)
    if m:
        try:
            return json.loads('"' + m.group(1) + '"')
        except Exception:  # noqa: BLE001
            pass
    m = SHORT_DESC_RE.search(html)
    if m:
        try:
            return json.loads('"' + m.group(1) + '"')
        except Exception:  # noqa: BLE001
            pass
    return None


def fetch_description(video_id, ts, timeout):
    url = f"https://web.archive.org/web/{ts}id_/https://www.youtube.com/watch?v={video_id}"
    raw = http_get(url, timeout=timeout)
    try:
        raw = gzip.decompress(raw)
    except Exception:  # noqa: BLE001
        pass
    html = raw.decode("utf-8", "replace")
    return extract_description(html)


def load_json(path, default):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="seo-suggestions.csv")
    ap.add_argument("--out", default="recovered-timestamps.json")
    ap.add_argument("--miss-file", default="recovered-timestamps.misses.json")
    ap.add_argument("--limit", type=int, default=0, help="Max NEW ids to process this run.")
    ap.add_argument("--max-snapshots", type=int, default=4, help="Snapshots to try per video.")
    ap.add_argument("--timeout", type=float, default=25.0)
    ap.add_argument("--sleep", type=float, default=0.5)
    ap.add_argument("--video-id", default="", help="Only process this id (ignores resume skip).")
    args = ap.parse_args()

    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        ids = [r["video_id"].strip() for r in csv.DictReader(f) if r.get("video_id")]

    recovered = load_json(args.out, [])
    misses = load_json(args.miss_file, [])
    have = {r["video_id"] for r in recovered}
    missed = set(misses)

    if args.video_id:
        ids = [args.video_id]
        have.discard(args.video_id)
        missed.discard(args.video_id)

    processed = 0
    new_hits = 0
    for i, vid in enumerate(ids, 1):
        if vid in have or vid in missed:
            continue
        if args.limit and processed >= args.limit:
            break
        processed += 1

        snaps = list_snapshots(vid, args.timeout)
        if snaps is None:
            print(f"[{i}/{len(ids)}] {vid} cdx-error (will retry next run)", flush=True)
            time.sleep(args.sleep)
            continue
        if not snaps:
            print(f"[{i}/{len(ids)}] {vid} no-snapshot", flush=True)
            missed.add(vid)
            save_json(args.miss_file, sorted(missed))
            time.sleep(args.sleep)
            continue

        found = None
        for ts in snaps[: args.max_snapshots]:
            try:
                desc = fetch_description(vid, ts, args.timeout)
            except Exception as e:  # noqa: BLE001
                print(f"    snapshot {ts} fetch err: {type(e).__name__}", flush=True)
                continue
            if desc and has_timestamps(desc):
                found = (ts, desc)
                break
            time.sleep(0.2)

        if found:
            ts, desc = found
            recovered.append({"video_id": vid, "description": desc, "wayback_ts": ts})
            save_json(args.out, recovered)
            new_hits += 1
            n = len(extract_timestamp_lines(desc))
            print(f"[{i}/{len(ids)}] {vid} RECOVERED ({n} ts lines) @ {ts}", flush=True)
        else:
            missed.add(vid)
            save_json(args.miss_file, sorted(missed))
            print(f"[{i}/{len(ids)}] {vid} archived-but-no-timestamps", flush=True)

        time.sleep(args.sleep)

    print(f"\nDONE this run: processed={processed}, new_recovered={new_hits}")
    print(f"Total recovered={len(recovered)}, total misses={len(missed)}, "
          f"remaining={len(ids) - len(have | missed) if not args.video_id else 'n/a'}")


if __name__ == "__main__":
    main()
