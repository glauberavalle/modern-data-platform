# Project Brief

## 1. Visão Geral

A Modern Data Platform é uma plataforma de dados construída de forma incremental para consolidar, organizar e disponibilizar dados de uma operação brasileira de e-commerce para análise.

O projeto representa a construção de um ambiente de dados capaz de transformar dados provenientes de fontes externas em uma base estruturada, confiável e reproduzível, evoluindo progressivamente de uma camada RAW para transformação, modelagem analítica e mecanismos de orquestração, qualidade e observabilidade.

O projeto é desenvolvido como um portfólio técnico, mas segue princípios de arquitetura, engenharia de dados e Analytics Engineering aplicáveis a ambientes profissionais.

---

## 2. Contexto do Negócio

A empresa fictícia representada pelo projeto é uma operação brasileira de e-commerce com dados relacionados a pedidos, clientes, produtos, vendedores, pagamentos, avaliações e localização.

Essas informações representam diferentes aspectos da operação comercial e podem ser utilizadas posteriormente para construção de análises e indicadores de negócio.

O projeto utiliza o Brazilian E-Commerce Public Dataset by Olist como fonte pública para representar esse cenário.

---

## 3. Problema

A plataforma busca representar problemas comuns em ambientes de dados ainda não consolidados:

- dados distribuídos em diferentes estruturas;
- ausência de uma camada central organizada;
- dificuldade de garantir consistência e rastreabilidade;
- necessidade de separar dados de origem de transformações analíticas;
- dificuldade de evoluir pipelines de forma controlada;
- necessidade de disponibilizar dados preparados para diferentes consumidores analíticos.

A introdução do dbt adiciona uma camada estruturada de transformação entre a RAW e os modelos analíticos, permitindo organizar dependências, testes, documentação e lineage sem transferir a responsabilidade de ingestão para a camada de transformação.

---

## 4. Objetivos

Os objetivos do projeto são:

- consolidar dados provenientes de fontes externas;
- preservar os dados de origem em uma camada RAW;
- construir pipelines reproduzíveis de aquisição, validação e ingestão;
- criar uma arquitetura modular e de baixo acoplamento;
- estruturar uma camada de transformação utilizando dbt;
- evoluir os dados para camadas analíticas estruturadas;
- aplicar práticas de Analytics Engineering na transformação dos dados;
- preparar a plataforma para execução orquestrada;
- estabelecer mecanismos progressivos de qualidade e observabilidade;
- disponibilizar uma base para análises, dashboards e indicadores futuros.

---

## 5. Escopo

O projeto contempla, de forma incremental:

- aquisição de dados;
- validação estrutural;
- ingestão;
- armazenamento da camada RAW;
- transformação e preparação técnica com dbt;
- modelagem analítica;
- testes de qualidade;
- orquestração;
- observabilidade;
- documentação técnica;
- automação de desenvolvimento e CI/CD;
- estrutura para consumo analítico futuro.

As funcionalidades são implementadas conforme o roadmap do projeto e não necessariamente estão todas disponíveis na versão atual.

---

## 6. Fora do Escopo

Os seguintes itens não fazem parte do escopo planejado:

- Apache Spark;
- Apache Kafka;
- Kubernetes;
- Terraform;
- streaming em tempo real;
- machine learning;
- data lake distribuído;
- infraestrutura cloud complexa;
- implementação de sistemas transacionais;
- soluções de negócio específicas fora do contexto da plataforma de dados.

Essas exclusões têm como objetivo manter o projeto focado em engenharia de dados, Analytics Engineering e evolução arquitetural incremental.

---

## 7. Fonte de Dados Atual

A fonte de dados atualmente utilizada é o:

**Brazilian E-Commerce Public Dataset by Olist**

Fonte pública:

```text
Kaggle
```

Versão configurada:

```text
2
```

A distribuição utilizada pelo projeto é um arquivo ZIP contendo nove arquivos CSV.

Os arquivos representam informações relacionadas a:

- pedidos;
- clientes;
- produtos;
- vendedores;
- pagamentos;
- avaliações;
- itens de pedido;
- geolocalização;
- tradução de categorias.

A aquisição é automatizada pelo projeto e os arquivos são armazenados localmente em:

```text
data/external/olist/
```

Os dados externos não são versionados pelo Git.

O código responsável pela aquisição, validação e ingestão é versionado no repositório.

---

## 8. Consumidores da Plataforma

Os principais consumidores esperados são:

- times de Marketing;
- times de Produto;
- área Financeira;
- liderança executiva;
- equipes de Analytics e Data;
- ferramentas de BI.

Esses consumidores representam possibilidades futuras de uso da camada analítica e não implicam integrações já implementadas.

---

## 9. Indicadores Esperados

A plataforma poderá futuramente apoiar análises relacionadas a:

- receita;
- ticket médio;
- clientes recorrentes;
- tempo de entrega;
- cancelamentos;
- avaliações;
- receita por categoria;
- receita por estado;
- comportamento de pedidos;
- desempenho de vendedores e produtos.

Os indicadores serão definidos e implementados nas camadas analíticas futuras.

Este documento não estabelece regras de cálculo ou definições métricas.

---

## 10. Arquitetura Conceitual

A evolução conceitual da plataforma segue:

```text
Data Sources
      ↓
Acquisition
      ↓
Validation
      ↓
RAW
      ↓
STAGING
      ↓
INTERMEDIATE
      ↓
MARTS
      ↓
Analytics / BI
```

Atualmente, as camadas RAW e STAGING estão implementadas.

A camada STAGING é construída com dbt a partir das tabelas RAW declaradas como sources.

As camadas INTERMEDIATE e MARTS ainda não foram implementadas.

A orquestração será adicionada posteriormente:

```text
                 Airflow
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   Acquisition  Ingestion      dbt
        │           │           │
        ▼           ▼           ▼
       RAW        RAW        STAGING
                              │
                              ▼
                            MARTS
```

O Apache Airflow ainda faz parte da evolução planejada.

---

## 11. Estado Atual

A fundação funcional da plataforma está concluída.

Atualmente o projeto possui:

- infraestrutura local com Docker Compose;
- PostgreSQL 16;
- pgAdmin 4;
- aquisição automatizada do Olist;
- validação estrutural dos nove arquivos;
- contratos técnicos dos arquivos;
- serviço de ingestão;
- carga idempotente;
- schema `raw`;
- nove tabelas RAW;
- **1.548.022 registros carregados**;
- testes automatizados;
- lint e formatação;
- pre-commit;
- GitHub Actions;
- documentação técnica.

A camada RAW preserva os valores da fonte e não aplica regras de negócio ou transformações analíticas.

A camada de transformação inicial também está implementada com dbt e possui:

- nove sources correspondentes às tabelas RAW;
- nove modelos de staging;
- transformações técnicas;
- tipagem;
- testes nativos do dbt;
- lineage entre RAW e staging;
- materialização dos modelos como views.

O próximo estágio será a definição de um problema analítico e a construção da primeira camada de modelagem/marts.

---

## 12. Restrições Técnicas

As tecnologias atualmente utilizadas ou previstas para a evolução da plataforma incluem:

### Implementadas

- Python 3.13;
- uv;
- Docker;
- Docker Compose;
- PostgreSQL 16;
- pgAdmin 4;
- dbt Core;
- dbt-postgres;
- pytest;
- Ruff;
- pre-commit;
- Git;
- GitHub Actions.

### Planejadas

- modelagem analítica e marts;
- Apache Airflow;
- evolução das camadas de qualidade;
- observability;
- evolução de CI/CD;
- camada de consumo analítico.

A adoção de novas tecnologias deverá ser justificada pela necessidade do projeto.

---

## 13. Premissas

As seguintes premissas orientam a evolução do projeto:

- o desenvolvimento inicial ocorre em ambiente local;
- a plataforma deve ser reproduzível;
- o dataset Olist representa o cenário inicial de negócio;
- a arquitetura poderá evoluir conforme novas necessidades forem identificadas;
- componentes futuros não devem ser implementados antes de serem necessários;
- a camada RAW deve preservar os dados de origem;
- transformações técnicas devem ocorrer na camada de staging;
- regras de negócio e métricas devem ocorrer nas camadas analíticas;
- decisões arquiteturais relevantes devem ser documentadas.

Estas premissas poderão ser revisadas conforme o projeto evoluir.

---

## 14. Roadmap de Alto Nível

A evolução da plataforma está organizada em etapas:

### Fundação

- estrutura do repositório;
- documentação e convenções;
- infraestrutura local;
- PostgreSQL e ambiente reproduzível.

### Ingestion Foundation

- aquisição do Olist;
- validação dos arquivos;
- ingestão;
- camada RAW;
- testes iniciais.

### Transformation & Analytics Engineering

- integração do dbt;
- definição das sources RAW;
- criação da camada staging;
- testes e documentação;
- definição do primeiro problema analítico;
- modelagem e criação dos primeiros marts.

### Orchestration

- Apache Airflow;
- execução coordenada dos pipelines;
- agendamento e dependências.

### Data Quality & Observability

- evolução dos testes de qualidade;
- monitoramento;
- observabilidade;
- métricas operacionais.

### Analytics

- evolução das camadas analíticas;
- estruturas para consumo;
- dashboards e análises futuras.

O detalhamento de cada etapa está disponível em `ROADMAP.md`.

---

## 15. Considerações Finais

Este documento define o contexto de negócio, os objetivos e o escopo da Modern Data Platform.

Ele serve como referência para as decisões arquiteturais e técnicas do projeto, mas não substitui a documentação específica de arquitetura, implementação ou operação.

A plataforma será desenvolvida incrementalmente, priorizando entregas funcionais, clareza arquitetural, reprodutibilidade e qualidade técnica.

Novas tecnologias, camadas e capacidades serão incorporadas conforme exista uma necessidade concreta para sua adoção.