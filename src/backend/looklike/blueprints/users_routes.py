from flask import Blueprint, jsonify

from looklike.authorizations import JWTAuthorization
from looklike.configs import config
from looklike.db_helper import UsersDBHelper
from looklike.exceptions import ObjectNotFoundException
from looklike.serializers import UserSerializer
from looklike.routes_decorators import get_json_data_from_body


url_prefix = '/api/v1/users/'
users_bp = Blueprint('users_bp', __name__, url_prefix=url_prefix)


@users_bp.route('register', methods=['POST'])
@get_json_data_from_body(required_fields=['username', 'password'])
def register(data):
    """Registers a user and returns it"""
    try:
        user = UsersDBHelper.get_user_by_username(data['username'])
    except ObjectNotFoundException:
        pass
    else:
        return jsonify(
            {'message': 'A user with the same name already exists'}
        ), 400

    user = UsersDBHelper.create_user(data['username'], data['password'])

    return jsonify(UserSerializer.serialize_one(user)), 201


@users_bp.route('login', methods=['POST'])
@get_json_data_from_body(required_fields=['username', 'password'])
def login(data):
    """Authorizes the user and returns access token"""
    try:
        user = UsersDBHelper.get_user_by_username(data['username'])
    except ObjectNotFoundException as e:
        return jsonify({"message": str(e)}), 404

    auth = JWTAuthorization(secret_key=config.SECRET_KEY)

    if not auth.is_correct_password(data['password'], user.password_hash):
        return jsonify({'message': 'Invalid password!'}), 400

    token = auth.create_token(user.id)

    return jsonify({'access_token': token})
