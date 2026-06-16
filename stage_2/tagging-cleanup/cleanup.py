import sys
import pathlib
import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.logging_config import get_logger

logger = get_logger(__name__)


def get_stopped_instances(client: BaseClient) -> list[dict]:
    """Retrieve all stopped EC2 instances in the account.

    Args:
        client: A boto3 EC2 client.

    Returns:
        List of stopped EC2 instance dicts.
    """
    try:
        paginator = client.get_paginator("describe_instances")
        stopped_instances = []
        for page in paginator.paginate(
            Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
        ):
            for reservation in page["Reservations"]:
                stopped_instances.extend(reservation["Instances"])
        logger.info("Retrieved %d stopped EC2 instances", len(stopped_instances))
        return stopped_instances
    except ClientError as e:
        logger.error("Failed to retrieve stopped EC2 instances: %s", e)
        return []


def get_instance_age(instance: dict) -> int:
    """Try StateTransitionReason first, fall back to LaunchTime."""
    reason = instance.get("StateTransitionReason", "")
    if "(" in reason and ")" in reason:
        try:
            date_str = reason.split("(")[1].split(")")[0].split(" ")[0]
            stopped_at = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - stopped_at).days
        except (IndexError, ValueError):
            logger.warning("Could not parse StateTransitionReason for %s, falling back to LaunchTime", instance.get("InstanceId"))
    launch_time = instance.get("LaunchTime")
    if launch_time is None:
        return 0
    return (datetime.now(timezone.utc) - launch_time).days


def terminate_instance(
    client: BaseClient, instance_id: str, dry_run: bool = True
) -> None:
    """Terminate an EC2 instance by its ID.

    Args:
        client:      A boto3 EC2 client.
        instance_id: The ID of the EC2 instance to terminate.
        dry_run:     If True, log the action without executing it.
    """
    if dry_run:
        logger.info("[DRY-RUN] Would terminate instance %s", instance_id)
        return
    try:
        client.terminate_instances(InstanceIds=[instance_id])
        logger.info("Terminated instance %s", instance_id)
    except ClientError as e:
        logger.error("Failed to terminate instance %s: %s", instance_id, e)


if __name__ == "__main__":
    MAX_STOPPED_DAYS = 7
    DRY_RUN = True  

    logger.info("Starting EC2 cleanup | dry_run=%s", DRY_RUN)

    client = boto3.client("ec2", region_name="us-east-1")
    stopped = get_stopped_instances(client)

    for instance in stopped:
        instance_id = instance["InstanceId"]
        tags = {tag["Key"]: tag["Value"] for tag in instance.get("Tags", [])}
        age = get_instance_age(instance)

        logger.info("Instance %s | age=%d day(s) | env=%s", instance_id, age, tags.get("Environment", "N/A"))

        if tags.get("Environment") != "dev":
            logger.info("Skipping %s — not a dev instance", instance_id)
            continue

        if age >= MAX_STOPPED_DAYS:
            terminate_instance(client, instance_id, dry_run=DRY_RUN)
        else:
            logger.info("Skipping %s — only stopped for %d day(s)", instance_id, age)

