"""PostgreSQL loader that preserves Olist CSV values in the RAW layer."""

from __future__ import annotations

import logging
from collections.abc import Iterable

import psycopg
from psycopg import sql

from src.ingestion.validation.csv_validator import ValidatedCsv

LOGGER = logging.getLogger(__name__)


class PostgresRawLoader:
    """Create and replace PostgreSQL RAW tables from validated CSV files."""

    def __init__(self, connection_url: str, schema: str) -> None:
        self._connection_url = connection_url
        self._schema = schema

    def load(self, files: Iterable[ValidatedCsv]) -> None:
        """Load every validated file in one transaction."""
        validated_files = tuple(files)
        with psycopg.connect(self._connection_url) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(self._schema))
                )
                for validated_file in validated_files:
                    self._create_table(cursor, validated_file)
                    self._replace_table_contents(cursor, validated_file)

        LOGGER.info("RAW load completed for %s file(s).", len(validated_files))

    def _create_table(self, cursor: psycopg.Cursor, validated_file: ValidatedCsv) -> None:
        column_definitions = sql.SQL(", ").join(
            sql.SQL("{} TEXT").format(sql.Identifier(column))
            for column in validated_file.contract.columns
        )
        statement = sql.SQL("CREATE TABLE IF NOT EXISTS {}.{} ({})").format(
            sql.Identifier(self._schema),
            sql.Identifier(validated_file.contract.table_name),
            column_definitions,
        )
        cursor.execute(statement)

    def _replace_table_contents(self, cursor: psycopg.Cursor, validated_file: ValidatedCsv) -> None:
        table_identifier = sql.Identifier(self._schema, validated_file.contract.table_name)
        columns = sql.SQL(", ").join(
            sql.Identifier(column) for column in validated_file.contract.columns
        )
        cursor.execute(sql.SQL("TRUNCATE TABLE {}").format(table_identifier))

        copy_statement = sql.SQL("COPY {} ({}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)").format(
            table_identifier,
            columns,
        )
        with validated_file.path.open("r", encoding="utf-8", newline="") as source_file:
            with cursor.copy(copy_statement) as copy:
                while chunk := source_file.read(1024 * 1024):
                    copy.write(chunk)

        LOGGER.info(
            "Loaded %s row(s) into %s.%s from %s.",
            validated_file.row_count,
            self._schema,
            validated_file.contract.table_name,
            validated_file.path.name,
        )
