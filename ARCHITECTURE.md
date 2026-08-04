# Arquitetura

Este documento descreve a arquitetura de alto nível do projeto modern-data-platform.

## Objetivo arquitetural

A plataforma é organizada para permitir desenvolvimento incremental de pipelines de dados com separação clara entre:
- ingestão;
- transformação;
- orquestração;
- armazenamento analítico;
- documentação e governança.

## Componentes principais

### 1. Ingestão

A camada de ingestão é responsável por receber dados de fontes externas ou internas e armazená-los em áreas de staging ou raw.

### 2. Transformação

Os dados passam por uma camada de transformação, onde a lógica de modelagem pode ser organizada de forma modular e progressiva.

### 3. Orquestração

O fluxo de execução é coordenado por Apache Airflow, permitindo o agendamento e a observabilidade dos pipelines.

### 4. Warehouse

O armazenamento analítico é tratado de forma separada, permitindo evolução do modelo de dados sem acoplar demais a camada operacional.

### 5. Governança e documentação

A documentação, o dbt e os arquivos de configuração servem como base para governança, rastreabilidade e entendimento do projeto.

## Princípios da arquitetura

- modularidade;
- separação de responsabilidades;
- baixo acoplamento;
- evolução incremental;
- documentação como parte do ativo do projeto.

## Observação

Esta fase inicial não implementa regras de negócio nem pipelines executáveis. O foco é estruturar a base para crescimento futuro.
