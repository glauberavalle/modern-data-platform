# Changelog

Todas as mudanças relevantes do projeto serão documentadas neste arquivo.

## [0.1.0] - 2026-08-11

### Added

- estrutura inicial do repositório `modern-data-platform`;
- documentação base de arquitetura, roadmap, project brief e diretrizes de desenvolvimento;
- infraestrutura local com Docker Compose;
- PostgreSQL 16;
- pgAdmin 4;
- rede Docker dedicada;
- volumes persistentes;
- configuração de ambiente por `.env`;
- comandos auxiliares de desenvolvimento;
- verificações de qualidade de código;
- aquisição reproduzível do dataset público Brazilian E-Commerce Public Dataset by Olist;
- download e extração dos arquivos do dataset;
- validação estrutural dos nove CSVs esperados;
- contratos técnicos para os arquivos de origem;
- serviço de ingestão;
- carga idempotente no schema PostgreSQL `raw`;
- nove tabelas RAW, uma por arquivo de origem;
- preservação dos valores de origem na camada RAW;
- testes automatizados para os componentes implementados;
- documentação operacional da aquisição e da camada RAW;
- documentação de arquitetura e evolução da plataforma.

### Validated

- aquisição real do dataset Olist;
- reutilização da aquisição local em execuções subsequentes;
- ingestão dos nove arquivos no PostgreSQL;
- 1.548.022 registros carregados na camada RAW;
- validação das contagens diretamente no PostgreSQL.

### Notes

- a camada RAW não aplica regras de negócio ou transformações analíticas;
- não há modelos dbt implementados;
- não há DAGs do Apache Airflow implementadas;
- as camadas STAGING, INTERMEDIATE e MARTS ainda não foram implementadas;
- qualidade de dados e observabilidade avançadas fazem parte das próximas etapas do roadmap.

## [Unreleased]

### Planned

- transformação e modelagem analítica com dbt;
- criação das camadas STAGING, INTERMEDIATE e MARTS;
- orquestração dos pipelines com Apache Airflow;
- evolução dos testes de qualidade;
- observabilidade;
- evolução da camada analítica.