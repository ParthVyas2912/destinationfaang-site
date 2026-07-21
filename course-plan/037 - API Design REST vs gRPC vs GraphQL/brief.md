# API Design: REST vs gRPC vs GraphQL

| | |
|---|---|
| **Publish order** | 037 |
| **Course #** | 44 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~20 min |
| **Primary search keyword** | `rest vs grpc vs graphql` |
| **Demand** | High |

**Thumbnail text idea:** PICK THE API
**One-line hook (first 15s):** REST, gRPC, and GraphQL are not religions—they’re tools with different failure modes, latency profiles, and client contracts.

## Learning objectives
- Compare REST, gRPC, and GraphQL for real system design use cases.
- Explain transport, schema, versioning, caching, and observability implications.
- Pick the right API style for mobile apps, internal services, and public platforms.
- State interview-ready tradeoffs without sounding dogmatic.

## Topics & items to cover
- **Hook:** the same `GetOrder` call can be a cacheable URL, a protobuf RPC, or a client-shaped graph query.
- **Definition:** REST models resources over HTTP; gRPC models typed service calls over HTTP/2 using protobuf; GraphQL lets clients request a typed graph shape from one endpoint.
- **Worked example:** mobile order screen needs order, items, driver, ETA. REST might call `/orders/123` plus subresources or a BFF endpoint. gRPC internal `OrderService.GetOrderSummary` returns protobuf in one low-latency call. GraphQL query requests exactly `order{id,total,driver{name},eta}` but needs resolver batching to avoid N+1.
- **Tradeoffs:** REST is simple and cache-friendly; gRPC is fast and strongly typed but less browser-native; GraphQL reduces over/under-fetching but shifts complexity to schema governance and resolvers.
- **Real-world usage:** public CRUD APIs often REST; microservice RPC often gRPC; product clients at GitHub/Shopify/Meta use GraphQL-style APIs.
- **Interview sentence:** “I’d expose REST/GraphQL at the product boundary and use gRPC for high-volume internal service-to-service calls.”
- **Recap:** choose by client needs, operational tooling, and evolution model.

## Anecdotes & war stories to use
- Google open-sourced gRPC from internal RPC patterns, making protobuf contracts common in microservices.
- GitHub’s public GraphQL API is a well-known example of client-shaped queries over a rich domain graph.
- Shopify uses GraphQL heavily for commerce APIs, showing schema governance at public API scale.
- REST’s HTTP caching and CDN compatibility remain powerful for public, resource-oriented APIs.

## Things to mention / interview tips
- Mention backward-compatible schema evolution: add fields, don’t break old clients.
- For GraphQL, immediately bring up dataloader/batching and query complexity limits.
- For gRPC, mention deadlines, retries, status codes, and load balancing.
- For REST, mention idempotent methods and cache headers.

## Common mistakes to call out
- Saying GraphQL is always faster because it is one endpoint.
- Ignoring browser/proxy tooling when choosing gRPC externally.
- Designing REST verbs like `/doThing` for every action.
- Forgetting API versioning and deprecation strategy.

## Diagrams / visuals to draw on screen
- Side-by-side call flow for one order screen in REST/gRPC/GraphQL.
- GraphQL resolver tree with N+1 risk and batching fix.
- API boundary diagram: external API gateway vs internal mesh.

## Series glue
- Reference API/Data model steps from previous case studies; next API Gateway video operationalizes these choices. CTA: subscribe and pull the API examples from GitHub.
