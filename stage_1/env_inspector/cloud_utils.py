import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

BYTE_CONVERSION = 1024


def get_resource_name(service: str, env: str, region: str) -> str:
    """
    Generate a standardized cloud resource name.

    Args:
        service (str): Cloud service name.
        env (str): Environment name.
        region (str): AWS region.

    Returns:
        str: Formatted resource name.
    """

    if not service or not env or not region:
        raise ValueError("Service, environment, and region must be provided.")

    resource_name = f"{service}-{env}-{region}"

    logging.info(f"Generated resource name: {resource_name}")

    return resource_name


def format_s3_size(size_bytes: int) -> str:
    """
    Convert a size in bytes into a human-readable format.

    Args:
        size_bytes (int): File size in bytes.

    Returns:
        str: Formatted size string.
    """

    if size_bytes < 0:
        raise ValueError("Size cannot be negative.")

    units = ["B", "KB", "MB", "GB", "TB", "PB"]

    size = float(size_bytes)

    for unit in units:
        if size < BYTE_CONVERSION or unit == units[-1]:
            formatted_size = f"{round(size, 2)}{unit}"

            logging.info(f"Formatted size: {formatted_size}")

            return formatted_size

        size /= BYTE_CONVERSION

    raise RuntimeError("Failed to format S3 object size.")


def get_time_stamp() -> str:
    """
    Return current timestamp formatted as YYYY-MM-DD.

    Returns:
        str: Current formatted date.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d")

    logging.info(f"Generated timestamp: {timestamp}")

    return timestamp


if __name__ == "__main__":

    try:
        print(get_resource_name("s3", "prod", "us-east-1"))
        print(format_s3_size(1105548))
        print(get_time_stamp())

    except ValueError as error:
        logging.error(f"Validation error: {error}")

    except Exception as error:
        logging.error(f"Unexpected error: {error}")



