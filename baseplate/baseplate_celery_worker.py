import logging
from celery import Celery
from flask import Flask
from baseplate.baseplate import Baseplate


class BaseplateCeleryWorker(Baseplate):
    def __init__(self, app: Celery = None) -> None:
        self.app = app
        self._set_root_logger()
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Celery) -> None:
        if app is not None:
            self.app = app

        self._set_log_levels()
        # self._set_default_configuration_locations(app)
        # self._set_default_configuration_options(app)
        # self._set_request_response_logging(app)
        # self._set_signals(app)
        # self._set_apm(app)

    @staticmethod
    def _set_log_levels():
        Baseplate._set_log_levels()
        logging.getLogger("celery.app.trace").setLevel(logging.INFO)

    @staticmethod
    def _set_flask_app_logger_level(app: Flask):
        logging.getLogger(app.name).setLevel(logging.INFO)

    # @staticmethod
    # def _set_default_configuration_locations(app: Flask) -> None:
    #   app.config.from_envvar("CONFIG")

    # @staticmethod
    # def _set_default_configuration_options(app: Flask) -> None:
    #   app.config.setdefault("ROOT_LOG_LEVEL", logging.ERROR)

    # @staticmethod
    # def _set_ping_route(app: Flask) -> None:
    #   app.register_blueprint(PING)

    # @staticmethod
    # def _set_request_response_logging(app: Flask) -> None:
    #   app.register_blueprint(REQ_RES_LOGGING)

    # @staticmethod
    # def _set_signals(app: Flask) -> None:
    #   app.apm = ElasticAPM(app, app.name)
    #   # disable celery logger
    # @setup_logging.connect
    # def after_setup_logger(**kwargs):
    #     pass

    # @staticmethod
    # def _set_apm(app: Flask) -> None:
    #   app.apm = ElasticAPM(app, app.name)

    @staticmethod
    def init_app_with_flask(app_celery: Celery, app_flask: Flask) -> None:
        BaseplateCeleryWorker._set_flask_app_logger_level(app_flask)
        app_celery.conf.update(app_flask.config)
        TaskBase = app_celery.Task

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                with app_flask.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        app_celery.Task = ContextTask
