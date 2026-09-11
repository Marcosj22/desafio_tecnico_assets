import argparse
import shutil
from pathlib import Path

from pyspark.sql import SparkSession

from etl.movimento_flat import build_movimento_flat


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa o ETL movimento_flat da SiCooperative."
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Diretório onde o movimento_flat será gravado.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    spark = (
        SparkSession.builder
        .appName("sicooperative_movimento_flat")
        .getOrCreate()
    )

    jdbc_url = "jdbc:postgresql://postgres:5432/sicooperative"

    properties = {
        "user": "sicooperative",
        "password": "sicooperative",
        "driver": "org.postgresql.Driver",
    }

    try:
        # Leitura das tabelas do PostgreSQL via JDBC
        associado_df = spark.read.jdbc(
            url=jdbc_url,
            table="db_cartoes.associado",
            properties=properties,
        )

        conta_df = spark.read.jdbc(
            url=jdbc_url,
            table="db_cartoes.conta",
            properties=properties,
        )

        cartao_df = spark.read.jdbc(
            url=jdbc_url,
            table="db_cartoes.cartao",
            properties=properties,
        )

        movimento_df = spark.read.jdbc(
            url=jdbc_url,
            table="db_cartoes.movimento",
            properties=properties,
        )

        # Construção do DataFrame flat
        movimento_flat_df = build_movimento_flat(
            associado_df=associado_df,
            conta_df=conta_df,
            cartao_df=cartao_df,
            movimento_df=movimento_df,
        )

        # Validações simples do processamento
        print("Schema do movimento_flat:")
        movimento_flat_df.printSchema()

        quantidade_movimentos = movimento_df.count()
        quantidade_flat = movimento_flat_df.count()

        print(
            f"Quantidade de movimentos: "
            f"{quantidade_movimentos}"
        )

        print(
            f"Quantidade de registros no flat: "
            f"{quantidade_flat}"
        )

        # Configuração dos caminhos de saída
        output_dir = Path(args.output_dir)

        temp_output_path = (
            output_dir / "movimento_flat_temp"
        )

        final_output_path = (
            output_dir / "movimento_flat.csv"
        )

        print(
            f"Escrevendo resultado temporário em: "
            f"{temp_output_path}"
        )

        # O coalesce(1) força a geração de apenas uma partição
        (
            movimento_flat_df
            .coalesce(1)
            .write
            .mode("overwrite")
            .option("header", "true")
            .csv(str(temp_output_path))
        )

        # Localiza o arquivo CSV gerado pelo Spark
        part_files = list(
            temp_output_path.glob("part-*.csv")
        )

        if len(part_files) != 1:
            raise RuntimeError(
                "Esperado exatamente 1 arquivo CSV, "
                f"mas foram encontrados {len(part_files)}."
            )

        # Remove uma versão anterior do arquivo final,
        # caso já exista
        if final_output_path.exists():
            final_output_path.unlink()

        # Renomeia o part-*.csv para movimento_flat.csv
        shutil.move(
            str(part_files[0]),
            str(final_output_path),
        )

        # Remove pasta temporária, _SUCCESS e arquivos .crc
        shutil.rmtree(temp_output_path)

        print(
            f"Arquivo gerado com sucesso: "
            f"{final_output_path}"
        )

        print("ETL concluído com sucesso.")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()