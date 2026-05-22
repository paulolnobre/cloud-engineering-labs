import logging

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_instances_by_state(state: str, client: BaseClient) -> list[dict]:
    """Return all EC2 instances matching the given state (e.g. 'running', 'stopped')."""
    try:
        response = client.describe_instances(
            Filters=[{"Name": "instance-state-name", "Values": [state]}]
        )
        instances = [
            instance
            for reservation in response["Reservations"]
            for instance in reservation["Instances"]
        ]
        logger.info("Found %d instance(s) in state '%s'.", len(instances), state)
        return instances
    except ClientError as e:
        logger.error("Failed to describe instances: %s", e)
        return []


def stop_instance(instance_id: str, client: BaseClient) -> dict:
    """Stop a single EC2 instance and log the state transition."""
    try:
        response = client.stop_instances(InstanceIds=[instance_id])
        state_change = response["StoppingInstances"][0]
        logger.info(
            "Instance %s: %s -> %s",
            instance_id,
            state_change["PreviousState"]["Name"],
            state_change["CurrentState"]["Name"],
        )
        return state_change
    except ClientError as e:
        logger.error("Failed to stop instance %s: %s", instance_id, e)
        return {}


def tag_instances(instance_ids: list[str], tags: dict, client: BaseClient) -> None:
    """Apply a dict of tags to one or more EC2 instances."""
    if not instance_ids or not tags:
        logger.warning("tag_instances called with empty instance_ids or tags. Skipping.")
        return
    boto3_tags = [{"Key": k, "Value": v} for k, v in tags.items()]
    try:
        client.create_tags(Resources=instance_ids, Tags=boto3_tags)
        logger.info("Tags applied to %d instance(s): %s", len(instance_ids), tags)
    except ClientError as e:
        logger.error("Failed to tag instances %s: %s", instance_ids, e)


def main() -> None:
    client = boto3.client("ec2", region_name="us-east-1")
    running = get_instances_by_state("running", client)

    for instance in running:
        instance_id = instance["InstanceId"]
        name = next(
            (tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"),
            "N/A",
        )
        logger.info("Instance: %s | Name: %s", instance_id, name)

    if running:
        # TEST ONLY — stops the first running instance found
        stop_instance(running[0]["InstanceId"], client)
    else:
        logger.info("No running instances found. Skipping stop test.")


if __name__ == "__main__":
    main()