"""CLI entry point for downloading the public Olist dataset."""

from __future__ import annotations

import argparse
import logging

from src.config import load_acquisition_settings
from src.ingestion.acquisition.olist_acquirer import OlistAcquirer
from src.logging_config import configure_logging


def main() -> None:
    """Download Olist source files without triggering validation or loading."""
    parser = argparse.ArgumentParser(description="Download the public Olist dataset.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Download the dataset again even when a complete acquisition already exists.",
    )
    arguments = parser.parse_args()

    try:
        settings = load_acquisition_settings()
        configure_logging(settings.log_level)
        OlistAcquirer(settings.olist_dataset_url, settings.olist_source_directory).acquire(
            force=arguments.force
        )
    except Exception:
        logging.getLogger(__name__).exception("Olist acquisition failed.")
        raise


if __name__ == "__main__":
    main()
