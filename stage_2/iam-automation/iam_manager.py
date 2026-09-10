import sys
import json
import pathlib

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.logging_config import get_logger

logger = get_logger(__name__)

def create_iam_user(client: BaseClient, user_name: str) -> dict:
    """Create a new IAM user.

    Args:
        client:    A boto3 IAM client.
        user_name: The name of the IAM user to create.

    Returns:
        AWS API response dict.
    """
    response = client.create_user(UserName=user_name)
    logger.info("Created IAM user: %s", user_name)
    return response

def create_policy(client: BaseClient, policy_name: str, policy_document: dict) -> dict:
    """Create a new IAM policy.

    Args:
        client:          A boto3 IAM client.
        policy_name:     The name of the IAM policy to create.
        policy_document: The JSON document defining the policy.

    Returns:
        AWS API response dict.
    """
    response = client.create_policy(
        PolicyName=policy_name,
        PolicyDocument=json.dumps(policy_document),
    )
    logger.info("Created IAM policy: %s", policy_name)
    return response

def attach_policy_to_user(client: BaseClient, user_name: str, policy_arn: str) -> None:
    """Attach an existing IAM policy to a user.

    Args:
        client:     A boto3 IAM client.
        user_name:  The name of the IAM user.
        policy_arn: The ARN of the IAM policy to attach.
    """
    client.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
    logger.info("Attached policy %s to user %s", policy_arn, user_name)

def detach_policy_from_user(client: BaseClient, user_name: str, policy_arn: str) -> None:
    """Detach an IAM policy from a user.

    Args:
        client:     A boto3 IAM client.
        user_name:  The name of the IAM user.
        policy_arn: The ARN of the IAM policy to detach.
    """
    client.detach_user_policy(UserName=user_name, PolicyArn=policy_arn)
    logger.info("Detached policy %s from user %s", policy_arn, user_name)

def delete_iam_user(client: BaseClient, user_name: str) -> None:
    """Delete an IAM user.

    Args:
        client:    A boto3 IAM client.
        user_name: The name of the IAM user to delete.
    """
    client.delete_user(UserName=user_name)
    logger.info("Deleted IAM user: %s", user_name)


if __name__ == "__main__":
    USER_NAME = "test-paulo-dev"
    POLICY_NAME = "test-s3-read-policy"
    POLICY_DOCUMENT = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:ListBucket"],
                "Resource": "*"
            }
        ]
    }

    try:
        client = boto3.client("iam")

        logger.info("--- CREATE USER ---")
        create_iam_user(client, USER_NAME)

        logger.info("--- CREATE POLICY ---")
        policy_response = create_policy(client, POLICY_NAME, POLICY_DOCUMENT)
        policy_arn = policy_response["Policy"]["Arn"]  # ← ARN vem da resposta

        logger.info("--- ATTACH POLICY ---")
        attach_policy_to_user(client, USER_NAME, policy_arn)

        logger.info("--- DETACH POLICY ---")
        detach_policy_from_user(client, USER_NAME, policy_arn)

        logger.info("--- DELETE POLICY ---")
        client.delete_policy(PolicyArn=policy_arn)
        logger.info("Deleted policy: %s", policy_arn)

        logger.info("--- DELETE USER ---")
        delete_iam_user(client, USER_NAME)

    except ClientError as e:
        logger.error("IAM operation failed: %s", e)
