# dbt Foundation

## Responsabilidade

O dbt transforma as tabelas preservadas no schema PostgreSQL `raw` em modelos técnicos no schema `staging`. A ingestão Python continua sendo a única responsável por aquisição, validação e carga da origem.

## Estrutura atual

Cada uma das nove tabelas RAW é declarada como source e possui um modelo staging correspondente. Os modelos são views e realizam somente padronização de valores vazios, casts técnicos e aliases de nomes incorretos na fonte.

## Execução

```bash
uv run dbt debug --project-dir dbt --profiles-dir dbt
uv run dbt build --project-dir dbt --profiles-dir dbt
```

O profile usa exclusivamente variáveis de ambiente. `DBT_TARGET_SCHEMA` define o schema de saída e deve ser `staging` no ambiente local.

## Limites

Não há modelos intermediate, marts, métricas, KPIs, regras de negócio ou orquestração. Essas etapas permanecem futuras.
