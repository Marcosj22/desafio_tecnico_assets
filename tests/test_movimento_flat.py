from typing import Generator

import pytest

from pyspark.sql import SparkSession

from src.etl.movimento_flat import build_movimento_flat


@pytest.fixture(scope="session")
def spark() -> Generator[SparkSession, None, None]:
    spark_session = (
        SparkSession.builder
        .master("local[1]")
        .appName("sicooperative-unit-tests")
        .getOrCreate()
    )

    yield spark_session

    spark_session.stop()


def test_build_movimento_flat(spark: SparkSession) -> None:
    associado_df = spark.createDataFrame(
        [
            (
                1,
                "Joao",
                "Silva",
                35,
                "joao@email.com",
            )
        ],
        [
            "id",
            "nome",
            "sobrenome",
            "idade",
            "email",
        ],
    )

    conta_df = spark.createDataFrame(
        [
            (
                10,
                "TITULAR",
                "2026-01-10",
                1,
            )
        ],
        [
            "id",
            "tipo",
            "data_criacao",
            "id_associado",
        ],
    )

    cartao_df = spark.createDataFrame(
        [
            (
                100,
                "1234567890123456",
                "JOAO SILVA",
                10,
                1,
            )
        ],
        [
            "id",
            "num_cartao",
            "nom_impresso",
            "id_conta",
            "id_associado",
        ],
    )

    movimento_df = spark.createDataFrame(
        [
            (
                1000,
                150.50,
                "Compra supermercado",
                "2026-02-01",
                100,
            )
        ],
        [
            "id",
            "vlr_transacao",
            "des_transacao",
            "data_movimento",
            "id_cartao",
        ],
    )

    resultado_df = build_movimento_flat(
        associado_df=associado_df,
        conta_df=conta_df,
        cartao_df=cartao_df,
        movimento_df=movimento_df,
    )

    resultado = resultado_df.collect()

    colunas_esperadas = [
        "nome_associado",
        "sobrenome_associado",
        "idade_associado",
        "vlr_transacao_movimento",
        "des_transacao_movimento",
        "data_movimento",
        "numero_cartao",
        "nome_impresso_cartao",
        "tipo_conta",
        "data_criacao_conta",
    ]

    assert resultado_df.columns == colunas_esperadas
    assert len(resultado) == 1

    registro = resultado[0]

    assert registro.nome_associado == "Joao"
    assert registro.sobrenome_associado == "Silva"
    assert registro.idade_associado == 35
    assert registro.vlr_transacao_movimento == 150.50
    assert registro.des_transacao_movimento == "Compra supermercado"
    assert registro.data_movimento == "2026-02-01"
    assert registro.numero_cartao == "1234567890123456"
    assert registro.nome_impresso_cartao == "JOAO SILVA"
    assert registro.tipo_conta == "TITULAR"
    assert registro.data_criacao_conta == "2026-01-10"