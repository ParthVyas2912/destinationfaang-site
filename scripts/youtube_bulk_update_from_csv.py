"""Bulk update YouTube titles/descriptions from seo-suggestions.csv.

Usage:
  python scripts/youtube_bulk_update_from_csv.py --csv seo-suggestions.csv --dry-run
  python scripts/youtube_bulk_update_from_csv.py --csv seo-suggestions.csv --apply

Required setup:
  1. Enable YouTube Data API v3 in Google Cloud.
  2. Create an OAuth client (Desktop app) and download client secret JSON.
  3. Pass --client-secrets path/to/client_secret.json (or set YT_OAUTH_CLIENT_SECRETS).

Notes:
  - videos.update requires OAuth and a signed-in account with edit access.
  - This script preserves existing snippet fields such as categoryId and tags.
"""

import argparse
import csv
import json
import os
import re
import sys
import time

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print(
        "Missing dependencies. Install with:\n"
        "  python -m pip install google-api-python-client google-auth-oauthlib",
        file=sys.stderr,
    )
    raise


SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
# A timecode like 0:00, 12:34 or 1:02:03 appearing anywhere on a line. This
# matches both "0:00 Intro" (time-first) and "Intro: 0:00" (label-first).
TIMECODE_RE = re.compile(r"(?<!\d)(?:\d{1,2}:)?\d{1,2}:\d{2}(?!\d)")
# A chapter/timestamp line: contains a timecode and isn't an overly long
# sentence that merely happens to mention a time.
MAX_TIMESTAMP_LINE_LEN = 160
MIN_TIMESTAMP_LINES = 2


def parse_args():
    ap = argparse.ArgumentParser(description="Bulk update YouTube metadata from CSV.")
    ap.add_argument("--csv", default="seo-suggestions.csv", help="Path to suggestions CSV.")
    ap.add_argument(
        "--client-secrets",
        default=os.environ.get("YT_OAUTH_CLIENT_SECRETS"),
        help="OAuth client secrets JSON (or set YT_OAUTH_CLIENT_SECRETS).",
    )
    ap.add_argument(
        "--token-file",
        default=os.environ.get("YT_OAUTH_TOKEN_FILE", ".secrets/youtube-token.json"),
        help="Path to OAuth token cache file.",
    )
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Actually write updates. Default is dry-run.",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only. This is the default if --apply is not set.",
    )
    ap.add_argument("--limit", type=int, default=0, help="Max rows to process (0 = all).")
    ap.add_argument("--video-id", default="", help="Update only this video_id.")
    ap.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.15,
        help="Pause between update calls to avoid spikes.",
    )
    ap.add_argument(
        "--timestamps-source-json",
        default=os.environ.get("YT_TIMESTAMPS_SOURCE_JSON", ""),
        help=(
            "Optional JSON file with original descriptions for timestamp recovery "
            "(supports videos[].id/video_id + description)."
        ),
    )
    args = ap.parse_args()
    # client_secrets is only needed for the interactive first-time OAuth flow.
    # When a valid/refreshable token file already exists (e.g. in CI), we can
    # authenticate token-only, so don't hard-fail here.
    if not args.client_secrets and not os.path.exists(args.token_file):
        sys.exit(
            "Missing OAuth client secrets JSON. Pass --client-secrets or set "
            "YT_OAUTH_CLIENT_SECRETS (only needed when no token file exists)."
        )
    return args


def ensure_parent_dir(path):
    parent = os.path.dirname(path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def load_service(client_secrets, token_file):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not client_secrets:
                sys.exit(
                    "No valid token and no client secrets available to start the "
                    "OAuth flow. Provide --client-secrets or a refreshable token file."
                )
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets, SCOPES)
            creds = flow.run_local_server(port=0)
        ensure_parent_dir(token_file)
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def read_rows(csv_path, only_video_id="", limit=0):
    rows = []
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"video_id", "suggested_title", "suggested_description"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"CSV is missing required columns: {', '.join(sorted(missing))}")
        for row in reader:
            vid = (row.get("video_id") or "").strip()
            title = (row.get("suggested_title") or "").strip()
            desc = (row.get("suggested_description") or "").strip()
            if not vid or not title or not desc:
                continue
            if only_video_id and vid != only_video_id:
                continue
            rows.append({"video_id": vid, "title": title, "description": desc})
            if limit > 0 and len(rows) >= limit:
                break
    return rows


def fetch_snippet(youtube, video_id):
    res = youtube.videos().list(part="snippet", id=video_id).execute()
    items = res.get("items", [])
    if not items:
        return None
    return items[0]["snippet"]


def build_updated_snippet(current, new_title, new_description):
    snippet = {
        "title": new_title,
        "description": new_description,
        "categoryId": current.get("categoryId", "22"),
    }
    for key in ("tags", "defaultLanguage", "defaultAudioLanguage"):
        if key in current:
            snippet[key] = current[key]
    return snippet


def _normalize_newlines(text):
    return (text or "").replace("\r\n", "\n").replace("\r", "\n")


def extract_timestamp_lines(description):
    lines = _normalize_newlines(description).split("\n")
    found = []
    for line in lines:
        clean = line.strip()
        if not clean or len(clean) > MAX_TIMESTAMP_LINE_LEN:
            continue
        if TIMECODE_RE.search(clean):
            found.append(clean)
    return found


def has_timestamps(description):
    return len(extract_timestamp_lines(description)) >= MIN_TIMESTAMP_LINES


def merge_description_with_timestamps(target_description, current_description, fallback_description=""):
    target = _normalize_newlines(target_description).strip()
    if has_timestamps(target):
        return target

    ts_lines = extract_timestamp_lines(current_description)
    if not ts_lines:
        ts_lines = extract_timestamp_lines(fallback_description)
    if not ts_lines:
        return target

    if target:
        return f"{target}\n\nTimestamps:\n" + "\n".join(ts_lines)
    return "Timestamps:\n" + "\n".join(ts_lines)


def load_timestamp_source(path):
    if not path:
        return {}
    if not os.path.exists(path):
        print(
            f"Note: timestamps source JSON not found ({path}); "
            "continuing with current-description preservation only.",
            file=sys.stderr,
        )
        return {}

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    if isinstance(data, dict) and isinstance(data.get("videos"), list):
        rows = data["videos"]
    elif isinstance(data, list):
        rows = data
    else:
        sys.exit("Unsupported timestamps-source JSON format.")

    out = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        vid = (row.get("video_id") or row.get("id") or "").strip()
        desc = row.get("description") or ""
        if vid and has_timestamps(desc):
            out[vid] = desc
    return out


def main():
    args = parse_args()
    dry_run = not args.apply or args.dry_run
    youtube = load_service(args.client_secrets, args.token_file)
    rows = read_rows(args.csv, only_video_id=args.video_id, limit=args.limit)
    timestamp_source = load_timestamp_source(args.timestamps_source_json)
    if not rows:
        sys.exit("No matching rows to process.")

    updated = 0
    skipped = 0
    failed = 0
    restored_from_current = 0
    restored_from_source = 0

    for i, row in enumerate(rows, start=1):
        vid = row["video_id"]
        title = row["title"]
        desc = row["description"]
        try:
            current = fetch_snippet(youtube, vid)
            if not current:
                print(f"[{i}/{len(rows)}] SKIP {vid}: video not found")
                skipped += 1
                continue

            current_desc = current.get("description") or ""
            fallback_desc = timestamp_source.get(vid, "")
            merged_desc = merge_description_with_timestamps(desc, current_desc, fallback_desc)

            if merged_desc != desc:
                if has_timestamps(current_desc):
                    restored_from_current += 1
                    source_label = "current description"
                elif fallback_desc:
                    restored_from_source += 1
                    source_label = "timestamps source JSON"
                else:
                    source_label = "unknown"
                print(f"  timestamps: preserved from {source_label}")

            if current.get("title") == title and _normalize_newlines(current_desc).strip() == merged_desc:
                print(f"[{i}/{len(rows)}] SKIP {vid}: already matches")
                skipped += 1
                continue

            print(f"[{i}/{len(rows)}] {'DRY' if dry_run else 'APPLY'} {vid}")
            print(f"  title: {title}")

            if not dry_run:
                snippet = build_updated_snippet(current, title, merged_desc)
                youtube.videos().update(
                    part="snippet",
                    body={"id": vid, "snippet": snippet},
                ).execute()
                updated += 1
                time.sleep(max(0.0, args.sleep_seconds))
            else:
                updated += 1

        except HttpError as e:
            failed += 1
            print(f"[{i}/{len(rows)}] FAIL {vid}: {e}", file=sys.stderr)
            if "quotaExceeded" in str(e):
                print(
                    "Quota exhausted for today. Re-run --apply tomorrow; "
                    "already-updated videos auto-skip.",
                    file=sys.stderr,
                )
                break

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(
        f"\n{mode} complete: processed={len(rows)}, "
        f"would_update/updated={updated}, skipped={skipped}, failed={failed}, "
        f"timestamps_from_current={restored_from_current}, "
        f"timestamps_from_source={restored_from_source}"
    )
    if dry_run:
        print("Re-run with --apply to commit these changes in YouTube.")


if __name__ == "__main__":
    main()
