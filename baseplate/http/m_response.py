"""Contains a common implementation for creating responses.
"""
from http import HTTPStatus
import json
from flask import Response
from baseplate.http import utils


class MResponse:
    """Mudrex Response Class"""
    def __init__(self):
        self.m_response_body = MResponseBody()
        self.headers = {}

    def add_error(self, code: int, text: str) -> "MResponse":
        error = MErrorBody(code, text)
        self.m_response_body = self.m_response_body.add_error(error)
        return self

    def add_data(self, data: any) -> "MResponse":
        self.m_response_body = self.m_response_body.add_data(data)
        return self

    def add_headers(self, headers: dict) -> "MResponse":
        self.headers = headers
        return self

    def send(
        self,
        status_code: HTTPStatus = HTTPStatus.OK,
        content_type: str = "application/json",
    ) -> Response:
        response = Response()

        response.data = json.dumps(self.m_response_body.create_response_body())
        response.status_code = status_code
        response.headers = self.headers
        response.content_type = content_type

        return response


class MResponseBody:
    def __init__(self) -> None:
        self.success = None
        self.data = None
        self.errors = None

    def add_data(self, data: any) -> "MResponseBody":
        self.data = data
        return self

    def add_error(self, error: "MErrorBody") -> "MResponseBody":
        if self.errors is None:
            self.errors = []
        self.errors.append(error.to_dict())
        return self

    def create_response_body(self) -> dict:
        if self.errors is not None:
            return self.__create_error_response_body()
        return self.__create_success_response_body()

    def __create_success_response_body(self) -> dict:
        self.success = True
        response_body = self.__dict__
        response_body.pop("errors", None)
        return response_body

    def __create_error_response_body(self) -> dict:
        self.success = False
        response_body = self.__dict__
        response_body.pop("data", None)
        return response_body


class MErrorBody:
    def __init__(self, code: int, text: str) -> None:
        self.code = code
        self.text = text

    def to_dict(self) -> dict:
        return self.__dict__


class MResponseLog(object):

    _MAX_BODY_LENGTH_IN_BYTES = 1 * 1024 * 1024  # 1 MB

    def __init__(self, status_code: int, headers: dict, body: dict) -> None:
        self.status_code = utils.verify_or_convert_to_int(status_code)
        self.headers = utils.verify_or_convert_to_dict(headers)
        self.body = utils.verify_or_convert_to_dict(body)

    def log_str(self) -> str:
        log_str = {
            "status_code": self.status_code,
            "headers": self.headers,
            "body": self.body,
        }
        return log_str


class MFlaskResponseLog(MResponseLog):
    """Mudrex Flask Response Log Class"""
    def __init__(self, response: Response) -> None:
        self.response = response
        self._init_m_response_log()

    def _init_m_response_log(self) -> None:
        super().__init__(
            self.response.status_code,
            self._convert_headers_to_dict(),
            self._convert_body_to_json(),
        )

    def _convert_headers_to_dict(self) -> dict:
        headers_dict = {}
        for key, value in self.response.headers.items():
            headers_dict[key] = value

        return headers_dict

    def _convert_body_to_json(self) -> dict:
        if (
            self.response.content_length is not None
            and self.response.content_length > self._MAX_BODY_LENGTH_IN_BYTES
        ):
            _parse_error = f"input object is greater than {self._MAX_BODY_LENGTH_IN_BYTES} bytes"
            return {
                "_parse_error": _parse_error
            }

        if (
            self.response.content_length is not None
            and self.response.content_length == 0
        ):
            return None

        try:
            if self.response.is_json:
                return self.response.json
        except:
            return {
                "_parse_error": "input object is not of type dict",
                "_data": self.response.get_data(as_text=True),
            }

        try:
            return self.response.get_json(force=True, silent=False)
        except:
            return {
                "_parse_error": "input object is not of type dict",
                "_data": self.response.get_data(as_text=True),
            }
