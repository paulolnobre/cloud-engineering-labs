VALID_ENVIRONMENTS = {"dev", "staging", "prod"}
VALID_REGIONS = {"us-east-1", "us-east-2", "us-west-1", "us-west-2"}


def format_bucket_name(project: str, environment: str, region: str) -> str:
    """Generate a standardized S3 bucket name."""
    if not validate_environment(environment):
        raise ValueError(f"Invalid environment: '{environment}'. Must be one of {VALID_ENVIRONMENTS}")
    if region not in VALID_REGIONS:
        raise ValueError(f"Invalid region: '{region}'. Must be one of {VALID_REGIONS}")
    return f"{project}-{environment}-{region}"


def validate_environment(env: str) -> bool:
    """Check if environment string is valid."""
    return env in VALID_ENVIRONMENTS


def build_lambda_arn(region: str, account_id: str, function_name: str) -> str:
    """Construct a Lambda function ARN from its components."""
    return f"arn:aws:lambda:{region}:{account_id}:function:{function_name}"


def main():
    # S3 bucket naming
    bucket = format_bucket_name("converge-crm", "prod", "us-east-1")
    print(f"Bucket name: {bucket}")

    # Environment validation
    for env in ["dev", "staging", "prod", "invalid", "production"]:
        status = "✓" if validate_environment(env) else "✗"
        print(f"  {status} '{env}'")

    # Lambda ARN
    arn = build_lambda_arn("us-east-1", "123456789012", "process-clinic-intake")
    print(f"Lambda ARN:  {arn}")

    # Invalid input — shows error handling
    try:
        bad_bucket = format_bucket_name("converge-crm", "production", "us-east-1")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
