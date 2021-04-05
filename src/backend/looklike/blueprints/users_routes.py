from flask import Blueprint, request

from looklike.authorizations import JWTAuthorization
from looklike.configs import config
from looklike.db_helper import UsersDBHelper
from looklike.exceptions import (
    ObjectNotFoundException,
    UserAlreadyExistsException
)
from looklike.models import UserRegistration, UserLogin
from looklike.utils import jsoning


url_prefix = '/api/v1/users/'
users_bp = Blueprint('users_bp', __name__, url_prefix=url_prefix)


@users_bp.route('register', methods=['POST'])
def register():
    """Registers a user and returns it"""
    data = UserRegistration.parse_raw(request.data)

    try:
        user = UsersDBHelper.create_user(data)
    except UserAlreadyExistsException as e:
        return jsoning({'message': str(e)}), 409

    return jsoning(user.json(exclude={'password_hash'})), 201


@users_bp.route('login', methods=['POST'])
def login():
    """Authorizes the user and returns access token"""
    data = UserLogin.parse_raw(request.data)

    try:
        user = UsersDBHelper.get_user_by_username(data.username)
    except ObjectNotFoundException as e:
        return jsoning({"message": str(e)}), 404

    auth = JWTAuthorization(secret_key=config.SECRET_KEY)

    if not auth.is_correct_password(data.password, user.password_hash):
        return jsoning({'message': 'Invalid password!'}), 401

    token = auth.create_token(data={'user_id': user.id})

    return jsoning({'access_token': token})
