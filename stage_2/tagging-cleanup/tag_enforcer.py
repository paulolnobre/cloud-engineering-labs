import sys
import pathlib
import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from utils.logging_config import get_logger

logger = get_logger(__name__)

REQUIRED_TAGS = ["Name", "Environment", "Owner"]

def get_instances(client: BaseClient) -> list:
    """Retrieve all EC2 instances in the account.

    Args:
        client: A boto3 EC2 client.

    Returns:
        List of EC2 instance dicts.
    """
    try:
        paginator = client.get_paginator('describe_instances')
        instances = []
        for page in paginator.paginate():
            for reservation in page['Reservations']:
                instances.extend(reservation['Instances'])
        logger.info("Retrieved %d EC2 instances", len(instances))
        return instances
    except ClientError as e:
        logger.error("Failed to retrieve EC2 instances: %s", e)
        return []
    
def audit_tags(instances: list) -> list:
    """Identify EC2 instances missing required tags.

    Args:
        instances: List of EC2 instance dicts.

    Returns:
        List of instance IDs missing required tags.
    """
    non_compliant_instances = []
        for instance in instances:
            instance_id = instance['InstanceId']
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            if not all(tag in tags for tag in REQUIRED_TAGS):
                non_compliant_instances.append(instance_id)
                logger.warning("Instance %s is missing required tags", instance_id)
        logger.info("Found %d non-compliant instances", len(non_compliant_instances))
        return non_compliant_instances
    