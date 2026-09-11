## utilizaremos uma imagem base do apache spark com suporte a python 3.9 e java 17
## O Spark precisa do arquivo .jar para conseguir conectar no Postgres

FROM apache/spark:3.5.9-scala2.12-java17-python3-ubuntu

USER root

## adiciona o driver JDBC do PostgreSQL ao classpath do Spark
ADD https://jdbc.postgresql.org/download/postgresql-42.7.13.jar \
    /opt/spark/jars/postgresql-42.7.13.jar

RUN chmod 644 /opt/spark/jars/postgresql-42.7.13.jar

## copia as dependências Python do projeto para a imagem
COPY requirements.txt /tmp/requirements.txt

## instala as dependências necessárias para execução e testes
RUN pip install --no-cache-dir -r /tmp/requirements.txt

USER spark

WORKDIR /opt/spark/work-dir