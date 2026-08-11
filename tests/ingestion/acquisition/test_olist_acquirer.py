from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from src.ingestion.acquisition.olist_acquirer import (
    EXPECTED_FILENAMES,
    OlistAcquirer,
    OlistAcquisitionError,
)


def test_extract_expected_files_writes_only_contract_files(tmp_path: Path) -> None:
    archive_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for filename in EXPECTED_FILENAMES:
            archive.writestr(filename, "header\nvalue\n")
        archive.writestr("README.txt", "ignored")

    destination = tmp_path / "olist"
    acquirer = OlistAcquirer("https://example.test/olist.zip", destination)
    acquirer._extract_expected_files(archive_path, destination)

    assert {path.name for path in destination.glob("*.csv")} == EXPECTED_FILENAMES


def test_extract_expected_files_rejects_incomplete_archive(tmp_path: Path) -> None:
    archive_path = tmp_path / "archive.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(next(iter(EXPECTED_FILENAMES)), "header\nvalue\n")

    acquirer = OlistAcquirer("https://example.test/olist.zip", tmp_path / "olist")

    with pytest.raises(OlistAcquisitionError, match="missing expected Olist files"):
        acquirer._extract_expected_files(archive_path, tmp_path / "staged")
