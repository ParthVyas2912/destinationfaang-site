# Kubernetes Architecture & Scheduling Explained

| | |
|---|---|
| **Publish order** | 093 |
| **Course #** | 71 |
| **Module** | M07 — Cloud & Infrastructure |
| **Type** | concept |
| **Target length** | ~20 min |
| **Primary search keyword** | `kubernetes architecture` |
| **Demand** | Very High |

**Thumbnail text idea:** PODS NEED HOMES
**One-line hook (first 15s):** If an interviewer asks “how does Kubernetes place a pod?”, they want the control-loop story, not just “the scheduler picks a node.”

## Learning objectives
- Explain API server, etcd, scheduler, controller manager, kubelet, CNI, and kube-proxy.
- Trace `kubectl apply` until containers become Ready endpoints.
- Reason about requests, taints, affinities, topology spread, and preemption.
- Diagnose API server/etcd pressure, image-pull storms, and noisy neighbors.

## Topics & items to cover
- Hook: Kubernetes stores desired state; controllers converge reality.
- Definition: a declarative orchestration system built around API objects and reconciliation loops.
- Worked example: 30 API replicas, each 500m CPU/1Gi, across six 4CPU/8Gi nodes; scheduler filters nodes without capacity, scores by least-allocated/topology spread, then binds Pods.
- How it works: client -> API admission -> etcd -> Deployment controller -> ReplicaSet -> Pod -> scheduler bind -> kubelet pulls image -> readiness adds Service endpoint.
- Tradeoffs: bin-packing improves utilization but raises blast radius; hard anti-affinity improves resilience but strands capacity; bigger clusters stress etcd/API server.
- Real-world usage: node pools for web/GPU/batch, PDBs for maintenance, HPA/VPA, cluster autoscaler or Karpenter.
- Interview sentence: “I model Kubernetes as eventually consistent controllers around API-server/etcd, with scheduling as filter-score-bind.”
- Recap: desired state, control loops, and resource requests are the mental model.

## Anecdotes & war stories to use
- Google’s Borg paper is the public ancestor: shared clusters scheduling services and batch jobs.
- Kubernetes controllers are level-triggered, so missed events recover by re-reading current state.
- Large clusters often feel etcd latency before raw CPU saturation.
- Rollback incidents can create image-pull storms; mature teams pre-pull or stagger critical images.

## Things to mention / interview tips
- Say “requests schedule; limits enforce.”
- Readiness controls traffic; liveness restarts containers.
- Mention topology spread for multi-AZ resilience.
- For databases, discuss StatefulSets, PVs, quorum, and PDBs.

## Common mistakes to call out
- Saying the scheduler starts containers; kubelet does.
- Forgetting etcd backups and latency.
- Setting limits without meaningful requests.
- Treating Kubernetes as magic HA for stateful databases.

## Diagrams / visuals to draw on screen
- Control plane with API server, etcd, scheduler, controllers, kubelets.
- Pod lifecycle from Deployment YAML to Ready endpoint.
- Scheduler pipeline: queue -> filter -> score -> bind.
- Node capacity grid across zones.

## Series glue
- Reference earlier load balancing/autoscaling videos for Services and HPA. Next: serverless when you do not want to manage nodes. CTA: subscribe and grab YAML examples from the GitHub repo.
