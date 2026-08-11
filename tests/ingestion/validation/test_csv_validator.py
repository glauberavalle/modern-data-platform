from pathlib import Path

import pytest

from src.ingestion.contracts import CsvContract
from src.ingestion.validation.csv_validator import CsvValidationError, validate_csv

CONTRACT = CsvContract("source.csv", "source", ("id", "description"))


def test_validate_csv_returns_row_count_for_matching_file(tmp_path: Path) -> None:
    (tmp_path / CONTRACT.filename).write_text(
        "id,description\n1,first\n2,second\n", encoding="utf-8"
    )

    validated_file = validate_csv(tmp_path, CONTRACT)

    assert validated_file.path == tmp_path / CONTRACT.filename
    assert validated_file.row_count == 2


def test_validate_csv_rejects_unexpected_header(tmp_path: Path) -> None:
    (tmp_path / CONTRACT.filename).write_text("id,name\n1,first\n", encoding="utf-8")

    with pytest.raises(CsvValidationError, match="Unexpected header"):
        validate_csv(tmp_path, CONTRACT)


def test_validate_csv_accepts_utf8_bom_in_source_header(tmp_path: Path) -> None:
    (tmp_path / CONTRACT.filename).write_text("id,description\n1,first\n", encoding="utf-8-sig")

    validated_file = validate_csv(tmp_path, CONTRACT)

    assert validated_file.row_count == 1


def test_validate_csv_rejects_rows_with_wrong_column_count(tmp_path: Path) -> None:
    (tmp_path / CONTRACT.filename).write_text("id,description\n1\n", encoding="utf-8")

    with pytest.raises(CsvValidationError, match="Invalid column count"):
        validate_csv(tmp_path, CONTRACT)
