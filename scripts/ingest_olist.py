"""CLI entry point for loading manually supplied Olist CSV files into RAW."""

from __future__ import annotations

import logging

from src.config import load_settings
from src.ingestion.service import OlistRawIngestionService
from src.logging_config import configure_logging


def main() -> None:
    """Run Olist RAW ingestion and report failures with actionable logs."""
    try:
        settings = load_settings()
        configure_logging(settings.log_level)
        OlistRawIngestionService(settings).run()
    except Exception:
        logging.getLogger(__name__).exception("Olist RAW ingestion failed.")
        raise


if __name__ == "__main__":
    main()
