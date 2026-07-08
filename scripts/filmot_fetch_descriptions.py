"""Fetch original YouTube descriptions from the Filmot metadata archive.

Filmot (https://filmot.com) indexes historical YouTube metadata (titles,
descriptions, subtitles). For videos it crawled BEFORE our SEO overwrite it
still holds the ORIGINAL description (often with the chapter timestamps that
were lost when we rewrote the descriptions).

Auth: RapidAPI. Subscribe (free tier) at
  https://rapidapi.com/Jopik1/api/filmot-tube-metadata-archive/
then export your key:  $env:FILMOT_RAPIDAPI_KEY = "<key>"

Endpoint: GET /getvideos?id=<comma,separated,ids>&flags=1   (flags bit 1 = description)
Host header: filmot-tube-metadata-archive.p.rapidapi.com

Usage:
  # inspect the raw JSON shape for a couple of ids first
  python scripts/filmot_fetch_descriptions.py --ids M2H61M1iq2E,HasOycW2_N0 --raw
  # then fetch all ids from the CSV -> filmot-descriptions.json
  python scripts/filmot_fetch_descriptions.py --csv seo-suggestions.csv

Read-only. Never commits the key.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from timestamps_util import has_timestamps  # noqa: E402

HOST = "filmot-tube-metadata-archive.p.rapidapi.com"


def call_getvideos(ids, key, flags, timeout):
    q = urllib.parse.urlencode({"id": ",".join(ids), "flags": str(flags)})
    url = f"https://{HOST}/getvideos?{q}"
    req = urllib.request.Request(
        url,
        headers={
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": HOST,
            "User-Agent": "Mozilla/5.0",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def extract_records(payload):
    """Filmot may wrap results differently; normalize to a list of dicts."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for k in ("result", "results", "videos", "data"):
            if isinstance(payload.get(k), list):
                return payload[k]
        # single object
        if payload.get("id"):
            return [payload]
    return []


def get_desc(rec):
    for k in ("description", "desc", "originaldescription", "descriptiontext"):
        v = rec.get(k)
        if isinstance(v, str) and v.strip():
            return v
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="seo-suggestions.csv")
    ap.add_argument("--ids", default="", help="Comma-separated ids (overrides CSV).")
    ap.add_argument("--out", default="filmot-descriptions.json")
    ap.add_argument("--key", default=os.environ.get("FILMOT_RAPIDAPI_KEY", ""))
    ap.add_argument("--flags", type=int, default=1)
    ap.add_argument("--batch", type=int, default=20, help="ids per request.")
    ap.add_argument("--timeout", type=float, default=40.0)
    ap.add_argument("--sleep", type=float, default=1.0)
    ap.add_argument("--raw", action="store_true", help="Print raw JSON and exit.")
    args = ap.parse_args()

    if not args.key:
        sys.exit("Missing key. Set FILMOT_RAPIDAPI_KEY or pass --key.")

    if args.ids:
        ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    else:
        with open(args.csv, encoding="utf-8-sig", newline="") as f:
            ids = [r["video_id"].strip() for r in csv.DictReader(f) if r.get("video_id")]

    if args.raw:
        payload = call_getvideos(ids[: args.batch], args.key, args.flags, args.timeout)
        print(json.dumps(payload, ensure_ascii=False, indent=2)[:6000])
        return

    out = {}
    if os.path.exists(args.out):
        out = {r["video_id"]: r for r in json.load(open(args.out, encoding="utf-8"))}

    todo = [v for v in ids if v not in out]
    for i in range(0, len(todo), args.batch):
        chunk = todo[i : i + args.batch]
        try:
            payload = call_getvideos(chunk, args.key, args.flags, args.timeout)
        except Exception as e:  # noqa: BLE001
            print(f"batch {i}-{i+len(chunk)} ERROR: {e}", file=sys.stderr)
            time.sleep(args.sleep * 3)
            continue
        recs = {str(r.get("id")): r for r in extract_records(payload)}
        for vid in chunk:
            rec = recs.get(vid, {})
            desc = get_desc(rec)
            out[vid] = {
                "video_id": vid,
                "title": rec.get("title", ""),
                "description": desc,
                "has_timestamps": has_timestamps(desc),
                "length": len(desc),
                "found": bool(rec),
            }
        json.dump(list(out.values()), open(args.out, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        got = sum(1 for v in chunk if out[v]["found"])
        ts = sum(1 for v in chunk if out[v]["has_timestamps"])
        print(f"[{i+len(chunk)}/{len(todo)}] batch found={got}/{len(chunk)} with_ts={ts}", flush=True)
        time.sleep(args.sleep)

    vals = list(out.values())
    print("\n===== FILMOT SUMMARY =====")
    print(f"total ids: {len(ids)}  fetched entries: {len(vals)}")
    print(f"found on filmot: {sum(v['found'] for v in vals)}")
    print(f"with timestamps: {sum(v['has_timestamps'] for v in vals)}")
    print(f"desc >300 chars: {sum(v['length'] > 300 for v in vals)}")


if __name__ == "__main__":
    main()
