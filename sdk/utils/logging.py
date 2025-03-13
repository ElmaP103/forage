"""Logging configuration for the SDK."""

import logging
import sys
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
) -> None:
    """Configure logging for the SDK.

    Args:
        level: Logging level
        format_string: Custom format string for log messages
    """
    if format_string is None:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(format_string))

    logger = logging.getLogger('sdk')
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
