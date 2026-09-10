# tagging_cleanup

Audits EC2 tag compliance and terminates long-stopped instances using `boto3`. Shared helpers live in `../utils/`.

## Files

### `tag_enforcer.py`
Fetches all EC2 instances and flags those missing required tags.

```bash
python -m pytest stage_2/tests -v
```

`tag_enforcer.py` is currently an importable audit module rather than a standalone command. The focused test suite demonstrates its use with simulated EC2 responses and makes no AWS calls.

| Function | Description |
|---|---|
| `get_instances(client)` | Paginates through all EC2 instances and returns them as a list |
| `audit_tags(instances)` | Checks each instance for required tags and returns a list of non-compliant IDs |

**Constants:**

| Constant | Value | Description |
|---|---|---|
| `REQUIRED_TAGS` | `["Name", "Environment", "Owner"]` | Tags every instance must have |

---

### `cleanup.py`
Fetches stopped EC2 instances and terminates those that have been stopped longer than a configurable threshold.

```bash
python -m stage_2.tagging_cleanup.cleanup
```

| Function | Description |
|---|---|
| `get_stopped_instances(client)` | Paginates all instances in `stopped` state and returns them |
| `get_instance_age(instance)` | Estimates age from `StateTransitionReason`, falls back to `LaunchTime`, and returns `0` when neither is usable |
| `terminate_instance(client, instance_id)` | Terminates a single instance by ID |

**`__main__` flow:**

```
get_stopped_instances
        ↓
  for each instance
        ↓
  get_instance_age  ──→  age < MAX_STOPPED_DAYS  →  skip
        ↓
  age >= MAX_STOPPED_DAYS
        ↓
  terminate_instance
```

**Constants (`__main__`):**

| Constant | Default | Description |
|---|---|---|
| `MAX_STOPPED_DAYS` | `7` | Instances stopped longer than this are terminated |
| `DRY_RUN` | `True` | Logs eligible termination actions without calling `TerminateInstances` |

## Requirements

- Python 3.10+
- `boto3`
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)
- IAM permissions: `ec2:DescribeInstances`, `ec2:TerminateInstances`

## Configuration, cost, and safety

`tag_enforcer.py` checks `Name`, `Environment`, and `Owner` using the boto3 client supplied by its caller. The executable cleanup example targets `us-east-1`, considers only stopped instances tagged `Environment=dev`, uses `MAX_STOPPED_DAYS`, and defaults to `DRY_RUN = True`.

Run cleanup once in dry-run mode, review every instance ID, its tags, and its data, and only then consider setting `DRY_RUN = False`. EC2 termination is irreversible and attached EBS volumes marked for deletion can be lost. Stopped EC2 instances can still incur EBS and other attached-resource charges.

The cleanup operation is itself the resource-removal path; it does not create AWS resources. If a termination call fails, inspect the logged instance ID and resolve it manually only after confirming ownership.

## Tests

The focused suite verifies tag decisions, paginator handling, and the dry-run safety boundary with mock clients:

```bash
python -m pytest stage_2/tests -v
```
