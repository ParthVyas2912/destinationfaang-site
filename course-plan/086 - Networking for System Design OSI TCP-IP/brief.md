# Networking for System Design: OSI & TCP/IP

| | |
|---|---|
| **Publish order** | 086 |
| **Course #** | 14 |
| **Module** | M02 — Networking & Delivery |
| **Type** | concept |
| **Target length** | ~16 min |
| **Primary search keyword** | `osi model tcp ip` |
| **Demand** | Moderate |

**Thumbnail text idea:** NETWORK MAP
**One-line hook (first 15s):** Most system design boxes talk over the network — so you need to know what can fail between them.

## Learning objectives
- Map OSI/TCP/IP layers to practical design decisions.
- Explain DNS, TCP handshake, TLS, HTTP, routing, and load balancing in one request path.
- Identify latency contributors and failure modes at each layer.
- Use networking vocabulary accurately in interviews.

## Topics & items to cover
- Hook: a slow API call may be DNS, TLS, congestion, load balancer queues, or the app.
- Definition: OSI/TCP/IP models organize how bytes move from application intent to physical transmission.
- Worked example: browser calls `api.example.com`: DNS resolves IP, TCP SYN/SYN-ACK/ACK, TLS negotiates keys, HTTP sends request, L7 load balancer routes to service, response returns.
- How it works: IP routing, ports, TCP reliability/congestion control, UDP, TLS certificates, HTTP semantics, L4 vs L7 load balancing, keep-alive.
- Tradeoffs: TCP reliability adds handshake/head-of-line costs; UDP gives control to QUIC; TLS termination centralizes certs but creates trust boundaries.
- Real-world usage: CDNs, AWS ALB/NLB, Envoy proxies, service mesh mTLS, QUIC/HTTP/3.
- Interview sentence: "I’ll separate L4 connectivity, TLS setup, and L7 request routing so we reason about latency and failure independently."
- Recap: networking is the hidden dependency in every distributed system.

## Anecdotes & war stories to use
- Google’s QUIC work led into HTTP/3 to reduce handshake latency and TCP head-of-line issues.
- Envoy emerged at Lyft to handle service-to-service networking consistently.
- CDNs such as Cloudflare and Akamai show how proximity and routing dominate latency.
- DNS or TLS certificate incidents have caused visible outages even when apps were healthy.

## Things to mention / interview tips
- Say L4 routes connections; L7 understands HTTP requests.
- Include DNS TTL and caching in failover designs.
- Mention connection reuse and TLS termination location.
- Diagnose with latency breakdowns, not "network slow."

## Common mistakes to call out
- Confusing TCP ports with application endpoints.
- Assuming DNS changes are instant.
- Ignoring TLS cost and certificate rotation.
- Choosing protocols without network implications.

## Diagrams / visuals to draw on screen
- Request path layered DNS to TCP/TLS to HTTP to app.
- L4 versus L7 load balancer diagram.
- Latency waterfall: DNS, connect, TLS, server, transfer.

## Series glue
- Starts networking/delivery after database foundations; next compares HTTP/3, gRPC, and WebSockets. CTA: subscribe and use repo network diagrams.
