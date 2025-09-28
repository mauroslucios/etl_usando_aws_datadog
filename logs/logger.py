import logging
import traceback

# configuração básica do logger
logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class ETLLogger:
    @staticmethod
    def log_event(event, db=None, table=None, action=None, result=None, error=None):
        """
        Cria um log detalhado do evento do ETL.
        """
        msg = f"[{event}] "

        if db:
            msg += f"Database={db} "
        if table:
            msg += f"Table={table} "
        if action:
            msg += f"Action={action} "
        if result:
            msg += f"Result={result} "
        if error:
            msg += f"Error={error} "

        if error:
            logging.error(msg)
        else:
            logging.info(msg)

