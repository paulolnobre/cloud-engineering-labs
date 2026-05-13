import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import logging


logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def get_identity():
    """
    Retrieves the AWS identity of the currently configured credentials.

    Uses the AWS STS (Security Token Service) to call GetCallerIdentity,
    which returns the Account ID, User ARN, and User ID associated with
    the credentials found in the environment (~/.aws/credentials, env vars, etc.).

    Returns:
        dict: A response dict containing 'Account', 'Arn', and 'UserId' keys,
        or None if credentials are missing or the request fails.
    """
    try:
        sts = boto3.client("sts")
        response = sts.get_caller_identity()
        return response
    except NoCredentialsError:
        logging.error("No AWS credentials found.", exc_info=True)
        return None
    except ClientError as e: 
        logging.error("AWS ClientError: %s", e, exc_info=True) 
        return None
    
if __name__ == "__main__":
    identity = get_identity()
    if identity:
        print(f"Account: {identity['Account']}")
        print(f"User ARN: {identity['Arn']}")
        print(f"User ID: {identity['UserId']}")
        session = boto3.session.Session()
        print(f"Region: {session.region_name}")
    else:
        print('Failed to retrieve identity')