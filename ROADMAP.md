# Roadmap

Este roadmap descreve a evolução incremental da Modern Data Platform.

Cada Sprint deve entregar uma capacidade funcional clara, mantendo simplicidade, reprodutibilidade e qualidade técnica. Novas tecnologias e decisões arquiteturais devem ser introduzidas conforme exista uma necessidade concreta.

---

## Princípios de priorização

- cada Sprint deve entregar valor real e verificável;
- mudanças arquiteturais devem ser avaliadas antes de serem implementadas;
- a complexidade deve acompanhar a necessidade do projeto;
- cada camada deve possuir uma responsabilidade clara;
- decisões técnicas devem ser documentadas;
- a plataforma deve evoluir de forma incremental;
- evitar over engineering.

---

# Sprint 1 — Fundação do repositório

**Status: Concluída**

### Objetivo

Estabelecer a estrutura inicial, as convenções e as ferramentas fundamentais do projeto.

### Entregas

- estrutura inicial do repositório;
- documentação inicial de arquitetura;
- `AGENTS.md`;
- `PROJECT_BRIEF.md`;
- `ARCHITECTURE.md`;
- `ROADMAP.md`;
- configuração inicial do Python;
- gerenciamento de dependências;
- configuração de qualidade de código;
- estrutura inicial para testes;
- configuração inicial de CI;
- definição das convenções de desenvolvimento.

---

# Sprint 2 — Infraestrutura local

**Status: Concluída**

### Objetivo

Estabelecer uma infraestrutura local reproduzível para desenvolvimento e execução da plataforma.

### Entregas

- Docker Compose;
- PostgreSQL 16;
- pgAdmin 4;
- volumes persistentes;
- rede Docker dedicada;
- healthcheck do PostgreSQL;
- configuração por variáveis de ambiente;
- `.env.example`;
- comandos auxiliares de desenvolvimento;
- documentação de inicialização da infraestrutura.

---

# Sprint 3 — Ingestion Foundation

**Status: Concluída**

### Objetivo

Implementar a primeira pipeline funcional de aquisição, validação e ingestão de dados.

### Fonte

**Brazilian E-Commerce Public Dataset by Olist**

Versão configurada:

```text
2
```

### Entregas

- aquisição automatizada do dataset Olist;
- download e extração do arquivo ZIP;
- armazenamento local dos arquivos externos;
- validação estrutural dos nove CSVs;
- contratos técnicos dos arquivos;
- separação entre aquisição, validação e carga;
- serviço de ingestão;
- carga idempotente;
- schema `raw` no PostgreSQL;
- nove tabelas RAW;
- preservação dos valores de origem;
- testes automatizados;
- logs da ingestão;
- documentação da aquisição e da camada RAW.

### Resultado validado

A ingestão foi executada com dados reais e resultou em:

- **9 tabelas RAW**
- **1.548.022 registros**

distribuídos entre os arquivos do dataset Olist.

---

# Sprint 4 — dbt Foundation

**Status: Concluída**

### Objetivo

Introduzir o dbt como camada de transformação, testes e documentação sobre a RAW.

### Entregas

- configuração do projeto dbt;
- integração com PostgreSQL;
- configuração do profile sem credenciais versionadas;
- definição das tabelas RAW como sources;
- criação da camada de staging;
- 9 modelos de staging;
- transformação e tipagem técnica dos dados;
- padronização técnica dos campos;
- testes nativos do dbt;
- definição das dependências entre sources e modelos;
- lineage entre RAW e staging;
- materialização dos modelos de staging como views;
- documentação da fundação dbt;
- validação com `dbt debug`;
- validação com `dbt build`.

### Arquitetura atual

```text
RAW
 ↓
dbt Sources
 ↓
STAGING
```

A camada RAW continua responsável pela preservação dos dados de origem.

O dbt é responsável pelas transformações posteriores.

Regras de negócio e métricas ainda não fazem parte desta etapa.

---

# Sprint 5 — Analytical Modeling & Marts

**Status: Próxima etapa**

### Objetivo

Transformar os dados preparados no staging em uma solução analítica orientada a um problema de negócio concreto.

Antes da implementação dos modelos, será definido um problema analítico que determine quais entidades, métricas e relacionamentos são necessários.

### Possíveis camadas

```text
STAGING
   ↓
INTERMEDIATE
   ↓
MARTS
   ↓
Analytics / BI
```

### Objetivos

- definir o primeiro problema analítico;
- identificar as perguntas de negócio que a solução deve responder;
- definir entidades e métricas necessárias;
- avaliar a necessidade de uma camada intermediate;
- construir modelos analíticos com dbt;
- criar fatos e/ou dimensões quando fizer sentido;
- definir testes de qualidade para os modelos;
- documentar os modelos e suas regras;
- disponibilizar uma primeira camada pronta para consumo analítico.

A modelagem será orientada pelo problema e não pela necessidade de criar tabelas arbitrariamente.

---

# Sprint 6 — Orchestration

**Status: Planejada**

### Objetivo

Introduzir orquestração quando a complexidade dos pipelines justificar um orquestrador dedicado.

### Objetivos

- integrar Apache Airflow;
- estruturar DAGs;
- definir dependências entre etapas;
- executar aquisição e ingestão de forma orquestrada;
- preparar execução dos modelos dbt;
- documentar operações do pipeline;
- tratar falhas e reexecuções.

### Arquitetura esperada

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

A introdução do Airflow será feita somente quando a complexidade do pipeline justificar a necessidade de um orquestrador dedicado.

---

# Sprint 7 — Data Quality & CI/CD

**Status: Planejada**

### Objetivo

Aumentar a confiabilidade dos dados, modelos e processos de desenvolvimento.

### Objetivos

- ampliar os testes de qualidade dos dados;
- integrar validações ao CI;
- executar testes automaticamente;
- validar código e modelos;
- evoluir GitHub Actions;
- estabelecer verificações de qualidade antes de alterações serem integradas;
- documentar os processos de qualidade;
- avaliar mecanismos adicionais de data contracts e validação.

---

# Sprint 8 — Observability & Analytics

**Status: Planejada**

### Objetivo

Evoluir a plataforma para maior visibilidade operacional e consumo analítico.

### Possíveis evoluções

- monitoramento dos pipelines;
- métricas de execução;
- identificação de falhas;
- documentação operacional;
- observabilidade dos modelos;
- evolução das camadas analíticas;
- camada de consumo para SQL e BI;
- indicadores derivados do dataset Olist.

A implementação desta Sprint dependerá das necessidades observadas nas etapas anteriores.

---

# Fase posterior

Após a consolidação das etapas anteriores, a plataforma poderá evoluir para cenários mais complexos envolvendo:

- novas fontes de dados;
- múltiplos pipelines;
- governança;
- data lineage;
- observabilidade avançada;
- ambientes separados;
- automação de deploy;
- evolução da arquitetura de armazenamento;
- novos casos de uso analítico.

Essas evoluções serão avaliadas conforme o projeto crescer e não fazem parte do escopo atual.

---

## Estado atual

```text
                 MODERN DATA PLATFORM

Sprint 1
Fundação
    ↓
Sprint 2
Infraestrutura
    ↓
Sprint 3
Olist → RAW
    ↓
Sprint 4
RAW → dbt → STAGING
    ↓
Sprint 5
STAGING → Modelagem → MART
    ↓
Sprint 6
Airflow
    ↓
Sprint 7
Quality + CI/CD
    ↓
Sprint 8
Observability + Analytics
```

**Current milestone: Analytical Modeling & Marts**

A fundação de ingestão está concluída.

A fundação dbt e a camada de staging também estão implementadas e validadas.

O próximo objetivo é definir um problema analítico e construir uma primeira camada de modelos/marts que entregue uma solução concreta.
