from functools import wraps
from typing import Optional

from flask import request, jsonify

from looklike.authorizations import JWTAuthorization
from looklike.configs import config
from looklike.exceptions import AuthorizationException


def get_json_data_from_body(
    required_fields: Optional[list[str]] = None
):
    """
    Retrieves a json data from the request body and passes it to the route
    handler
    """
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify(
                    {
                        'message':
                        'The request body must only be of type \'JSON\''
                    }
                ), 400

            data = request.get_json(silent=True)

            if not data:
                return jsonify(
                    {'message': 'Received an error while parsing JSON'}
                ), 400

            if required_fields:
                if not isinstance(data, dict):
                    return jsonify(
                        {
                            'message':
                            'You must send JSON object in request body'
                        }
                    ), 400

                for field in required_fields:
                    field_data = data.get(field)

                    if not field_data:
                        return jsonify(
                            {
                                'message':
                                f'You must send \'{field}\' in request body'
                            }
                        ), 400
            return func(*args, **kwargs, data=data)
        return wrapper
    return actual_decorator


def authorized_required(func):
    """Available to authorized users only"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            auth = JWTAuthorization(secret_key=config.SECRET_KEY)
            token = auth.get_acces_token_from_headers(request.headers)
            user_id = auth.get_user_id_from_acces_token(token)
        except AuthorizationException as e:
            return jsonify({'message': str(e)}), 401
        return func(*args, **kwargs, user_id=user_id)
    return decorated_function
