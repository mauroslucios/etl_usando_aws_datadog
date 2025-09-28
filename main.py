from pyspark.sql import SparkSession
import traceback

from logs.etl_logger import ETLLogger
from util.extractor import Extractor
from util.transformer import Transformer
from util.loader import Loader
from util.config import S3_BUCKET, S3_PREFIX, MAX_FILE_SIZE_BYTES

def main():
    ETLLogger.log_event("ETL iniciado")

    spark = (
        SparkSession.builder.appName("ETL")
        .config("spark.sql.shuffle.partitions", "4")
        .config("spark.jars", "mysql-connector-j-8.0.33.jar")
        .getOrCreate()
    )

    try:
        extractor = Extractor(spark)
        transformer = Transformer()
        loader = Loader()

        df_cliente = extractor.extract_table("cliente")
        df_endereco = extractor.extract_table("endereco")
        df_prop = extractor.extract_table("propriedades")
        df_neg = extractor.extract_table("negativacao")

        df_decisao = transformer.transform_business_rule(df_cliente, df_endereco, df_prop, df_neg) # noqa
        df_decisao.show(5, truncate=False)

        loader.load_as_chunked_json_to_s3(df_decisao, S3_BUCKET, S3_PREFIX, MAX_FILE_SIZE_BYTES) # noqa

        ETLLogger.log_event("ETL finalizado", result="Sucesso")
    except Exception:
        ETLLogger.log_event("ETL finalizado", result="Erro", error=traceback.format_exc()) # noqa
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
