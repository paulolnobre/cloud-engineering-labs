# iam_automation

Manages the IAM user and policy lifecycle using `boto3`: create, attach, detach, and delete. Shared helpers live in `../utils/`.

## Files

### `iam_manager.py`
Provides functions covering the full IAM lifecycle and a `__main__` block that runs a live end-to-end test.

```bash
python -m stage_2.iam_automation.iam_manager
```

| Function | Description |
|---|---|
| `create_iam_user(client, user_name)` | Creates a new IAM user |
| `create_policy(client, policy_name, policy_document)` | Creates a new IAM policy from a dict and returns the response (including the policy ARN) |
| `attach_policy_to_user(client, user_name, policy_arn)` | Attaches an existing policy to a user |
| `detach_policy_from_user(client, user_name, policy_arn)` | Detaches a policy from a user |
| `delete_iam_user(client, user_name)` | Deletes an IAM user |

**`__main__` lifecycle test:**

```
create_iam_user
      ↓
create_policy  ──→  policy_arn (from response)
      ↓
attach_policy_to_user
      ↓
detach_policy_from_user
      ↓
delete_policy  (direct client call)
      ↓
delete_iam_user
```

Creates user `test-paulo-dev` and a minimal S3 read policy (`s3:GetObject`, `s3:ListBucket`), attaches and detaches it, then cleans up both the policy and the user. Any `ClientError` is caught and logged without re-raising.

> The policy ARN is not known until after `create_policy` — it is extracted from the response via `policy_response["Policy"]["Arn"]` and reused in the subsequent calls.

## Requirements

- Python 3.10+
- `boto3`
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)
- IAM permissions: `iam:CreateUser`, `iam:CreatePolicy`, `iam:AttachUserPolicy`, `iam:DetachUserPolicy`, `iam:DeletePolicy`, `iam:DeleteUser`

## Configuration

The executable example uses the constants `USER_NAME`, `POLICY_NAME`, and `POLICY_DOCUMENT` in `iam_manager.py`. Review the names and policy document before running. The sample policy permits only S3 read actions, but its `Resource: "*"` scope is intentionally simple for the lab and should be narrowed to specific bucket ARNs in production.

IAM is global rather than regional. Select the intended AWS account with `AWS_PROFILE` and verify it before execution:

```bash
AWS_PROFILE=lab aws sts get-caller-identity
AWS_PROFILE=lab python -m stage_2.iam_automation.iam_manager
```

## Cost, security, and cleanup

IAM users and customer-managed policies do not normally create direct service charges, but mistakes can grant account-wide access. Use a sandbox account, least-privilege credentials, and never create access keys for the temporary user.

The normal script flow detaches and removes the policy and user. If an API error interrupts the flow, inspect and remove leftovers in dependency order:

```bash
aws iam list-attached-user-policies --user-name test-paulo-dev
aws iam detach-user-policy --user-name test-paulo-dev --policy-arn POLICY_ARN
aws iam delete-policy --policy-arn POLICY_ARN
aws iam delete-user --user-name test-paulo-dev
```

Confirm the user and policy names/ARN before deletion.
