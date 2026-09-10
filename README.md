## 🎯 Cenário Identificado

**Problema:** Relatórios demorados e com baixa confiabilidade de dados, impactando a velocidade e a assertividade na tomada de decisão por parte de gestores e diretores.

**Causa:** Dificuldade em agregar diferentes fontes de informação em um único ponto, exigindo tempo excessivo na criação de relatórios individuais e em análises comparativas.

**Solução proposta:** Fazer uma POC para construção de um Data Lake.

## Etapas a serem concluídas

Para melhor organizar o desafio, o problema foi dividido em quatro etapas:

1. Levantar os pré requisitos do projeto
2. Criação das tabelas em banco relacional
3. Ingestão de dados fictícios
4. ETL para criação da tabela Flat
5. Exportação parametrizável de arquivo CSV em diretório local


## Proposta de Solução | Stack

Para este desafio, optei por Python e SQL como linguagens principais, por serem as mais amplamente utilizadas em times de dados, em comparação a alternativas como Scala ou Java.

Visando portabilidade e agilidade no desenvolvimento, utilizei **Docker** para provisionar o banco de dados **PostgreSQL** e o framework de processamento **Spark**. A escolha do Spark levou em conta sua ampla utilização no ambiente do Sicredi.

Cada ferramenta da stack foi definida com uma responsabilidade específica, conforme resumido abaixo:

| Tecnologia | Responsabilidade |
| --- | --- |
| 🐍 **Python** | Linguagem principal |
| ⚡ **PySpark** | Processamento e transformação dos dados |
| 🧪 **Pytest** | Testes automatizados |
| 🐳 **Docker** | Containerização e isolamento do ambiente |
| 🐘 **PostgreSQL** | Banco de dados de origem |
| ⚡ **Apache Spark** | Runtime de processamento |

O objetivo foi construir uma arquitetura **reprodutível, simples, testável, organizada e preparada para escalabilidade**.

Por se tratar de uma POC, irei abistrair a criação de gerenciadores de dependencias e versões de python, como o (**Pyenv**) para controle de versão e (**Poetry**) para gerenciamento de dependências.

---


## 🏗️ Desenho de Pipeline e Arquitetura

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
│   Transform      │
│   Validate       │
│   Load           │
└────────┬─────────┘
         │
         │ Load
         ▼
┌──────────────────┐
│      Target      │
│     Storage      │
└──────────────────┘


             DEVELOPMENT ENVIRONMENT

┌─────────────────────────────────────────┐
│                  Docker                 │
│                                         │
│  ┌────────────────┐ ┌────────────────┐  │
│  │   PostgreSQL   │ │     Spark      │  │
│  │                │ │                │  │
│  │ Source DB      │ │ Spark Runtime  │  │
│  └────────────────┘ └────────────────┘  │
│                                         │
└─────────────────────────────────────────┘
                    ▲
                    │
              PySpark / Python
                    │
┌─────────────────────────────────────────┐
│                Python                   │
│                                         │
│  PySpark → Data processing              │
│  Pytest → Automated tests               │
└─────────────────────────────────────────┘
```

## Decisões de Arquitetura

1. Banco de Dados Postgres e Spark serão provisioandos usando Docker, em imagens separadas. Para comunicação entre os dois usei uma conexão JDBC, dessa forma conseguimos separar o que é armazenamento e o que é processamento.

```text
┌──────────────────── Docker Environment ───────────────────┐
│                                                           │
│   ┌──────────────────┐          JDBC       ┌───────────┐  │
│   │   PostgreSQL     │◄───────────────────►│   Spark   │  │
│   │                  │                     │           │  |
│   │  Source Database │                     │ PySpark   │  │
│   └──────────────────┘                     └───────────┘  │
│                                                           │
└───────────────────────────────────────────────────────────┘
                                                   │
                                                   ▼
                                             CSV / output
```

2. Usaramoes o Spark de forma local dentro do container, através do PySpark. Por se tratar de uma POC, não precisamos nos preocupar no momento com o gerenciamento e configuração de clusters.

3. Para popular os dados nas nossas tabelas no banco postgree usaremos o proprio Spark via JDBC para ingerir os dados para teste. Os dados ficticios serão gerados através de IA e disponibilizados no repositorio para melhor replicação.

4. Por se tratar de uma POC, colocaremos infomrações de infraestrutura diretamente no docker compose, sem precisar de um arquivo .env 

5. Para a saída parametrizavel do arquivo CSV, utilizaremos o proprio CLI para o output dos dados. 

## Organização do Diretório

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

## Anotações durante o desenvolvimento 

1. Durante a montagem do Dockerfile e docker-compose.yml precisei revisitar alguns estudos sobre docker, para melhor configurar o container, tanto para o Spark conversar com o Postgres quanto para exportar o arquivo final.

