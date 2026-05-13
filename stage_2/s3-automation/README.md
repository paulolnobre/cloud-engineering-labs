# S3 Automation

Utility module for common Amazon S3 operations: creating buckets, uploading, listing, retrieving, and deleting objects.

---

## What it does

- Creates an S3 bucket in a specified region (handles `us-east-1` constraint automatically)
- Uploads a string payload as an S3 object
- Lists objects in a bucket, optionally filtered by prefix
- Retrieves and returns the text content of an S3 object
- Deletes an object from a bucket
- Logs all operations and errors via Python's `logging` module

---

## Functions

| Function | Description | Returns |
|---|---|---|
| `create_bucket(bucket_name, region)` | Creates an S3 bucket | `bool` |
| `upload_object(bucket_name, key, body)` | Uploads a UTF-8 string as an object | `bool` |
| `list_objects(bucket_name, prefix)` | Lists objects with key and size | `list[dict]` |
| `get_object(bucket_name, key)` | Retrieves object content as a string | `str \| None` |
| `delete_object(bucket_name, key)` | Deletes an object | `bool` |

---

## Requirements

- Python 3.10+
- `boto3` installed (`pip install boto3`)
- AWS credentials configured via one of:
  - `~/.aws/credentials`
  - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
  - IAM role (if running on EC2 or Lambda)
- IAM permissions: `s3:CreateBucket`, `s3:PutObject`, `s3:ListBucket`, `s3:GetObject`, `s3:DeleteObject`

---

## Usage

```bash
python s3_manager.py
```

---

## Example Output

```
INFO - Bucket created: paulo-dev-s3-automation
INFO - Uploaded: s3://paulo-dev-s3-automation/reports/jan.txt
INFO - Uploaded: s3://paulo-dev-s3-automation/reports/feb.txt
INFO - Found 2 object(s) in s3://paulo-dev-s3-automation/reports/
  reports/jan.txt (0.03 KB)
  reports/feb.txt (0.03 KB)
INFO - Retrieved: s3://paulo-dev-s3-automation/reports/jan.txt
Content: January AWS cost report - $142.30
INFO - Deleted: s3://paulo-dev-s3-automation/reports/jan.txt
INFO - Found 1 object(s) in s3://paulo-dev-s3-automation/reports/
Objects remaining: 1
```

---

## Error Handling

| Exception | Cause | Action |
|---|---|---|
| `ClientError` (create) | Bucket already exists, access denied | Logs error, returns `False` |
| `ClientError` (upload) | Invalid bucket, access denied | Logs error, returns `False` |
| `ClientError` (list) | Bucket not found, access denied | Logs error, returns `[]` |
| `ClientError` (get) | Object not found, access denied | Logs error, returns `None` |
| `ClientError` (delete) | Object not found, access denied | Logs error, returns `False` |
