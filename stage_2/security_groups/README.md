# security_groups

Audits EC2 Security Groups using `boto3`, flagging inbound rules that expose sensitive ports to open CIDRs. Shared helpers live in `../utils/`.

## Files

### `sg_auditor.py`
Fetches all Security Groups in the account and audits their inbound rules, logging any rule that allows traffic from `0.0.0.0/0` or `::/0`, with an extra warning when the exposed port is critical (22, 3389, 3306, 5432).

```bash
python -m stage_2.security_groups.sg_auditor
```

| Function | Description |
|---|---|
| `describe_security_groups(client)` | Fetches all SGs and calls `audit_inbound_rules` for each |
| `audit_inbound_rules(sg_id, sg_name, rules)` | Flags rules with open CIDRs and warns on sensitive ports |

**Constants:**

| Constant | Value | Description |
|---|---|---|
| `DANGEROUS_PORTS` | `{22, 3389, 3306, 5432}` | SSH, RDP, MySQL, PostgreSQL — trigger `[CRITICAL]` warning |
| `OPEN_CIDRS` | `{"0.0.0.0/0", "::/0"}` | IPv4 and IPv6 open ranges |

**Log levels:**

| Tag | Level | Condition |
|---|---|---|
| `[OPEN]` | `INFO` | Any rule with `0.0.0.0/0` or `::/0` |
| `[CRITICAL]` | `WARNING` | Open CIDR + port within `DANGEROUS_PORTS` range |

> When `IpProtocol` is `"-1"` (all traffic), AWS omits `FromPort`/`ToPort`. The auditor defaults to `0–65535` so all sensitive ports are still detected.

## Requirements

- Python 3.10+
- `boto3`
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)
- IAM permission `ec2:DescribeSecurityGroups`

## Configuration, cost, and security

The executable example reads Security Groups from `us-east-1`. Set a lab profile explicitly if needed:

```bash
AWS_PROFILE=lab python -m stage_2.security_groups.sg_auditor
```

The auditor is read-only, creates no resources, and requires no cleanup. Its findings are signals for review rather than an automatic remediation policy: confirm attached resources and intended traffic before changing a Security Group.

## Tests

The unit suite exercises open-port detection without contacting AWS:

```bash
python -m pytest stage_2/tests -v
```
