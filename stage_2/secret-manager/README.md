# secret-manager

CRUD wrapper for AWS Secrets Manager using `boto3`. Stores and retrieves secrets as JSON-serialised dicts. Shared helpers live in `../utils/`.

## Files

### `secret_manager.py`
Provides four functions covering the full secret lifecycle (create, read, update, delete) and a `__main__` block that runs a live end-to-end test against `us-east-1`.

```bash
python stage_2/secret-manager/secret_manager.py
```

| Function | Description |
|---|---|
| `create_secret(client, name, value)` | Creates a new secret, serialising `value` as JSON |
| `get_secret(client, name)` | Retrieves a secret and returns its parsed dict |
| `update_secret(client, name, value)` | Overwrites an existing secret's value |
| `delete_secret(client, name, force, recovery_window)` | Deletes a secret, optionally bypassing the recovery window |

**`delete_secret` parameters:**

| Parameter | Default | Description |
|---|---|---|
| `force` | `False` | If `True`, deletes immediately with no recovery window (use for test secrets to avoid billing) |
| `recovery_window` | `7` | Days before permanent deletion (7–30). Ignored when `force=True` |

**`__main__` lifecycle test:**

Creates `test/converge/db` with initial credentials, retrieves and logs it, updates the password, retrieves again, then force-deletes the secret. Any `ClientError` is caught and logged without re-raising.

## Requirements

- Python 3.10+
- `boto3`
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)
- IAM permissions: `secretsmanager:CreateSecret`, `GetSecretValue`, `UpdateSecret`, `DeleteSecret`

## Configuration

The executable example uses `us-east-1` and the constants `SECRET_NAME`, `INITIAL_VALUE`, and `UPDATED_VALUE` in `secret_manager.py`. The included values are disposable examples only. Never place production credentials or real secrets in source code, logs, screenshots, or shell history.

Choose the account/profile explicitly when needed:

```bash
AWS_PROFILE=lab python stage_2/secret-manager/secret_manager.py
```

## Cost, security, and cleanup

Secrets Manager charges for stored secrets and API operations under current AWS pricing. The example logs the retrieved sample value and therefore must not be reused for real secrets.

The normal flow force-deletes the test secret to avoid leaving it billable. If the script stops before cleanup, remove the disposable secret explicitly:

```bash
aws secretsmanager delete-secret \
  --secret-id test/converge/db \
  --force-delete-without-recovery \
  --region us-east-1
```

Forced deletion is irreversible and can take time to complete. For non-lab secrets, use a recovery window instead.
