import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from utils.logging_config import get_logger

logger = get_logger(__name__)

DANGEROUS_PORTS = {22, 3389, 3306}
OPEN_CIDRS = {"0.0.0.0/0", "::/0"}


def audit_inbound_rules(sg_id: str, sg_name: str, rules: list[dict]) -> None:
    """Flag inbound rules that expose sensitive ports to open CIDRs."""
    for rule in rules:
        # when IpProtocol is "-1" (all traffic), AWS omits FromPort/ToPort entirely
        from_port = rule.get("FromPort", 0)
        to_port = rule.get("ToPort", 65535)
        protocol = rule.get("IpProtocol", "-1")

        cidrs = [r["CidrIp"] for r in rule.get("IpRanges", [])]
        cidrs += [r["CidrIpv6"] for r in rule.get("Ipv6Ranges", [])]

        for cidr in cidrs:
            if cidr in OPEN_CIDRS:
                logger.info(
                    "[OPEN] %s (%s) | proto=%s ports=%s-%s cidr=%s",
                    sg_id, sg_name, protocol, from_port, to_port, cidr,
                )
                for port in DANGEROUS_PORTS:
                    if from_port <= port <= to_port:
                        logger.warning(
                            "[CRITICAL] %s (%s) porta %d exposta para %s",
                            sg_id, sg_name, port, cidr,
                        )


def describe_security_groups(client: BaseClient) -> None:
    """Describe all security groups and audit their inbound rules."""
    try:
        response = client.describe_security_groups()
        sgs = response.get("SecurityGroups", [])
        logger.info("Total security groups found: %d", len(sgs))

        for sg in sgs:
            sg_id   = sg.get("GroupId", "N/A")
            sg_name = sg.get("GroupName", "N/A")
            vpc_id  = sg.get("VpcId", "N/A")
            logger.info("SG: %s | Name: %s | VPC: %s", sg_id, sg_name, vpc_id)
            audit_inbound_rules(sg_id, sg_name, sg.get("IpPermissions", []))

    except ClientError as e:
        logger.error("Failed to describe security groups: %s", e)
        raise


if __name__ == "__main__":
    logger.info("Starting Security Group audit")

    try:
        client = boto3.client("ec2", region_name="us-east-1")
        describe_security_groups(client)
    except ClientError as e:
        logger.error("An error occurred during the security group audit: %s", e)
