import logging
from baseplate.logging.logger import Logger


class Baseplate(object):
    # Common functions of flask and celery
    @staticmethod
    def _set_root_logger() -> None:
        Logger.create_logger(logger_names=["root"])

    @staticmethod
    def _set_gunicorn_logger() -> None:
        Logger.create_logger(logger_names=["gunicorn.error", "gunicorn.access"])

    @staticmethod
    def _set_log_levels() -> None:
        logging.getLogger("elasticapm").setLevel(logging.CRITICAL)
        logging.getLogger("ddtrace").setLevel(logging.CRITICAL)
        # This logger is used by both flask and celery
        # However, this logger is incorrect.
        # logging.getLogger('flask.app').setLevel(logging.INFO)
