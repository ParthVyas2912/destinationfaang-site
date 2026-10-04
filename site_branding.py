"""Brand the website's presentation catalog without changing YouTube or archives."""

import re

BRAND_NAME = "Destination Engineer"
LEGACY_BRAND_NAME = "Destination FAANG"
_LEGACY_NAME = re.compile(r"\bDestination\s+FAANG\b", re.IGNORECASE)


def rebrand_text(text):
    return _LEGACY_NAME.sub(BRAND_NAME, text)


def rebrand_catalog(payload):
    branded = dict(payload)
    branded["videos"] = []
    for video in payload["videos"]:
        entry = dict(video)
        for field in ("title", "description"):
            if isinstance(entry.get(field), str):
                entry[field] = rebrand_text(entry[field])
        branded["videos"].append(entry)
    if isinstance(branded.get("channelTitle"), str):
        branded["channelTitle"] = rebrand_text(branded["channelTitle"])
    return branded
