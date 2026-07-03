"""Post a support/CTA top-level comment on every YouTube video in seo-suggestions.csv.

Usage:
  python scripts/youtube_post_pinned_comment.py --dry-run
  python scripts/youtube_post_pinned_comment.py --apply

Required setup (same OAuth flow as youtube_bulk_update_from_csv.py):
  1. Enable YouTube Data API v3 in Google Cloud.
  2. Create an OAuth client (Desktop app) and download client secret JSON.
  3. Pass --client-secrets path/to/client_secret.json (or set YT_OAUTH_CLIENT_SECRETS).

Notes:
  - commentThreads.insert costs ~50 quota units, so the default 10k/day quota
    caps roughly ~190-200 comments/day. Re-run --apply on later days; already
    commented videos auto-skip via the history file and/or the MARKER string.
  - Progress is persisted to youtube-comment-history.json so a daily cloud job
    (see .github/workflows/youtube-comments.yml) can resume until all are done.
  - The YouTube Data API v3 CANNOT pin comments. Pinning is a manual UI action.
    After posting, this script writes pin-checklist.csv so you can pin each one
    (open the video, find the channel comment, ... menu -> Pin) and tick it off.
"""

import argparse
import csv
import json
import os
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

# Stable substring used to detect an already-posted CTA comment (idempotency).
MARKER = "buy.stripe.com"

ONE_TIME_URL = "https://buy.stripe.com/8x2cMYb1Z6k4bzK7Ml1Fe01"
MEMBERSHIP_URL = "https://buy.stripe.com/dRm4gs3zx5g0eLWgiR1Fe00"

COMMENT_TEXT = (
    "\U0001F64F Destination FAANG is free \u2014 now and forever.\n\n"
    "This channel will always stay free for everyone preparing for their "
    "dream tech jobs. If it has helped you on your journey, please consider "
    "chipping in so it can stay free and keep growing \u2014 help if you can:\n\n"
    f"\u2764\ufe0f One-time $15 contribution: {ONE_TIME_URL}\n"
    f"\U0001F31F Become a member for $9.99/month: {MEMBERSHIP_URL}\n\n"
    "Every bit helps cover costs and keeps new interview-prep content coming. "
    "And if you can't contribute right now, that's completely okay \u2014 just "
    "keep learning and pass it on. Thank you for being here! \U0001F499"
)


def parse_args():
    ap = argparse.ArgumentParser(description="Post a CTA comment on all videos.")
    ap.add_argument("--csv", default="seo-suggestions.csv", help="Path to CSV with video_id column.")
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
    ap.add_argument("--apply", action="store_true", help="Actually post comments. Default is dry-run.")
    ap.add_argument("--dry-run", action="store_true", help="Preview only (default).")
    ap.add_argument("--limit", type=int, default=0, help="Max videos to process (0 = all).")
    ap.add_argument("--video-id", default="", help="Only this video_id.")
    ap.add_argument("--sleep-seconds", type=float, default=0.3, help="Pause between inserts.")
    ap.add_argument(
        "--history-file",
        default="youtube-comment-history.json",
        help="JSON file tracking video_ids already commented (for cloud resume).",
    )
    ap.add_argument(
        "--no-remote-check",
        action="store_true",
        help="Skip the commentThreads.list dedupe API call; rely only on history file.",
    )
    ap.add_argument(
        "--checklist",
        default="pin-checklist.csv",
        help="Where to write the manual-pin checklist of posted comments.",
    )
    return ap.parse_args()


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
                    "Cached token missing/invalid and no client secrets provided. "
                    "Pass --client-secrets or set YT_OAUTH_CLIENT_SECRETS to "
                    "authorize a new token."
                )
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets, SCOPES)
            creds = flow.run_local_server(port=0)
        ensure_parent_dir(token_file)
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def read_video_ids(csv_path, only_video_id="", limit=0):
    rows = []
    seen = set()
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if "video_id" not in (reader.fieldnames or []):
            sys.exit("CSV is missing required column: video_id")
        for row in reader:
            vid = (row.get("video_id") or "").strip()
            title = (row.get("suggested_title") or row.get("current_title") or "").strip()
            if not vid or vid in seen:
                continue
            if only_video_id and vid != only_video_id:
                continue
            seen.add(vid)
            rows.append({"video_id": vid, "title": title})
            if limit > 0 and len(rows) >= limit:
                break
    return rows


def already_commented(youtube, video_id, marker=MARKER, max_pages=3):
    """Return True if a top-level comment containing the marker already exists."""
    page_token = None
    for _ in range(max_pages):
        try:
            res = (
                youtube.commentThreads()
                .list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    order="relevance",
                    textFormat="plainText",
                    pageToken=page_token,
                )
                .execute()
            )
        except HttpError:
            # Comments disabled or not listable -> treat as not-commented; insert will report.
            return False
        for item in res.get("items", []):
            text = (
                item.get("snippet", {})
                .get("topLevelComment", {})
                .get("snippet", {})
                .get("textDisplay", "")
            )
            if marker in text:
                return True
        page_token = res.get("nextPageToken")
        if not page_token:
            break
    return False


def post_comment(youtube, video_id, text):
    body = {
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {"snippet": {"textOriginal": text}},
        }
    }
    return youtube.commentThreads().insert(part="snippet", body=body).execute()


def load_history(path):
    """Return set of video_ids already commented, from the JSON history file."""
    if not path or not os.path.exists(path):
        return set()
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return set()
    ids = data.get("commented", data) if isinstance(data, dict) else data
    return set(ids) if isinstance(ids, (list, set)) else set()


def save_history(path, ids):
    if not path:
        return
    ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"commented": sorted(ids)}, f, indent=2)


def main():
    args = parse_args()
    dry_run = not args.apply or args.dry_run
    youtube = load_service(args.client_secrets, args.token_file)
    rows = read_video_ids(args.csv, only_video_id=args.video_id, limit=args.limit)
    if not rows:
        sys.exit("No matching videos to process.")

    history = load_history(args.history_file)

    posted = 0
    skipped = 0
    failed = 0
    checklist = []

    for i, row in enumerate(rows, start=1):
        vid = row["video_id"]
        try:
            if vid in history:
                print(f"[{i}/{len(rows)}] SKIP {vid}: in history file")
                skipped += 1
                continue

            if not args.no_remote_check and already_commented(youtube, vid):
                print(f"[{i}/{len(rows)}] SKIP {vid}: CTA comment already present")
                skipped += 1
                if not dry_run:
                    history.add(vid)
                    save_history(args.history_file, history)
                continue

            print(f"[{i}/{len(rows)}] {'DRY' if dry_run else 'POST'} {vid}  {row['title'][:60]}")

            if not dry_run:
                post_comment(youtube, vid, COMMENT_TEXT)
                posted += 1
                checklist.append(row)
                history.add(vid)
                save_history(args.history_file, history)
                time.sleep(max(0.0, args.sleep_seconds))
            else:
                posted += 1
                checklist.append(row)

        except HttpError as e:
            failed += 1
            print(f"[{i}/{len(rows)}] FAIL {vid}: {e}", file=sys.stderr)
            if "quotaExceeded" in str(e):
                print("Quota exhausted for today. Re-run --apply tomorrow.", file=sys.stderr)
                break

    if checklist and not dry_run:
        ensure_parent_dir(args.checklist)
        write_header = not os.path.exists(args.checklist)
        with open(args.checklist, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            if write_header:
                w.writerow(["video_id", "url", "title", "pinned"])
            for r in checklist:
                w.writerow([
                    r["video_id"],
                    f"https://www.youtube.com/watch?v={r['video_id']}",
                    r["title"],
                    "no",
                ])

    mode = "DRY-RUN" if dry_run else "POST"
    remaining = len(rows) - len(history) if not dry_run else 0
    print(
        f"\n{mode} complete: processed={len(rows)}, "
        f"posted={posted}, skipped={skipped}, failed={failed}"
    )
    if dry_run:
        print("Re-run with --apply to actually post the comments.")
    else:
        print(f"History: {len(history)} commented, ~{max(0, remaining)} remaining.")
        print(
            f"Wrote pin checklist to {args.checklist}. The API cannot pin comments;\n"
            "pin each manually: open the video -> your comment -> ... -> Pin."
        )


if __name__ == "__main__":
    main()
