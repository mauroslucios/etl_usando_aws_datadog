import traceback
from pyspark.sql import SparkSession
from util.config import MYSQL_URL, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DRIVER
from logs.etl_logger import ETLLogger

class Extractor:
    def __init__(self, spark):
        self.spark = spark

    def extract_table(self, table_name):
        try:
            df = (
                self.spark.read.format("jdbc")
                .option("url", MYSQL_URL)
                .option("driver", MYSQL_DRIVER)
                .option("dbtable", table_name)
                .option("user", MYSQL_USER)
                .option("password", MYSQL_PASSWORD)
                .load()
            )
            ETLLogger.log_event(
                event="Extração",
                db="elysium",
                table=table_name,
                action="Lendo dados",
                result=f"{df.count()} registros extraídos",
            )
            return df
        except Exception:
            ETLLogger.log_event(
                    event="Extração",
                    db="elysium",
                    table=table_name,
                    action="Leitura",
                    result="Erro",
                    error=traceback.format_exc()
                )
            raise