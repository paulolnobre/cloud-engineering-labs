# AWS Naming Utilities

Utility functions for generating and validating standardized AWS resource names and ARNs.
Enforces naming conventions across environments and regions.

Stack: Python 3 | Context: AWS resource naming and governance

---

## What it does

- Generates standardized S3 bucket names following the pattern `project-environment-region`
- Validates environment strings against allowed values (`dev`, `staging`, `prod`)
- Validates region strings against allowed AWS regions
- Constructs Lambda function ARNs from their components
- Raises errors on invalid input — fails loud instead of silently wrong

---

## AWS Applications

- **S3**: Enforce consistent bucket naming across teams and environments
- **Lambda**: Programmatically build ARNs for function invocation and IAM policies
- **Governance**: Prevent typos and invalid environment names from reaching AWS API calls
- **IaC prep**: Use as a naming helper layer before provisioning resources via boto3 or Terraform

---

## Sample Output
```
Bucket name: converge-crm-prod-us-east-1
  ✓ 'dev'
  ✓ 'staging'
  ✓ 'prod'
  ✗ 'invalid'
  ✗ 'production'
Lambda ARN:  arn:aws:lambda:us-east-1:123456789012:function:process-clinic-intake
Error: Invalid environment: 'production'. Must be one of {'dev', 'staging', 'prod'}
```
