# boto3 Setup Check

Verifies that boto3 is installed and AWS credentials are correctly configured by calling the AWS STS `GetCallerIdentity` API.

## What it does

- Connects to AWS using the credentials configured on the machine
- Retrieves and prints the Account ID, User ARN, User ID, and active region
- Logs errors if credentials are missing or the request fails

## Requirements

- Python 3.x
- `boto3` installed (`pip install boto3`)
- AWS credentials configured via one of:
  - `~/.aws/credentials`
  - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
  - IAM role (if running on EC2 or Lambda)

## Usage

```bash
python boto3_setup_check.py
```

## Example Output

```
Account: 123456789012
User ARN: arn:aws:iam::123456789012:user/paulo-dev
User ID: AIDARABGFVH6AGEWB5UGL
Region: us-east-1
```

## Error Handling

| Exception | Cause | Action |
|---|---|---|
| `NoCredentialsError` | No credentials found | Logs error, returns `None` |
| `ClientError` | AWS rejected the request | Logs error with details, returns `None` |
