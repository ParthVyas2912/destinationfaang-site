# Design Proximity Services (Quad-Trees & Geohash)

| | |
|---|---|
| **Publish order** | 025 |
| **Course #** | 103 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design proximity service` |
| **Demand** | High |

**Thumbnail text idea:** NEARBY NOW
**One-line hook (first 15s):** Finding nearby restaurants is not a full-table distance scan; it is spatial indexing plus ranking.

## Learning objectives
- Design nearby search using geohash, quad-trees, or S2 cells.
- Support updates, radius queries, ranking, and pagination.
- Explain precision, boundary handling, and hot-cell mitigation.

## Topics & items to cover
- Requirements: find nearby restaurants/drivers/stores, filter by category/open-now, sort by distance/rating, update locations, support radius and map viewport.
- Estimation: reads are frequent; active entities update often; dense city cells become hot.
- API/Data model: `GET /nearby?lat=&lng=&radius=&category=`, `PATCH /places/{id}/location`; `Place(place_id, lat,lng, geohash, attrs)`, secondary index `cell -> place_ids`; shard by geohash/S2 cell, with replicas for hot metro cells.
- High-level design: write path computes cell IDs, stores place metadata and cell index; read path finds covering cells, fetches candidates, filters by exact haversine distance and business rules, ranks results.
- Deep dives/bottlenecks: boundary queries need neighboring cells; dense cells require smaller precision or sub-shards; moving objects need TTL/staleness filters.
- Wrap-up: spatial index narrows candidates; exact distance/ranking happens after retrieval.

## Anecdotes & war stories to use
- Geohash and Google S2 are widely used for mapping earth coordinates into sortable spatial cells.
- Ride-hailing companies publish engineering discussions around geospatial dispatch and region partitioning.
- Yelp/Google Maps-style local search blends distance with relevance, ratings, hours, and ads rather than pure nearest-first.

## Things to mention / interview tips
- Say: "The spatial index is a candidate generator, not the final ranking."
- Always query neighboring cells to avoid edge misses.
- Choose precision based on radius and density.
- Include stale location expiry for moving entities.

## Common mistakes to call out
- Full-table scanning with distance calculation.
- Returning all entities in a cell without exact distance filtering.
- Ignoring cell-boundary artifacts.
- Using one cell precision for rural and dense-city cases.

## Diagrams / visuals to draw on screen
- Map grid/geohash cells around a query point.
- Candidate retrieval then exact filtering/ranking.
- Hot downtown cell split into subcells/shards.

## Series glue
- Reference SQL vs NoSQL access patterns; point forward to Google Maps where proximity is one component of tiles, routing, and traffic. CTA: subscribe and get the GitHub visuals.
