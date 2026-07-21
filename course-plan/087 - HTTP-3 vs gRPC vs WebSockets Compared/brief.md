# HTTP/3 vs gRPC vs WebSockets Compared

| | |
|---|---|
| **Publish order** | 087 |
| **Course #** | 15 |
| **Module** | M02 — Networking & Delivery |
| **Type** | concept |
| **Target length** | ~16 min |
| **Primary search keyword** | `http3 grpc websockets` |
| **Demand** | High |

**Thumbnail text idea:** PICK PROTOCOL
**One-line hook (first 15s):** HTTP/3, gRPC, and WebSockets are not upgrades of each other — they solve different communication shapes.

## Learning objectives
- Compare request/response, streaming RPC, and bidirectional messaging.
- Choose HTTP/3, gRPC, WebSockets, or REST for a workload.
- Explain QUIC, Protobuf, multiplexing, and lifecycle tradeoffs.
- Design fallbacks and operations for each protocol.

## Topics & items to cover
- Hook: a chat app, payment API, and video metadata service should not all use the same protocol.
- Definition: HTTP/3 is HTTP over QUIC; gRPC is contract-based RPC commonly over HTTP/2; WebSocket is a long-lived bidirectional channel.
- Worked example: mobile feed API uses HTTP/3 for reconnects; internal recommendations use gRPC with Protobuf deadlines; live chat uses WebSockets with connection gateways and heartbeats.
- How it works: QUIC over UDP, HTTP/2 streams, Protobuf schemas, deadlines/cancellation, WebSocket upgrade, ping/pong, backpressure.
- Tradeoffs: gRPC is efficient but less browser-native; WebSockets handle realtime but need stateful scaling; HTTP/3 may face UDP blocking and ops learning curve.
- Real-world usage: Google/Cloudflare HTTP/3, Kubernetes/Envoy gRPC APIs, Slack/Discord-style realtime channels.
- Interview sentence: "I’ll choose by interaction pattern: REST/HTTP for public request-response, gRPC for typed internal RPC, WebSockets for bidirectional realtime."
- Recap: protocol choice follows traffic shape.

## Anecdotes & war stories to use
- QUIC began at Google and became the foundation of standardized HTTP/3.
- gRPC grew from Google’s internal RPC experience and is common in microservice fleets.
- WebSockets became a practical browser-native path for realtime apps before WebTransport matured.
- Envoy and service meshes made HTTP/2/gRPC observability and retries easier.

## Things to mention / interview tips
- Include deadlines/retries for gRPC; heartbeat/reconnect for WebSockets.
- Discuss proxies, load balancers, firewalls, and mobile networks.
- Use Protobuf schema compatibility for gRPC evolution.
- Separate client-facing protocol from internal protocol.

## Common mistakes to call out
- Saying gRPC is always faster without browser/ops context.
- Using WebSockets for simple polling data.
- Forgetting long-lived connections make servers stateful.
- Ignoring stream backpressure.

## Diagrams / visuals to draw on screen
- Decision table: REST/HTTP3 vs gRPC vs WebSocket.
- WebSocket gateway fanout to chat rooms.
- gRPC unary and streaming call timeline.

## Series glue
- Builds directly on networking layers; next moves to choosing the right database for data shape. CTA: subscribe and clone protocol examples.
