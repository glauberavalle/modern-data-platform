# AGENTS.md

Este repositório é um projeto pessoal de portfólio, mas deve ser tratado como um produto interno de tecnologia: com foco em arquitetura, engenharia de software, organização, documentação, modelagem de dados e qualidade técnica.

## Constituição do projeto

- O objetivo não é apenas escrever código que funcione.
- O objetivo é demonstrar capacidade de projetar arquiteturas, aplicar boas práticas de engenharia, organizar repositórios, documentar bem, modelar dados, construir pipelines e tomar decisões técnicas com clareza.
- Todas as implementações devem priorizar clareza, simplicidade, manutenção e escalabilidade.
- O desenvolvimento ocorrerá de forma incremental, com cada Sprint entregando valor real.
- Evite over engineering. Implemente apenas o necessário para a Sprint atual.
- Quando identificar melhorias arquiteturais, não implemente automaticamente. Explique a melhoria e proponha adicioná-la ao ROADMAP para avaliação posterior.
- Este projeto evoluirá ao longo de semanas ou meses. A estrutura deve permitir crescimento sem grandes refatorações.

## Princípios de trabalho

- Seguir princípios de Clean Code e manter o código legível e bem estruturado.
- Utilizar typing sempre que possível para aumentar clareza e segurança.
- Preferir composição a herança quando a solução exigir abstrações.
- Nunca colocar lógica SQL em Python quando ela puder ser implementada no dbt.
- Documentar decisões arquiteturais e trade-offs relevantes.
- Escrever código modular, com responsabilidade bem definida por camada.
- Manter baixo acoplamento entre componentes e módulos.
- Evitar introduzir regras de negócio nesta fase inicial.
- Preservar a separação entre infraestrutura, transformação, orquestração e documentação.
- Sempre que existir mais de uma solução possível, explicar trade-offs, justificar a recomendação e escolher a solução mais simples que atenda ao cenário atual.
- Todo código deve ser pensado com qualidade de produção, mesmo sendo um projeto de portfólio.
- A documentação deve possuir o mesmo nível de qualidade esperado em um projeto profissional.

## Padrões esperados

- Arquivos devem ser bem nomeados e com propósito claro.
- Documentação deve acompanhar mudanças significativas.
- Configurações devem ser centralizadas sempre que possível.
- Alterações devem favorecer evolução incremental e manutenção.
- Cada mudança deve refletir uma decisão técnica coerente com a visão do projeto.

## Regras operacionais para implementação

Sempre que iniciar uma tarefa:
1. explicar o que será feito;
2. informar quais arquivos serão alterados;
3. justificar a abordagem;
4. somente então implementar.

Ao finalizar uma tarefa:
- resumir as alterações;
- informar possíveis impactos;
- sugerir próximos passos;
- sugerir uma mensagem de commit seguindo Conventional Commits.

## Escopo atual

Este repositório está em fase inicial de estruturação. O foco atual é preparar uma fundação profissional, sem implementar soluções de negócio ou excesso de abstração.
