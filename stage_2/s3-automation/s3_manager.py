import json

import boto3
from botocore.exceptions import ClientError

from utils.logging_config import get_logger

logger = get_logger(__name__)


def create_bucket(bucket_name: str, region: str = "us-east-1") -> bool:
    """Create an S3 bucket in the specified region."""
    s3 = boto3.client("s3", region_name=region)

    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region}
            )
        logger.info("Bucket created: %s", bucket_name)
        return True

    except ClientError as e:
        logger.error("Create failed: %s", e.response["Error"]["Message"])
        return False


def upload_object(bucket_name: str, key: str, body: str) -> bool:
    """Upload a string payload as an S3 object."""
    s3 = boto3.client("s3")

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=body.encode("utf-8")
        )
        logger.info("Uploaded: s3://%s/%s", bucket_name, key)
        return True

    except ClientError as e:
        logger.error("Upload failed: %s", e.response["Error"]["Message"])
        return False


def list_objects(bucket_name: str, prefix: str = "") -> list[dict]:
    """List objects in a bucket, optionally filtered by prefix."""
    s3 = boto3.client("s3")
    results = []

    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        for obj in response.get("Contents", []):
            results.append({
                "key": obj["Key"],
                "size_kb": round(obj["Size"] / 1024, 2)
            })

        logger.info("Found %d object(s) in s3://%s/%s", len(results), bucket_name, prefix)
        return results

    except ClientError as e:
        logger.error("List failed: %s", e.response["Error"]["Message"])
        return []


def get_object(bucket_name: str, key: str) -> str | None:
    """Retrieve and return the text content of an S3 object."""
    s3 = boto3.client("s3")

    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        content = response["Body"].read().decode("utf-8")
        logger.info("Retrieved: s3://%s/%s", bucket_name, key)
        return content

    except ClientError as e:
        logger.error("Get failed: %s", e.response["Error"]["Message"])
        return None


def delete_object(bucket_name: str, key: str) -> bool:
    """Delete an object from an S3 bucket."""
    s3 = boto3.client("s3")

    try:
        s3.delete_object(Bucket=bucket_name, Key=key)
        logger.info("Deleted: s3://%s/%s", bucket_name, key)
        return True

    except ClientError as e:
        logger.error("Delete failed: %s", e.response["Error"]["Message"])
        return False
    

def set_bucket_policy(bucket_name: str, policy: dict) -> bool:
    """Attach a JSON policy document to an S3 bucket."""
    s3 = boto3.client("s3")

    try:
        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
        logger.info("Policies applied to bucket: %s", bucket_name)
        return True
    except ClientError as e:
        logger.error("Policy failed: %s", e.response["Error"]["Message"])
        return False


def set_lifecycle_rule(bucket_name: str, rule_id: str, prefix: str, expiration_days: int) -> bool:
    """
    Set a lifecycle rule that expires objects after a given number of days.
    prefix filters which objects the rule applies to.
    """
    s3 = boto3.client("s3")

    lifecycle_policy = {
        "Rules": [
            {
                "ID": rule_id,
                "Filter": {"Prefix": prefix},
                "Status": "Enabled",
                "Expiration": {"Days": expiration_days}
            }
        ]
    }

    try:
        s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration=lifecycle_policy
        )
        logger.info(
            "Lifecycle rule '%s' set: delete after %d days (prefix: '%s')",
            rule_id, expiration_days, prefix
        )
        return True

    except ClientError as e:
        logger.error("Lifecycle failed: %s", e.response["Error"]["Message"])
        return False


if __name__ == "__main__":
    BUCKET = "paulo-dev-s3-automation"
    REGION = "us-east-1"


    create_bucket(BUCKET, REGION)

    upload_object(BUCKET, "reports/jan.txt", "January AWS cost report - $142.30")
    upload_object(BUCKET, "reports/feb.txt", "February AWS cost report - $198.75")

    objects = list_objects(BUCKET, prefix="reports/")
    for obj in objects:
        print(f"  {obj['key']} ({obj['size_kb']} KB)")

    content = get_object(BUCKET, "reports/jan.txt")
    if content:
        print(f"Content: {content}")

    delete_object(BUCKET, "reports/jan.txt")

    remaining = list_objects(BUCKET, prefix="reports/")
    print(f"Objects remaining: {len(remaining)}")

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "DenyHTTP",
                "Effect": "Deny",
                "Principal": "*",
                "Action": "s3:*",
                "Resource": [f"arn:aws:s3:::{BUCKET}", f"arn:aws:s3:::{BUCKET}/*"],
                "Condition": {"Bool": {"aws:SecureTransport": "false"}}
            }
        ]
    }
    set_bucket_policy(BUCKET, policy)
    set_lifecycle_rule(BUCKET, rule_id="expire-reports", prefix="reports/", expiration_days=90)

  




