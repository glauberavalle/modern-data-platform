"""CSV structural validation performed before any database mutation."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from src.ingestion.contracts import CsvContract


class CsvValidationError(ValueError):
    """Raised when an external CSV does not match its source contract."""


@dataclass(frozen=True)
class ValidatedCsv:
    """A CSV verified as ready for RAW loading."""

    contract: CsvContract
    path: Path
    row_count: int


def validate_csv(source_directory: Path, contract: CsvContract) -> ValidatedCsv:
    """Validate filename, header and row width while preserving source values."""
    path = source_directory / contract.filename
    if not path.is_file():
        raise CsvValidationError(f"Required Olist file was not found: {path}")

    try:
        with path.open("r", encoding="utf-8-sig", newline="") as source_file:
            reader = csv.reader(source_file)
            header = next(reader, None)
            if header is None:
                raise CsvValidationError(f"CSV file is empty: {path.name}")
            if tuple(header) != contract.columns:
                raise CsvValidationError(
                    f"Unexpected header in {path.name}. Expected {contract.columns}, "
                    f"got {tuple(header)}."
                )

            row_count = 0
            for line_number, row in enumerate(reader, start=2):
                if len(row) != len(contract.columns):
                    raise CsvValidationError(
                        f"Invalid column count in {path.name} at line {line_number}: "
                        f"expected {len(contract.columns)}, got {len(row)}."
                    )
                row_count += 1
    except UnicodeDecodeError as error:
        raise CsvValidationError(f"CSV file is not valid UTF-8: {path.name}") from error
    except csv.Error as error:
        raise CsvValidationError(f"CSV parsing failed for {path.name}: {error}") from error

    return ValidatedCsv(contract=contract, path=path, row_count=row_count)
