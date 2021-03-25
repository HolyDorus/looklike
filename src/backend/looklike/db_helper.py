from typing import Optional

from looklike.authorizations import JWTAuthorization
from looklike.configs import config
from looklike.database import get_db_cursor
from looklike.exceptions import (
    ObjectNotFoundException,
    UserAlreadyExistsException,
    CharacterAlreadyInFavorites
)
from looklike.models import (
    Clothes, Character,
    User, UserRegistration
)


class ClothesDBHelper:
    @staticmethod
    def get_all_clothes() -> list[Clothes]:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT id, name, image_path, parent_id, parent_path FROM '
                 'all_clothes;')
            )
            data = cursor.fetchall()

        all_clothes = [Clothes(**item) for item in data]
        return all_clothes

    @staticmethod
    def get_clothes_by_parent_id(parent_id: int) -> list[Clothes]:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT id, name, image_path, parent_id, parent_path FROM '
                 'all_clothes WHERE parent_id = %s ORDER BY '
                 'display_priority;'),
                (parent_id,)
            )
            data = cursor.fetchall()

        clothes_by_parent = [Clothes(**item) for item in data]
        return clothes_by_parent

    @staticmethod
    def get_primary_clothes() -> list[Clothes]:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT id, name, image_path, parent_id, parent_path FROM '
                 'all_clothes WHERE parent_path ~ \'*{,2}\' ORDER BY '
                 'display_priority;')
            )
            data = cursor.fetchall()

        primary_clothes = [Clothes(**item) for item in data]
        return primary_clothes

    @staticmethod
    def get_clothes_parent_paths(clothes_ids: list[int]) -> list[str]:
        with get_db_cursor() as cursor:
            query = 'SELECT parent_path FROM all_clothes WHERE id = any(%s)'
            cursor.execute(query, (clothes_ids,))
            data = cursor.fetchall()

        parent_paths = [item['parent_path'] for item in data]
        return parent_paths

    @staticmethod
    def get_character_clothes(character: Character) -> list[Clothes]:
        with get_db_cursor() as cursor:
            query = (
                'SELECT id, name, image_path, parent_id, parent_path FROM '
                'all_clothes WHERE id in (SELECT clothes_id FROM '
                'clothes_on_characters WHERE character_id = %s) ORDER BY '
                'display_priority'
            )
            cursor.execute(query, (character.id,))
            data = cursor.fetchall()

        clothes = [Clothes(**item) for item in data]
        return clothes


class CharactersDBHelper:
    @staticmethod
    def get_favorites(
        user_id: int,
        with_clothes: bool = False
    ) -> list[Character]:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT id, author_id, image_path, description, posted_at '
                 'FROM characters WHERE characters.id IN (SELECT character_id '
                 'FROM favorite_characters_of_users WHERE user_id = %s);'),
                (user_id,)
            )
            data = cursor.fetchall()

        favorite_characters = [Character(**item) for item in data]

        if with_clothes:
            CharactersDBHelper._inject_clothes_to_characters(
                favorite_characters
            )

        if user_id:
            CharactersDBHelper._inject_is_favorite_field(
                user_id=user_id,
                characters=favorite_characters
            )

        return favorite_characters

    @staticmethod
    def add_to_favorites(character_id: int, user_id: int) -> None:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT EXISTS (SELECT 1 FROM characters WHERE id = %s);'),
                (character_id,)
            )
            data = cursor.fetchone()

        if not data.get('exists'):
            raise ObjectNotFoundException(
                f'Character with id={character_id} not found!'
            )

        if CharactersDBHelper.is_favorite_character(user_id, character_id):
            raise CharacterAlreadyInFavorites(
                'The character already exists in favorites'
            )

        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                ('INSERT INTO favorite_characters_of_users (character_id, '
                 'user_id) VALUES (%s, %s);'),
                (character_id, user_id)
            )

    @staticmethod
    def remove_from_favorites(character_id: int, user_id: int) -> None:
        if not CharactersDBHelper.is_favorite_character(user_id, character_id):
            raise ObjectNotFoundException(
                'This character was not found in favorites!'
            )

        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                ('DELETE FROM favorite_characters_of_users WHERE character_id '
                 '= %s AND user_id = %s;'),
                (character_id, user_id)
            )

    @staticmethod
    def get_all_characters(
        user_id: Optional[int] = None,
        with_clothes: bool = False
    ) -> list[Character]:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT id, author_id, image_path, description, posted_at '
                 'FROM characters;')
            )
            data = cursor.fetchall()

        all_characters = [Character(**item) for item in data]

        if with_clothes:
            CharactersDBHelper._inject_clothes_to_characters(all_characters)

        if user_id:
            CharactersDBHelper._inject_is_favorite_field(
                user_id=user_id,
                characters=all_characters
            )

        return all_characters

    @staticmethod
    def get_character_by_id(
        character_id: int,
        with_clothes: bool = False
    ) -> Character:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT id, author_id, image_path, description, posted_at '
                 'FROM characters WHERE id = %s;'),
                (character_id,)
            )
            data = cursor.fetchone()

        if not data:
            raise ObjectNotFoundException(
                f'Character with id={character_id} not found!'
            )

        character = Character(**data)

        if with_clothes:
            CharactersDBHelper._inject_clothes_to_characters([character])

        return character

    @staticmethod
    def get_newest_characters(
        user_id: Optional[int] = None,
        limit: int = 10,
        with_clothes: bool = False
    ) -> list[Character]:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT id, author_id, image_path, description, posted_at '
                 'FROM characters ORDER BY posted_at DESC LIMIT %s;'),
                (limit,)
            )
            data = cursor.fetchall()

        newest_characters = [Character(**item) for item in data]

        if with_clothes:
            CharactersDBHelper._inject_clothes_to_characters(newest_characters)

        if user_id:
            CharactersDBHelper._inject_is_favorite_field(
                user_id=user_id,
                characters=newest_characters
            )

        return newest_characters

    @staticmethod
    def get_characters_by_clothes(
        clothes_ids: list[int],
        user_id: Optional[int] = None,
        with_clothes: bool = False
    ) -> list[Character]:
        with get_db_cursor() as cursor:
            parent_paths = ClothesDBHelper.get_clothes_parent_paths(
                clothes_ids
            )

            if not parent_paths:
                raise ObjectNotFoundException(
                    'One or more Clothes from the list were not found!'
                )

            query = CharactersDBHelper._format_specific_query(parent_paths)
            cursor.execute(query, parent_paths)
            data = cursor.fetchall()

        characters = [Character(**item) for item in data]

        if with_clothes:
            CharactersDBHelper._inject_clothes_to_characters(characters)

        if user_id:
            CharactersDBHelper._inject_is_favorite_field(
                user_id=user_id,
                characters=characters
            )

        return characters

    @staticmethod
    def is_favorite_character(user_id: int, character_id: int) -> bool:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT EXISTS (SELECT 1 FROM favorite_characters_of_users '
                 'WHERE character_id = %s AND user_id = %s);'),
                (character_id, user_id)
            )
            data = cursor.fetchone()

        return data.get('exists')

    @staticmethod
    def _inject_clothes_to_characters(characters: list[Character]):
        for character in characters:
            character.clothes = ClothesDBHelper.get_character_clothes(
                character
            )

    @staticmethod
    def _inject_is_favorite_field(user_id: int, characters: list[Character]):
        for character in characters:
            character.is_favorite = CharactersDBHelper.is_favorite_character(
                user_id=user_id,
                character_id=character.id
            )

    @staticmethod
    def _format_specific_query(parent_paths: list[str]) -> str:
        base_query = (
            'SELECT id, author_id, image_path, description, posted_at FROM '
            'characters WHERE id IN (SELECT character_id FROM '
            'clothes_on_characters WHERE clothes_id IN (SELECT id FROM '
            'all_clothes WHERE parent_path <@ %s))'
        )

        for i, _ in enumerate(parent_paths):
            if i == 0:
                query = f'{base_query}'
            else:
                query = f'{query} INTERSECT {base_query}'

        return query


class UsersDBHelper:
    @staticmethod
    def get_user_by_username(username: str) -> User:
        with get_db_cursor() as cursor:
            cursor.execute(
                ('SELECT id, username, password_hash, registered_at FROM '
                 'users WHERE username = %s;'), (username,)
            )
            data = cursor.fetchone()

        if not data:
            raise ObjectNotFoundException(
                'User with this name was not found!'
            )

        return User(**data)

    @staticmethod
    def is_user_exists(username: str) -> bool:
        with get_db_cursor() as cursor:
            cursor.execute(
                'SELECT EXISTS (SELECT 1 FROM users WHERE username = %s);',
                (username,)
            )
            data = cursor.fetchone()

        return data.get('exists')

    @staticmethod
    def create_user(user: UserRegistration) -> User:
        if UsersDBHelper.is_user_exists(user.username):
            raise UserAlreadyExistsException(
                'User with this name already exists!'
            )

        auth = JWTAuthorization(secret_key=config.SECRET_KEY)
        password_hash = auth.generate_password(user.password)

        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                ('INSERT INTO users (username, password_hash) VALUES (%s, %s) '
                 'RETURNING id, registered_at'), (user.username, password_hash)
            )
            data = cursor.fetchone()

        return User(
            id=data['id'],
            username=user.username,
            password_hash=password_hash,
            registered_at=data['registered_at']
        )
