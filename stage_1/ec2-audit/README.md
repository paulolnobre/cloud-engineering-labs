# EC2 Audit Script

Audit script for EC2 instances simulating AWS API responses.
Filters stopped instances, identifies high-cost running instances,
and generates instance count by state.

---

## What it does

- Iterates over a list of EC2 instances (simulated boto3 response)
- Counts running vs stopped instances
- Flags instances missing required tags (`env`, `owner`)
- Prints a formatted audit report

---

## Stack

- Python 3.x
- Context: AWS EC2 cost control and tag compliance

---

## Usage
```bash
python audit_ec2.py
```

## Sample Output
```
ID: i-001 | State: running | Region: us-west-1 | Env: production | Owner: team-a
ID: i-002 | State: stopped | Region: us-west-1 | Env: staging | Owner: N/A
...

=== Audit Report ===
Running:       4
Stopped:       2
Missing owner: ['i-002', 'i-004']
Missing env:   ['i-003']
```
