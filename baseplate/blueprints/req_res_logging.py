import logging
from flask import Blueprint
from flask import Blueprint, current_app as app, request, jsonify
from werkzeug import datastructures as ds, Response
from baseplate.http import m_request
from baseplate.http import m_response

_LOGGER = logging.getLogger(__name__)
BP_REQ_RES_LOGGING = Blueprint("bp_req_res_logging", __name__)


@BP_REQ_RES_LOGGING.before_app_request
def before_request():
    log_dict = m_request.MFlaskRequestLog(request).log_str()
    _LOGGER.info("::RECEIVED-REQUEST::", extra=log_dict)


@BP_REQ_RES_LOGGING.after_app_request
def after_request(response: Response):
    log_dict = m_response.MFlaskResponseLog(response).log_str()
    _LOGGER.info("::SENT-RESPONSE::", extra=log_dict)
    return response
