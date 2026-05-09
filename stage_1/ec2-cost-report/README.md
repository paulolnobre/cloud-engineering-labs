# EC2 Cost Report

A Python script that generates a formatted cost and status report for EC2 instances.

## What it does

- Lists EC2 instances with their ID, state, region, and monthly cost
- Generates a summary with total monthly cost and running vs stopped instance count

## Usage

```bash
python ec2-cost-report.py
```

## Sample Output

```
ID         State      Region             Monthly Cost
======================================================
i-001      running    us-west-1               $120.50
i-002      stopped    us-west-1                 $0.00
i-003      running    us-east-1                $85.25
i-004      running    us-east-1               $150.00
i-005      stopped    us-west-2                 $0.00
i-006      running    us-west-2               $200.75
======================================================
                   === Summary ===
------------------------------------------------------
  Total Monthly Cost:             $556.50
  Running Instances:                    4
  Stopped Instances:                    2
======================================================
```

## Stage

Stage 1 — Core Python for Cloud Scripting
