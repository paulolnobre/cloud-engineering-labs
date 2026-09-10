# utils

Shared utilities used across `stage_2` modules. Imported as a package via `from utils.<module> import ...`.

## Files

### `ec2_utils.py`
Reusable EC2 helper functions backed by `boto3`.

| Function | Description |
|---|---|
| `get_instances_by_state(state, client)` | Returns all EC2 instances matching a given state (`"running"`, `"stopped"`, etc.) |
| `stop_instance(instance_id, client)` | Stops an instance and logs the previous → current state transition |
| `tag_instances(instance_ids, tags, client)` | Applies a `dict` of tags to one or more instances |

---

### `logging_config.py`
Centralised logging setup — ensures `basicConfig` is only called once regardless of how many modules import it.

| Function | Description |
|---|---|
| `setup_logging(level)` | Configures root logger once (idempotent) |
| `get_logger(name)` | Calls `setup_logging()` then returns a named logger |

**Usage:**
```python
from utils.logging_config import get_logger

logger = get_logger(__name__)
```

## Requirements and configuration

- Python 3.10+
- `boto3`/`botocore`
- `stage_2` available on `PYTHONPATH` when a caller does not add it itself

Example from the repository root:

```bash
PYTHONPATH=stage_2 python stage_2/ec2-manager/ec2_manager.py
```

The utilities do not select an account or Region; they use the boto3 client passed by each calling project. `logging_config.py` writes to standard output at `INFO` level by default.

## Cost, security, and tests

The package creates no resources on import. Cost and permissions depend on the client operation invoked by a caller: `get_instances_by_state` is read-only, while `stop_instance` changes instance state and `tag_instances` changes metadata. Review the calling script and selected resources before use.

Focused Stage 2 tests use mock clients and can be run without AWS credentials:

```bash
python -m pytest stage_2/tests -v
```
