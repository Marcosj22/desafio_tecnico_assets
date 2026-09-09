## 🎯 Cenário Identificado

**Problema:** Relatórios demorados e com baixa confiabilidade de dados, impactando a velocidade e a assertividade na tomada de decisão por parte de gestores e diretores.

**Causa:** Dificuldade em agregar diferentes fontes de informação em um único ponto, exigindo tempo excessivo na criação de relatórios individuais e em análises comparativas.

**Solução proposta:** Iniciar uma POC para construção de um Data Lake.

## Etapas a serem concluídas

Para melhor organizar o desafio, o problema foi dividido em quatro etapas:

1. Criação das tabelas em banco relacional
2. Ingestão de dados fictícios
3. ETL para criação da tabela Flat
4. Exportação parametrizável de arquivo CSV em diretório local


## Proposta de Solução | Stack

Para este desafio, optei por Python e SQL como linguagens principais, por serem as mais amplamente utilizadas em times de dados, em comparação a alternativas como Scala ou Java.

Para garantir um código resiliente e portátil, utilizei ferramentas de controle de versão (**Pyenv**), gerenciamento de dependências (**Poetry**) e testes automatizados (**Pytest**).

Visando portabilidade e agilidade no desenvolvimento, utilizei **Docker Compose** para instanciar o banco de dados **PostgreSQL** e o framework de processamento **Spark**. A escolha do Spark levou em conta sua ampla utilização no ambiente do Sicredi.

Cada ferramenta da stack foi definida com uma responsabilidade específica, conforme resumido abaixo:

| Tecnologia | Responsabilidade |
| --- | --- |
| 🐍 **Python** | Linguagem principal |
| 🔧 **Pyenv** | Gerenciamento da versão do Python |
| 📦 **Poetry** | Gerenciamento de dependências |
| ⚡ **PySpark** | Processamento e transformação dos dados |
| 🧪 **Pytest** | Testes automatizados |
| 🐳 **Docker** | Containerização e isolamento do ambiente |
| 🐘 **PostgreSQL** | Banco de dados de origem |
| ⚡ **Apache Spark** | Runtime de processamento |

O objetivo foi construir uma arquitetura **reprodutível, simples, testável, organizada e preparada para escalabilidade**.

---


## 🏗️ Desenho da Arquitetura

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
│  pyenv → Python version                 │
│  Poetry → Dependencies                  │
│  PySpark → Data processing              │
│  Pytest → Automated tests               │
└─────────────────────────────────────────┘
```

