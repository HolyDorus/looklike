import pytest

from looklike.authorizations import JWTAuthorization
from looklike.exceptions import AuthorizationException


@pytest.fixture
def jwtauth() -> JWTAuthorization:
    return JWTAuthorization(
        secret_key='123456789',
        hash_method='sha256',
        hash_iterations=1000,
        jwt_algorithm='HS256'
    )


def test_generate_password_hash(jwtauth: JWTAuthorization) -> None:
    password = 'qwerty'
    hashed_password = jwtauth.generate_password_hash(password)
    correct_hashed_password = 'ecfd9facee1af81965365b3d90b6de098d5a13ea85583a5437348354567e1724'

    assert hashed_password == correct_hashed_password


@pytest.mark.parametrize('password,hashed_password,expected', [
    ('qwerty', 'ecfd9facee1af81965365b3d90b6de098d5a13ea85583a5437348354567e1724', True),
    ('qwerty', '0000000000000000000000000000000000000000000000000000000000000000', False)
])
def test_is_correct_password(
    jwtauth: JWTAuthorization,
    password: str,
    hashed_password: str,
    expected: bool
) -> None:
    assert jwtauth.is_correct_password(password, hashed_password) == expected


@pytest.mark.parametrize('data,expected', [
    ({'user_id': 23}, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyM30.9_QrzHxs0r-0x1ehZPZ1rigxNTbi5XAZ7DbnUSY6_ds'),
    ({'user_id': 38, 'exp': 360}, 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozOCwiZXhwIjozNjB9.18XmF4jXcAA5WxXRD7r5wm40Hy8Mm7eTy31riAUdAG4')
])
def test_create_token(
    jwtauth: JWTAuthorization,
    data: dict,
    expected: str
) -> None:
    assert jwtauth.create_token(data) == expected


def test_get_acces_token_from_headers(jwtauth: JWTAuthorization) -> None:
    data = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjN9.ujIWxQKmpEuhBH1OhBvYD5bWYZfrq4kHRjOmj_6fKDk'}
    assert jwtauth.get_acces_token_from_headers(data) == 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjN9.ujIWxQKmpEuhBH1OhBvYD5bWYZfrq4kHRjOmj_6fKDk'


def test_get_acces_token_from_headers_invalid(jwtauth: JWTAuthorization) -> None:
    data = {'Authorization': 'asda00doao0so0d'}
    func = jwtauth.get_acces_token_from_headers
    pytest.raises(AuthorizationException, func, data)


def test_get_acces_token_from_headers_empty(jwtauth: JWTAuthorization) -> None:
    data = {}
    func = jwtauth.get_acces_token_from_headers
    pytest.raises(AuthorizationException, func, data)


def test_get_user_id_from_acces_token_valid(jwtauth: JWTAuthorization) -> None:
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyM30.9_QrzHxs0r-0x1ehZPZ1rigxNTbi5XAZ7DbnUSY6_ds'
    correct_user_id = 23
    assert jwtauth.get_user_id_from_acces_token(token) == correct_user_id


def test_get_user_id_from_acces_token(jwtauth: JWTAuthorization):
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyM30.9_QrzHxs0r-0x1ehZPZ1rigxNTbi5XAZ7DbnUSY6_ds'
    correct_user_id = 23
    assert jwtauth.get_user_id_from_acces_token(token) == correct_user_id
