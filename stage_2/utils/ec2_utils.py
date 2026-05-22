import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


def stop_instance(ec2_client: boto3.client, instance_id: str) -> None:
    """Stop a single EC2 instance and log the state transition."""
    try:
        response = ec2_client.stop_instances(InstanceIds=[instance_id])
        previous = response["StoppingInstances"][0]["PreviousState"]["Name"]
        current = response["StoppingInstances"][0]["CurrentState"]["Name"]
        logger.info("Stop requested: %s | %s → %s", instance_id, previous, current)
    except ClientError as e:
        logger.error("Failed to stop %s: %s", instance_id, e)
        raise