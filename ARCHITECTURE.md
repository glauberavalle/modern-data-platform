# Arquitetura

Este documento descreve a arquitetura de alto nível da `modern-data-platform` e sua evolução planejada.

A plataforma está sendo construída de forma incremental, começando pela fundação local e pela ingestão de dados e evoluindo posteriormente para transformação, orquestração, qualidade, observabilidade e consumo analítico.

---

## Objetivo arquitetural

A plataforma foi projetada para permitir a construção incremental de pipelines de dados com separação clara entre:

- aquisição;
- validação;
- ingestão;
- transformação;
- orquestração;
- armazenamento analítico;
- qualidade e observabilidade;
- documentação e governança.

A arquitetura deve permitir que novas capacidades sejam adicionadas sem acoplar desnecessariamente as diferentes etapas do ciclo de vida dos dados.

---

## Arquitetura atual

A primeira versão funcional da plataforma implementa o fluxo:

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
Componentes atuais
Acquisition

Responsável pela aquisição do dataset público Olist.

Principais responsabilidades:

realizar o download da fonte configurada;
extrair os arquivos do dataset;
armazenar os arquivos externamente ao código;
reutilizar uma aquisição local válida quando possível;
garantir que a aquisição anterior não seja substituída em caso de falha.

A aquisição não possui responsabilidade sobre PostgreSQL ou regras de negócio.

Validation

Responsável pela validação estrutural dos arquivos antes da carga.

Entre as verificações estão:

existência dos arquivos esperados;
estrutura dos CSVs;
cabeçalhos;
quantidade de colunas;
integridade estrutural básica.

A validação não transforma os dados.

Ingestion Service

Responsável por coordenar as etapas de validação e carga.

O serviço funciona como ponto de coordenação entre os componentes especializados, mantendo a lógica de aquisição, validação e carregamento separada.

PostgreSQL RAW

O PostgreSQL é utilizado atualmente como armazenamento local da camada RAW.

A carga cria:

schema raw;
uma tabela para cada arquivo fonte;
valores preservados como TEXT.

A ingestão é idempotente e uma nova execução substitui o conteúdo das tabelas RAW após a validação bem-sucedida.

A camada RAW não aplica:

regras de negócio;
métricas;
KPIs;
deduplicação;
relacionamentos analíticos;
transformações analíticas.
Arquitetura planejada

A plataforma será expandida progressivamente para incluir transformação, orquestração e consumo analítico.

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
                    ┌─────────┐
                    │   dbt   │
                    └────┬────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           STAGING   INTERMEDIATE   MARTS
                                     │
                                     ▼
                              ANALYTICS / BI

A orquestração será adicionada posteriormente:

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
                    MARTS

Esses componentes representam a arquitetura planejada e não devem ser interpretados como funcionalidades já implementadas.

Camadas de dados

A evolução da plataforma seguirá uma separação progressiva das responsabilidades.

RAW

Responsável pela preservação dos dados de origem.

Source → RAW

Não deve conter regras de negócio ou transformações analíticas.

STAGING

Camada futura destinada à preparação dos dados para modelagem.

Responsabilidades esperadas:

tipagem;
padronização;
renomeação;
tratamento técnico dos dados;
aplicação de transformações simples e consistentes.
INTERMEDIATE

Camada futura para transformações reutilizáveis e lógica intermediária necessária à construção dos modelos analíticos.

MARTS

Camada futura destinada aos modelos orientados ao consumo analítico.

Poderá conter:

entidades de negócio;
métricas;
agregações;
modelos dimensionais;
estruturas para consumo por SQL ou ferramentas de BI.
Orquestração

A orquestração com Apache Airflow está planejada para uma etapa posterior.

A decisão de introduzir um orquestrador dedicado será baseada na complexidade dos pipelines e na necessidade de:

agendamento;
dependências entre tarefas;
execução coordenada;
monitoramento operacional;
tratamento de falhas.

Enquanto a complexidade permanecer baixa, a execução local por scripts continuará sendo suficiente.

Qualidade e observabilidade

A plataforma será evoluída progressivamente para incluir mecanismos de qualidade e observabilidade.

Entre as possibilidades futuras estão:

testes de qualidade dos dados;
validações automatizadas;
monitoramento de pipelines;
métricas de execução;
identificação de falhas;
documentação operacional.

Esses componentes serão introduzidos conforme a plataforma adquirir maior complexidade.

Infraestrutura local

A infraestrutura atual utiliza Docker Compose para fornecer o ambiente local.

Docker Compose
      │
      ├── PostgreSQL 16
      │
      └── pgAdmin 4

Os serviços utilizam:

volumes persistentes;
rede Docker dedicada;
healthcheck do PostgreSQL;
configuração por variáveis de ambiente.

O objetivo é manter a infraestrutura local reproduzível e simples.

Organização do código

A implementação segue separação por responsabilidade:

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

Os pontos de entrada ficam separados da implementação:

scripts/
├── download_olist.py
└── ingest_olist.py

Isso permite que a lógica de negócio e infraestrutura seja reutilizada por diferentes mecanismos de execução no futuro.

Princípios da arquitetura

A evolução da plataforma segue os seguintes princípios:

Separação de responsabilidades — cada componente deve possuir uma função clara.
Baixo acoplamento — componentes devem depender o mínimo possível de detalhes de outras camadas.
Evolução incremental — novas capacidades são adicionadas conforme a necessidade.
Reprodutibilidade — ambientes, dependências e fontes devem permitir reproduzir o processo.
Idempotência — execuções repetidas não devem produzir duplicações inesperadas.
Preservação da origem — a camada RAW deve manter os dados próximos da fonte.
Testabilidade — componentes críticos devem possuir testes automatizados.
Evitar over engineering — ferramentas e abstrações devem ser introduzidas quando houver justificativa técnica.
Estado atual

A primeira fundação funcional da plataforma está concluída:

Infrastructure
      ↓
Olist Acquisition
      ↓
Validation
      ↓
PostgreSQL RAW

O estágio atual da arquitetura inclui a camada de transformação técnica com dbt:

RAW
 ↓
STAGING
 ↓
INTERMEDIATE
 ↓
MARTS

A arquitetura será revisada conforme novas capacidades forem implementadas e os requisitos do projeto evoluírem.


### Por que essa versão é melhor?

Porque agora o documento separa explicitamente:

**🟢 O que existe**

```text
Docker
PostgreSQL
Acquisition
Validation
Service
RAW
Tests

🔵 O que está planejado

dbt
STAGING
INTERMEDIATE
MARTS
Airflow
Quality
Observability
Analytics

Isso é especialmente importante para o seu GitHub. Um recrutador que abrir ARCHITECTURE.md não vai ficar com a impressão de que você está dizendo que implementou Airflow quando, na verdade, ele está no roadmap.

E agora temos uma sequência documental coerente:

README
  │
  ├── "O que é?"
  │
  ▼
ARCHITECTURE.md
  │
  ├── "Como funciona?"
  │
  ▼
ROADMAP.md
  │
  └── "Para onde vai?"
