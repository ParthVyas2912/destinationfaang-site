# Design an Auto-Scaling ML Pipeline

| | |
|---|---|
| **Publish order** | 124 |
| **Course #** | 125 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~32 min |
| **Primary search keyword** | `design ml pipeline` |
| **Demand** | Moderate |

**Thumbnail text idea:** ML PIPELINE
**One-line hook (first 15s):** An auto-scaling ML pipeline is a factory: ingest data, train, validate, deploy, monitor, and roll back without waking humans for every run.
## Learning objectives
- Design an end-to-end ML training and deployment pipeline.
- Autoscale batch training, feature generation, and inference separately.
- Include model registry, validation gates, and rollback.
- Explain cost and reliability controls for ML workloads.

## Topics & items to cover
- **Requirements:** ingest training data, compute features, train models, evaluate, deploy to online serving, monitor drift; support scheduled and triggered retraining.
- **Estimation:** daily 500GB feature build, weekly full retrain, hourly incremental jobs; GPU training jobs burst, inference is steady.
- **API/Data model:** `POST /training-jobs`, `GET /models/{id}`, `POST /deployments`; entities `DatasetVersion`, `FeatureSet`, `TrainingJob`, `ModelArtifact`, `EvaluationReport`, `Deployment`; shard job metadata by `project_id`, store artifacts in object storage.
- **High-level design:** orchestrator → data validation → feature pipeline → training cluster → model registry → eval gate → canary deployment → monitoring/drift alerts.
- **Deep dives/bottlenecks:** autoscale workers by queue depth and resource labels; reproducibility via dataset/model/prompt versions; safe deployment through shadow/canary and automatic rollback on latency/quality regression.
- **Wrap-up:** separate control plane from compute plane; optimize for reproducibility and cost.

## Anecdotes & war stories to use
- Google’s TFX popularized pipeline components for validation, transform, training, and serving.
- Uber Michelangelo demonstrated centralized ML lifecycle management across many teams.
- Kubernetes-based ML platforms like Kubeflow arose because training workloads have bursty resource needs.
- Model incidents often come from data drift, not failed code deployments.

## Things to mention / interview tips
- Say “model registry is the source of truth for what is deployed.”
- Version data, features, code, hyperparameters, and artifacts together.
- Include spot/preemptible workers only for checkpointable jobs.
- Define rollback on both technical and model-quality metrics.

## Common mistakes to call out
- Autoscaling training and inference as if they were the same workload.
- Deploying the newest model without an evaluation gate.
- Losing reproducibility by overwriting datasets/artifacts.
- Ignoring drift after launch.

## Diagrams / visuals to draw on screen
- ML lifecycle pipeline from data to monitoring.
- Model registry with stages: candidate, staging, production, archived.
- Autoscaling compute pools for CPU, GPU, and inference.

## Series glue
- Builds on feature stores, Airflow/Temporal, and inference scaling; next is video processing. CTA: subscribe and use the repo’s ML pipeline diagram.
