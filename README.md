# Desafio Técnico — Engenharia de Dados

## 📑 Sumário

* [🎯 Cenário Identificado](#-cenário-identificado)
* [📋 Etapas do Projeto](#-etapas-do-projeto)
* [🛠️ Proposta de Solução | Stack](#️-proposta-de-solução--stack)
* [🏗️ Desenho do Pipeline](#️-desenho-do-pipeline)
* [🚀 Guia de Execução](#-guia-de-execução)
* [🧱 Decisões de Arquitetura](#-decisões-de-arquitetura)
* [📁 Organização do Diretório](#-organização-do-diretório)
* [📝 Desafios e Decisões Durante o Desenvolvimento](#-desafios-e-decisões-durante-o-desenvolvimento)
* [✅ Resultado da POC](#-resultado-da-poc)
* [🟢 Avanços para a versão definitiva](#-avanços-para-a-versão-definitiva)



## 🎯 Cenário Identificado

**Problema:** Relatórios demorados e com baixa confiabilidade de dados, impactando a velocidade e a assertividade na tomada de decisão por parte de gestores e diretores.

**Causa:** Dificuldade em agregar diferentes fontes de informação em um único ponto, exigindo tempo excessivo na criação de relatórios individuais e em análises comparativas.

**Solução proposta:** Fazer uma POC para construção de um Data Lake.

---

## 📋 Etapas do Projeto

Para melhor organizar o desafio, o problema foi dividido nas seguintes etapas:

1. Levantamento dos pré-requisitos do projeto.
2. Criação das tabelas em banco relacional.
3. Ingestão de dados fictícios.
4. ETL para criação da tabela flat.
5. Exportação parametrizável do arquivo CSV em diretório local.
6. Criação dos testes unitários.

---

## 🛠️ Proposta de Solução | Stack

Para este desafio, optei por Python e SQL como linguagens principais, por serem amplamente utilizadas em times de dados, em comparação com alternativas como Scala ou Java.

Visando portabilidade e agilidade no desenvolvimento, utilizei **Docker** para provisionar o banco de dados **PostgreSQL** e o framework de processamento **Spark**. A escolha do Spark levou em conta sua ampla utilização no ambiente do Sicredi.

Cada ferramenta da stack foi definida com uma responsabilidade específica, conforme resumido abaixo:

| Tecnologia         | Responsabilidade                         |
| ------------------ | ---------------------------------------- |
| 🐍 **Python**      | Linguagem principal                      |
| ⚡ **PySpark**      | Processamento e transformação dos dados  |
| 🧪 **Pytest**      | Testes automatizados                     |
| 🐳 **Docker**      | Containerização e isolamento do ambiente |
| 🐘 **PostgreSQL**  | Banco de dados de origem                 |
| ⚡ **Apache Spark** | Runtime de processamento                 |

O objetivo foi construir uma arquitetura **reprodutível, simples, testável, organizada e preparada para escalabilidade**.

Por se tratar de uma POC, irei abstrair a utilização de gerenciadores de versões e dependências do Python, como o **Pyenv**, para controle de versão, e o **Poetry**, para gerenciamento de dependências.

---

## 🏗️ Desenho do Pipeline

```text
                         ETL PIPELINE

┌──────────────────┐
│    PostgreSQL    │
│  Source Database │
└────────┬─────────┘
         │
         │ Extract
         ▼
┌──────────────────┐
│     PySpark      │
│                  │
│    Transform     │
│    Validate      │
│      Load        │
└────────┬─────────┘
         │
         │ Load
         ▼
┌──────────────────┐
│      Target      │
│     Storage      │
└──────────────────┘
```


## 🚀 Guia de Execução

A tabela abaixo apresenta o fluxo completo para execução da POC, desde o clone do repositório até a geração do arquivo final `movimento_flat.csv`.

| Etapa                                | Ambiente     | Comando                                                                                                                                  | Função                                                                                                                                                                                  |
| ------------------------------------ | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Clonar o repositório              | Host         | `git clone <URL_DO_REPOSITORIO>`                                                                                                         | Clona o repositório do projeto para a máquina local.                                                                                                                                    |
| 2. Acessar o projeto                 | Host         | `cd desafio_tecnico_assets`                                                                                                              | Acessa o diretório raiz do projeto.                                                                                                                                                     |
| 3. Instalar dependências             | Host         | `pip install -r requirements.txt`                                                                                                        | Instala as dependências Python necessárias, incluindo Psycopg, PySpark e Pytest.                                                                                                        |
| 4. Subir a infraestrutura            | Host         | `docker compose up --build -d`                                                                                                           | Constrói a imagem customizada do Spark e inicia PostgreSQL, Spark Master e Spark Worker.                                                                                                |
| 5. Validar os containers             | Host         | `docker compose ps`                                                                                                                      | Verifica se os serviços provisionados pelo Docker Compose estão em execução.                                                                                                            |
| 6. Acessar o Spark Master            | Host         | `docker compose exec spark-master bash`                                                                                                  | Abre um terminal dentro do container Spark Master para execução dos testes.                                                                                                             |
| 7. Acessar o diretório de trabalho   | Spark Master | `cd /opt/spark/work-dir`                                                                                                                 | Acessa o diretório do projeto disponibilizado dentro do container.                                                                                                                      |
| 8. Executar testes unitários         | Spark Master | `python3 -m pytest -v`                                                                                                                   | Executa os testes unitários da transformação Spark antes do processamento principal.                                                                                                    |
| 9. Sair do Spark Master              | Spark Master | `exit`                                                                                                                                   | Retorna ao terminal da máquina host.                                                                                                                                                    |
| 10. Carregar dados fictícios         | Host         | `python src/seed/seed_data.py --reset`                                                                                                   | Limpa a massa anterior e carrega os CSVs de `data/input` nas tabelas do PostgreSQL.                                                                                                     |
| 11. Acessar novamente o Spark Master | Host         | `docker compose exec spark-master bash`                                                                                                  | Entra no container responsável pela submissão da aplicação Spark.                                                                                                                       |
| 12. Executar o ETL                   | Spark Master | `/opt/spark/bin/spark-submit --master spark://spark-master:7077 /opt/spark/work-dir/src/main.py --output-dir /opt/spark/work-dir/output` | Submete a aplicação ao cluster Spark, lê os dados do PostgreSQL via JDBC, executa as transformações e gera o arquivo flat no diretório informado pelo usuário dentro da pasta `output`. |
| 13. Validar a saída                  | Host         | `output/movimento_flat.csv`                                                                                                              | Arquivo CSV final produzido pelo pipeline e disponibilizado no diretório `output` da máquina host.     

---

## 🧱 Decisões de Arquitetura

### 1. PostgreSQL e Spark em containers separados

O banco de dados PostgreSQL e o Spark serão provisionados utilizando Docker, em containers separados. Para comunicação entre os dois, utilizei uma conexão JDBC. Dessa forma, conseguimos separar o que é armazenamento do que é processamento.

```text
┌──────────────────── Docker Environment ───────────────────┐
│                                                           │
│   ┌──────────────────┐          JDBC       ┌───────────┐  │
│   │    PostgreSQL    │◄───────────────────►│   Spark   │  │
│   │                  │                     │           │  │
│   │ Source Database  │                     │ PySpark   │  │
│   └──────────────────┘                     └───────────┘  │
│                                                   │       │
└───────────────────────────────────────────────────┼───────┘
                                                    │
                                                    ▼
                                               CSV / output
```

### 2. Execução do Spark

Usaremos o Spark por meio do PySpark. Por se tratar de uma POC, não precisamos nos preocupar, neste momento, com configurações mais complexas de gerenciamento de clusters.

### 3. Ingestão e processamento dos dados

Para ingerir os dados nas tabelas do PostgreSQL, usaremos a biblioteca **Psycopg** para realizar a operação de `COPY`. Utilizaremos o Spark via JDBC para leitura dos dados e exportação da tabela flat no formato CSV.

Os dados fictícios serão gerados por meio de IA e disponibilizados no repositório para facilitar a replicação do projeto.

### 4. Configurações de infraestrutura

Por se tratar de uma POC, colocaremos as informações de infraestrutura diretamente no `docker-compose.yml`, sem a necessidade de um arquivo `.env`.

### 5. Saída parametrizável

Para a saída parametrizável do arquivo CSV, utilizaremos a própria CLI para informar o diretório de output dos dados.

---

## 📁 Organização do Diretório

```text
desafio_tecnico_assets/
│
├── data/
│   └── input/
│       ├── associado.csv
│       ├── conta.csv
│       ├── cartao.csv
│       └── movimento.csv
│
├── docker/
│   └── spark/
│       └── Dockerfile
│
├── sql/
│   └── ddl/
│       └── create_tables.sql
│
├── src/
│   ├── seed/
│   │   └── seed_data.py
│   │
│   ├── etl/
│   │   └── movimento_flat.py
│   │
│   └── main.py
│
├── tests/
│   └── test_movimento_flat.py
│
├── output/
│
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📝 Desafios e Decisões Durante o Desenvolvimento

### 1. Configuração do ambiente Docker

Durante a montagem do `Dockerfile` e do `docker-compose.yml`, precisei revisitar alguns estudos sobre Docker para configurar melhor os containers, tanto para permitir a comunicação entre Spark e PostgreSQL quanto para possibilitar a exportação do arquivo final.

### 2. Criação do banco de dados

Criei um schema chamado `db_cartoes` para armazenar as tabelas criadas pelo script `create_tables.sql`.

#### 2.1 Ajustes no Docker Compose

Tive que ajustar algumas configurações no `docker-compose.yml`, pois as configurações do Worker não estavam seguindo o mesmo padrão das configurações do Master.

#### 2.2 Validação do PostgreSQL

Com o comando:

```bash
docker compose up --build
```

conseguimos subir o PostgreSQL corretamente e aplicar o script DDL.

Com o comando:

```text
\dt db_cartoes.*
```

conseguimos visualizar a criação das quatro tabelas, conforme o print abaixo:

![Tabelas criadas no PostgreSQL](docs/images/banco_postgres_up.png)

#### 2.3 Validação do Spark

Também verifiquei se o Spark subiu corretamente e se o Worker e o Master estavam conectados. O Worker aparece como **Alive**, comprovando que a comunicação ocorreu corretamente:

![Spark Up](docs/images/spark_up.png)

### 3. Disponibilização dos arquivos CSV para o Spark

Na hora de testar o Spark, acabei não adicionando o path dos arquivos CSV. Foi necessário configurar o `docker-compose.yml` e adicionar os caminhos na seção `volumes`, tanto do Spark Master quanto do Spark Worker.

Após realizar os ajustes e executar o teste novamente, conseguimos verificar que a aplicação estava ativa:

![Bash com Spark](docs/images/bash_spark_running.png)

![Aplicação rodando no Spark](docs/images/spark_aplication_running.png)

### 4. Ingestão dos arquivos CSV no PostgreSQL

A ingestão dos arquivos CSV no PostgreSQL foi uma etapa tranquila. Utilizamos o `COPY` nativo do banco para carregar os arquivos.

A montagem do arquivo `seed_data.py` foi um pouco mais complexa devido à necessidade de adicionar comandos via CLI, para os quais utilizei a biblioteca nativa `argparse`.

#### 4.1 Tratamento de falhas e integridade referencial

Na criação do `seed_data.py`, montei uma lógica para que, caso alguma ingestão falhe, todas as operações falhem, evitando cargas parciais.

Além disso, o processo segue a ordem definida pelo DDL e por suas FKs:

```text
associado → conta → cartao → movimento
```

Caso essa ordem não seja respeitada, o banco retornaria erro devido à ausência das chaves necessárias para atender às relações de chave estrangeira.

#### 4.2 Validação dos dados carregados

Após executar o comando:

```bash
python src/seed/seed_data.py --reset
```

podemos visualizar os dados já inseridos nas tabelas. Também realizamos uma consulta para verificar se as chaves estavam sendo respeitadas:

![PostgreSQL com dados](docs/images/banco_com_dados.png)

### 5. Construção da pipeline `movimento_flat`

Para construirmos a pipeline de criação da tabela `movimento_flat`, primeiro testei a conexão do Spark com o PostgreSQL por meio do comando `spark.read.jdbc()`, que funcionou corretamente para a tabela `associado`:

![Spark x PostgreSQL](docs/images/conexao_spark_postgres.png)

#### 5.1 Coluna `data_criacao_cartao`

Durante a montagem da query da tabela `movimento_flat`, percebi que uma das colunas esperadas, `data_criacao_cartao`, não está presente em nenhuma das tabelas iniciais.

Para não criar um campo nulo e "martelar" essa coluna, optei por não trazê-la. Também não utilizei a data de criação da conta como data de criação do cartão, pois podemos ter associados que não possuem cartão de crédito.

#### 5.2 Diretório parametrizável para o CSV

Para que o destino do CSV seja parametrizável, precisamos configurar os volumes do container, pois o Spark terá acesso somente aos diretórios disponibilizados para ele.

Nesta POC, disponibilizei a pasta `output` para que possamos salvar o arquivo. Com o argumento `--output-dir`, podemos salvar em qualquer pasta criada dentro desse caminho, como, por exemplo:

```text
/opt/spark/work-dir/output/teste_novo_caminho
```

Basta informar esse caminho ao executar o código `main.py` dentro do Spark.

Como exemplo do resultado final, deixei salvo o arquivo `exemple_movimento_flat.csv`. Quando o código for executado, o resultado será salvo como `movimento_flat.csv`.

### 6. Testes unitários

O teste unitário foi pensado para cobrir três pontos principais:

1. Os DataFrames precisam ser relacionáveis.
2. O resultado deve conter as colunas esperadas.
3. Os valores do registro final devem ser provenientes corretamente das tabelas de origem.

## ✅ Resultado da POC

Entendo que foi gerado material suficiente para demonstrar que conseguimos montar um pipeline automatizado que pega os dados do nosso banco de dados de cartões e os salva em outro local. Caso optássemos por salvar esse relatório em um bucket S3 na AWS, por exemplo, também seria possível. Apenas teríamos o trabalho de estabelecer a comunicação entre o nosso cluster Spark e a AWS.


## 🟢 Avanços para a versão definitiva

Esta POC tinha como objetivo viabilizar a criação de um Data Lake na empresa, porém conseguimos extrair muito mais valor utilizando um ambiente na nuvem com um Data Lakehouse, onde faríamos a ingestão de todas as tabelas no Data Lake e usaríamos essas tabelas para criar os relatórios para a diretoria. Assim, "desafogamos" o ambiente transacional e centralizamos demandas analíticas em ambientes analíticos.

Por se tratar de uma POC, foram abstraídos diversos fatores que, se colocássemos a aplicação em produção, teríamos que analisar de forma diferente, principalmente no que diz respeito ao runtime do Spark, gerenciamento de containers, dependências de bibliotecas e camadas de segurança. Para uma versão final, também usaríamos alguma ferramenta de orquestração, tanto de containers quanto da execução da própria pipeline, além de buscarmos ter testes automatizados.

Em um cenário em que construíssemos toda a infraestrutura do projeto do zero, ainda teríamos um trabalho com IaC para provisionar os clusters na AWS, por exemplo.

No contexto do Sicredi, em que já temos uma plataforma de dados (Databricks), se nos deparássemos com esse tipo de problema, seria muito mais fácil resolvê-lo, pois já usaríamos frameworks do time de centro para ingerir tabelas de bancos transacionais, como PostgreSQL, por exemplo. Com isso, teríamos no Lake, na camada Ref, as tabelas de que precisaríamos para criar um relatório executivo e publicá-lo na camada Gold.


