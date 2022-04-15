import logging
from flask import Flask
from baseplate.baseplate import Baseplate
from baseplate.blueprints.req_res_logging import BP_REQ_RES_LOGGING
from baseplate.blueprints.ping import BP_PING


class BaseplateFlask(Baseplate):
    def __init__(self, app: Flask = None) -> None:
        self.app = app
        self._set_root_logger()
        self._set_gunicorn_logger()
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        if app is not None:
            self.app = app

        self._set_log_levels(app)
        # self._set_default_configuration_locations(app)
        # self._set_default_configuration_options(app)
        self._set_ping_route(app)
        self._set_request_response_logging(app)
        # self._set_teardown_request(app)
        # self._set_apm(app)

    @staticmethod
    def _set_log_levels(app: Flask):
        Baseplate._set_log_levels()
        logging.getLogger("gunicorn.error").setLevel(logging.ERROR)
        logging.getLogger("gunicorn.access").setLevel(logging.ERROR)
        logging.getLogger(app.name).setLevel(logging.INFO)
        logging.getLogger("baseplate.blueprints.req_res_logging").setLevel(logging.INFO)

    # @staticmethod
    # def _set_default_configuration_locations(app: Flask) -> None:
    #   app.config.from_envvar("CONFIG")

    # @staticmethod
    # def _set_default_configuration_options(app: Flask) -> None:
    #   app.config.setdefault("ROOT_LOG_LEVEL", logging.ERROR)

    @staticmethod
    def _set_ping_route(app: Flask) -> None:
        app.register_blueprint(BP_PING)

    @staticmethod
    def _set_request_response_logging(app: Flask) -> None:
        app.register_blueprint(BP_REQ_RES_LOGGING)

    # @staticmethod
    # def _set_apm(app: Flask) -> None:
    #   #app.apm = ElasticAPM(app, app.name)
    #   pass
