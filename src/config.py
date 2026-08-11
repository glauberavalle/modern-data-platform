"""Centralized settings for local ingestion execution."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from the local .env file."""

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    olist_source_directory: Path
    raw_schema: str
    log_level: str

    @property
    def postgres_connection_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@dataclass(frozen=True)
class AcquisitionSettings:
    """Configuration required exclusively by source acquisition."""

    olist_source_directory: Path
    olist_dataset_url: str
    log_level: str


def load_settings() -> Settings:
    """Load required local configuration without logging sensitive values."""
    load_dotenv(PROJECT_ROOT / ".env")

    postgres_port = _get_required_int("POSTGRES_PORT")
    source_directory = Path(_get_required("OLIST_SOURCE_DIRECTORY"))
    if not source_directory.is_absolute():
        source_directory = PROJECT_ROOT / source_directory

    return Settings(
        postgres_host=_get_required("POSTGRES_HOST"),
        postgres_port=postgres_port,
        postgres_db=_get_required("POSTGRES_DB"),
        postgres_user=_get_required("POSTGRES_USER"),
        postgres_password=_get_required("POSTGRES_PASSWORD"),
        olist_source_directory=source_directory,
        raw_schema=_get_required("RAW_SCHEMA"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )


def load_acquisition_settings() -> AcquisitionSettings:
    """Load only the settings needed to acquire Olist source files."""
    load_dotenv(PROJECT_ROOT / ".env")
    source_directory = Path(_get_required("OLIST_SOURCE_DIRECTORY"))
    if not source_directory.is_absolute():
        source_directory = PROJECT_ROOT / source_directory

    return AcquisitionSettings(
        olist_source_directory=source_directory,
        olist_dataset_url=_get_required("OLIST_DATASET_URL"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )


def _get_required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Required environment variable is missing: {name}")
    return value


def _get_required_int(name: str) -> int:
    value = _get_required(name)
    try:
        return int(value)
    except ValueError as error:
        raise ValueError(f"Environment variable {name} must be an integer.") from error
