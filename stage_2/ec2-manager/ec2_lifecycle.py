import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from utils.ec2_utils import stop_instance
from utils.logging_config import get_logger

logger = get_logger(__name__)

AMI_BY_REGION: dict[str, str] = {
    "us-east-1": "ami-0c55b159cbfafe1f0",
    "us-west-2": "ami-0892d3c7ee96c0bf7",
}

TERMINATE: bool = False
REGION: str = "us-east-1"


def launch_instance(ec2_client: BaseClient) -> str:
    """Launch a t2.micro instance and return its ID."""
    response = ec2_client.run_instances(
        ImageId=AMI_BY_REGION[REGION],
        InstanceType="t2.micro",
        MinCount=1,
        MaxCount=1,
        KeyName="my-key-pair",
        SecurityGroupIds=["sg-0123456789abcdef0"],
        SubnetId="subnet-0123456789abcdef0",
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {"Key": "Name", "Value": "MyInstance"},
                    {"Key": "Environment", "Value": "Development"},
                    {"Key": "ManagedBy", "Value": "boto3"},
                ],
            }
        ],
    )
    instance_id: str = response["Instances"][0]["InstanceId"]
    logger.info("Launched instance: %s", instance_id)
    return instance_id


def log_instance_details(ec2_client: BaseClient, instance_id: str) -> None:
    """Describe and log key attributes of a running instance."""
    instance = ec2_client.describe_instances(
        InstanceIds=[instance_id]
    )["Reservations"][0]["Instances"][0]

    logger.info("Instance ID: %s", instance_id)
    logger.info("Public IP:   %s", instance.get("PublicIpAddress", "N/A"))
    logger.info("State:       %s", instance["State"]["Name"])


def terminate_with_dry_run(ec2_client: BaseClient, instance_id: str) -> None:
    """Terminate an instance using dry-run as a permission pre-check."""
    logger.info("Waiting for instance to stop before terminating...")
    stop_waiter = ec2_client.get_waiter("instance_stopped")
    stop_waiter.wait(InstanceIds=[instance_id])

    try:
        ec2_client.terminate_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DryRunOperation":
            logger.info("Dry-run passed. Terminating instance: %s", instance_id)
            ec2_client.terminate_instances(InstanceIds=[instance_id])
        else:
            logger.error("Dry-run failed: %s", e)
            raise


def main() -> None:
    ec2 = boto3.client("ec2", region_name=REGION)

    try:
        instance_id = launch_instance(ec2)

        logger.info("Waiting for instance to reach running state...")
        waiter = ec2.get_waiter("instance_running")
        waiter.wait(InstanceIds=[instance_id])

        log_instance_details(ec2, instance_id)

        stop_instance(instance_id, ec2)

        if TERMINATE:
            terminate_with_dry_run(ec2, instance_id)

    except ClientError as e:
        logger.error("AWS API error: %s", e)


if __name__ == "__main__":
    main()