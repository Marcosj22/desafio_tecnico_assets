## utilizaremos uma imagem base do apache spark com suporte a python 3.9 e java 17
## O Spark precisa do aquirvo .jar para conseguir conectar no Postgres

FROM apache/spark:3.5.9-scala2.12-java17-python3-ubuntu

USER root

ADD https://jdbc.postgresql.org/download/postgresql-42.7.13.jar \
    /opt/spark/jars/postgresql-42.7.13.jar

RUN chmod 644 /opt/spark/jars/postgresql-42.7.13.jar

USER spark

WORKDIR /opt/spark/work-dir