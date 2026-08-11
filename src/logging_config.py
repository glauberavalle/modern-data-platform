"""Logging configuration for local platform commands."""

from __future__ import annotations

import logging


def configure_logging(level: str) -> None:
    """Configure clear, consistent console logs once per process."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )
