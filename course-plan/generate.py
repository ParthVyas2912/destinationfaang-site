"""Generate the sequenced folder structure + manifest for the System Design Mega Course.

Publish order is demand-led: high-search case studies front-loaded and interleaved
~2:1 with the foundation concepts they depend on. Concepts are taught inside case
studies, then reinforced by standalone explainer videos.

Run:  python course-plan/generate.py
Outputs:
  course-plan/manifest.json   - machine-readable plan (source of truth)
  course-plan/SCHEDULE.md     - human-readable publishing table
  course-plan/<NNN - Title>/  - one folder per video (brief.md added separately)
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

# Each entry: (course_num, module, type, length_min, youtube_title, primary_keyword, demand)
# course_num: sheet number, or a string id for unnumbered rows.
# type: case | concept | intro | mock
# demand: 3=very high, 2=high, 1=moderate  (relative YouTube search demand)
# Publish number is assigned by list position, starting at 5 (1-4 already published).
PLAN = [
    # ---- Phase 1: Traffic launch — top case studies + the concepts they need ----
    (88,  "M09", "case",    30, "Design TinyURL — System Design Interview (Step by Step)", "design tinyurl", 3),
    (94,  "M09", "case",    35, "Design Twitter / X — System Design Interview", "design twitter", 3),
    (11,  "M01", "concept", 14, "Consistent Hashing — The #1 Concept Interviewers Love", "consistent hashing", 3),
    (92,  "M09", "case",    40, "Design Instagram — System Design Interview", "design instagram", 3),
    (95,  "M09", "case",    40, "Design WhatsApp — Real-Time Chat System Design", "design whatsapp", 3),
    (8,   "M01", "concept", 12, "CAP Theorem in 10 Minutes (with Real Examples)", "cap theorem", 3),
    (18,  "M02", "concept", 20, "Design a Rate Limiter — System Design Interview", "design rate limiter", 3),
    (93,  "M09", "case",    45, "Design YouTube / Netflix — Video Streaming System", "design youtube", 3),
    (101, "M09", "case",    45, "Design Uber — Ride-Hailing System Design", "design uber", 3),
    (16,  "M02", "concept", 18, "Load Balancing Explained (L4 vs L7, DNS, Anycast)", "load balancing", 3),
    (96,  "M09", "case",    30, "Design a Notification System (Push / SMS / Email)", "design notification system", 2),
    (97,  "M09", "case",    30, "Design Search Autocomplete (Google-Style Typeahead)", "design autocomplete", 2),
    (31,  "M03", "concept", 16, "Caching Explained: LRU, LFU & TTL (Interview Guide)", "caching lru lfu ttl", 2),
    (90,  "M09", "case",    35, "Design Dropbox / Google Drive — File Sync System", "design dropbox", 3),
    (99,  "M09", "case",    40, "Design a Payment System (Stripe-Style)", "design payment system", 2),
    (36,  "M04", "concept", 18, "Why Kafka Is So Fast — Message Queues Explained", "what is kafka", 3),
    (98,  "M09", "case",    45, "Design Amazon / an E-Commerce Platform", "design amazon", 2),
    (6,   "M01", "concept", 14, "Strong vs Eventual Consistency (with Examples)", "eventual consistency", 2),
    (112, "M09", "case",    35, "Design a Web Crawler (Google-Scale)", "design web crawler", 2),
    (20,  "M03", "concept", 22, "SQL vs NoSQL — When to Use Which (Deep Dive)", "sql vs nosql", 3),

    # ---- Phase 2: Broaden case studies + supporting concepts ----
    (103, "M09", "case",    30, "Design Proximity Services (Quad-Trees & Geohash)", "design proximity service", 2),
    (102, "M09", "case",    40, "Design Google Maps — System Design Interview", "design google maps", 2),
    (22,  "M03", "concept", 18, "Database Sharding & Rebalancing at Scale", "database sharding", 2),
    (106, "M09", "case",    35, "Design a Ticket Booking System (Concurrency & Locking)", "design ticketmaster", 2),
    (40,  "M04", "concept", 20, "Distributed Transactions & the Saga Pattern", "saga pattern", 2),
    (89,  "M09", "case",    22, "Design Pastebin / a Text-Storage Service", "design pastebin", 2),
    (17,  "M02", "concept", 16, "What Is a CDN? Edge Delivery Explained", "what is a cdn", 2),
    (91,  "M09", "case",    28, "Design an Image CDN (Pinterest-Style)", "design image cdn", 1),
    (35,  "M04", "concept", 16, "Message Queues vs Event Streams (Kafka vs RabbitMQ)", "message queue vs event stream", 2),
    (104, "M09", "case",    35, "Design a Food Delivery App (DoorDash / Zomato)", "design food delivery", 2),
    (10,  "M01", "concept", 18, "Database Replication & Partitioning Explained", "database replication", 2),
    (108, "M09", "case",    35, "Design a Ledger & Payment Reconciliation System", "design ledger system", 1),
    (44,  "M05", "concept", 20, "API Design: REST vs gRPC vs GraphQL", "rest vs grpc vs graphql", 2),
    (100, "M09", "case",    35, "Design an Ad Platform & Real-Time Auctions (RTB)", "design ad system", 1),
    (34,  "M03", "concept", 14, "Hot Keys & Cache Stampedes (and How to Fix Them)", "cache stampede", 1),
    (105, "M09", "case",    30, "Design an Inventory & Warehouse Management System", "design inventory system", 1),
    (37,  "M04", "concept", 14, "Pub/Sub Systems & Event Routing Explained", "pub sub system", 1),
    (115, "M09", "case",    30, "Design a Distributed Job Scheduler", "design job scheduler", 2),
    (54,  "M05", "concept", 20, "Paxos & Raft — Distributed Consensus Explained", "raft consensus", 2),
    (114, "M09", "case",    30, "Design Multi-Region Database Replication", "multi region database", 2),

    # ---- Phase 3: Data/storage depth + more systems ----
    (19,  "M03", "concept", 20, "RDBMS Internals: Indexes, B-Trees & ACID", "database indexing", 2),
    (117, "M09", "case",    28, "Design an API Gateway (Architecture Deep Dive)", "design api gateway", 2),
    (24,  "M03", "concept", 12, "Bloom Filters Explained (with Examples)", "bloom filter", 2),
    (107, "M09", "case",    30, "Design a Logistics & Fleet Tracking System", "design fleet tracking", 1),
    (25,  "M03", "concept", 12, "HyperLogLog: Counting Billions with Kilobytes", "hyperloglog", 1),
    (111, "M09", "case",    30, "Design a Real-Time Analytics Dashboard", "design analytics dashboard", 1),
    (27,  "M03", "concept", 18, "Search Architecture: Elasticsearch Fundamentals", "elasticsearch system design", 2),
    (110, "M09", "case",    30, "Design an Event Analytics Platform (Mixpanel-Style)", "design analytics platform", 1),
    (26,  "M03", "concept", 14, "Time-Series Databases & Scalable Counters", "time series database", 1),
    (116, "M09", "case",    30, "Design an IoT Platform & Device Telemetry System", "design iot system", 1),
    (32,  "M03", "concept", 12, "Layered Caching: CDN, App & Client Caches", "layered caching", 1),
    (109, "M09", "case",    30, "Design a Cloud Data Warehouse (Snowflake-Style)", "design data warehouse", 1),
    (33,  "M03", "concept", 12, "Write-Through vs Write-Back Caching", "write through vs write back", 1),
    (113, "M09", "case",    22, "Design a Feature Flag System (LaunchDarkly-Style)", "design feature flags", 1),
    (23,  "M03", "concept", 12, "Secondary Indexes & Precomputation Tactics", "secondary index", 1),
    (118, "M09", "case",    28, "Design a Scalable ETL Data Pipeline", "design etl pipeline", 1),

    # ---- Phase 4: Messaging, microservices & reliability concepts ----
    (38,  "M04", "concept", 18, "Event Sourcing & CQRS Explained", "event sourcing cqrs", 2),
    (122, "M09", "case",    32, "Design a Fraud Detection System", "design fraud detection", 1),
    (39,  "M04", "concept", 14, "Exactly-Once Processing & the Outbox Pattern", "exactly once outbox", 1),
    (41,  "M04", "concept", 16, "Stream Processing at Scale (Flink / Spark)", "stream processing", 1),
    (119, "M09", "case",    35, "Design a Recommendation Engine (Netflix / YouTube)", "design recommendation system", 2),
    (43,  "M05", "concept", 18, "Microservices: DDD & Service Boundaries", "microservices design", 2),
    (47,  "M05", "concept", 14, "Circuit Breakers, Retries & Resiliency Patterns", "circuit breaker pattern", 2),
    (48,  "M05", "concept", 10, "Exponential Backoff & Jitter (Retry Storms)", "exponential backoff jitter", 1),
    (49,  "M05", "concept", 14, "Backpressure & Load Shedding Explained", "backpressure load shedding", 1),
    (53,  "M05", "concept", 16, "High Availability: Active-Active Architectures", "active active architecture", 2),
    (55,  "M05", "concept", 14, "Leader Election & Quorum in Distributed Systems", "leader election", 1),
    (56,  "M05", "concept", 12, "Stateful vs Stateless Scaling", "stateful vs stateless", 1),
    (45,  "M05", "concept", 12, "Service Discovery & Config Management", "service discovery", 1),
    (46,  "M05", "concept", 12, "Gossip Protocols: Decentralized Discovery", "gossip protocol", 1),
    (50,  "M05", "concept", 12, "Schema Management & API Versioning", "api versioning", 1),
    (51,  "M05", "concept", 14, "Multi-Tenancy Models for SaaS", "multi tenancy saas", 1),
    (52,  "M05", "concept", 10, "Quotas, Fair-Use & Resource Isolation", "rate limiting quotas", 1),
    (57,  "M05", "concept", 14, "Chaos Engineering: Testing for Failure", "chaos engineering", 2),
    (58,  "M05", "concept", 12, "Incident Response & Blameless Postmortems", "blameless postmortem", 1),
    (42,  "M04", "concept", 12, "Data Replays & Backfill Strategies", "data backfill", 1),

    # ---- Phase 5: Foundations cleanup (M01/M02) + networking ----
    (5,   "M01", "concept", 14, "Availability: SLA, SLO & SLI Explained (Nines)", "sla slo sli", 2),
    (9,   "M01", "concept", 12, "Every System Design Tradeoff You Must Know", "system design tradeoffs", 2),
    (7,   "M01", "concept", 12, "Vector Clocks & Conflict Resolution", "vector clocks", 1),
    (12,  "M01", "concept", 12, "Scaling Databases: Connection Pooling", "database connection pooling", 1),
    (13,  "M01", "concept", 14, "Zero-Downtime Database Migrations", "zero downtime migration", 2),
    (14,  "M02", "concept", 16, "Networking for System Design: OSI & TCP/IP", "osi model tcp ip", 1),
    (15,  "M02", "concept", 16, "HTTP/3 vs gRPC vs WebSockets Compared", "http3 grpc websockets", 2),
    (21,  "M03", "concept", 16, "How to Choose a Database (Decision Matrix)", "how to choose a database", 2),
    (28,  "M03", "concept", 12, "Data Formats & Compression (Protobuf, Avro)", "protobuf avro parquet", 1),
    (29,  "M03", "concept", 14, "Backups & Disaster Recovery (RPO / RTO)", "backup disaster recovery", 1),
    (30,  "M03", "concept", 14, "Data Lake Architecture & Governance", "data lake architecture", 1),

    # ---- Phase 6: Cloud & infrastructure ----
    (70,  "M07", "concept", 16, "Docker & Containers for System Design Interviews", "docker containers explained", 2),
    (71,  "M07", "concept", 20, "Kubernetes Architecture & Scheduling Explained", "kubernetes architecture", 3),
    (73,  "M07", "concept", 14, "Serverless & Event-Driven Architectures", "serverless architecture", 2),
    (74,  "M07", "concept", 16, "Multi-AZ & Multi-Region Cloud Design", "multi region architecture", 2),
    (72,  "M07", "concept", 16, "Service Mesh Explained (Istio & Linkerd)", "service mesh istio", 1),
    (77,  "M07", "concept", 14, "Canary, Blue-Green & Shadow Deployments", "blue green canary deployment", 2),
    (76,  "M07", "concept", 14, "Infrastructure as Code: Terraform Basics", "terraform infrastructure as code", 1),
    (75,  "M07", "concept", 12, "Hybrid Cloud & Edge Deployment Models", "hybrid cloud edge", 1),

    # ---- Phase 7: Security, observability & FinOps ----
    (59,  "M06", "concept", 20, "Auth Explained: OAuth2, OIDC, JWT & mTLS", "oauth2 oidc jwt", 3),
    (64,  "M06", "concept", 14, "Preventing Abuse, Bots & Scraping", "bot prevention system design", 1),
    (63,  "M06", "concept", 14, "Handling PII/PCI: Tokenization & Masking", "pii tokenization", 1),
    (60,  "M06", "concept", 12, "Secrets Management & Key Rotation", "secrets management", 1),
    (61,  "M06", "concept", 12, "Threat Modeling with STRIDE", "stride threat modeling", 1),
    (62,  "M06", "concept", 10, "Zero-Downtime Security Patching", "zero downtime patching", 1),
    (66,  "M06", "concept", 14, "Metrics & Dashboards: RED vs USE", "red use metrics", 1),
    (67,  "M06", "concept", 14, "Distributed Tracing & Root-Cause Analysis", "distributed tracing", 2),
    (65,  "M06", "concept", 12, "Scalable Logging & Retention Strategies", "scalable logging", 1),
    (68,  "M06", "concept", 12, "Advanced Observability: eBPF & Telemetry", "ebpf observability", 1),
    (69,  "M06", "concept", 14, "FinOps: Cloud Cost & Unit Economics", "finops cloud cost", 1),

    # ---- Phase 8: Data engineering & AI systems (differentiator) ----
    (84,  "M08", "concept", 24, "Designing RAG Architectures for LLMs", "rag architecture", 3),
    (83,  "M08", "concept", 20, "Vector Search & ANN Indexing (HNSW) Explained", "vector search ann", 3),
    (120, "M09", "case",    35, "Design an LLM Chatbot & Query System (ChatGPT-Style)", "design chatgpt", 3),
    (82,  "M08", "concept", 18, "Feature Stores & Real-Time ML Systems", "feature store ml", 2),
    (87,  "M08", "concept", 18, "Scalable Inference & GPU Autoscaling", "llm inference scaling", 2),
    (86,  "M08", "concept", 16, "LLM Evaluation & AI Safety Guardrails", "llm evaluation guardrails", 2),
    (85,  "M08", "concept", 14, "Prompt Caching & Token Optimization", "prompt caching tokens", 2),
    (124, "M09", "case",    32, "Design a Real-Time Personalization Engine", "real time personalization", 1),
    (78,  "M08", "concept", 14, "Batch vs Streaming Data Pipelines", "batch vs streaming", 2),
    (79,  "M08", "concept", 14, "Orchestration: Airflow vs Temporal", "airflow vs temporal", 1),
    (80,  "M08", "concept", 14, "Data Warehouse vs Data Lakehouse", "warehouse vs lakehouse", 2),
    (81,  "M08", "concept", 12, "Ensuring Data Quality & Lineage", "data quality lineage", 1),
    (123, "M09", "case",    28, "Design an A/B Testing Framework", "design ab testing", 2),
    (125, "M09", "case",    32, "Design an Auto-Scaling ML Pipeline", "design ml pipeline", 1),
    (126, "M09", "case",    32, "Design a Scalable Video Processing Pipeline", "design video processing", 1),
    ("VS", "M09", "case",   28, "Design a Document Vector Search System", "document vector search", 2),
    ("RAG","M09", "case",   35, "Design an End-to-End RAG System (Production)", "end to end rag system", 3),

    # ---- Phase 9: Mock interviews & capstone ----
    ("MOCK1", "M10", "mock", 55, "Mock System Design Interview: Social Media Feed", "mock system design interview", 3),
    ("MOCK2", "M10", "mock", 55, "Mock System Design Interview: File Storage & Sync", "mock system design interview", 2),
    ("MOCK3", "M10", "mock", 55, "Mock System Design Interview: E-Commerce Checkout", "mock system design interview", 2),
    ("MOCK4", "M10", "mock", 30, "Speed Drills: APIs, Schemas & Estimation", "system design estimation practice", 2),
    ("MOCK5", "M10", "mock", 25, "Storytelling Tactics That Win System Design Interviews", "system design interview tips", 2),
    ("MOCK6", "M10", "mock", 90, "Final Project: Design Your Own System (Capstone)", "system design project", 1),
]

MODULE_NAMES = {
    "M00": "Orientation & Template",
    "M01": "Scalability Foundations",
    "M02": "Networking & Delivery",
    "M03": "Data, Storage & Caching",
    "M04": "Messaging & Event-Driven Systems",
    "M05": "Microservices & Reliability",
    "M06": "Security, Observability & FinOps",
    "M07": "Cloud & Infrastructure",
    "M08": "Data Engineering & AI Systems",
    "M09": "System Design Case Studies",
    "M10": "Mock Interview & Practice",
}

DEMAND_LABEL = {3: "Very High", 2: "High", 1: "Moderate"}


def slugify(title):
    t = title.split(" — ")[0].split(" (")[0]
    t = re.sub(r"[^\w\s\-/]", "", t)
    t = t.replace("/", "-")
    t = re.sub(r"\s+", " ", t).strip()
    return t[:52].strip()


def main():
    manifest = []
    start = 5  # 1-4 already published
    for i, (cnum, mod, typ, length, yt, kw, demand) in enumerate(PLAN):
        pub = start + i
        folder = f"{pub:03d} - {slugify(yt)}"
        manifest.append({
            "publish_order": pub,
            "course_num": cnum,
            "module": mod,
            "module_name": MODULE_NAMES[mod],
            "type": typ,
            "length_min": length,
            "youtube_title": yt,
            "primary_keyword": kw,
            "demand": demand,
            "demand_label": DEMAND_LABEL[demand],
            "folder": folder,
        })

    # write manifest
    with open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # create folders
    for m in manifest:
        os.makedirs(os.path.join(HERE, m["folder"]), exist_ok=True)

    # write SCHEDULE.md
    lines = [
        "# System Design Mega Course — Full Publishing Schedule",
        "",
        f"**{len(manifest)} remaining videos** in demand-led publish order "
        "(videos 1-4 already published).",
        "",
        "Publish order is optimized for YouTube: high-search case studies are front-loaded "
        "and interleaved ~2:1 with the foundation concepts they use. Each video is standalone "
        "(ranks in search), teaches a reusable concept (course glue), and links onward.",
        "",
        "| # | Video (YouTube Title) | Module | Type | Length | Primary Search Keyword | Demand |",
        "|---|---|---|---|---|---|---|",
    ]
    for m in manifest:
        lines.append(
            f"| {m['publish_order']:03d} | {m['youtube_title']} | {m['module']} "
            f"| {m['type']} | {m['length_min']}m | `{m['primary_keyword']}` | {m['demand_label']} |"
        )
    lines += [
        "",
        "## Module summary",
        "",
        "| Module | Name | Videos |",
        "|---|---|---|",
    ]
    counts = {}
    for m in manifest:
        counts[m["module"]] = counts.get(m["module"], 0) + 1
    for mod in sorted(counts):
        lines.append(f"| {mod} | {MODULE_NAMES[mod]} | {counts[mod]} |")
    lines.append("")
    with open(os.path.join(HERE, "SCHEDULE.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote manifest ({len(manifest)} videos), SCHEDULE.md, and {len(manifest)} folders.")
    assert len({m['course_num'] for m in manifest}) == len(manifest), "duplicate course_num!"


if __name__ == "__main__":
    main()
