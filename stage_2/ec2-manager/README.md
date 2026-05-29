# ec2-manager

Modules for managing and auditing EC2 instances using `boto3`. Shared helpers live in `../utils/`.

## Files

### `ec2_manager.py`
Queries running instances, logs their ID and Name tag, and stops the first one found (test mode).

```bash
python ec2_manager.py
```

| Function | Description |
|---|---|
| `get_instances_by_state(state, client)` | Returns all instances matching a given state |
| `stop_instance(instance_id, client)` | Stops an instance and logs the state transition |

---

### `ec2_lifecycle.py`
Full instance lifecycle: launch → wait → log → stop → terminate (optional).

```bash
python ec2_lifecycle.py
```

| Function | Description |
|---|---|
| `launch_instance(ec2_client)` | Launches a `t2.micro` with tags, returns instance ID |
| `log_instance_details(ec2_client, instance_id)` | Logs ID, public IP, and current state |
| `terminate_with_dry_run(ec2_client, instance_id)` | Terminates using a dry-run permission pre-check |

**Config flags:**

| Flag | Default | Description |
|---|---|---|
| `REGION` | `"us-east-1"` | Target AWS region |
| `TERMINATE` | `False` | Set to `True` to terminate after stopping |

> `KeyName`, `SecurityGroupIds`, and `SubnetId` are placeholders — replace with real values before running.

---

### `ec2_auditor.py`
Audits all running and stopped instances, flagging any missing `Name` or `Environment` tags.

```bash
python ec2_auditor.py
```

| Function | Description |
|---|---|
| `get_ec2_client()` | Creates and returns a boto3 EC2 client |
| `audit_instances(instances, state)` | Logs instance details and warns on missing tags |

## Requirements

- Python 3.10+
- `boto3`
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)
