from typing import Union

from looklike.configs import config
from looklike.models import Clothes, Character


class ClothesSerializer():
    @staticmethod
    def serialize(clothes) -> Union[dict, list]:
        if isinstance(clothes, list) or isinstance(clothes, tuple):
            return [ClothesSerializer.serialize_one(cl) for cl in clothes]
        else:
            return ClothesSerializer.serialize_one(clothes)

    @staticmethod
    def serialize_one(clothes: Clothes) -> dict:
        base_url = 'http://127.0.0.1:5000'
        media_url = config.MEDIA_URL
        image_url = f'{base_url}{media_url}{clothes.image_path}'

        return {
            'id': clothes.id,
            'name': clothes.name,
            'image_path': image_url,
            'parent_id': clothes.parent_id
        }

    @staticmethod
    def serialize_primary_only(primary_clothes: list[Clothes]) -> list[dict]:
        result = []
        for clothes in primary_clothes:
            if clothes.parent_id:
                continue

            serialized = ClothesSerializer.serialize_one(clothes)
            children = ClothesSerializer._get_children(clothes, primary_clothes)

            serialized['children'] = [
                ClothesSerializer.serialize_one(child) for child in children
            ]

            result.append(serialized)
        return result

    @staticmethod
    def _get_children(clothes: Clothes, clothing_list: list[Clothes]) -> list[Clothes]:
        children = [cl for cl in clothing_list if cl.parent_id == clothes.id]
        return children        


class CharactersSerializer():
    @staticmethod
    def serialize(character) -> Union[dict, list]:
        if isinstance(character, list) or isinstance(character, tuple):
            return [CharactersSerializer.serialize_one(cl) for cl in character]
        else:
            return CharactersSerializer.serialize_one(character)

    @staticmethod
    def serialize_one(character: Character) -> dict:
        base_url = 'http://127.0.0.1:5000'
        media_url = config.MEDIA_URL
        image_url = f'{base_url}{media_url}{character.image_path}'
        
        return {
            'id': character.id,
            'author_id': character.author_id,
            'image_path': image_url,
            'description': character.description,
            'posted_at': {
                'date': character.posted_at.strftime('%d.%m.%Y'),
                'time': character.posted_at.strftime('%H:%M:%S'),
                'full': character.posted_at.strftime('%d.%m.%Y %H:%M:%S')
            }
        }

    @staticmethod
    def serialize_characters_with_clothes(characters_with_clothes: list) -> list:
        result = []
        for obj in characters_with_clothes:
            character = CharactersSerializer.serialize_one(obj['character'])
            clothes = ClothesSerializer.serialize(obj['clothes'])
            character['clothes'] = clothes
            result.append(character)
        return result
