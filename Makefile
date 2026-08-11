.PHONY: help setup lint format precommit test download-olist ingest-olist docker-up docker-down docker-restart docker-logs docker-status docker-config

help:
	@echo "Available commands:"
	@echo "  make setup        Create a local .env from .env.example"
	@echo "  make lint         Run Ruff checks"
	@echo "  make format       Format Python files with Ruff"
	@echo "  make precommit    Run pre-commit hooks"
	@echo "  make test         Run the test suite"
	@echo "  make download-olist Download the Olist source CSV files"
	@echo "  make ingest-olist Validate and load Olist CSV files into PostgreSQL RAW"
	@echo "  make docker-up    Start local services"
	@echo "  make docker-down  Stop local services"
	@echo "  make docker-restart Restart local services"
	@echo "  make docker-logs  Follow container logs"
	@echo "  make docker-status Show container status"
	@echo "  make docker-config Validate and show the resolved Docker Compose configuration"

setup:
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env from .env.example"; else echo ".env already exists"; fi

lint:
	uv run --extra dev ruff check .

format:
	uv run --extra dev ruff format .

precommit:
	uv run --extra dev pre-commit run --all-files

test:
	uv run --extra dev pytest

download-olist:
	uv run python -m scripts.download_olist

ingest-olist:
	uv run python -m scripts.ingest_olist

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-restart:
	docker compose down
	docker compose up -d

docker-logs:
	docker compose logs -f

docker-status:
	docker compose ps

docker-config:
	docker compose config
