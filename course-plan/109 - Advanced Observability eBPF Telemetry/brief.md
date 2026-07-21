# Advanced Observability: eBPF & Telemetry

| | |
|---|---|
| **Publish order** | 109 |
| **Course #** | 68 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `ebpf observability` |
| **Demand** | Moderate |

**Thumbnail text idea:** SEE THE KERNEL
**One-line hook (first 15s):** When application metrics stop at “timeout,” eBPF can show the kernel-level network, disk, and syscall behavior underneath.

## Learning objectives
- Explain what eBPF is and why it is useful for observability.
- Identify telemetry eBPF can collect: syscalls, TCP, DNS, files, containers.
- Compare eBPF visibility with app instrumentation.
- Understand safety, overhead, and operational constraints.

## Topics & items to cover
- Hook: sometimes the app code is innocent and the real issue is packet drops, DNS latency, or kernel throttling.
- Definition: eBPF lets verified programs run safely in the Linux kernel to observe or influence events without custom kernel modules.
- Worked example: checkout latency spikes; traces show DB call slow, but eBPF TCP telemetry shows retransmits between app nodes and DB subnet, plus DNS lookup delays during resolver saturation.
- How it works: eBPF program attaches to kprobes/tracepoints/socket hooks -> verifier checks safety -> maps export events -> agent correlates PID/container/pod/service -> backend visualizes flows.
- Tradeoffs: deep visibility with little app change versus kernel/version constraints, privileged agents, data volume, and need for expert interpretation.
- Real-world usage: Cilium networking, Pixie observability, Falco runtime security, Datadog/Parca profiling, Kubernetes network maps.
- Interview sentence: “I would use eBPF as complementary telemetry for kernel/network/runtime behavior, while keeping business SLIs in application instrumentation.”
- Recap: eBPF sees below the app, not inside product intent.

## Anecdotes & war stories to use
- Cilium uses eBPF for Kubernetes networking and policy, making eBPF visible to many platform teams.
- Brendan Gregg’s Linux performance work popularized tracing kernel-level bottlenecks rather than guessing.
- Falco uses kernel event streams for runtime security detection.
- Continuous profilers use low-overhead sampling to find CPU hot paths that logs never reveal.

## Things to mention / interview tips
- Say eBPF complements OpenTelemetry; it does not replace semantic spans.
- Discuss permissions and node-agent deployment carefully.
- Correlate kernel events to pod/container metadata.
- Avoid collecting payload/PII unnecessarily.

## Common mistakes to call out
- Claiming eBPF magically explains business-level failures.
- Ignoring kernel compatibility and managed-cluster restrictions.
- Running privileged agents without security review.
- Drowning teams in raw low-level events.

## Diagrams / visuals to draw on screen
- App, runtime, kernel layers with eBPF hooks.
- TCP retransmit/DNS latency timeline.
- Node agent mapping PID -> container -> pod -> service.
- eBPF plus OpenTelemetry correlation view.

## Series glue
- Build from metrics, traces, and logs into deeper telemetry. Next: FinOps, because every observability choice also has a cost. CTA: subscribe and check GitHub for the observability decision tree.
