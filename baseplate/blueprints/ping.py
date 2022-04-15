from flask import Blueprint

from baseplate.http import m_response

BP_PING = Blueprint("bp_ping", __name__)


@BP_PING.route("/ping")
def get_pong():
    return m_response.MResponse().add_data({"data": "pong"}).send()
