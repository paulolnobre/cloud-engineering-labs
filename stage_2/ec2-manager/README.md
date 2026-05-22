# EC2 Manager

A Python script for managing EC2 instances using `boto3`. Provides utilities to query instances by state, stop instances, and apply tags.

## Functions

### `get_instances_by_state(state, client)`
Returns all EC2 instances matching a given state (e.g. `"running"`, `"stopped"`).

### `stop_instance(instance_id, client)`
Stops a single EC2 instance and logs the previous/current state transition.

### `tag_instances(instance_ids, tags, client)`
Applies a dictionary of tags to one or more EC2 instances.

## Usage

```bash
python ec2_manager.py
```

The `main()` function connects to `us-east-1`, lists all running instances, logs their IDs and Name tags, and stops the first running instance found (for testing purposes).

## Requirements

- Python 3.10+
- `boto3`
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)

## Notes

- The stop operation in `main()` is marked **TEST ONLY** — it stops the first running instance found. Remove or guard it before using in production.
