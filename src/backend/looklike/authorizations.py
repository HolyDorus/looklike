from typing import Optional
from hashlib import pbkdf2_hmac

import jwt

from looklike.exceptions import AuthorizationException


class JWTAuthorization:
    def __init__(
        self, secret_key,
        hash_method='sha256',
        hash_iterations=10000,
        jwt_algorithm='HS256'
    ):
        self.secret_key = secret_key
        self.hash_method = hash_method
        self.hash_iterations = hash_iterations
        self.jwt_algorithm = jwt_algorithm

    def generate_password(self, password: str) -> str:
        """Creates a hashed password from a raw password"""
        return pbkdf2_hmac(
            hash_name=self.hash_method,
            password=password.encode('utf-8'),
            salt=self.secret_key.encode('utf-8'),
            iterations=self.hash_iterations
        ).hex()

    def is_correct_password(self, password: str, hash: str) -> bool:
        """Compares the raw password with a hashed password"""
        return pbkdf2_hmac(
            hash_name=self.hash_method,
            password=password.encode('utf-8'),
            salt=self.secret_key.encode('utf-8'),
            iterations=self.hash_iterations
        ).hex() == hash

    def create_token(self, user_id: int, exp: Optional[int] = None) -> str:
        """Creates and returns a JWT with the required data"""
        data = {'user_id': user_id}

        if exp:
            data['exp'] = exp

        return jwt.encode(
            payload=data,
            key=self.secret_key,
            algorithm=self.jwt_algorithm
        )

    def get_acces_token_from_headers(self, headers: dict) -> Optional[str]:
        """Retrieves and returns a token from the request headers"""
        auth_data = headers.get('Authorization')

        if not auth_data:
            raise AuthorizationException(
                'You should add the \'Authorization\' header to your request!'
            )

        if not auth_data.startswith('Bearer '):
            raise AuthorizationException(
                'The \'Authorization\' header must start with \'Bearer \'!'
            )

        return auth_data[7:]

    def get_user_id_from_acces_token(self, token: str) -> Optional[int]:
        """Retrieves and returns user_id from token"""
        try:
            data = jwt.decode(
                jwt=token,
                key=self.secret_key,
                algorithms=self.jwt_algorithm
            )
            return data['user_id']
        except KeyError:
            raise AuthorizationException(
                'Can\'t extract \'user_id\' from token!'
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthorizationException(
                'You are using an expired token!'
            )
        except jwt.exceptions.DecodeError:
            raise AuthorizationException(
                'Token cannot be decoded because it failed validation!'
            )
        except jwt.exceptions.InvalidSignatureError:
            raise AuthorizationException(
                ('Token’s signature doesn’t match the one provided as part of '
                 'the token!')
            )
        except jwt.exceptions.InvalidTokenError:
            raise AuthorizationException(
                'Token cannot be decoded!'
            )
