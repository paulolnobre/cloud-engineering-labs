# Cloud Engineering Labs

Hands-on labs for building practical skills across Cloud Engineering, Infrastructure Engineering, and Platform Engineering.

This repository documents a progressive journey from focused scripts to reproducible, observable, and cost-aware cloud environments and systems. Python remains an important part of that journey: it is used for automation, auditing, validation, and operational tooling, but as one tool within a broader cloud engineering stack that also includes infrastructure as code, containers, CI/CD, networking, security, and observability.

Stages 1 and 2 contain the projects currently implemented in this repository. Stages 3 through 8 describe the planned direction and do not represent completed deliverables.

## Repository Structure

```text
cloud-engineering-labs/
├── stage_1/
│   ├── aws_naming/
│   ├── ec2-audit/
│   ├── ec2-cost-report/
│   ├── ec2-tag-audit/
│   ├── env_inspector/
│   ├── error_handler/
│   └── file-io/
├── stage_2/
│   ├── boto3_setup/
│   ├── ec2-manager/
│   ├── iam-automation/
│   ├── s3-automation/
│   ├── secret-manager/
│   ├── security-groups/
│   ├── tagging-cleanup/
│   └── utils/
├── requirements.txt
└── README.md
```

## Stage 1 — Core Python for Cloud Engineering

Stage 1 establishes Python foundations through cloud and infrastructure scenarios. The labs use simulated infrastructure data and local utilities to practice automation patterns before interacting with live cloud resources.

| Project | Focus |
|---|---|
| [`aws_naming`](stage_1/aws_naming/) | Standardized AWS resource names, ARN construction, and input validation |
| [`ec2-audit`](stage_1/ec2-audit/) | EC2 inventory simulation, state counts, and missing-tag detection |
| [`ec2-cost-report`](stage_1/ec2-cost-report/) | EC2 cost calculation and formatted status reporting |
| [`ec2-tag-audit`](stage_1/ec2-tag-audit/) | Infrastructure metadata inspection and tag compliance auditing |
| [`env_inspector`](stage_1/env_inspector/) | Environment variables, reusable utilities, structured logging, and JSON output |
| [`error_handler`](stage_1/error_handler/) | Input validation and handling of simulated AWS API failures |
| [`file-io`](stage_1/file-io/) | JSON configuration, EC2 data filtering, and report generation |

## Stage 2 — AWS Automation with boto3

Stage 2 moves from simulated data to AWS API interactions with `boto3`. These labs cover resource lifecycle operations, security checks, governance, shared tooling, and cleanup practices. Some scripts can create, modify, or delete AWS resources and should be reviewed before use in a live account.

| Project | Focus |
|---|---|
| [`boto3_setup`](stage_2/boto3_setup/) | AWS credential and connectivity verification through STS |
| [`ec2-manager`](stage_2/ec2-manager/) | EC2 lifecycle management, state filtering, and instance auditing |
| [`iam-automation`](stage_2/iam-automation/) | IAM user and policy creation, attachment, detachment, and cleanup |
| [`s3-automation`](stage_2/s3-automation/) | S3 bucket and object operations, bucket policies, and lifecycle rules |
| [`secret-manager`](stage_2/secret-manager/) | AWS Secrets Manager create, retrieve, update, and delete workflows |
| [`security-groups`](stage_2/security-groups/) | Inbound-rule auditing, open CIDR detection, and sensitive-port checks |
| [`tagging-cleanup`](stage_2/tagging-cleanup/) | EC2 tag compliance and cleanup of long-stopped development instances |
| [`utils`](stage_2/utils/) | Shared EC2 helpers and centralized logging configuration |

## Current Technology and Engineering Focus

- Python 3 and virtual environments
- AWS and `boto3`
- Automation and operational tooling
- Resource lifecycle and cost awareness
- Infrastructure auditing, tagging, and governance
- IAM, secrets, networking security, and least-privilege concepts
- Logging, exception handling, type hints, and input validation
- Git and GitHub workflows

## Roadmap

The following stages are planned labs. Their tools and infrastructure are not yet included in this repository.

### Stage 3 — Infrastructure as Code

- Terraform
- VPC, subnets, route tables, and Internet Gateway
- EC2, Security Groups, IAM, and S3
- Temporary labs using `terraform apply` and `terraform destroy`
- Cost controls and resource lifecycle management

### Stage 4 — Containers and Deployment

- Docker and Docker Compose
- Containerized FastAPI service
- Reverse proxy, HTTPS, and health checks
- Reproducible deployment to a VPS

### Stage 5 — CI/CD

- GitHub Actions
- Linting, tests, and Docker image builds
- Deployment pipelines

### Stage 6 — Observability

- Structured logs
- Prometheus
- Grafana
- Loki
- OpenTelemetry

### Stage 7 — Serverless and Event-Driven AWS

- Lambda
- API Gateway
- EventBridge
- SQS and SNS

### Stage 8 — Cloud Architecture Labs

- Public and private subnets
- Load Balancer and Auto Scaling
- Managed databases
- High availability
- Security, resilience, and cost trade-offs

## Next Labs

1. Terraform AWS networking lab
2. Dockerized FastAPI service with Prometheus and Grafana
3. GitHub Actions CI pipeline

## Purpose

The goal of this repository is to build and demonstrate practical cloud engineering judgment: automating repeatable work, designing infrastructure that can be reproduced and operated, adding visibility into system behavior, and understanding the security, resilience, and cost trade-offs behind technical decisions.
