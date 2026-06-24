"""Post one Destination FAANG YouTube video to a LinkedIn Page.

The script is designed for GitHub Actions:
  - reads videos.json
  - skips videos already recorded in linkedin-post-history.json
  - publishes one text/link post to a LinkedIn organization page
  - updates linkedin-post-history.json after a successful post

Required environment variables:
  LINKEDIN_ACCESS_TOKEN
  LINKEDIN_ORGANIZATION_ID
"""

import argparse
import json
import os
import random
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone


VIDEOS_FILE = "videos.json"
HISTORY_FILE = "linkedin-post-history.json"
LINKEDIN_POSTS_API = "https://api.linkedin.com/rest/posts"
DEFAULT_ORGANIZATION_ID = "107371838"
CHANNEL_URL = "https://www.youtube.com/channel/UC49H999tjewVmrdLoCWCs4g"
SITE_URL = "https://destinationfaang.com/"


HASHTAGS_BY_CATEGORY = {
    "system-design": [
        "#SystemDesign",
        "#SoftwareArchitecture",
        "#Scalability",
        "#TechInterview",
        "#FAANG",
    ],
    "dsa": [
        "#DataStructures",
        "#Algorithms",
        "#CodingInterview",
        "#LeetCode",
        "#FAANG",
    ],
    "behavioral": [
        "#BehavioralInterview",
        "#CareerGrowth",
        "#SoftwareEngineering",
        "#TechCareer",
        "#FAANG",
    ],
    "misc": [
        "#SoftwareEngineering",
        "#TechCareer",
        "#InterviewPrep",
        "#CareerGrowth",
        "#FAANG",
    ],
}


HOOKS = [
    "Preparing for FAANG or top tech interviews?",
    "System design and coding interviews reward clear fundamentals.",
    "If you are serious about breaking into top tech, this is worth watching.",
    "Interview prep gets easier when you learn the patterns behind the questions.",
    "A strong interview answer starts with a simple, structured mental model.",
]


CTAS = [
    "Watch the full video here:",
    "Here is the full breakdown:",
    "Save this for your next prep session:",
    "Use this as part of your interview prep roadmap:",
]


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, payload):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def clean_text(value):
    value = re.sub(r"https?://\S+", "", value or "")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def short_description(video):
    description = clean_text(video.get("description", ""))
    match = re.search(r"Description:\s*(.+)", description, flags=re.IGNORECASE)
    if match:
        description = match.group(1).strip()
    if not description:
        return ""
    if len(description) > 190:
        description = description[:187].rsplit(" ", 1)[0].rstrip() + "..."
    return description


def category_label(category):
    return {
        "system-design": "system design",
        "dsa": "DSA and coding interview",
        "behavioral": "behavioral interview",
        "misc": "software engineering career",
    }.get(category, "software engineering")


def post_body(video, post_number):
    rng = random.Random(f"{video.get('id', '')}:{post_number}")
    category = video.get("category", "misc")
    description = short_description(video)
    hashtags = " ".join(HASHTAGS_BY_CATEGORY.get(category, HASHTAGS_BY_CATEGORY["misc"]))

    lines = [
        rng.choice(HOOKS),
        "",
        f"New Destination FAANG pick: {video.get('title', '').strip()}",
    ]
    if description:
        lines.extend(["", description])
    lines.extend(
        [
            "",
            f"This is useful for {category_label(category)} preparation, especially if you want practical, interview-focused explanations instead of memorized answers.",
            "",
            rng.choice(CTAS),
            video.get("url") or CHANNEL_URL,
            "",
            f"Explore the full video library: {SITE_URL}",
            "",
            hashtags,
        ]
    )
    return "\n".join(lines)


def posted_video_ids(history):
    return {entry.get("videoId") for entry in history.get("posts", []) if entry.get("videoId")}


def next_video(videos, history):
    posted = posted_video_ids(history)
    candidates = [video for video in videos if video.get("id") and video.get("id") not in posted]
    if not candidates:
        return None

    category_rank = {
        "system-design": 0,
        "dsa": 1,
        "behavioral": 2,
        "misc": 3,
    }

    def published_timestamp(video):
        published_at = video.get("publishedAt", "")
        if not published_at:
            return 0.0
        try:
            return datetime.fromisoformat(published_at.replace("Z", "+00:00")).timestamp()
        except ValueError:
            return 0.0

    def sort_key(video):
        return (
            category_rank.get(video.get("category"), 9),
            -published_timestamp(video),
        )

    return sorted(candidates, key=sort_key)[0]


def create_linkedin_post(access_token, organization_id, text):
    payload = {
        "author": f"urn:li:organization:{organization_id}",
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        LINKEDIN_POSTS_API,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": "202506",
            "X-Restli-Protocol-Version": "2.0.0",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        response_body = response.read().decode("utf-8")
        return {
            "status": response.status,
            "id": response.headers.get("x-restli-id"),
            "body": response_body,
        }


def main():
    parser = argparse.ArgumentParser(description="Publish one YouTube video promotion post to LinkedIn.")
    parser.add_argument("--dry-run", action="store_true", help="Print the selected post without publishing.")
    parser.add_argument("--videos", default=VIDEOS_FILE, help="Path to videos.json.")
    parser.add_argument("--history", default=HISTORY_FILE, help="Path to post history JSON.")
    args = parser.parse_args()

    videos_payload = load_json(args.videos, {})
    videos = videos_payload.get("videos", [])
    if not videos:
        sys.exit(f"No videos found in {args.videos}.")

    history = load_json(args.history, {"posts": []})
    video = next_video(videos, history)
    if not video:
        print("All videos have already been posted to LinkedIn.")
        return

    text = post_body(video, len(history.get("posts", [])) + 1)

    if args.dry_run:
        print(f"Selected video: {video.get('title')} ({video.get('id')})")
        print()
        print(text)
        return

    access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    organization_id = os.environ.get("LINKEDIN_ORGANIZATION_ID", DEFAULT_ORGANIZATION_ID)
    if not access_token:
        sys.exit("Missing LINKEDIN_ACCESS_TOKEN.")
    if not organization_id:
        sys.exit("Missing LINKEDIN_ORGANIZATION_ID.")

    try:
        result = create_linkedin_post(access_token, organization_id, text)
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        sys.exit(f"LinkedIn API returned HTTP {error.code}: {details}")

    history.setdefault("posts", []).append(
        {
            "videoId": video.get("id"),
            "title": video.get("title", ""),
            "url": video.get("url", ""),
            "category": video.get("category", ""),
            "postedAt": datetime.now(timezone.utc).isoformat(),
            "linkedinPostId": result.get("id"),
        }
    )
    write_json(args.history, history)
    print(f"Posted to LinkedIn: {video.get('title')} ({video.get('id')})")


if __name__ == "__main__":
    main()
