import logging
from datetime import datetime


logger = logging.getLogger(__name__)

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

    logger.info(f"Generated resource name: {resource_name}")

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

    for unit in units[:-1]:
        if size < BYTE_CONVERSION:
            formatted_size = f"{round(size, 2)}{unit}"

            logger.info(f"Formatted size: {formatted_size}")

            return formatted_size

        size /= BYTE_CONVERSION

    formatted_size = f"{round(size, 2)}{units[-1]}"

    logger.info(f"Formatted size: {formatted_size}")

    return formatted_size


def get_time_stamp() -> str:
    """
    Return current timestamp formatted as YYYY-MM-DD.

    Returns:
        str: Current formatted date.
    """

    timestamp = datetime.now().strftime("%Y-%m-%d")

    logger.info(f"Generated timestamp: {timestamp}")

    return timestamp


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

    try:
        print(get_resource_name("s3", "prod", "us-east-1"))
        print(format_s3_size(1105548))
        print(get_time_stamp())

    except ValueError as error:
        logger.error(f"Validation error: {error}")

    except Exception as error:
        logger.error(f"Unexpected error: {error}")



