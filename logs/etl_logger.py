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
    def log_event(event, db=None, table=None, action=None, result=None, error=None, extra=None, level="INFO"):
        """
        Cria um log detalhado do evento do ETL.
        """
        msg = f"[{event}]"

        if db:
            msg += f" | Database: {db}"
        if table:
            msg += f" | Table: {table}"
        if action:
            msg += f" | Action: {action}"
        if result:
            msg += f" | Result: {result}"
        if extra:
            msg += f" | Extra: {extra}"
        if error:
            msg += f" | Error: {error}"

        if level == "ERROR":
            logging.error(msg)
        elif level == "WARNING":
            logging.warning(msg)
        else:
            logging.info(msg)

    @staticmethod
    def log_exception(event, db=None, table=None, action=None):
        """
        Loga exceções automaticamente com stacktrace.
        """
        error_msg = traceback.format_exc()
        ETLLogger.log_event(
            event=event,
            db=db,
            table=table,
            action=action,
            result="Erro",
            error=error_msg,
            level="ERROR"
        )
