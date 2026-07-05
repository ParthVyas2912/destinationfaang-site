"""Dependency-free helpers for detecting and preserving YouTube chapter timestamps.

Kept free of third-party imports so it can be reused by tooling (e.g. the
Wayback recovery script) that must run without the Google API client libraries.
"""

import re

# A timecode like 0:00, 12:34 or 1:02:03 appearing anywhere on a line. This
# matches both "0:00 Intro" (time-first) and "Intro: 0:00" (label-first).
TIMECODE_RE = re.compile(r"(?<!\d)(?:\d{1,2}:)?\d{1,2}:\d{2}(?!\d)")
# A chapter/timestamp line contains a timecode and isn't an overly long
# sentence that merely happens to mention a time.
MAX_TIMESTAMP_LINE_LEN = 160
# Chapter blocks always have multiple entries; require this many to qualify.
MIN_TIMESTAMP_LINES = 2


def normalize_newlines(text):
    return (text or "").replace("\r\n", "\n").replace("\r", "\n")


def extract_timestamp_lines(description):
    lines = normalize_newlines(description).split("\n")
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
    """Return target_description, appending recovered timestamp lines if it lacks them.

    Preference order for the timestamp source: the target itself (already has
    them -> unchanged), then the current live description, then a fallback
    (e.g. a recovered original description).
    """
    target = normalize_newlines(target_description).strip()
    if has_timestamps(target):
        return target

    ts_lines = extract_timestamp_lines(current_description)
    if not ts_lines:
        ts_lines = extract_timestamp_lines(fallback_description)
    if len(ts_lines) < MIN_TIMESTAMP_LINES:
        return target

    if target:
        return f"{target}\n\nTimestamps:\n" + "\n".join(ts_lines)
    return "Timestamps:\n" + "\n".join(ts_lines)
