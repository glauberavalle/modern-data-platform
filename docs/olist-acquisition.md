# Aquisição do dataset Olist

## Fonte

Os dados são obtidos do [Brazilian E-Commerce Public Dataset by Olist no Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), identificado como `olistbr/brazilian-ecommerce`.

A configuração padrão utiliza a versão `2` da fonte para manter a aquisição reproduzível.

A fonte é distribuída como um arquivo `archive.zip`.

---

## Objetivo

A etapa de aquisição é responsável por obter uma cópia local dos arquivos de origem necessários para a ingestão da plataforma.

A aquisição é isolada das etapas de validação e carga. Ela não acessa o PostgreSQL e não aplica transformações aos dados.

---

## Fluxo de aquisição

```text
Kaggle / Olist
      ↓
Download temporário do archive.zip
      ↓
Validação do arquivo ZIP
      ↓
Extração temporária
      ↓
Verificação dos arquivos esperados
      ↓
Publicação segura
      ↓
data/external/olist/

A publicação somente ocorre após a conclusão bem-sucedida das verificações da aquisição.

Arquivos esperados

A aquisição utiliza o contrato técnico definido pelo projeto para identificar os arquivos esperados.

Atualmente são esperados nove arquivos:

olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv

Somente esses arquivos são publicados no diretório de aquisição.

Arquivos adicionais eventualmente presentes no ZIP não fazem parte da aquisição.

Diretório de destino

Os arquivos adquiridos são publicados em:

data/external/olist/

A estrutura esperada é:

data/
└── external/
    └── olist/
        ├── olist_customers_dataset.csv
        ├── olist_geolocation_dataset.csv
        ├── olist_order_items_dataset.csv
        ├── olist_order_payments_dataset.csv
        ├── olist_order_reviews_dataset.csv
        ├── olist_orders_dataset.csv
        ├── olist_products_dataset.csv
        ├── olist_sellers_dataset.csv
        └── product_category_name_translation.csv

Os arquivos de dados não são versionados pelo Git.

Execução

Com o ambiente local configurado, execute:

make download-olist

Em ambientes sem make:

uv run python -m scripts.download_olist

Para solicitar explicitamente uma nova aquisição:

uv run python -m scripts.download_olist --force
Reutilização da aquisição

Antes de realizar um novo download, o processo verifica se já existe uma aquisição completa no diretório de destino.

Uma aquisição é considerada completa quando:

o diretório existe;
os nove arquivos esperados existem;
todos os arquivos possuem tamanho maior que zero.

Quando essas condições são atendidas, a aquisição existente é reutilizada e nenhum novo download é realizado.

A opção --force permite solicitar explicitamente uma nova aquisição.

Download

O arquivo da fonte é baixado para uma área temporária.

O download:

utiliza a URL configurada para o dataset;
possui timeout de 60 segundos;
é realizado em blocos de 1 MB;
não mantém o arquivo ZIP no diretório final de dados.

Após o download, o arquivo é verificado para confirmar que representa um arquivo ZIP válido.

Extração

A extração também ocorre em uma área temporária.

Durante essa etapa:

o conteúdo do ZIP é analisado;
os nove arquivos esperados são identificados;
arquivos que não pertencem ao contrato são ignorados;
entradas duplicadas para um mesmo arquivo esperado são rejeitadas;
somente os arquivos esperados são extraídos.

A aquisição falha caso algum dos nove arquivos esperados não esteja presente.

Publicação segura

Os arquivos não são publicados diretamente no diretório final durante o download ou a extração.

Primeiro, uma cópia completa é construída em uma área temporária.

Somente depois que os nove arquivos esperados forem extraídos e considerados não vazios a nova aquisição é publicada.

Quando já existe uma aquisição anterior, o diretório existente é temporariamente preservado durante a substituição.

Se a publicação da nova aquisição falhar, o processo tenta restaurar a aquisição anterior.

Essa estratégia reduz o risco de substituir uma aquisição válida por uma cópia incompleta.

Garantias

A etapa de aquisição garante:

existência dos nove arquivos esperados;
rejeição de arquivos ZIP inválidos;
rejeição de arquivos esperados ausentes;
rejeição de entradas duplicadas para um mesmo arquivo;
verificação de que os arquivos publicados não estão vazios;
publicação somente após a preparação completa da nova aquisição;
reutilização de uma aquisição local completa;
possibilidade de forçar uma nova aquisição.
Limites da aquisição

A aquisição não é responsável por validar o conteúdo estrutural dos CSVs.

Ela não realiza:

validação de codificação;
validação de cabeçalhos;
validação de quantidade de colunas;
validação de tipos;
limpeza de dados;
conversão de tipos;
deduplicação;
enriquecimento;
regras de negócio;
métricas ou KPIs;
criação de tabelas;
acesso ao PostgreSQL;
execução da carga RAW.

Essas responsabilidades pertencem às etapas posteriores da pipeline.

Relação com a validação e a carga

A aquisição produz os arquivos que serão consumidos pelas etapas seguintes:

Acquisition
     ↓
data/external/olist/*.csv
     ↓
Validation
     ↓
Ingestion Service
     ↓
Loading
     ↓
PostgreSQL / raw

A separação permite que a aquisição seja executada e testada independentemente do banco de dados e da lógica de ingestão.

Reprodutibilidade

A URL da fonte e sua versão são configuráveis por variáveis de ambiente.

A configuração padrão utiliza a versão 2 do dataset Olist.

O código responsável pela aquisição é versionado no Git, enquanto os arquivos de dados permanecem fora do repositório.

Dessa forma, o projeto mantém no Git a lógica necessária para reproduzir a aquisição sem incorporar os arquivos brutos ao controle de versão.
