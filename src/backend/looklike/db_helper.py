from looklike.database import get_db_cursor
from looklike.models import Clothes


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
        