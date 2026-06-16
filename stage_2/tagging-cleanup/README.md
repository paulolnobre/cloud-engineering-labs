# tagging-cleanup

Audits EC2 tag compliance and terminates long-stopped instances using `boto3`. Shared helpers live in `../utils/`.

## Files

### `tag_enforcer.py`
Fetches all EC2 instances and flags those missing required tags.

```bash
python tag_enforcer.py
```

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
python cleanup.py
```

| Function | Description |
|---|---|
| `get_stopped_instances(client)` | Paginates all instances in `stopped` state and returns them |
| `get_instance_age(instance)` | Returns how many days an instance has been stopped; returns `0` if `StoppedAt` is unavailable |
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

## Requirements

- Python 3.10+
- `boto3`
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)
- IAM permissions: `ec2:DescribeInstances`, `ec2:TerminateInstances`
