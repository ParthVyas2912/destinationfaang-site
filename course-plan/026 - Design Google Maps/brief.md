# Design Google Maps — System Design Interview

| | |
|---|---|
| **Publish order** | 026 |
| **Course #** | 102 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~40 min |
| **Primary search keyword** | `design google maps` |
| **Demand** | High |

**Thumbnail text idea:** ROUTES & TILES
**One-line hook (first 15s):** Google Maps is tiles, places, traffic, and routing stitched together under strict latency.

## Learning objectives
- Decompose maps into tiles, places, routing, geocoding, and traffic.
- Design low-latency map rendering and route computation.
- Explain precomputation, graph partitioning, and live traffic updates.

## Topics & items to cover
- Requirements: render map tiles, search places, geocode addresses, compute routes/ETA, live traffic, favorites/reviews optional.
- Estimation: tile reads are massive and cacheable; route queries are CPU-heavy; traffic updates stream continuously.
- API/Data model: `GET /tiles/{z}/{x}/{y}`, `GET /places/search`, `GET /routes?origin=&dest=`; `RoadSegment(segment_id, geometry, speed_limit)`, `Place`, `Traffic(segment_id, speed, updated_at)`; shard tiles by z/x/y, road graph by region/cell.
- High-level design: tile service serves pre-rendered/vector tiles from CDN, places service uses search + spatial index, routing service loads regional graph, traffic pipeline updates edge weights, clients cache tiles.
- Deep dives/bottlenecks: route algorithms use A*/Dijkstra with heuristics plus contraction hierarchies/precomputed shortcuts; live traffic updates edge weights without rebuilding whole graph; tile generation pipeline handles multiple zoom levels and styles.
- Wrap-up: separate mostly-static map data from dynamic traffic and user queries.

## Anecdotes & war stories to use
- Google Maps popularized slippy map tiles and massive client-side interaction expectations.
- OpenStreetMap shows how road/places data can be represented as nodes, ways, and relations for routing and rendering.
- Modern routing engines use graph preprocessing techniques like contraction hierarchies to answer routes quickly.

## Things to mention / interview tips
- Say: "Tiles are cacheable read traffic; routing is graph compute; traffic is a streaming weight update problem."
- Clarify whether using raster or vector tiles.
- Discuss regional graph partitioning and cross-region routes.
- Include offline/client caching for mobile users.

## Common mistakes to call out
- Rendering every map view dynamically from raw geometry.
- Running plain Dijkstra over a planet-scale graph for every route.
- Mixing place search ranking with road-network routing.
- Ignoring stale traffic and map-data versioning.

## Diagrams / visuals to draw on screen
- Tile pyramid with z/x/y coordinates and CDN cache.
- Road graph partitioned by regions with routing service.
- Traffic stream updating segment weights used by ETA.

## Series glue
- Reference proximity services for spatial indexes and close this run by pointing to later sharding, CDN, and high-availability videos. CTA: subscribe and clone the GitHub repo.
