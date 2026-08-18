# Arquitetura

Este documento descreve a arquitetura de alto nível da `modern-data-platform` e sua evolução planejada.

A plataforma está sendo construída de forma incremental, começando pela fundação local e pela ingestão de dados e evoluindo para transformação, modelagem analítica, orquestração, qualidade, observabilidade e consumo analítico.

---

## Objetivo arquitetural

A plataforma foi projetada para permitir a construção incremental de pipelines de dados com separação clara entre:

- aquisição;
- validação;
- ingestão;
- transformação;
- modelagem analítica;
- orquestração;
- armazenamento analítico;
- qualidade e observabilidade;
- documentação e governança.

A arquitetura deve permitir que novas capacidades sejam adicionadas sem acoplar desnecessariamente as diferentes etapas do ciclo de vida dos dados.

---

## Arquitetura atual

A arquitetura atualmente implementada segue o fluxo:

```text
Kaggle / Olist
      │
      ▼
 Acquisition
      │
      ▼
External Files
      │
      ▼
 Validation
      │
      ▼
Ingestion Service
      │
      ▼
PostgreSQL RAW
      │
      ▼
dbt Sources
      │
      ▼
dbt Staging
```

A aquisição, validação, ingestão e transformação são componentes separados.

A camada RAW permanece sob responsabilidade da ingestão Python. O dbt consome as tabelas RAW como `sources` e constrói os modelos de staging.

O fluxo atual termina na camada de staging. A modelagem de negócio e os marts ainda não foram implementados.

---

## Componentes atuais

### Acquisition

Responsável pela aquisição do dataset público Olist.

Principais responsabilidades:

- realizar o download da fonte configurada;
- extrair os arquivos do dataset;
- armazenar os arquivos externamente ao código;
- reutilizar uma aquisição local válida quando possível;
- garantir que a aquisição anterior não seja substituída em caso de falha.

A aquisição não possui responsabilidade sobre PostgreSQL, dbt ou regras de negócio.

### Validation

Responsável pela validação estrutural dos arquivos antes da carga.

Entre as verificações estão:

- existência dos arquivos esperados;
- estrutura dos CSVs;
- cabeçalhos;
- quantidade de colunas;
- integridade estrutural básica.

A validação não transforma os dados.

### Ingestion Service

Responsável por coordenar as etapas de validação e carga.

O serviço funciona como ponto de coordenação entre os componentes especializados, mantendo a lógica de aquisição, validação e carregamento separada.

### PostgreSQL RAW

O PostgreSQL é utilizado atualmente como armazenamento local da camada RAW.

A carga cria:

- schema `raw`;
- uma tabela para cada arquivo fonte;
- valores preservados como `TEXT`.

A ingestão é idempotente e uma nova execução substitui o conteúdo das tabelas RAW após a validação bem-sucedida.

A camada RAW não aplica:

- regras de negócio;
- métricas;
- KPIs;
- deduplicação;
- relacionamentos analíticos;
- transformações analíticas.

### dbt

O dbt foi introduzido como camada de transformação e modelagem sobre a RAW.

Sua responsabilidade atual inclui:

- declarar as tabelas RAW como sources;
- construir modelos de staging;
- realizar transformações técnicas;
- aplicar tipagem;
- executar testes de dados;
- estabelecer dependências e lineage entre as camadas.

O dbt não substitui a ingestão Python.

A separação atual é:

```text
Python → aquisição, validação e ingestão
dbt    → transformação, testes e modelagem
```

### STAGING

A camada `staging` é atualmente implementada com dbt.

Os modelos são derivados diretamente das sources RAW e são materializados como views.

As transformações atuais são estritamente técnicas, incluindo:

- conversão de tipos;
- tratamento técnico de valores vazios;
- padronização de nomes;
- preparação dos dados para as próximas camadas.

Não são aplicadas regras de negócio, métricas ou agregações nesta camada.

---

## Arquitetura de dados

A evolução da plataforma segue a seguinte separação:

```text
                    DATA SOURCES
                         │
                         ▼
                   ACQUISITION
                         │
                         ▼
                    VALIDATION
                         │
                         ▼
                       RAW
                         │
                         ▼
                  dbt SOURCES
                         │
                         ▼
                     STAGING
                         │
                         ▼
                  ANALYTICAL MODELING
                         │
                         ▼
                       MARTS
                         │
                         ▼
                  ANALYTICS / BI
```

As partes até `STAGING` estão implementadas.

As camadas de modelagem analítica, marts e consumo ainda fazem parte da evolução planejada.

---

## Camadas de dados

A evolução da plataforma segue uma separação progressiva das responsabilidades.

### RAW

Responsável pela preservação dos dados de origem.

```text
Source → RAW
```

A RAW deve permanecer próxima da fonte e não deve conter regras de negócio ou transformações analíticas.

### STAGING

Camada implementada com dbt para preparação técnica dos dados.

```text
RAW → STAGING
```

Responsabilidades:

- tipagem;
- padronização;
- renomeação;
- tratamento técnico dos dados;
- aplicação de transformações simples e consistentes;
- testes estruturais.

Os modelos atuais são materializados como views.

### INTERMEDIATE

Camada futura para transformações reutilizáveis e lógica intermediária necessária à construção dos modelos analíticos.

Ainda não implementada.

### MARTS

Camada futura destinada aos modelos orientados ao consumo analítico.

Poderá conter:

- entidades de negócio;
- métricas;
- agregações;
- modelos dimensionais;
- estruturas para consumo por SQL ou ferramentas de BI.

A primeira camada de marts será definida a partir de um problema analítico específico, ainda não escolhido.

---

## Orquestração

A orquestração com Apache Airflow está planejada para uma etapa posterior.

A decisão de introduzir um orquestrador dedicado será baseada na complexidade dos pipelines e na necessidade de:

- agendamento;
- dependências entre tarefas;
- execução coordenada;
- monitoramento operacional;
- tratamento de falhas.

Enquanto a complexidade permanecer baixa, a execução local por scripts e comandos dbt continuará sendo suficiente.

Uma evolução futura poderá seguir o fluxo:

```text
                    AIRFLOW
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
     Acquisition   Validation      dbt
          │            │            │
          └────────────┴────────────┘
                       │
                       ▼
                     RAW
                       │
                       ▼
                    STAGING
                       │
                       ▼
                     MARTS
```

O Airflow ainda não faz parte da implementação atual.

---

## Qualidade e observabilidade

A plataforma será evoluída progressivamente para incluir mecanismos de qualidade e observabilidade.

A implementação atual já possui:

- testes automatizados para componentes de ingestão;
- validação estrutural dos arquivos;
- testes declarados nos modelos dbt;
- validação do build da camada de staging.

Entre as possibilidades futuras estão:

- testes de qualidade de dados mais abrangentes;
- monitoramento de pipelines;
- métricas de execução;
- identificação de falhas;
- documentação operacional;
- observabilidade da plataforma.

Esses componentes serão introduzidos conforme a plataforma adquirir maior complexidade.

---

## Infraestrutura local

A infraestrutura atual utiliza Docker Compose para fornecer o ambiente local.

```text
Docker Compose
      │
      ├── PostgreSQL 16
      │
      └── pgAdmin 4
```

Os serviços utilizam:

- volumes persistentes;
- rede Docker dedicada;
- healthcheck do PostgreSQL;
- configuração por variáveis de ambiente.

O objetivo é manter a infraestrutura local reproduzível e simples.

O dbt é executado no ambiente Python local e utiliza o PostgreSQL como destino para execução dos modelos.

---

## Organização do código

A implementação segue separação por responsabilidade:

```text
src/
└── ingestion/
    ├── acquisition/
    │   └── olist_acquirer.py
    │
    ├── validation/
    │   └── csv_validator.py
    │
    ├── loading/
    │   └── postgres_loader.py
    │
    ├── contracts.py
    └── service.py
```

Os pontos de entrada ficam separados da implementação:

```text
scripts/
├── download_olist.py
└── ingest_olist.py
```

A camada dbt possui estrutura própria:

```text
dbt/
├── dbt_project.yml
├── profiles.yml
└── models/
    └── staging/
        └── olist/
```

Isso permite manter a lógica de ingestão Python separada das transformações e modelos SQL do dbt.

---

## Princípios da arquitetura

A evolução da plataforma segue os seguintes princípios:

- **Separação de responsabilidades** — cada componente deve possuir uma função clara.
- **Baixo acoplamento** — componentes devem depender o mínimo possível de detalhes de outras camadas.
- **Evolução incremental** — novas capacidades são adicionadas conforme a necessidade.
- **Reprodutibilidade** — ambientes, dependências e fontes devem permitir reproduzir o processo.
- **Idempotência** — execuções repetidas não devem produzir duplicações inesperadas.
- **Preservação da origem** — a camada RAW deve manter os dados próximos da fonte.
- **Testabilidade** — componentes críticos devem possuir testes automatizados.
- **Modelagem explícita** — transformações e dependências devem ser versionadas e documentadas.
- **Evitar over engineering** — ferramentas e abstrações devem ser introduzidas quando houver justificativa técnica.

---

## Estado atual

A fundação de ingestão está concluída:

```text
Infrastructure
      ↓
Olist Acquisition
      ↓
Validation
      ↓
PostgreSQL RAW
```

A primeira camada de transformação também está implementada:

```text
PostgreSQL RAW
      ↓
dbt Sources
      ↓
dbt STAGING
```

O próximo estágio será:

```text
STAGING
      ↓
Problema analítico
      ↓
Modelagem
      ↓
MART
      ↓
Analytics / BI
```

A definição da primeira solução analítica será feita antes da implementação dos marts.

Apache Airflow, observabilidade avançada e outras capacidades de plataforma permanecem planejados para etapas futuras.

A arquitetura será revisada conforme novas capacidades forem implementadas e os requisitos do projeto evoluírem.