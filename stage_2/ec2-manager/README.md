# ec2-manager

Modules for managing and auditing EC2 instances using `boto3`. Shared helpers live in `../utils/`.

## Files

### `ec2_manager.py`
Queries running instances, logs their ID and Name tag, and stops the first one found (test mode).

```bash
PYTHONPATH=stage_2 python stage_2/ec2-manager/ec2_manager.py
```

| Function | Description |
|---|---|
| `get_instances_by_state(state, client)` | Returns all instances matching a given state |
| `stop_instance(instance_id, client)` | Stops an instance and logs the state transition |

---

### `ec2_lifecycle.py`
Full instance lifecycle: launch → wait → log → stop → terminate (optional).

```bash
PYTHONPATH=stage_2 python stage_2/ec2-manager/ec2_lifecycle.py
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
PYTHONPATH=stage_2 python stage_2/ec2-manager/ec2_auditor.py
```

| Function | Description |
|---|---|
| `get_ec2_client()` | Creates and returns a boto3 EC2 client |
| `audit_instances(instances, state)` | Logs instance details and warns on missing tags |

## Requirements

- Python 3.10+
- `boto3`
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)
- IAM permissions appropriate to the selected script: `ec2:DescribeInstances` for audit; additionally `ec2:StopInstances`, `ec2:RunInstances`, `ec2:CreateTags`, and `ec2:TerminateInstances` for lifecycle operations

## Configuration

These learning scripts currently keep configuration as constants in code. Review them before execution:

- `ec2_manager.py` uses `us-east-1` and **stops the first running instance it finds**;
- `ec2_lifecycle.py` uses `REGION`, `AMI_BY_REGION`, `TERMINATE`, and placeholder values for `KeyName`, `SecurityGroupIds`, and `SubnetId`;
- `ec2_auditor.py` uses `us-east-1` and is read-only.

Replace placeholders only with resources from an isolated lab environment. Do not run `ec2_manager.py` in an account where “first running instance” is not a safe selection rule.

## Cost, security, and cleanup

The auditor only reads inventory. The manager can stop an existing instance, and the lifecycle script can create an EC2 instance and EBS volume; stopped instances can still incur EBS charges. A public IP, data transfer, or instance runtime may also be billable under current AWS pricing.

Keep `TERMINATE = False` until you have verified the full flow. After a lifecycle run, record the instance ID and explicitly inspect it:

```bash
aws ec2 describe-instances --instance-ids i-REPLACE_ME --region us-east-1
aws ec2 terminate-instances --instance-ids i-REPLACE_ME --region us-east-1
```

Termination is destructive. Confirm that the ID belongs to this lab and that no required data remains on its volumes.

## Tests

Shared EC2 governance and cleanup safeguards are covered by the focused Stage 2 suite:

```bash
python -m pytest stage_2/tests -v
```
