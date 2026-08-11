"""Reliable acquisition of the public Olist dataset into the external data area."""

from __future__ import annotations

import logging
import shutil
import tempfile
import zipfile
from collections.abc import Iterable
from pathlib import Path, PurePosixPath
from urllib.request import Request, urlopen
from uuid import uuid4

from src.ingestion.contracts import OLIST_CSV_CONTRACTS

LOGGER = logging.getLogger(__name__)
EXPECTED_FILENAMES = frozenset(contract.filename for contract in OLIST_CSV_CONTRACTS)
DOWNLOAD_CHUNK_SIZE = 1024 * 1024


class OlistAcquisitionError(RuntimeError):
    """Raised when the Olist archive cannot be acquired safely."""


class OlistAcquirer:
    """Download and atomically publish the expected Olist source CSV files."""

    def __init__(self, dataset_url: str, destination_directory: Path) -> None:
        self._dataset_url = dataset_url
        self._destination_directory = destination_directory

    def acquire(self, *, force: bool = False) -> tuple[Path, ...]:
        """Ensure a complete local copy of the nine source files exists."""
        if self._is_complete(self._destination_directory) and not force:
            LOGGER.info(
                "A complete Olist acquisition already exists at %s; reusing it.",
                self._destination_directory,
            )
            return self._expected_paths(self._destination_directory)

        if force:
            LOGGER.info("Downloading Olist again because force was requested.")
        else:
            LOGGER.info("Downloading Olist because no complete local acquisition was found.")

        self._destination_directory.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix=f".{self._destination_directory.name}-download-",
            dir=self._destination_directory.parent,
        ) as temporary_directory:
            temporary_root = Path(temporary_directory)
            archive_path = temporary_root / "archive.zip"
            staged_directory = temporary_root / self._destination_directory.name

            self._download_archive(archive_path)
            self._extract_expected_files(archive_path, staged_directory)
            if not self._is_complete(staged_directory):
                raise OlistAcquisitionError("The extracted Olist files are incomplete.")

            self._publish(staged_directory)

        LOGGER.info("Olist acquisition completed at %s.", self._destination_directory)
        return self._expected_paths(self._destination_directory)

    def _download_archive(self, archive_path: Path) -> None:
        request = Request(self._dataset_url, headers={"User-Agent": "modern-data-platform/0.1"})
        try:
            with urlopen(request, timeout=60) as response, archive_path.open("wb") as archive_file:
                while chunk := response.read(DOWNLOAD_CHUNK_SIZE):
                    archive_file.write(chunk)
        except OSError as error:
            raise OlistAcquisitionError("Unable to download the Olist dataset archive.") from error

        if not zipfile.is_zipfile(archive_path):
            raise OlistAcquisitionError("The downloaded Olist file is not a valid ZIP archive.")

    def _extract_expected_files(self, archive_path: Path, staged_directory: Path) -> None:
        staged_directory.mkdir(parents=True)
        (staged_directory / ".gitkeep").touch()

        try:
            with zipfile.ZipFile(archive_path) as archive:
                members = self._expected_members(archive.infolist())
                missing_files = EXPECTED_FILENAMES - members.keys()
                if missing_files:
                    missing = ", ".join(sorted(missing_files))
                    raise OlistAcquisitionError(
                        f"The archive is missing expected Olist files: {missing}."
                    )

                for filename, member in members.items():
                    target_path = staged_directory / filename
                    with archive.open(member) as source_file, target_path.open("wb") as target_file:
                        shutil.copyfileobj(source_file, target_file, length=DOWNLOAD_CHUNK_SIZE)
        except zipfile.BadZipFile as error:
            raise OlistAcquisitionError(
                "The downloaded Olist archive could not be opened."
            ) from error

    def _expected_members(self, members: Iterable[zipfile.ZipInfo]) -> dict[str, zipfile.ZipInfo]:
        expected_members: dict[str, zipfile.ZipInfo] = {}
        for member in members:
            filename = PurePosixPath(member.filename).name
            if filename not in EXPECTED_FILENAMES:
                continue
            if filename in expected_members:
                raise OlistAcquisitionError(
                    f"The archive contains duplicate file entries for {filename}."
                )
            expected_members[filename] = member
        return expected_members

    def _publish(self, staged_directory: Path) -> None:
        backup_directory: Path | None = None
        if self._destination_directory.exists():
            backup_directory = self._destination_directory.parent / (
                f".{self._destination_directory.name}-backup-{uuid4().hex}"
            )
            self._destination_directory.rename(backup_directory)

        try:
            staged_directory.rename(self._destination_directory)
        except OSError:
            if backup_directory is not None and backup_directory.exists():
                backup_directory.rename(self._destination_directory)
            raise
        else:
            if backup_directory is not None:
                shutil.rmtree(backup_directory)

    @staticmethod
    def _is_complete(directory: Path) -> bool:
        return directory.is_dir() and all(
            (directory / filename).is_file() and (directory / filename).stat().st_size > 0
            for filename in EXPECTED_FILENAMES
        )

    @staticmethod
    def _expected_paths(directory: Path) -> tuple[Path, ...]:
        return tuple(directory / filename for filename in sorted(EXPECTED_FILENAMES))
