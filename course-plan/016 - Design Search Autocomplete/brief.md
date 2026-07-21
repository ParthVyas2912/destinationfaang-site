# Design Search Autocomplete (Google-Style Typeahead)

| | |
|---|---|
| **Publish order** | 016 |
| **Course #** | 97 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design autocomplete` |
| **Demand** | High |

**Thumbnail text idea:** TYPEAHEAD FAST
**One-line hook (first 15s):** Autocomplete has to answer before the user finishes typing, which changes the data structure completely.

## Learning objectives
- Build low-latency prefix suggestions using tries, caches, and precomputation.
- Separate query logging, ranking, and serving paths.
- Handle freshness, personalization, and abuse constraints.

## Topics & items to cover
- Requirements: return top suggestions for a typed prefix, typo tolerance optional, trending updates, location/language personalization, low latency.
- Estimation: read-heavy, every keystroke can call service; top prefixes are extremely hot.
- API/Data model: `GET /suggest?q=iph&locale=en-US&user_ctx=...`; data `Suggestion(prefix, term, score, locale)`, query logs stream; shard by prefix range or first characters, cache hot prefixes.
- High-level design: clients debounce, API checks edge/cache, suggestion service queries in-memory trie/FST or key-value top-k lists, offline jobs build global rankings, streaming jobs update trends.
- Deep dives/bottlenecks: top-k per prefix precomputed to avoid scanning; hot prefixes like "a" cached at edge; ranking blends frequency, freshness, locale, and safety filters.
- Wrap-up: exactness is less important than latency and relevance.

## Anecdotes & war stories to use
- Google Search autocomplete is a visible example of prefix suggestions shaped by popularity, freshness, locale, and policy.
- Search engines have had to remove or demote harmful/illegal suggestions, showing safety filtering belongs in serving.
- Lucene/FST-style compact automata are widely used for efficient term dictionaries.

## Things to mention / interview tips
- Say: "I precompute top-k suggestions per prefix; serving should not scan raw query logs."
- Include client-side debounce and cancellation.
- Mention cache strategy for one-character and two-character prefixes.
- Discuss locale and safety filtering explicitly.

## Common mistakes to call out
- Querying the full database on every keystroke.
- Building only a trie and ignoring ranking.
- Forgetting hot-prefix cache skew.
- Returning stale or unsafe suggestions without filters.

## Diagrams / visuals to draw on screen
- Trie/FST with prefix `iph` and top-k list.
- Offline query-log aggregation pipeline.
- Serving path with debounce, cache, and ranking filters.

## Series glue
- Reference notification queues for async processing; point forward to caching policies that make typeahead fast. CTA: subscribe and use GitHub examples.
