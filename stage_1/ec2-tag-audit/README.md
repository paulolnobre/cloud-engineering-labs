# EC2 Instance Audit Script

## Overview

This Python script simulates a basic AWS EC2 infrastructure audit.  
It processes a list of EC2 instance dictionaries, extracts metadata, validates tags, and generates a simple audit report.

The script demonstrates practical usage of:

- Lists and dictionaries
- Nested dictionary access
- Type hints
- Loops
- Conditional logic
- Counters
- Default values with `.get()`
- Basic reporting and auditing logic

This is a beginner-friendly cloud automation example inspired by real-world AWS operational tasks.

---

## Features

- Iterates through multiple EC2 instances
- Displays instance metadata
- Counts running and stopped instances
- Detects missing `owner` tags
- Detects missing `env` tags
- Generates a final audit report

---

## Technologies Used

- Python 3
- Basic data structures
- Type hints

---

## Code Structure

### EC2 Instance Dataset

The script starts with a list of dictionaries representing EC2 instances:

```python
ec2_instances: list[dict]
```

Each instance contains:

- `id`
- `state`
- `region`
- `tags`

Example:

```python
{
    "id": "i-001",
    "state": "running",
    "region": "us-west-1",
    "tags": {
        "env": "production",
        "owner": "team-a"
    }
}
```

---

## Audit Logic

The script performs the following checks:

### 1. Instance Status Count

Tracks how many instances are:

- Running
- Stopped

---

### 2. Tag Validation

Checks if instances are missing:

- `owner`
- `env`

Missing values are replaced with:

```python
"N/A"
```

using:

```python
tags.get("owner", "N/A")
```

---

### 3. Reporting

Prints detailed instance information:

```text
ID: i-001 | State: running | Region: us-west-1 | Env: production | Owner: team-a
```

Then generates a summary report:

```text
=== Audit Report ===
Running:       4
Stopped:       2
Missing owner: ['i-002', 'i-004']
Missing env:   ['i-003']
```

---

## Learning Objectives

This project helps practice:

- Iterating through nested data structures
- Working with cloud-like infrastructure data
- Defensive programming using `.get()`
- Building simple automation and auditing scripts
- Writing clean and readable Python

---

## Possible Improvements

Future enhancements could include:

- Exporting reports to JSON or CSV
- Using classes/dataclasses
- Integrating with real AWS APIs using Boto3
- Filtering by region or environment
- Logging support
- Exception handling
- Unit tests with `pytest`

---

## Example Use Cases

- Cloud inventory auditing
- Infrastructure validation
- Tag compliance checking
- Learning AWS automation concepts
- Python practice for DevOps/Cloud Engineering



