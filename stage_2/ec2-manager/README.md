# EC2 Manager

Utilities for managing the full lifecycle of EC2 instances using `boto3`. Split across two modules:

- **`ec2_manager.py`** — query, stop, and tag existing instances
- **`ec2_lifecycle.py`** — launch, wait, log, stop, and optionally terminate instances

Shared helpers live in `../utils/ec2_utils.py`.

## Modules

### `ec2_manager.py`

| Function | Description |
|---|---|
| `get_instances_by_state(state, client)` | Returns all instances matching a given state (`"running"`, `"stopped"`, etc.) |
| `stop_instance(instance_id, client)` | Stops an instance and logs the state transition |
| `tag_instances(instance_ids, tags, client)` | Applies a dict of tags to one or more instances |

```bash
python ec2_manager.py
```

### `ec2_lifecycle.py`

Full instance lifecycle in sequence:

| Function | Description |
|---|---|
| `launch_instance(ec2_client)` | Launches a `t2.micro` with tags and returns its ID |
| `log_instance_details(ec2_client, instance_id)` | Logs ID, public IP, and state |
| `terminate_with_dry_run(ec2_client, instance_id)` | Terminates using a dry-run permission pre-check |

**Config flags** (top of file):

| Flag | Default | Description |
|---|---|---|
| `REGION` | `"us-east-1"` | Target AWS region |
| `TERMINATE` | `False` | Set to `True` to terminate after stopping |

```bash
python ec2_lifecycle.py
```

## Requirements

- Python 3.10+
- `boto3`
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)

## Notes

- `KeyName`, `SecurityGroupIds`, and `SubnetId` in `ec2_lifecycle.py` are placeholders — replace with real values before running.
- `TERMINATE = False` by default — billing-safe until explicitly enabled.
