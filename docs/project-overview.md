# Visão geral do projeto

## Propósito

O `modern-data-platform` é uma plataforma de dados local, desenvolvida incrementalmente como projeto de portfólio. O objetivo atual é demonstrar uma fundação técnica reproduzível para receber dados públicos, preservá-los em uma camada RAW e preparar a evolução futura para transformação, orquestração e consumo analítico.

O dataset utilizado atualmente é o [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

## Estado atual

As três primeiras sprints disponibilizaram:

- infraestrutura local com PostgreSQL 16 e pgAdmin 4 via Docker Compose;
- volumes Docker persistentes e rede dedicada aos serviços;
- configuração local centralizada no arquivo `.env`;
- aquisição reproduzível dos nove arquivos CSV do Olist;
- validação estrutural dos arquivos antes da carga;
- criação automática do schema `raw` e das tabelas de origem;
- carga idempotente dos CSVs no PostgreSQL, sem transformações analíticas;
- logs de execução;
- testes automatizados;
- documentação técnica e operacional da ingestão e da camada RAW.

### Resultado validado

A ingestão foi executada com dados reais e resultou em:

- **9 tabelas no schema `raw`**;
- **1.548.022 registros carregados**.

As contagens foram verificadas diretamente no PostgreSQL utilizando `COUNT(*)` em cada tabela RAW.

## Fluxo de dados

```text
Kaggle: dataset público Olist (ZIP)
                ↓
acquisition: download e extração
                ↓
data/external/olist/*.csv
                ↓
validation: arquivo, codificação,
cabeçalho e estrutura
                ↓
ingestion service
                ↓
loading: PostgreSQL / schema raw

Cada etapa possui responsabilidade única:

Acquisition obtém e extrai os arquivos; não acessa o banco de dados.
Validation confirma que os CSVs correspondem ao contrato técnico esperado; não altera os arquivos.
Ingestion Service coordena as etapas de validação e carga.
Loading cria as tabelas e carrega os valores originais; não aplica lógica de negócio.
Componentes principais
Componente	Localização	Responsabilidade
Infraestrutura	docker-compose.yml	PostgreSQL 16 e pgAdmin 4 locais
Configuração	src/config.py	Leitura e validação da configuração de execução
Aquisição	src/ingestion/acquisition/	Download e extração do dataset Olist
Validação	src/ingestion/validation/	Validação estrutural dos CSVs
Carga	src/ingestion/loading/	Carga dos CSVs no PostgreSQL
Coordenação	src/ingestion/service.py	Coordenação local da validação e carga
Contratos	src/ingestion/contracts.py	Definição dos arquivos esperados
Comandos	scripts/ e Makefile	Pontos de execução de desenvolvimento
Como executar

Crie a configuração local:

make setup

Inicie a infraestrutura:

docker compose up -d

Adquira os dados de origem:

make download-olist

Valide e carregue a RAW:

make ingest-olist
Consulte os serviços:
PostgreSQL: localhost:5432
pgAdmin: http://localhost:5050

Em ambientes sem make, execute diretamente:

uv run python -m scripts.download_olist
uv run python -m scripts.ingest_olist
Camada RAW

O schema raw possui uma tabela para cada arquivo CSV do Olist.

As colunas são carregadas como TEXT para representar a origem com fidelidade e evitar antecipar decisões de modelagem.

A RAW não realiza:

conversão analítica de tipos;
limpeza de valores;
deduplicação;
criação de relacionamentos analíticos;
regras de negócio;
métricas ou KPIs;
modelos dbt;
DAGs do Airflow.

Esses limites preservam a rastreabilidade da fonte e permitem que as transformações futuras sejam realizadas em camadas posteriores.

Veja também raw-layer.md.

Estrutura de dados local
data/
├── external/
│   └── olist/          # CSVs originais adquiridos; ignorados pelo Git
├── raw/                # reservado para artefatos locais futuros
└── processed/          # reservado para camadas futuras

Os arquivos externos do dataset não são versionados pelo Git.

A aquisição utiliza uma área temporária e somente substitui a cópia local existente após a extração bem-sucedida dos nove CSVs esperados.

Veja olist-acquisition.md para detalhes.

Evolução planejada

A próxima etapa da plataforma é a transformação e modelagem analítica com dbt.

A evolução planejada segue:

RAW
 ↓
STAGING
 ↓
INTERMEDIATE
 ↓
MARTS
 ↓
Analytics / BI

Posteriormente, o Apache Airflow poderá ser introduzido para orquestrar as etapas do pipeline.

O projeto ainda não implementa:

modelos dbt;
transformações analíticas;
DAGs do Airflow;
métricas de negócio;
dashboards;
observabilidade avançada.

Essas capacidades fazem parte das próximas etapas do roadmap.

O dbt deverá consumir as tabelas raw como fontes, enquanto o Airflow poderá acionar os componentes existentes de aquisição e ingestão sem duplicar suas regras de execução.


### Uma correção conceitual importante

Eu também mudei:

> `loading: PostgreSQL / schema raw`

para:

```text
ingestion service
        ↓
loading
        ↓
PostgreSQL / raw

porque agora nossa arquitetura deixa mais evidente que service.py coordena e o loader executa a carga. Isso é exatamente a separação que construímos.

E agora os quatro documentos começam a contar a mesma história:

Documento	Papel
README.md	Visão pública do projeto
PROJECT_BRIEF.md	Contexto, objetivos e escopo
ARCHITECTURE.md	Como a plataforma é estruturada
docs/project-overview.md	Como a implementação atual funciona
ROADMAP.md	Próximas etapas
CHANGELOG.md	O que já foi entregue
