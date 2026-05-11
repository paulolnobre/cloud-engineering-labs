# Env Inspector

Utility project for inspecting and displaying AWS-related environment configuration using Python.

This project demonstrates foundational cloud engineering and Python automation concepts, including:
- Environment variable inspection
- Modular utility design
- Structured logging
- JSON serialization
- Type hints
- Exception handling
- Input validation
- Reusable cloud-oriented helper functions

---

## Project Structure

```text
env_inspector/
│
├── cloud_utils.py
└── env_inspector.py
```

---

## Files Overview

### `cloud_utils.py`

Contains reusable utility functions commonly used in cloud and infrastructure workflows.

#### Features

- Generate standardized AWS resource names
- Convert S3 object sizes into human-readable format
- Generate formatted timestamps
- Validate input values
- Log operational events using module-level logger

#### Functions

| Function | Description |
|---|---|
| `get_resource_name()` | Creates standardized cloud resource names |
| `format_s3_size()` | Converts bytes into KB/MB/GB/TB/PB |
| `get_time_stamp()` | Returns current formatted timestamp |

---

### `env_inspector.py`

Main script responsible for inspecting runtime AWS environment configuration.

#### Features

- Reads AWS environment variables
- Uses reusable utility functions from `cloud_utils`
- Returns structured JSON output
- Uses logging for operational visibility
- Handles unexpected runtime errors

#### Environment Variables Used

| Variable | Purpose |
|---|---|
| `AWS_PROFILE` | AWS CLI profile name |
| `AWS_DEFAULT_REGION` | AWS default region |

---

## Example Output

```text
2026-05-09 13:01:17,582 | INFO | Generated timestamp: 2026-05-09
2026-05-09 13:01:17,582 | INFO | Environment inspection completed.
{
  "region": "unknown",
  "profile": "default",
  "timestamp": "2026-05-09"
}
```

---

## Concepts Practiced

- Python modules
- Imports
- Environment variables
- JSON serialization
- Structured logging
- Utility function design
- Reusable infrastructure tooling
- Type hints
- Exception handling
- Input validation
- Basic cloud automation concepts

---

## Technologies Used

- Python 3
- Python Virtual Environment (`venv`)
- Standard Library
  - `os`
  - `json`
  - `logging`
  - `datetime`

---

## Future Improvements

- Add unit tests with `pytest`
- Export logs to files
- Support `.env` configuration files
- Integrate with boto3
- Add CLI support with `argparse`
- Create custom exception classes
- Package utilities into reusable modules

---

## Purpose

This project was created as a practice exercise focused on:
- cloud engineering fundamentals
- Python automation
- infrastructure tooling
- AWS-oriented scripting
- clean and maintainable code structure