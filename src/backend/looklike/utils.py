from datetime import datetime

from flask import current_app


def get_ids_from_string(string: str) -> list[int]:
    return [int(id) for id in string.strip('[]').split(',')]


def datetime_to_timestamp(value: datetime) -> str:
    return value.strftime('%s')


def raw_json_to_response(data: str):
    return current_app.response_class(
        data,
        mimetype=current_app.config["JSONIFY_MIMETYPE"],
    )
