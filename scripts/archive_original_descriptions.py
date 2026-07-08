"""Archive the FULL ORIGINAL description of every video in seo-suggestions.csv.

Why: the SEO descriptions were first generated from only ~300 chars of context,
and for the ~356 already-updated videos the original text now survives only in
the Wayback Machine. This builds a single archive of every original description so
we can (a) know definitively which videos had chapter timestamps, (b) regenerate
better SEO descriptions from the full text, and (c) keep a permanent reference.

Source selection per video (decided from youtube-audit.json):
  - recovered : already captured in recovered-timestamps.json (Wayback, has ts).
  - live      : NOT yet updated on YouTube -> the current public description IS
                the original; read it with yt-dlp (no OAuth needed).
  - wayback   : already updated -> pull the newest pre-overwrite Wayback snapshot
                and keep its full description (even if it has no timestamps).
  - lost      : updated but no usable Wayback snapshot found.

Output: original-descriptions.json
  [{"video_id","source","wayback_ts","has_timestamps","length","original_description"}]

Resumable and read-only against YouTube / archive.org.
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
from recover_timestamps import list_snapshots, fetch_description  # noqa: E402

SEP = "\x1f"


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


def fetch_live_description(video_id, timeout, client="android"):
    cmd = [
        "yt-dlp", "--skip-download", "--no-warnings",
        "--extractor-args", f"youtube:player_client={client}",
        "--print", f"%(description)s",
        f"https://www.youtube.com/watch?v={video_id}",
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except Exception:  # noqa: BLE001
        return None
    text = (out.stdout or b"").decode("utf-8", "replace").strip()
    return text or None


def wayback_original(video_id, timeout, max_snapshots):
    """Return (description, wayback_ts) for the newest pre-cutoff snapshot with a
    non-empty description, or (None, None). Retries transient CDX errors so we
    don't wrongly fall back when archive.org is just rate-limiting us."""
    snaps = None
    for attempt in range(3):
        snaps = list_snapshots(video_id, timeout)
        if snaps is not None:
            break
        time.sleep(2.0 * (attempt + 1))
    if not snaps:
        return None, None
    for ts in snaps[:max_snapshots]:
        try:
            desc = fetch_description(video_id, ts, timeout)
        except Exception:  # noqa: BLE001
            continue
        if desc and desc.strip():
            return desc, ts
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="seo-suggestions.csv")
    ap.add_argument("--audit", default="youtube-audit.json")
    ap.add_argument("--recovered", default="recovered-timestamps.json")
    ap.add_argument(
        "--fallback-json",
        default="",
        help="Pre-overwrite videos.json (original titles/descriptions, 300-char) "
        "used only when no full original can be recovered.",
    )
    ap.add_argument("--out", default="original-descriptions.json")
    ap.add_argument("--limit", type=int, default=0, help="Max NEW ids to process this run.")
    ap.add_argument("--max-snapshots", type=int, default=6)
    ap.add_argument("--timeout", type=float, default=25.0)
    ap.add_argument("--video-id", default="")
    ap.add_argument(
        "--no-wayback",
        action="store_true",
        help="Skip live archive.org calls (use recovered seed + fallback only). "
        "Use when archive.org is rate-limiting; expand Wayback via Actions instead.",
    )
    args = ap.parse_args()

    with open(args.csv, encoding="utf-8-sig", newline="") as f:
        ids = [r["video_id"].strip() for r in csv.DictReader(f) if r.get("video_id")]

    audit = {r["video_id"]: r for r in load_json(args.audit, [])}
    recovered = {r["video_id"]: r for r in load_json(args.recovered, [])}

    fallback = {}
    if args.fallback_json:
        fb = load_json(args.fallback_json, [])
        fb_items = fb if isinstance(fb, list) else fb.get("videos", [])
        fallback = {x["id"]: x.get("description", "") for x in fb_items if x.get("id")}

    out_list = load_json(args.out, [])
    have = {r["video_id"] for r in out_list}

    if args.video_id:
        ids = [args.video_id]
        have.discard(args.video_id)

    processed = 0
    for i, vid in enumerate(ids, 1):
        if vid in have:
            continue
        if args.limit and processed >= args.limit:
            break
        processed += 1

        # 1) already recovered from Wayback (full original, with timestamps)
        if vid in recovered:
            desc = recovered[vid]["description"]
            entry = {
                "video_id": vid, "source": "recovered",
                "wayback_ts": recovered[vid].get("wayback_ts", ""),
                "has_timestamps": has_timestamps(desc),
                "length": len(desc), "original_description": desc,
            }
            out_list.append(entry)
            save_json(args.out, out_list)
            print(f"[{i}/{len(ids)}] {vid} recovered ({entry['length']}c ts={entry['has_timestamps']})", flush=True)
            continue

        a = audit.get(vid)
        updated = bool(a and a.get("title_updated"))

        if a is not None and not updated:
            # 2) not updated yet -> live description IS the original
            desc = fetch_live_description(vid, args.timeout)
            if desc:
                entry = {
                    "video_id": vid, "source": "live", "wayback_ts": "",
                    "has_timestamps": has_timestamps(desc),
                    "length": len(desc), "original_description": desc,
                }
                out_list.append(entry)
                save_json(args.out, out_list)
                print(f"[{i}/{len(ids)}] {vid} live ({entry['length']}c ts={entry['has_timestamps']})", flush=True)
                continue
            # fall through to wayback if live fetch failed

        # 3) updated (or live failed) -> pull original from Wayback
        desc, ts = (None, None)
        if not args.no_wayback:
            desc, ts = wayback_original(vid, args.timeout, args.max_snapshots)
        if desc:
            entry = {
                "video_id": vid, "source": "wayback", "wayback_ts": ts,
                "has_timestamps": has_timestamps(desc),
                "length": len(desc), "original_description": desc,
            }
            print(f"[{i}/{len(ids)}] {vid} wayback @ {ts} ({entry['length']}c ts={entry['has_timestamps']})", flush=True)
        else:
            fb_desc = fallback.get(vid, "")
            if fb_desc.strip():
                entry = {
                    "video_id": vid, "source": "videos_json_fallback", "wayback_ts": "",
                    "has_timestamps": has_timestamps(fb_desc),
                    "length": len(fb_desc), "original_description": fb_desc,
                }
                print(f"[{i}/{len(ids)}] {vid} fallback ({entry['length']}c ts={entry['has_timestamps']})", flush=True)
            else:
                entry = {
                    "video_id": vid, "source": "lost", "wayback_ts": "",
                    "has_timestamps": False, "length": 0, "original_description": "",
                }
                print(f"[{i}/{len(ids)}] {vid} LOST (no snapshot, no fallback)", flush=True)
        out_list.append(entry)
        save_json(args.out, out_list)

    by_src = {}
    for r in out_list:
        by_src[r["source"]] = by_src.get(r["source"], 0) + 1
    with_ts = sum(1 for r in out_list if r["has_timestamps"])
    print(f"\nDONE run: processed={processed} total_archived={len(out_list)}")
    print(f"by source: {by_src}")
    print(f"originals WITH timestamps: {with_ts}")
    print(f"remaining: {len(ids) - len(have | {r['video_id'] for r in out_list})}")


if __name__ == "__main__":
    main()
