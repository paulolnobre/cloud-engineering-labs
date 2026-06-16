# iam-automation

Manages the IAM user and policy lifecycle using `boto3`: create, attach, detach, and delete. Shared helpers live in `../utils/`.

## Files

### `iam_manager.py`
Provides functions covering the full IAM lifecycle and a `__main__` block that runs a live end-to-end test.

```bash
python iam_manager.py
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
