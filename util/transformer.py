from pyspark.sql.functions import col, sum as spark_sum
from logs.etl_logger import ETLLogger

class Transformer:
    @staticmethod
    def transform_business_rule(df_cliente, df_endereco, df_prop, df_neg):
        ETLLogger.log_event(event="Transformação", action="Aplicar regra de negócio")

        bens_sum = df_prop.groupBy("cliente_id").agg(spark_sum(col("valor")).alias("valor_total_bens"))

        joined = (
            df_cliente.alias("c")
            .join(df_endereco.alias("e"), col("c.cliente_id") == col("e.cliente_id"), "left")
            .join(bens_sum.alias("b"), col("c.cliente_id") == col("b.cliente_id"), "left")
            .join(df_neg.alias("n"), col("c.cliente_id") == col("n.cliente_id"), "left")
            .select(
                col("c.cliente_id").alias("cliente_id"),
                col("c.nome").alias("nome"),
                col("c.tipo_pessoa").alias("tipo_pessoa"),
                col("c.renda_mensal").alias("renda_mensal"),
                col("e.zona").alias("zona"),
                col("b.valor_total_bens").alias("valor_total_bens"),
                col("n.negativacao").alias("negativado"),
            )
        )

        joined = joined.na.fill({"valor_total_bens": 0})

        joined = joined.withColumn(
            "aprovado_para_envio",  
            (col("zona") == "rural")
            & (col("tipo_pessoa") == "PF")
            & (col("valor_total_bens") >= 300000)
            & (col("negativado") == False)
        )

        ETLLogger.log_event(event="Transformação", action="Aplicar regra de negócio")

        return joined
        
