"""Contains a common implementation for requests.
"""
from baseplate.http import utils
from flask import Request, request
from werkzeug import datastructures as ds


class MRequestLog(object):

    _MAX_BODY_LENGTH_IN_BYTES = 1 * 1024 * 1024  # 1 MB

    def __init__(
        self,
        scheme: str,
        path: str,
        remote_addr: str,
        method: str,
        headers: dict,
        body: any,
        params: dict,
    ) -> None:
        self.scheme = utils.verify_or_convert_to_str(scheme)
        self.path = utils.verify_or_convert_to_str(path)
        self.remote_addr = utils.verify_or_convert_to_str(remote_addr)
        self.method = utils.verify_or_convert_to_str(method)
        self.headers = utils.verify_or_convert_to_dict(headers)
        self.body = utils.verify_or_convert_to_dict(body)
        self.params = utils.verify_or_convert_to_dict(params)

    def log_str(self) -> str:
        log_str = {
            "scheme": self.scheme,
            "path": self.path,
            "remote_addr": self.remote_addr,
            "method": self.method,
            "headers": self.headers,
            "body": self.body,
            "params": self.params,
        }
        return log_str


class MFlaskRequestLog(MRequestLog):
    def __init__(self, request: Request) -> None:
        self.request = request
        self._init_m_request_log()

    def _init_m_request_log(self) -> None:
        super().__init__(
            self.request.scheme,
            self.request.path,
            self.request.remote_addr,
            self.request.method,
            self._convert_headers_to_dict(),
            self._convert_body_to_json(),
            self._convert_params_to_dict(),
        )

    def _convert_headers_to_dict(self) -> dict:
        headers_dict = {}
        for key, value in self.request.headers:
            headers_dict[key] = value

        return headers_dict

    def _convert_body_to_json(self) -> dict:
        if (
            self.request.content_length is not None
            and self.request.content_length > self._MAX_BODY_LENGTH_IN_BYTES
        ):
            return {
                "_parse_error": f"input object is greater than {self._MAX_BODY_LENGTH_IN_BYTES} bytes"
            }

        if self.request.content_length is not None and self.request.content_length == 0:
            return None

        try:
            if self.request.is_json:
                return self.request.json
        except:
            return {
                "_parse_error": "input object is not of type dict",
                "_data": request.get_data(as_text=True),
            }

        try:
            return self.request.get_json(force=True, silent=False)
        except:
            return {
                "_parse_error": "input object is not of type dict",
                "_data": request.get_data(as_text=True),
            }

    def _convert_params_to_dict(self) -> dict:
        return self.request.args.to_dict()
