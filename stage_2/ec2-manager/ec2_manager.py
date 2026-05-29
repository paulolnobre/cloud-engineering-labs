import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from utils.ec2_utils import get_instances_by_state, stop_instance
from utils.logging_config import get_logger

logger = get_logger(__name__)


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