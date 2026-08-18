# Modern Data Platform

> Uma plataforma de dados local construída de forma incremental para demonstrar práticas de Data Engineering e Analytics Engineering, com foco em arquitetura, reprodutibilidade, qualidade e manutenibilidade.

Projeto pessoal de portfólio utilizando o **Brazilian E-Commerce Public Dataset by Olist** como primeira fonte de dados.

---

## Overview

O objetivo do projeto é construir uma plataforma de dados moderna de forma incremental, começando pela aquisição, validação e armazenamento dos dados e evoluindo posteriormente para transformação, modelagem analítica, orquestração e consumo.

A primeira milestone funcional já está concluída: uma pipeline reproduzível que adquire o dataset Olist, valida os arquivos e realiza a ingestão em uma camada RAW no PostgreSQL.

O projeto prioriza **separação de responsabilidades, reprodutibilidade, idempotência e evolução sem over engineering**.

---

## Current Status

### Ingestion Foundation — Completed

A primeira etapa funcional foi implementada e validada com dados reais.

- ✅ Dataset Olist adquirido automaticamente
- ✅ 9 arquivos CSV validados
- ✅ 9 tabelas no schema `raw`
- ✅ **1.548.022 registros carregados**
- ✅ Ingestão idempotente
- ✅ PostgreSQL 16
- ✅ Docker Compose
- ✅ Testes automatizados
- ✅ Ruff e pre-commit
- ✅ GitHub Actions para CI
- ✅ Documentação técnica

As contagens foram verificadas diretamente no PostgreSQL utilizando `COUNT(*)`.

### Current Data Load

| RAW Table | Records |
|---|---:|
| `olist_customers_dataset` | 99,441 |
| `olist_geolocation_dataset` | 1,000,163 |
| `olist_order_items_dataset` | 112,650 |
| `olist_order_payments_dataset` | 103,886 |
| `olist_order_reviews_dataset` | 99,224 |
| `olist_orders_dataset` | 99,441 |
| `olist_products_dataset` | 32,951 |
| `olist_sellers_dataset` | 3,095 |
| `product_category_name_translation` | 71 |
| **Total** | **1,548,022** |

---

## Architecture

![Modern Data Platform Architecture](docs/assets/architecture.png)

### Current Flow

```text
Kaggle / Olist
      ↓
Acquisition
      ↓
data/external/olist/
      ↓
Validation
      ↓
Ingestion Service
      ↓
PostgreSQL RAW
```

A aquisição, a validação e a carga são componentes separados.

O fluxo atual inclui modelos dbt de staging sobre o schema `raw`.

**dbt está implementado para staging; Apache Airflow continua futuro.**

---

## Architectural Principles

### Separation of Responsibilities

Cada etapa possui uma responsabilidade específica:

```text
Acquisition → Validation → Loading
```

A aquisição não acessa o banco de dados, a validação não modifica os dados e o carregamento não aplica regras de negócio.

### RAW Preserves the Source

A camada `raw` representa a origem dos dados.

Os valores são carregados sem limpeza, enriquecimento, métricas ou regras de negócio.

### Idempotency

A ingestão foi projetada para permitir novas execuções sem gerar duplicações inesperadas na camada RAW.

### Reproducibility

A fonte possui uma versão configurada e o processo de aquisição pode ser reproduzido localmente.

### Incremental Evolution

Novos componentes são introduzidos conforme a necessidade da plataforma, evitando complexidade prematura.

---

## Data Source

**Brazilian E-Commerce Public Dataset by Olist**

| Item | Value |
|---|---|
| Source | Kaggle |
| Dataset version | `2` |
| Distribution | `archive.zip` |
| Expected files | 9 CSVs |

Os arquivos de dados são armazenados localmente e **não são versionados pelo Git**.

O código, configuração, testes e documentação são versionados no repositório.

---

## Tech Stack

### Current

- Python 3.13
- uv
- Docker
- Docker Compose
- PostgreSQL 16
- pgAdmin 4
- pytest
- Ruff
- pre-commit
- Git
- GitHub Actions
- dbt-postgres 1.11.0

### Planned

- **Apache Airflow** — orquestração
- Data Quality
- Observability
- Camadas analíticas e consumo de dados

---

## Project Structure

```text
modern-data-platform/
│
├── .github/
│   └── workflows/             # CI
│
├── airflow/                   # Orquestração futura
├── dbt/                       # Sources e modelos staging implementados
│
├── data/
│   └── external/
│       └── olist/             # Dados externos locais
│
├── docs/
│   ├── assets/
│   │   └── architecture.png   # Diagrama da arquitetura
│   ├── project-overview.md
│   ├── olist-acquisition.md
│   └── raw-layer.md
│   └── dbt-foundation.md
│
├── scripts/
│   ├── download_olist.py      # Aquisição
│   └── ingest_olist.py        # Ingestão
│
├── src/
│   ├── config.py
│   ├── logging_config.py
│   └── ingestion/
│       ├── acquisition/
│       ├── validation/
│       ├── loading/
│       ├── contracts.py
│       └── service.py
│
├── tests/
│   └── ingestion/
│
├── warehouse/                 # Artefatos analíticos futuros
│
├── ARCHITECTURE.md
├── PROJECT_BRIEF.md
├── ROADMAP.md
├── docker-compose.yml
├── Makefile
├── pyproject.toml
└── README.md
```

---

## Getting Started

### Prerequisites

- Git
- Docker Desktop
- Python 3.13
- uv

### 1. Clone the repository

```bash
git clone git@github.com:glauberavalle/modern-data-platform.git
cd modern-data-platform
```

### 2. Configure environment

Unix/Linux ou Git Bash:

```bash
cp .env.example .env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

### 3. Start infrastructure

```bash
docker compose up -d
```

Isso inicia:

- PostgreSQL 16
- pgAdmin 4

### 4. Acquire the dataset

```bash
uv run python -m scripts.download_olist
```

### 5. Run RAW ingestion

```bash
uv run python -m scripts.ingest_olist
```

O pipeline irá:

1. adquirir ou reutilizar os arquivos do Olist;
2. validar os nove CSVs esperados;
3. criar o schema `raw`;
4. criar as tabelas RAW;
5. carregar os dados no PostgreSQL.

### Local Services

| Service | Address |
|---|---|
| PostgreSQL | `localhost:5432` |
| pgAdmin | `http://localhost:5050` |

---

## Testing

Os testes estão organizados de acordo com as responsabilidades da aplicação:

```text
tests/
└── ingestion/
    ├── acquisition/
    ├── validation/
    └── loading/
```

A implementação atual possui testes automatizados para **aquisição e validação**.

Execução:

```bash
uv run pytest
```

Também podem ser executados:

```bash
uv run ruff format --check .
uv run ruff check .
```

---

## Development

Principais comandos:

```bash
make setup

make docker-up
make docker-down
make docker-status
make docker-logs

make download-olist
make ingest-olist

make lint
make format
```

Em ambientes sem `make`, os scripts Python podem ser executados diretamente com `uv`.

---

## Roadmap

### Completed

- fundação do repositório;
- infraestrutura local;
- PostgreSQL e pgAdmin;
- aquisição automatizada do Olist;
- validação dos arquivos;
- ingestão RAW;
- testes iniciais;
- documentação técnica.

### Next

- transformação e modelagem com dbt;
- criação das camadas analíticas;
- orquestração com Airflow;
- evolução dos testes de qualidade;
- observabilidade;
- camada analítica para consumo dos dados.

O roadmap completo está disponível em [`ROADMAP.md`](ROADMAP.md).

---

## Documentation

| Document | Description |
|---|---|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Arquitetura de alto nível |
| [`PROJECT_BRIEF.md`](PROJECT_BRIEF.md) | Contexto, objetivos e escopo |
| [`ROADMAP.md`](ROADMAP.md) | Evolução planejada |
| [`AGENTS.md`](AGENTS.md) | Princípios e convenções de desenvolvimento |
| [`docs/project-overview.md`](docs/project-overview.md) | Visão detalhada do estado atual |
| [`docs/olist-acquisition.md`](docs/olist-acquisition.md) | Processo de aquisição do Olist |
| [`docs/raw-layer.md`](docs/raw-layer.md) | Responsabilidades da camada RAW |
| [`docs/README.md`](docs/README.md) | Índice da documentação técnica |

---

## Project Status

**Current milestone: Ingestion Foundation**

A primeira pipeline funcional está concluída e validada com dados reais.

O próximo estágio da plataforma será direcionado à **transformação e modelagem analítica com dbt**.

O projeto continua em desenvolvimento e será evoluído de forma incremental.

---

## License

MIT License.

Consulte [`LICENSE`](LICENSE) para os termos completos.
