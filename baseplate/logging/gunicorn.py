import logging
from baseplate.logging.logger import Logger as BaseplateLogger
from gunicorn import glogging


class Logger(glogging.Logger):
    def setup(self, cfg):
        BaseplateLogger.create_logger(
            logger_names=["root", "gunicorn.access", "gunicorn.error"]
        )
        logging.getLogger("gunicorn.error").setLevel(logging.INFO)
        logging.getLogger("gunicorn.access").setLevel(logging.INFO)
