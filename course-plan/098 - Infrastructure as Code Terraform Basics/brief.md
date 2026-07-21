# Infrastructure as Code: Terraform Basics

| | |
|---|---|
| **Publish order** | 098 |
| **Course #** | 76 |
| **Module** | M07 — Cloud & Infrastructure |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `terraform infrastructure as code` |
| **Demand** | Moderate |

**Thumbnail text idea:** CLOUD IN GIT
**One-line hook (first 15s):** Terraform is not just scripts for AWS; it is a desired-state graph, a state file, and a reviewable process for infrastructure.

## Learning objectives
- Explain providers, resources, modules, plan/apply, and state.
- Describe Terraform’s dependency graph from references.
- Handle remote state, locking, drift, secrets, and environments.
- Use IaC as a signal for repeatability and disaster recovery.

## Topics & items to cover
- Hook: if rebuilding production requires console clicking, recovery is tribal knowledge.
- Definition: IaC stores cloud resources as versioned configuration and reconciles real infrastructure to declared state.
- Worked example: VPC, two public subnets, two private subnets, ALB, autoscaling group, and RDS; references make Terraform create networking before target groups and ASG attachments.
- How it works: provider reads APIs -> compare config, state, and reality -> `plan` shows create/update/destroy -> `apply` runs with a state lock -> state records IDs.
- Tradeoffs: repeatability/reviewability versus sensitive state, provider bugs, slow applies, and painful refactors.
- Real-world usage: landing zones, IAM, DNS, Kubernetes clusters, observability stacks, DR environments.
- Interview sentence: “I keep infrastructure declarative, remote locked state, CI-reviewed plans, and back-port any emergency console change.”
- Recap: IaC is source control plus stateful reconciliation.

## Anecdotes & war stories to use
- Terraform became popular because teams needed one workflow across many providers.
- Manual console drift often causes surprise later when `apply` reconciles code against reality.
- S3 plus DynamoDB locking is a common AWS remote-state pattern.
- Policy-as-code catches public buckets, broad IAM, or missing tags before apply.

## Things to mention / interview tips
- Protect state because it contains production metadata and may expose secrets.
- Use modules for repeatable patterns, not every tiny resource.
- Separate dev/stage/prod with accounts/projects and careful workspaces.
- Treat plan output like an application diff.

## Common mistakes to call out
- Committing local state files.
- Running applies from laptops with no lock/audit.
- Importing resources without dependency understanding.
- Using Terraform for high-churn application data.

## Diagrams / visuals to draw on screen
- Config/state/cloud API comparison triangle.
- Dependency graph: VPC -> subnets -> ALB -> ASG.
- CI pipeline: fmt, validate, plan, policy, apply.
- Drift example detected in plan.

## Series glue
- Connect to blue-green environments created reproducibly. Next: hybrid/edge, where provisioning gets harder across locations. CTA: subscribe and clone GitHub Terraform skeletons.
