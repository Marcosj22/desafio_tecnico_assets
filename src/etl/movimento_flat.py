from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def build_movimento_flat(
    associado_df: DataFrame,
    conta_df: DataFrame,
    cartao_df: DataFrame,
    movimento_df: DataFrame,
) -> DataFrame:
    
    """
    Aqui criamos a query que irá gerar o dataframe movimento_flat, que é o resultado do join entre os dataframes associados, contas, cartões e movimentos.
    """
    movimento_flat_df = (
        movimento_df.alias("m")
        .join(
            cartao_df.alias("ca"),
            F.col("m.id_cartao") == F.col("ca.id"),
            "inner",
        )
        .join(
            conta_df.alias("co"),
            F.col("ca.id_conta") == F.col("co.id"),
            "inner",
        )
        .join(
            associado_df.alias("a"),
            F.col("ca.id_associado") == F.col("a.id"),
            "inner",
        )
        .select(
            F.col("a.nome").alias("nome_associado"),
            F.col("a.sobrenome").alias("sobrenome_associado"),
            F.col("a.idade").alias("idade_associado"),
            F.col("m.vlr_transacao").alias("vlr_transacao_movimento"),
            F.col("m.des_transacao").alias("des_transacao_movimento"),
            F.col("m.data_movimento").alias("data_movimento"),
            F.col("ca.num_cartao").alias("numero_cartao"),
            F.col("ca.nom_impresso").alias("nome_impresso_cartao"),
            F.col("co.tipo").alias("tipo_conta"),
            F.col("co.data_criacao").alias("data_criacao_conta"),
        )
    )

    return movimento_flat_df