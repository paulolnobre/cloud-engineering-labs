import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from utils.logging_config import get_logger

logger = get_logger(__name__)

DANGEROUS_PORTS: set[int] = {22, 3389, 3306, 5432}
OPEN_CIDRS: set[str] = {"0.0.0.0/0", "::/0"}


def get_security_groups(client: BaseClient) -> list[dict]:
    """Fetch all security groups from AWS.

    Args:
        client: A boto3 EC2 client.

    Returns:
        List of security group dicts as returned by the AWS API.
    """
    response = client.describe_security_groups()
    return response.get("SecurityGroups", [])


def audit_inbound_rules(sg_id: str, sg_name: str, rules: list[dict]) -> None:
    """Audit inbound rules for a single security group.

    Logs [CRITICAL] for dangerous ports exposed to open CIDRs,
    [OPEN] for any rule open to the world, and [OK] if no open rules exist.

    Args:
        sg_id:   Security group ID (e.g. sg-0abc123).
        sg_name: Security group name.
        rules:   List of inbound rule dicts from IpPermissions.
    """
    has_issue = False

    for rule in rules:
        # When IpProtocol is "-1" (all traffic), AWS omits FromPort/ToPort entirely.
        from_port = rule.get("FromPort", 0)
        to_port   = rule.get("ToPort", 65535)
        protocol  = rule.get("IpProtocol", "-1")

        cidrs: list[str] = [r["CidrIp"]   for r in rule.get("IpRanges",   [])]
        cidrs            += [r["CidrIpv6"] for r in rule.get("Ipv6Ranges", [])]

        for cidr in cidrs:
            if cidr in OPEN_CIDRS:
                has_issue = True
                logger.info(
                    "[OPEN] %s (%s) | proto=%s ports=%s-%s cidr=%s",
                    sg_id, sg_name, protocol, from_port, to_port, cidr,
                )
                for port in DANGEROUS_PORTS:
                    if from_port <= port <= to_port:
                        logger.warning(
                            "[CRITICAL] %s (%s) port %d exposed to %s",
                            sg_id, sg_name, port, cidr,
                        )

    if not has_issue:
        logger.info("[OK] %s (%s) — no open CIDR rules", sg_id, sg_name)


def audit_security_groups(sgs: list[dict]) -> None:
    """Audit inbound rules for a list of security groups.

    Args:
        sgs: List of security group dicts as returned by get_security_groups().
    """
    logger.info("Total security groups found: %d", len(sgs))

    for sg in sgs:
        sg_id   = sg.get("GroupId",   "N/A")
        sg_name = sg.get("GroupName", "N/A")
        vpc_id  = sg.get("VpcId",     "N/A")
        logger.info("Auditing SG: %s | Name: %s | VPC: %s", sg_id, sg_name, vpc_id)
        audit_inbound_rules(sg_id, sg_name, sg.get("IpPermissions", []))


if __name__ == "__main__":
    logger.info("Starting Security Group audit")
    try:
        client = boto3.client("ec2", region_name="us-east-1")
        sgs = get_security_groups(client)
        audit_security_groups(sgs)
    except ClientError as e:
        logger.error("Audit failed: %s", e)