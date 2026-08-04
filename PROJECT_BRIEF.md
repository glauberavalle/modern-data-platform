# 1. Visão Geral

Esta plataforma tem como objetivo consolidar dados de uma operação brasileira de e-commerce em uma base analítica estruturada, confiável e reproduzível. O projeto representa a fundação de um ambiente de dados capaz de apoiar a tomada de decisão, a análise de negócio e o crescimento da organização.

A proposta é construir uma plataforma que transforme dados dispersos e desconectados em uma camada analítica organizada, com foco em clareza, governança e evolução incremental.

# 2. Contexto do Negócio

A empresa fictícia é uma operação brasileira de e-commerce com múltiplas fontes de dados distribuídas em diferentes sistemas e formatos. Atualmente, a informação necessária para decisões estratégicas e operacionais encontra-se fragmentada, dificultando a consolidação de visão analítica consistente.

O projeto representa a construção de uma plataforma de dados para reunir, organizar e disponibilizar essas informações de forma mais estruturada, permitindo maior qualidade de análise e apoio à decisão.

# 3. Problema

A plataforma resolve uma série de problemas operacionais e analíticos comuns em ambientes de dados ainda não consolidados:

- dados distribuídos em diferentes fontes e sistemas;
- ausência de padronização entre fontes de informação;
- dificuldade de geração de indicadores confiáveis e consistentes;
- baixa governança e rastreabilidade sobre os dados;
- limitação na capacidade de responder com rapidez a perguntas de negócio.

# 4. Objetivos

Os objetivos deste projeto são:

- consolidar dados provenientes de diferentes fontes;
- construir uma camada analítica organizada e compreensível;
- disponibilizar conjuntos de dados com maior confiabilidade para análise;
- apoiar a criação de dashboards e relatórios futuros;
- criar uma arquitetura que possa ser reproduzida localmente para desenvolvimento e validação.

# 5. Escopo

Este projeto contempla as seguintes áreas:

- ingestão de dados;
- armazenamento inicial da informação;
- transformação e organização dos dados;
- modelagem analítica em nível conceitual;
- orquestração do fluxo de execução;
- documentação da plataforma e do processo;
- estrutura para testes e validação futura.

# 6. Fora do Escopo

Os seguintes itens não fazem parte deste projeto:

- Spark;
- Kafka;
- Kubernetes;
- Terraform;
- streaming em tempo real;
- machine learning;
- data lake distribuído;
- implementação de soluções de negócio específicas não relacionadas à fundação da plataforma.

# 7. Fontes de Dados

Como referência, o projeto utilizará o dataset público brasileiro Olist como fonte de contexto para a estrutura da plataforma.

As fontes de dados disponíveis no dataset público incluem, entre outras, os arquivos públicos relacionados a:

- pedidos;
- clientes;
- produtos;
- vendedores;
- pagamentos;
- avaliações;
- geolocalização;
- categorias;
- itens de pedido.

Este documento não modela os dados nem define relações específicas entre as tabelas. A intenção é apenas descrever as fontes disponíveis como referência inicial para a plataforma.

# 8. Consumidores da Plataforma

Os principais consumidores esperados da plataforma são:

- times de Marketing;
- times de Produto;
- área Financeira;
- liderança executiva;
- equipes analíticas internas.

# 9. Indicadores Esperados

Futuramente, a plataforma poderá apoiar a construção de indicadores como:

- receita;
- ticket médio;
- clientes recorrentes;
- tempo médio de entrega;
- cancelamentos;
- avaliações;
- receita por categoria;
- receita por estado.

Estes indicadores são apresentados como exemplos de uso analítico futuro e não implicam implementação imediata ou definição de cálculo neste documento.

# 10. Arquitetura Conceitual

O fluxo conceitual da plataforma pode ser descrito como:

Fontes de Dados
↓
Python
↓
PostgreSQL
↓
dbt
↓
Data Warehouse
↓
Power BI

Este trecho descreve apenas a lógica conceitual de fluxo e não detalha decisões técnicas específicas.

# 11. Restrições Técnicas

As tecnologias obrigatórias consideradas para este projeto são:

- Python 3.13;
- Docker;
- PostgreSQL;
- dbt;
- Airflow;
- GitHub Actions;
- Ruff;
- pre-commit.

# 12. Premissas

As seguintes informações são hipóteses temporárias e poderão ser revisadas no futuro:

- a plataforma será desenvolvida inicialmente em ambiente local, com foco em reprodutibilidade;
- o dataset Olist será utilizado como referência inicial para estruturação do projeto;
- a arquitetura conceitual poderá ser ajustada conforme o escopo evoluir;
- a definição exata de consumidores e indicadores pode ser refinada em etapas posteriores.

Estas premissas não devem ser tratadas como fatos definitivos e poderão ser alteradas conforme o projeto avance.

# 13. Roadmap de Alto Nível

O projeto deverá evoluir em grandes fases, considerando progressão gradual e foco em valor real:

1. estruturação inicial do repositório e documentação base;
2. preparação do ambiente local e infraestrutura inicial;
3. consolidação de fontes e organização dos dados;
4. construção da camada analítica e modelagem inicial;
5. orquestração, governança e evolução da plataforma.

# 14. Considerações Finais

Este documento serve como referência de negócio e orientação estratégica para o projeto. Ele foi elaborado com foco em clareza, consistência e alinhamento arquitetural, sem introduzir implementação detalhada ou requisitos não confirmados.

Ele deverá ser utilizado como base para as decisões futuras do projeto, com a possibilidade de revisão conforme novas informações forem definidas.
