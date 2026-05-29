import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timezone
from typing import List, Dict, Any

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

import utils.ec2_utils as ec2_utils
from utils.logging_config import get_logger

logger = get_logger(__name__)


def get_ec2_client() -> BaseClient:
    """Create and return a boto3 EC2 client."""
    try:
        return boto3.client("ec2", region_name="us-east-1")
    except ClientError as e:
        logger.error("Failed to create EC2 client: %s", e)
        raise


def audit_instances(instances: List[Dict[str, Any]], state: str) -> None:
    """Log details for a list of EC2 instances."""
    logger.info("EC2 instances in state '%s': %d", state, len(instances))
    for instance in instances:
        instance_id = instance["InstanceId"]
        tags = instance.get("Tags", [])
        name = next((t["Value"] for t in tags if t["Key"] == "Name"), "MISSING")
        environment = next((t["Value"] for t in tags if t["Key"] == "Environment"), "MISSING")

        if "MISSING" in (name, environment):
            logger.warning(
                "  [UNTAGGED] %s | Name: %s | Environment: %s",
                instance_id, name, environment,
            )
        else:
            logger.info(
                "  %s | Name: %s | Environment: %s",
                instance_id, name, environment,
            )


if __name__ == "__main__":
    logger.info("Starting EC2 audit at %s", datetime.now(timezone.utc).isoformat())
    
    client = get_ec2_client()

    for state in ["running", "stopped"]:
        instances = ec2_utils.get_instances_by_state(state, client)
        audit_instances(instances, state)