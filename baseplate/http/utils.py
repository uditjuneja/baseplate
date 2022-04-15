from ast import parse
from urllib.parse import urlparse
from werkzeug import datastructures as ds
from flask import current_app as app
from requests import Response, PreparedRequest
import json


def verify_or_convert_to_dict(input: any) -> dict:
    if input is None:
        return {}

    if isinstance(input, dict):
        return input

    try:
        return dict(input)
    except:
        pass

    return {"_parse_error": "input object is not of type dict"}


def verify_or_convert_to_str(input: any) -> str:
    if input is None:
        return ""

    if isinstance(input, str):
        return input

    try:
        return str(input)
    except:
        pass

    return "input object is not of type str"


def verify_or_convert_to_int(input: any) -> int:
    if input is None:
        return -1

    if isinstance(input, int):
        return input

    try:
        return int(input)
    except:
        pass

    return -1


# def log_requests_request(request: PreparedRequest):
#     parsed_url = urlparse(request.url)
#     log_request = {
#         "scheme" : parsed_url.scheme,
#         "path" : parsed_url.path,
#         "hostname" : parsed_url.hostname,
#         "method": request.method,
#         "headers" : convert_res_headers_to_json(request.headers),
#         "body" : request.body,
#         "params" : parsed_url.params
#     }
#     app.logger.info(log_request)

# def log_requests_data(response : Response, *args, **kwargs):
#     log_requests_request(response.request)
#     log_response = {
#         "status_code" : response.status_code,
#         "headers" : convert_res_headers_to_json(response.headers),
#         "body" : response.json()
#     }
#     app.logger.info(log_response)
