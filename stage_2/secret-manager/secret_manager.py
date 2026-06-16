import sys
import json
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from utils.logging_config import get_logger

logger = get_logger(__name__)


def create_secret(client: BaseClient, secret_name: str, secret_value: dict) -> dict:
    """Create a new secret in AWS Secrets Manager.

    Args:
        client:       A boto3 secretsmanager client.
        secret_name:  Name/path of the secret (e.g. 'converge/prod/db').
        secret_value: Dict to store as the secret value.

    Returns:
        AWS API response dict.
    """
    response = client.create_secret(
        Name=secret_name,
        SecretString=json.dumps(secret_value),
    )
    logger.info("Secret created: %s", secret_name)
    return response


def get_secret(client: BaseClient, secret_name: str) -> dict:
    """Retrieve and parse a secret from AWS Secrets Manager.

    Args:
        client:      A boto3 secretsmanager client.
        secret_name: Name or ARN of the secret to retrieve.

    Returns:
        Parsed secret value as a dict.
    """
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])
    logger.info("Secret retrieved: %s", secret_name)
    return secret


def update_secret(client: BaseClient, secret_name: str, secret_value: dict) -> dict:
    """Update the value of an existing secret.

    Args:
        client:       A boto3 secretsmanager client.
        secret_name:  Name or ARN of the secret to update.
        secret_value: New dict value to store.

    Returns:
        AWS API response dict.
    """
    response = client.update_secret(
        SecretId=secret_name,
        SecretString=json.dumps(secret_value),
    )
    logger.info("Secret updated: %s", secret_name)
    return response


def delete_secret(
    client: BaseClient,
    secret_name: str,
    force: bool = False,
    recovery_window: int = 7,
) -> dict:
    """Delete a secret from AWS Secrets Manager.

    Args:
        client:          A boto3 secretsmanager client.
        secret_name:     Name or ARN of the secret to delete.
        force:           If True, delete immediately with no recovery window.
                         Use for test secrets to avoid billing.
        recovery_window: Days before permanent deletion (7–30). Ignored if force=True.

    Returns:
        AWS API response dict.
    """
    kwargs: dict = {"SecretId": secret_name}
    if force:
        kwargs["ForceDeleteWithoutRecovery"] = True
    else:
        kwargs["RecoveryWindowInDays"] = recovery_window

    response = client.delete_secret(**kwargs)
    logger.info("Secret deleted: %s (force=%s)", secret_name, force)
    return response


if __name__ == "__main__":
    logger.info("Starting Secrets Manager lifecycle test")

    SECRET_NAME = "test/converge/db"
    INITIAL_VALUE = {"username": "admin", "password": "password123"}
    UPDATED_VALUE = {"username": "admin", "password": "newpassword456"}

    try:
        client = boto3.client("secretsmanager", region_name="us-east-1")

        logger.info("--- CREATE ---")
        create_secret(client, SECRET_NAME, INITIAL_VALUE)

        logger.info("--- GET ---")
        secret = get_secret(client, SECRET_NAME)
        logger.info("Value: %s", secret)

        logger.info("--- UPDATE ---")
        update_secret(client, SECRET_NAME, UPDATED_VALUE)

        logger.info("--- GET (after update) ---")
        updated = get_secret(client, SECRET_NAME)
        logger.info("Value: %s", updated)

        logger.info("--- DELETE (force=True to avoid billing) ---")
        delete_secret(client, SECRET_NAME, force=True)

    except ClientError as e:
        logger.error("Secrets Manager operation failed: %s", e)
