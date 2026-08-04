# Roadmap

Este roadmap descreve as sprints planejadas para a evolução inicial do projeto, sempre com foco em entregar valor real, manter simplicidade e evitar over engineering.

## Princípios de priorização

- cada Sprint deve entregar algo útil e compreensível;
- mudanças arquiteturais devem ser avaliadas antes de serem implementadas;
- melhorias importantes podem ser adicionadas ao roadmap para análise posterior;
- a estrutura deve permitir crescimento sem grandes refatorações.

## Sprint 1 — Fundação do repositório

- criar estrutura inicial do projeto;
- documentar arquitetura e diretrizes;
- configurar ferramentas de qualidade;
- preparar ambientes com Docker Compose;
- definir padrões de contribuição.

## Sprint 2 — Infraestrutura base

- definir variáveis de ambiente;
- preparar containers e serviços iniciais;
- estruturar diretórios para pipelines e modelos;
- documentar fluxos de desenvolvimento.

## Sprint 3 — Ingestão e transformação

- definir fontes de dados iniciais;
- estruturar pipelines de ingestão;
- preparar camada de staging e warehouse;
- organizar modelos no dbt.

## Sprint 4 — Orquestração e observabilidade

- integrar Apache Airflow;
- criar organização inicial de DAGs;
- preparar logs, monitoramento e documentação operacional.

## Sprint 5 — Qualidade e CI/CD

- integrar GitHub Actions;
- aplicar verificações automáticas;
- preparar evolução da governança do projeto.

## Fase posterior

A partir desta base, o projeto poderá evoluir para cenários mais complexos de dados, governança e automação.
