# EC2 Error Handler

Utility script that simulates and handles the most common AWS API errors
encountered when operating EC2 instances via boto3.

## What it does

- Validates EC2 instance ID format before making API calls
- Handles permission errors (IAM policy violations)
- Handles resource not found errors
- Returns structured output for each failure type

## Error types covered

| Error | Trigger | Real AWS equivalent |
|---|---|---|
| `ValueError` | Empty instance ID | Client-side validation before API call |
| `PermissionError` | Unauthorized instance ID | `AccessDeniedException` from IAM |
| `LookupError` | Invalid ID format | `InvalidInstanceID.NotFound` from EC2 |

## Sample output

    [INVALID INPUT] Instance ID cannot be empty
    [ACCESS DENIED] Check your IAM policy. Detail: Not authorized: ec2:DescribeInstances
    [NOT FOUND] Instance not found: x-9999
    [OK] Instance state: running

