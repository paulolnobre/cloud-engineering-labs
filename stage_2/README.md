# Stage 2 — AWS Automation with boto3

Stage 2 is complete as the repository's operational automation phase. Its labs demonstrate authenticated AWS API access, EC2 lifecycle operations, S3 and Secrets Manager workflows, IAM lifecycle management, Security Group auditing, tag governance, safe cleanup, shared logging, and reusable helpers.

The emphasis is not the number of services covered. It is the engineering practice shown across the projects: explicit configuration, least-privilege permissions, error handling, pagination, dry-run safeguards, observability, and cleanup of temporary resources.

## Projects

| Project | Demonstrated capability | Risk profile |
|---|---|---|
| [`boto3_setup`](boto3_setup/) | Credential and identity verification with STS | Read-only |
| [`ec2-manager`](ec2-manager/) | EC2 inventory, audit, stop, launch, and optional termination | Can create, stop, or terminate EC2 |
| [`iam-automation`](iam-automation/) | IAM user and managed-policy lifecycle | Changes account-level access control |
| [`s3-automation`](s3-automation/) | Bucket, object, policy, and lifecycle operations | Creates stored data and policies |
| [`secret-manager`](secret-manager/) | Secret lifecycle | Stores billable sensitive data |
| [`security-groups`](security-groups/) | Detection of publicly exposed sensitive ports | Read-only |
| [`tagging-cleanup`](tagging-cleanup/) | Tag compliance and guarded EC2 cleanup | Audit is read-only; cleanup can terminate EC2 |
| [`utils`](utils/) | Shared boto3 and logging helpers | Depends on the caller |

Read each project README before execution. Use a sandbox account or dedicated lab profile, confirm the active account and Region, and keep destructive flags in their safe defaults until the target resources have been reviewed.

## Unit tests

The focused pytest suite covers local governance and cleanup decisions without making AWS calls. AWS clients and paginators are represented by `unittest.mock` objects, while pytest supplies test discovery, assertions, and log capture.

Install the development dependency from the repository root:

```bash
python -m pip install -r requirements-dev.txt
```

From the repository root:

```bash
python -m pytest stage_2/tests -v
```

The suite intentionally does not pursue a coverage percentage. Live AWS integration behavior remains the responsibility of an isolated lab account and explicit operator review.

## Transition to Stage 3

Stage 2 answers: “How can Python automate and audit operational actions in AWS?” Stage 3 moves to: “How can infrastructure be declared, reviewed as a plan, reproduced, and destroyed consistently?”

The next implementation is [`stage_3/terraform-aws-networking-lab`](../stage_3/terraform-aws-networking-lab/), which introduces Terraform through a temporary VPC, public subnet, routing, Security Group, and EC2 lab.
