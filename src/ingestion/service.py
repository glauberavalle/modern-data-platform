"""Application service for the Olist RAW ingestion flow."""

from __future__ import annotations

import logging

from src.config import Settings
from src.ingestion.contracts import OLIST_CSV_CONTRACTS
from src.ingestion.loading.postgres_loader import PostgresRawLoader
from src.ingestion.validation.csv_validator import ValidatedCsv, validate_csv

LOGGER = logging.getLogger(__name__)


class OlistRawIngestionService:
    """Validate all source files before loading them into PostgreSQL."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def run(self) -> None:
        """Execute the validation and RAW loading stages."""
        LOGGER.info("Starting Olist RAW ingestion from %s.", self._settings.olist_source_directory)
        validated_files = self._validate_all_files()
        loader = PostgresRawLoader(
            connection_url=self._settings.postgres_connection_url,
            schema=self._settings.raw_schema,
        )
        loader.load(validated_files)
        LOGGER.info("Olist RAW ingestion finished successfully.")

    def _validate_all_files(self) -> tuple[ValidatedCsv, ...]:
        if not self._settings.olist_source_directory.is_dir():
            raise FileNotFoundError(
                f"Olist source directory was not found: {self._settings.olist_source_directory}"
            )

        validated_files = tuple(
            validate_csv(self._settings.olist_source_directory, contract)
            for contract in OLIST_CSV_CONTRACTS
        )
        LOGGER.info("Validated %s Olist CSV file(s).", len(validated_files))
        return validated_files
