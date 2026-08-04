# modern-data-platform

Este repositório é um projeto pessoal de portfólio, mas deve ser tratado como um produto interno de tecnologia, com foco em arquitetura, engenharia de software, organização, documentação, modelagem de dados e qualidade técnica.

## Constituição do projeto

- O objetivo não é apenas escrever código que funcione, mas demonstrar capacidade de projetar soluções robustas e bem organizadas.
- O projeto será desenvolvido de forma incremental, entregando valor real a cada Sprint.
- Evite over engineering e implemente apenas o necessário para a fase atual.
- Sempre que uma melhoria arquitetural surgir, ela será avaliada antes de entrar no escopo.
- A documentação e as decisões técnicas devem ter o mesmo padrão esperado em um projeto profissional.

## Objetivo

O projeto estabelece a base estrutural para um ambiente de dados preparado para:
- ingestão de dados em diferentes fontes;
- transformação e modelagem progressiva;
- orquestração de pipelines;
- observabilidade e documentação;
- evolução incremental do stack.

## Arquitetura

A arquitetura proposta segue uma abordagem modular, com separação entre:
- ingestão;
- transformação;
- orquestração;
- armazenamento analítico;
- documentação e governança.

Consulte [ARCHITECTURE.md](ARCHITECTURE.md) para detalhes do desenho de alto nível.

## Stack

- Python 3.13
- uv
- Docker
- Docker Compose
- PostgreSQL
- dbt
- Apache Airflow
- Ruff
- pre-commit
- GitHub Actions

## Roadmap

A estratégia inicial está descrita em [ROADMAP.md](ROADMAP.md).

## Instalação

### Pré-requisitos

- Docker e Docker Compose instalados
- Git

### Passos iniciais

1. Clone o repositório.
2. Copie o arquivo [.env.example](.env.example) para `.env` localmente.
3. Ajuste as variáveis de ambiente, se necessário.
4. Inicie a infraestrutura local:

```bash
docker compose up -d
```

Como alternativa, use `make setup` para criar o `.env` e `make docker-up` para iniciar os serviços.

### Serviços disponíveis

- PostgreSQL: `localhost:5432`
- pgAdmin: `http://localhost:5050`

Credenciais padrão do pgAdmin são definidas no arquivo [.env.example](.env.example). Para acessar o PostgreSQL, use as mesmas credenciais definidas no `.env`.

### Registrar o PostgreSQL no pgAdmin

O pgAdmin é iniciado sem conexões pré-configuradas. Após autenticar-se, registre um servidor com os valores abaixo. O hostname deve ser o nome do serviço Docker, pois os dois containers compartilham a rede interna.

- **Name**: `PostgreSQL local` (ou outro nome de sua escolha)
- **Host name/address**: `postgres`
- **Port**: `5432`
- **Maintenance database**: valor de `POSTGRES_DB`
- **Username**: valor de `POSTGRES_USER`
- **Password**: valor de `POSTGRES_PASSWORD`

Nenhuma tabela, schema ou dado inicial é criado por esta Sprint.

### Comandos úteis

```bash
make setup
make docker-up
make docker-down
make docker-restart
make docker-status
make docker-logs
make docker-config
```

## Estrutura do repositório

- [src/](src/) para componentes de aplicação e utilidades;
- [airflow/](airflow/) para orquestração;
- [dbt/](dbt/) para modelos e documentação;
- [warehouse/](warehouse/) para artefatos de armazenamento;
- [docs/](docs/) para documentação adicional;
- [tests/](tests/) para testes futuros;
- [scripts/](scripts/) para automações e utilidades.

## Próximos passos

Este repositório está preparado para receber:
- definições de infraestrutura;
- pipelines de ingestão;
- modelos dbt;
- DAGs do Airflow;
- automações de qualidade e CI/CD.

> Nenhuma regra de negócio ou lógica operacional foi implementada neste momento.
