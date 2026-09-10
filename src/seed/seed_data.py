import argparse
import os
from pathlib import Path

import psycopg


LOAD_ORDER = (
    (
        "associado",
        "associado.csv",
        ("id", "nome", "sobrenome", "idade", "email"),
    ),
    (
        "conta",
        "conta.csv",
        ("id", "tipo", "data_criacao", "id_associado"),
    ),
    (
        "cartao",
        "cartao.csv",
        ("id", "num_cartao", "nom_impresso", "id_conta", "id_associado"),
    ),
    (
        "movimento",
        "movimento.csv",
        (
            "id",
            "vlr_transacao",
            "des_transacao",
            "data_movimento",
            "id_cartao",
        ),
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Carrega os arquivos CSV fictícios no PostgreSQL."
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/input"),
        help="Diretório contendo os arquivos CSV.",
    )

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Limpa as tabelas antes de realizar a carga.",
    )

    return parser.parse_args()


def get_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "sicooperative"),
        user=os.getenv("POSTGRES_USER", "sicooperative"),
        password=os.getenv("POSTGRES_PASSWORD", "sicooperative"),
    )


def validate_input_files(input_dir: Path) -> None:
    missing_files = []

    for _, file_name, _ in LOAD_ORDER:
        file_path = input_dir / file_name

        if not file_path.is_file():
            missing_files.append(str(file_path))

    if missing_files:
        files = "\n".join(f"- {file}" for file in missing_files)

        raise FileNotFoundError(
            f"Arquivos obrigatórios não encontrados:\n{files}"
        )


def reset_tables(conn: psycopg.Connection) -> None:
    print("Limpando tabelas...")

    with conn.cursor() as cursor:
        cursor.execute(
            """
            TRUNCATE TABLE
                db_cartoes.movimento,
                db_cartoes.cartao,
                db_cartoes.conta,
                db_cartoes.associado
            RESTART IDENTITY;
            """
        )


def load_csv(
    conn: psycopg.Connection,
    table_name: str,
    file_path: Path,
    columns: tuple[str, ...],
) -> None:
    print(f"Carregando {file_path} -> db_cartoes.{table_name}")

    column_list = ", ".join(columns)

    copy_sql = f"""
        COPY db_cartoes.{table_name} ({column_list})
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE
        )
    """

    with file_path.open("r", encoding="utf-8") as csv_file:
        with conn.cursor() as cursor:
            with cursor.copy(copy_sql) as copy:
                while data := csv_file.read(8192):
                    copy.write(data)


def main() -> None:
    args = parse_args()

    input_dir = args.input_dir.resolve()

    print(f"Diretório de entrada: {input_dir}")

    validate_input_files(input_dir)

    try:
        with get_connection() as conn:
            print("Conexão com PostgreSQL estabelecida.")

            if args.reset:
                reset_tables(conn)

            for table_name, file_name, columns in LOAD_ORDER:
                file_path = input_dir / file_name

                load_csv(
                    conn=conn,
                    table_name=table_name,
                    file_path=file_path,
                    columns=columns,
                )

            conn.commit()

        print("Carga concluída com sucesso.")

    except Exception as exc:
        print(f"Erro durante a carga: {exc}")
        raise


if __name__ == "__main__":
    main()