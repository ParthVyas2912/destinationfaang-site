"""Keyword-based categorization for YouTube videos.

Each video is assigned to exactly one of four categories:
  - dsa            (Data Structures & Algorithms)
  - system-design  (System Design)
  - behavioral     (Behavioral interview questions)
  - misc           (everything else)

The category is decided by scoring the video's title + description against
weighted keyword lists. The highest-scoring category wins; ties and zero
scores fall back to "misc".
"""

import re

CATEGORIES = ["dsa", "system-design", "behavioral", "misc"]

CATEGORY_LABELS = {
    "dsa": "DSA",
    "system-design": "System Design",
    "behavioral": "Behavioral",
    "misc": "Miscellaneous",
}

# Keyword -> weight. Multi-word phrases are matched as substrings; single
# words are matched on word boundaries to avoid false positives.
KEYWORDS = {
    "dsa": {
        "leetcode": 5, "data structure": 5, "algorithm": 4, "dynamic programming": 5,
        "binary search": 4, "binary tree": 4, "linked list": 4, "two pointer": 4,
        "sliding window": 4, "backtracking": 4, "breadth first": 4, "depth first": 4,
        "time complexity": 3, "space complexity": 3, "big o": 3, "recursion": 3,
        "sorting": 3, "graph": 3, "tree": 2, "array": 2, "string": 1, "stack": 2,
        "queue": 2, "heap": 3, "hash": 2, "hashmap": 3, "hash map": 3, "trie": 4,
        "greedy": 3, "bfs": 4, "dfs": 4, "dp": 3, "dijkstra": 4, "kadane": 4,
        "prefix sum": 4, "bit manipulation": 4, "matrix": 2, "subarray": 3,
        "subsequence": 3, "palindrome": 3, "anagram": 3, "interval": 2,
        "dsa": 5, "neetcode": 5,
    },
    "system-design": {
        "system design": 6, "scalability": 5, "scalable": 4, "load balancer": 5,
        "load balancing": 5, "microservice": 5, "distributed system": 5,
        "distributed": 3, "caching": 4, "cache": 3, "message queue": 4, "kafka": 4,
        "rate limiter": 5, "rate limiting": 5, "sharding": 5, "replication": 4,
        "consistency": 3, "cap theorem": 5, "database design": 4, "api design": 4,
        "design a": 4, "design twitter": 5, "design instagram": 5, "design url": 5,
        "design youtube": 5, "design uber": 5, "design netflix": 5, "cdn": 4,
        "high availability": 4, "throughput": 3, "latency": 3, "nosql": 3,
        "sql vs": 3, "horizontal scaling": 4, "vertical scaling": 4, "proxy": 2,
        "pub sub": 4, "event driven": 3, "consistent hashing": 5,
    },
    "behavioral": {
        "behavioral": 6, "behavioural": 6, "star method": 6, "tell me about a time": 6,
        "tell me about yourself": 6, "soft skill": 4, "interview tips": 3,
        "salary negotiation": 5, "negotiation": 3, "resume": 3, "cv ": 2,
        "conflict": 3, "leadership": 3, "teamwork": 3, "weakness": 3, "strength": 2,
        "why should we hire": 5, "biggest mistake": 4, "handle pressure": 4,
        "company culture": 3, "career advice": 3, "hr round": 5, "hr interview": 5,
        "manager round": 4, "amazon leadership principle": 6, "non technical": 3,
        "communication skill": 4, "body language": 3, "mock interview": 2,
    },
}

_WORD_KEYS = {}  # category -> list of (regex, weight) for single-word keys
_PHRASE_KEYS = {}  # category -> list of (phrase, weight) for multi-word keys


def _build():
    for cat, kws in KEYWORDS.items():
        words, phrases = [], []
        for kw, w in kws.items():
            if " " in kw.strip():
                phrases.append((kw.lower(), w))
            else:
                words.append((re.compile(r"\b" + re.escape(kw.lower()) + r"s?\b"), w))
        _WORD_KEYS[cat] = words
        _PHRASE_KEYS[cat] = phrases


_build()


def score_text(text):
    """Return a dict of category -> score for the given text."""
    text = (text or "").lower()
    scores = {}
    for cat in KEYWORDS:
        s = 0
        for phrase, w in _PHRASE_KEYS[cat]:
            if phrase in text:
                s += w
        for rx, w in _WORD_KEYS[cat]:
            if rx.search(text):
                s += w
        scores[cat] = s
    return scores


def categorize(title, description=""):
    """Return the best category id for a video.

    Strategy (tuned for promo-heavy descriptions):

    1. Score the **title**. The title is the most reliable signal, so if any
       category scores above zero there, the highest wins.
    2. If the title is uninformative, fall back to the **description** — but
       only for the DSA signal. Many videos here are LeetCode problems whose
       title is just the problem name ("Open the Lock: 752 ...") and whose
       description carries the real signal (``#leetcode #stack`` hashtags,
       algorithm names). Crucially, the channel's promotional boilerplate
       advertises a "system design" course and "resume" reviews, which would
       otherwise misfile unrelated videos into System Design / Behavioral.
       Algorithmic DSA terms don't appear in that boilerplate, so trusting the
       description for DSA only recovers real problem videos without importing
       those false positives.
    """
    title_scores = score_text(title)
    best = max(title_scores, key=title_scores.get)
    if title_scores[best] > 0:
        return best

    if score_text(description).get("dsa", 0) > 0:
        return "dsa"
    return "misc"


# --- Secondary metadata extraction (companies, difficulty, topics) ----------

COMPANIES = {
    "Google": [r"\bgoogle\b"],
    "Amazon": [r"\bamazon\b", r"\baws\b"],
    "Microsoft": [r"\bmicrosoft\b"],
    "Meta": [r"\bmeta\b", r"\bfacebook\b"],
    "Apple": [r"\bapple\b"],
    "Netflix": [r"\bnetflix\b"],
}
_COMPANY_RX = {name: [re.compile(p) for p in pats] for name, pats in COMPANIES.items()}

# DSA topic tags surfaced as secondary filters/badges.
TOPICS = {
    "Array": [r"\barrays?\b"],
    "String": [r"\bstrings?\b"],
    "Linked List": [r"\blinked lists?\b"],
    "Tree": [r"\btrees?\b", r"\bbinary tree\b", r"\bbst\b"],
    "Graph": [r"\bgraphs?\b", r"\bbfs\b", r"\bdfs\b", r"\bdijkstra\b"],
    "Dynamic Programming": [r"\bdynamic programming\b", r"\bdp\b"],
    "Stack": [r"\bstacks?\b"],
    "Queue": [r"\bqueues?\b", r"\bheap\b", r"\bpriority queue\b"],
    "Hashing": [r"\bhash(maps?|ing)?\b"],
    "Two Pointers": [r"\btwo pointers?\b", r"\bsliding window\b"],
    "Recursion": [r"\brecursion\b", r"\bbacktracking\b"],
    "Greedy": [r"\bgreedy\b"],
    "Binary Search": [r"\bbinary search\b"],
}
_TOPIC_RX = {name: [re.compile(p) for p in pats] for name, pats in TOPICS.items()}

_DIFF_RX = {
    "Easy": re.compile(r"#easy\b|\beasy\b"),
    "Medium": re.compile(r"#medium\b|\bmedium\b"),
    "Hard": re.compile(r"#hard\b|\bhard\b"),
}


def extract_companies(title, description=""):
    """Return a list of FAANG-style companies referenced in the TITLE.

    Title only: descriptions on this channel list every FAANG company as
    boilerplate ("most asked at Google, Amazon, Meta..."), so using them would
    tag nearly every video with all companies. The title names the company that
    actually asks the specific question.
    """
    blob = (title or "").lower()
    return [name for name, rxs in _COMPANY_RX.items() if any(r.search(blob) for r in rxs)]


def extract_difficulty(description=""):
    """Return 'Easy' | 'Medium' | 'Hard' | None.

    Prefers explicit #easy/#medium/#hard hashtags; the hardest tag present wins
    when several appear (videos rarely tag more than one).
    """
    text = (description or "").lower()
    hits = [lvl for lvl in ("Hard", "Medium", "Easy") if ("#" + lvl.lower()) in text]
    if hits:
        return hits[0]
    return None


def extract_topics(title, description=""):
    """Return a list of DSA topic tags found in the title (preferred) or desc."""
    title_l = (title or "").lower()
    found = [name for name, rxs in _TOPIC_RX.items() if any(r.search(title_l) for r in rxs)]
    if found:
        return found
    desc_l = (description or "").lower()
    return [name for name, rxs in _TOPIC_RX.items() if any(r.search(desc_l) for r in rxs)]


def enrich(video):
    """Add category, companies, difficulty and topics to a video dict in place."""
    title = video.get("title", "")
    desc = video.get("description", "")
    video["category"] = categorize(title, desc)
    video["companies"] = extract_companies(title, desc)
    video["difficulty"] = extract_difficulty(desc)
    video["topics"] = extract_topics(title, desc) if video["category"] == "dsa" else []
    return video


if __name__ == "__main__":
    tests = [
        "Two Sum LeetCode Solution - HashMap Approach",
        "Design a URL Shortener | System Design Interview",
        "Tell Me About Yourself - Best Answer for Interviews",
        "My trip to Goa vlog",
    ]
    for t in tests:
        print(f"{categorize(t):14s} <- {t}")
