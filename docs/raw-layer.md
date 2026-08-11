# Camada RAW

## Objetivo

A camada RAW representa a primeira camada de armazenamento da plataforma e tem como objetivo preservar os dados de origem de forma estruturalmente fiel.

Nesta plataforma, os arquivos CSV públicos do Olist são adquiridos, validados e carregados no PostgreSQL, utilizando o schema `raw` e uma tabela para cada arquivo de origem.

A RAW funciona como uma representação técnica da fonte antes da aplicação de transformações analíticas.

---

## Fluxo

```text
Arquivo de origem
       ↓
Acquisition
       ↓
Validation
       ↓
RAW Loader
       ↓
PostgreSQL / raw

A validação ocorre antes da carga. A camada RAW recebe somente arquivos que atendem aos contratos técnicos definidos para a ingestão.

Responsabilidades

O processo de ingestão da RAW é responsável por:

criar o schema raw, quando necessário;
criar as tabelas técnicas correspondentes aos arquivos de origem;
preservar os nomes das colunas provenientes dos cabeçalhos;
carregar os valores de origem sem aplicação de regras de negócio;
utilizar carga idempotente;
registrar logs sobre as etapas de validação e carga;
manter a separação entre dados de origem e transformações analíticas.
Estrutura atual

O dataset Olist possui nove arquivos CSV esperados, representados atualmente por nove tabelas no schema raw.

PostgreSQL
└── raw
    ├── olist_customers_dataset
    ├── olist_geolocation_dataset
    ├── olist_order_items_dataset
    ├── olist_order_payments_dataset
    ├── olist_order_reviews_dataset
    ├── olist_orders_dataset
    ├── olist_products_dataset
    ├── olist_sellers_dataset
    └── product_category_name_translation

A ingestão real resultou em:

9 tabelas

1.548.022 registros

As contagens foram verificadas diretamente no PostgreSQL utilizando COUNT(*).

Representação dos dados

As colunas da RAW são carregadas como TEXT.

Essa decisão evita antecipar decisões de modelagem e mantém a camada de origem próxima da estrutura fornecida pelo dataset.

Tipagem, padronização e transformações analíticas serão responsabilidade das camadas posteriores.

Permitido

Podem existir na RAW:

tabelas que representem arquivos-fonte;
colunas com os mesmos nomes dos cabeçalhos de origem;
valores preservados conforme a fonte;
estruturas técnicas necessárias para a carga;
mecanismos de carga idempotente;
logs técnicos relacionados à ingestão.
Não permitido

A RAW não deve conter:

limpeza de dados;
conversão analítica de tipos;
deduplicação;
enriquecimento;
criação de relacionamentos analíticos;
regras de negócio;
métricas;
KPIs;
agregações;
modelos dimensionais;
lógica específica de consumo.

A RAW não é uma camada analítica.

Idempotência

A ingestão foi projetada para permitir novas execuções sem gerar duplicações inesperadas.

Após a validação bem-sucedida dos arquivos, o conteúdo das tabelas RAW pode ser substituído pela nova carga.

Esse comportamento permite que a mesma fonte seja ingerida novamente de forma controlada.

Relação com o dbt

Em uma sprint futura, o dbt consumirá as tabelas raw como fontes declaradas.

A evolução esperada será:

RAW
 ↓
STAGING
 ↓
INTERMEDIATE
 ↓
MARTS

A camada RAW permanecerá responsável pela preservação da origem.

O dbt será responsável pelas etapas posteriores de:

tipagem;
padronização;
transformações;
testes de dados;
modelagem;
construção das estruturas analíticas.

Dessa forma, as transformações permanecem separadas da origem e a rastreabilidade até os arquivos fonte é preservada.

Limites da camada

A RAW deve permanecer simples.

Seu objetivo não é produzir dados prontos para consumo, mas fornecer uma representação confiável e rastreável da fonte para as camadas posteriores.

Qualquer transformação que altere o significado, a estrutura analítica ou a interpretação dos dados deve ser avaliada para implementação fora da RAW.


### Esse documento agora fecha uma lacuna importante

A arquitetura fica:

```text
                 OLIST
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
             ┌─────┴─────┐
             ▼           ▼
           dbt         futuro
             │
             ▼
          STAGING
             │
             ▼
        INTERMEDIATE
             │
             ▼
           MARTS