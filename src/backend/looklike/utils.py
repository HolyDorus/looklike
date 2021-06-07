from datetime import datetime

from flask import current_app
from flask.wrappers import Response


def get_ids_from_string(string: str) -> list[int]:
    return [int(id) for id in string.strip('[]').split(',')]


def datetime_to_timestamp(value: datetime) -> str:
    return int(value.timestamp())


def raw_json_to_response(data: str) -> Response:
    return current_app.response_class(
        data,
        mimetype=current_app.config["JSONIFY_MIMETYPE"],
    )
