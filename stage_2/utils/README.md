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
