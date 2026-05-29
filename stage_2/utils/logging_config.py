import logging
import sys

_CONFIGURED = False

LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] - %(message)s"


def setup_logging(level: int = logging.INFO) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    logging.basicConfig(level=level, format=LOG_FORMAT, stream=sys.stdout)
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    setup_logging()
    return logging.getLogger(name)
