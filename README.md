# cloud-python

Structured Python learning repository focused on Cloud Engineering, AWS automation, and infrastructure tooling.

This repository documents a progressive journey from Python fundamentals to real-world cloud automation and AWS-based development.

The projects are organized into stages covering:
- Python scripting fundamentals
- Infrastructure-oriented utilities
- AWS automation concepts
- Error handling and validation
- JSON and file processing
- Logging and operational tooling
- Future boto3 and serverless workflows

---

## Repository Structure

```text
cloud-python/
│
├── stage_1/
│   ├── aws_naming/
│   ├── ec2-audit/
│   ├── ec2-cost-report/
│   ├── ec2-tag-audit/
│   ├── env_inspector/
│   ├── error_handler/
│   └── file-io/
│
├── stage_2/
│   ├── boto3_setup/
│   ├── ec2-manager/
│   ├── iam-automation/
│   ├── s3-automation/
│   ├── secret-manager/
│   ├── security-groups/
│   ├── tagging-cleanup/
│   └── utils/
│
├── requirements.txt
└── README.md
```

---

## Stage 1 — Core Python for Cloud Engineering

Stage 1 focuses on building strong Python foundations applied to cloud and infrastructure scenarios.

| Project | Concepts Practiced |
|---|---|
| `aws_naming` | Functions, reusable naming utilities |
| `ec2-audit` | Lists, loops, EC2 filtering |
| `ec2-cost-report` | Dictionaries, cost calculation |
| `ec2-tag-audit` | Tag validation and infrastructure auditing |
| `env_inspector` | Environment variables, logging, JSON output |
| `error_handler` | Exception handling and simulated AWS API errors |
| `file-io` | JSON parsing and report generation |

---

## Stage 2 — AWS Automation with boto3

Stage 2 focuses on real AWS interactions using the boto3 SDK, EC2 lifecycle management, S3 operations, and security group auditing.

| Project | Concepts Practiced |
|---|---|
| `boto3_setup` | boto3 installation and connectivity verification |
| `ec2-manager` | EC2 lifecycle management, auditing, and automation |
| `iam-automation` | IAM user and policy lifecycle (create, attach, detach, delete) |
| `s3-automation` | S3 bucket operations and file management |
| `secret-manager` | Secrets Manager CRUD — create, retrieve, update, and delete secrets |
| `security-groups` | Security group auditing and open CIDR detection |
| `tagging-cleanup` | Tag compliance auditing and automated termination of long-stopped dev instances |
| `utils` | Shared EC2 utilities and logging configuration |

---

## Technologies Used

- Python 3.13
- Python Virtual Environments (`venv`)
- Git & GitHub
- AWS CLI concepts
- AWS Free Tier

---

## Engineering Concepts Practiced

- Modular code organization
- Utility function design
- Logging
- Exception handling
- Type hints
- Input validation
- JSON serialization
- Environment variable management
- Infrastructure-oriented scripting
- Git branching and version control workflows

---

## Roadmap

### Stage 1 — Core Python for Cloud Engineering
- Python fundamentals
- Infrastructure scripting
- File handling
- Logging and validation

### Stage 2 — AWS Automation with boto3
- EC2 automation
- S3 operations
- IAM user and policy management
- Secrets Manager lifecycle
- Tag compliance auditing and automated cleanup
- Security group auditing

### Stage 3 — Serverless and Lambda
- AWS Lambda
- Event-driven workflows
- API Gateway
- Scheduled automation

### Stage 4 — AI Agents on AWS
- AI automation workflows
- AWS-hosted agents
- LLM integrations
- Event orchestration

### Stage 5 — CI/CD and Infrastructure as Code
- GitHub Actions
- Terraform
- Docker
- Deployment pipelines

---

## Purpose

This repository was created as a practical learning portfolio focused on:
- Cloud Engineering
- AWS Solutions Architecture
- Python automation
- Infrastructure tooling
- Backend operational scripting
