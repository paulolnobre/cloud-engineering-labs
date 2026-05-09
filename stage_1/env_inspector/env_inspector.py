import json
import logging
import os

import cloud_utils


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def describe_environment() -> dict:
    """
    Inspect and return AWS environment configuration.

    Returns:
        dict: Environment metadata including region,
        profile, and timestamp.
    """

    environment_data = {
        "region": os.environ.get("AWS_DEFAULT_REGION", "unknown"),
        "profile": os.environ.get("AWS_PROFILE", "default"),
        "timestamp": cloud_utils.get_time_stamp()
    }

    logging.info("Environment inspection completed.")

    return environment_data


if __name__ == "__main__":

    try:
        result = describe_environment()

        print(json.dumps(result, indent=2))

    except Exception as error:
        logging.error(f"Unexpected error: {error}")
