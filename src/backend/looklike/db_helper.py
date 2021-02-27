from psycopg2 import sql

from looklike.database import get_db_cursor
from looklike.exceptions import ObjectNotFoundException
from looklike.models import Clothes, Character


class DBHelper:
    @staticmethod
    def get_all_clothes() -> list[Clothes]:
        with get_db_cursor() as cursor: 
            cursor.execute('SELECT * FROM all_clothes;') 
            data = cursor.fetchall()
        
        all_clothes = [Clothes(**item) for item in data]
        return all_clothes

    @staticmethod
    def get_clothes_by_parent_id(parent_id: int) -> list[Clothes]:
        with get_db_cursor() as cursor:
            cursor.execute(
                'SELECT * FROM all_clothes WHERE ' + \
                'parent_id = %s;', (parent_id,)
            ) 
            data = cursor.fetchall()
        
        clothes_by_parent = [Clothes(**item) for item in data]
        return clothes_by_parent

    @staticmethod
    def get_primary_clothes() -> list[Clothes]:
        with get_db_cursor() as cursor:
            cursor.execute(
                'SELECT * FROM all_clothes WHERE parent_path ~ \'*{,2}\';'
            ) 
            data = cursor.fetchall()
        
        primary_clothes = [Clothes(**item) for item in data]
        return primary_clothes

    @staticmethod
    def get_all_characters() -> list[Character]:
        with get_db_cursor() as cursor: 
            cursor.execute('SELECT * FROM characters;') 
            data = cursor.fetchall()
            
        all_characters = [Character(**item) for item in data]
        return all_characters

    @staticmethod
    def get_character_by_id(character_id: int) -> Character:
        with get_db_cursor() as cursor:
            cursor.execute(
                'SELECT * FROM characters WHERE id = %s;', (character_id,)
            ) 
            data = cursor.fetchone()

        if not data:
            raise ObjectNotFoundException(
                f'Character with id={character_id} not found!'
            )

        character = Character(**data)
        return character

    @staticmethod
    def get_characters_by_clothes(clothes_ids: list[int]) -> list[Character]:
        with get_db_cursor() as cursor:
            parent_paths = DBHelper._get_clothes_parent_paths(clothes_ids)

            if not parent_paths:
                raise ObjectNotFoundException(
                    f'One or more Clothes from the list were not found!'
                )

            query = DBHelper._format_specific_query(parent_paths)
            cursor.execute(query, parent_paths)
            data = cursor.fetchall()
        
        characters = [Character(**item) for item in data]
        return characters

    @staticmethod
    def _get_clothes_parent_paths(clothes_ids: list[int]) -> list[str]:
        with get_db_cursor() as cursor:
            query = 'SELECT parent_path FROM all_clothes WHERE id = any(%s)'
            cursor.execute(query, (clothes_ids,))
            data = cursor.fetchall()
        
        parent_paths = [item['parent_path'] for item in data]
        return parent_paths

    @staticmethod
    def _format_specific_query(parent_paths: list[str]) -> str:
        base_query = 'SELECT * FROM characters WHERE id IN ' + \
        '(SELECT character_id FROM clothes_on_characters WHERE ' + \
        'clothes_id IN (SELECT id FROM all_clothes WHERE ' + \
        'parent_path <@ %s))'

        for i, _ in enumerate(parent_paths):
            if i == 0:
                query = f'{base_query}'
            else:
                query = f'{query} INTERSECT {base_query}'

        return query
