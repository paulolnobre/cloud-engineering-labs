import sys
import pathlib
import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.logging_config import get_logger


logger = get_logger(__name__)


def get_stopped_instances(client: BaseClient) -> list:
    """Retrieve all stopped EC2 instances in the account.

    Args:
        client: A boto3 EC2 client.

    Returns:
        List of stopped EC2 instance dicts.
    """
    try:
        paginator = client.get_paginator('describe_instances')
        stopped_instances = []
        for page in paginator.paginate(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]):
            for reservation in page['Reservations']:
                stopped_instances.extend(reservation['Instances'])
        logger.info("Retrieved %d stopped EC2 instances", len(stopped_instances))
        return stopped_instances
    except ClientError as e:
        logger.error("Failed to retrieve stopped EC2 instances: %s", e)
        return []


def get_instance_age(instance: dict) -> int:
    """Return how many days an instance has been stopped.

    Args:
        instance: EC2 instance dict from describe_instances.

    Returns:
        Days since the instance was stopped, or 0 if unknown.
    """
    stopped_at = instance.get('StateTransitionReason', {}).get('StoppedAt')
    if stopped_at is None:
        return 0
    return (datetime.now(timezone.utc) - stopped_at).days


def terminate_instance(client: BaseClient, instance_id: str) -> None:
    """Terminate an EC2 instance by its ID.

    Args:
        client:      A boto3 EC2 client.
        instance_id: The ID of the EC2 instance to terminate.
    """
    try:
        client.terminate_instances(InstanceIds=[instance_id])
        logger.info("Terminated instance %s", instance_id)
    except ClientError as e:
        logger.error("Failed to terminate instance %s: %s", instance_id, e)


if __name__ == "__main__":
    MAX_STOPPED_DAYS = 7
    logger.info("Starting EC2 cleanup at %s", datetime.now(timezone.utc).isoformat())

    client = boto3.client("ec2", region_name="us-east-1")

    stopped = get_stopped_instances(client)

    for instance in stopped:
        instance_id = instance['InstanceId']
        age = get_instance_age(instance)
        logger.info("Instance %s stopped for %d day(s)", instance_id, age)

        if age >= MAX_STOPPED_DAYS:
            terminate_instance(client, instance_id)
