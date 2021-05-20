from datetime import datetime

from flask import jsonify, current_app


def get_ids_from_string(string: str) -> list[int]:
    return [int(id) for id in string.strip('[]').split(',')]


def datetime_to_timestamp(value: datetime) -> str:
    return value.strftime('%s')


def jsoning(data):
    if isinstance(data, str):
        return current_app.response_class(
            data,
            mimetype=current_app.config["JSONIFY_MIMETYPE"],
        )

    return jsonify(data)
