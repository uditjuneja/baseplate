"""Creates a json based logger.

  Usage:
    Logger.create_logger(logger_names=['root'])
"""
import logging
from logging.config import dictConfig
import os
from pythonjsonlogger import jsonlogger


class Logger:
    """Creates a JSON Logger using pythonjsonlogger."""

    _LOG_LEVEL_ENV_NAME = "LOG_LEVEL"
    _ROOT_LOGGER_NAME = "root"

    @staticmethod
    def _get_log_level() -> str:
        """Gets the log level from the environment variable
        mentioned in ~_LOG_LEVEL_ENV_NAME.

        Returns:
            str: The log level.
        """
        log_level = os.getenv(Logger._LOG_LEVEL_ENV_NAME, "ERROR")
        return log_level

    @staticmethod
    def _get_handlers() -> dict:
        """Creates handlers for the logger.

        Returns:
            dict: A dict containing all the handlers.
        """
        handlers = {"console": {"class": "logging.StreamHandler", "formatter": "json"}}
        return handlers

    @staticmethod
    def _get_formatters() -> dict:
        """Creates formatters for the logger

        Returns:
            dict: A dict containing all the formatters.
        """
        formatters = {
            "json": {
                "format": "%(asctime)s \
          %(name)s \
          %(levelname)s \
          %(filename)s \
          %(module)s \
          %(funcName)s \
          %(lineno)d \
          %(message)s \
          [dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s]",
                "class": "baseplate.logging.logger._JsonFormatter",
            }
        }
        return formatters

    @staticmethod
    def _get_loggers(logger_names: list, handlers: list) -> dict:
        """Creates all the loggers and applies all handlers to all loggers.

        Args:
            logger_names (list): List of names of loggers.
            handlers (list): List of handlers to be applied to all loggers.

        Returns:
            dict: A dict containing all loggers.
        """
        loggers = {}
        for logger_name in logger_names:
            if logger_name == Logger._ROOT_LOGGER_NAME:
                logger_name = ""
            loggers[f"{logger_name}"] = {
                "handlers": handlers,
                "level": Logger._get_log_level(),
            }

        return loggers

    @staticmethod
    def create_logger_dict(logger_names: list) -> dict:
        """Creates a log config dictionary. See
        https://docs.python.org/3/library/logging.config.html for
        details.

        Args:
            logger_names (list): List of names of loggers.

        Returns:
            dict: A dict of the form of logging.config.dictConfig.
        """
        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": Logger._get_formatters(),
            "handlers": Logger._get_handlers(),
            "loggers": Logger._get_loggers(
                logger_names=logger_names, handlers=Logger._get_handlers()
            ),
        }
        return config

    @staticmethod
    def create_logger(logger_names: list) -> None:
        """Creates all loggers and intializes them.

        Args:
            logger_names (list): List of names of loggers.
        """
        dictConfig(Logger.create_logger_dict(logger_names=logger_names))

    @staticmethod
    def add_adapter(logger_names: list, adapter_dict: dict) -> None:
        """Add a dictionary to all loggers specified in input.

        Args:
            logger_names (list):  List of names of loggers.
            adapter_dict (dict): The dictioanry to add to all loggers.
        """
        for logger_name in logger_names:
            logging.LoggerAdapter(logging.getLogger(logger_name), adapter_dict)


class _JsonFormatter(jsonlogger.JsonFormatter):
    """Custom class for formatting logs in json.

    Args:
        jsonlogger (jsonlogger.JsonFormatter): Inhertied from pythonjsonlogging.
    """

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        span = None
        env = ""
        service = ""
        version = ""

        try:
            import ddtrace
            from ddtrace import tracer

            span = tracer.current_span()
            env = ddtrace.config.env
            service = ddtrace.config.service
            version = ddtrace.config.version
        except ModuleNotFoundError or ImportError:
            pass

        trace_id, span_id = (span.trace_id, span.span_id) if span else (None, None)
        log_record["dd.trace_id"] = str(trace_id or 0)
        log_record["dd.span_id"] = str(span_id or 0)
        log_record["dd.env"] = env
        log_record["dd.service"] = service
        log_record["dd.version"] = version
