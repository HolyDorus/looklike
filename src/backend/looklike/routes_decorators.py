from functools import wraps

from flask import request, jsonify

from looklike.authorizations import JWTAuthorization
from looklike.configs import config
from looklike.exceptions import AuthorizationException


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


def authorized_optional(func):
    """Available to all users"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            auth = JWTAuthorization(secret_key=config.SECRET_KEY)
            token = auth.get_acces_token_from_headers(request.headers)
            user_id = auth.get_user_id_from_acces_token(token)
        except AuthorizationException:
            return func(*args, **kwargs)
        return func(*args, **kwargs, user_id=user_id)

    return decorated_function
