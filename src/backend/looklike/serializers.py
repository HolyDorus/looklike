from typing import Union

from looklike.configs import config
from looklike.models import Clothes, Character


class ClothesSerializer():
    @classmethod
    def serialize(cls, clothes) -> Union[dict, list]:
        if isinstance(clothes, list) or isinstance(clothes, tuple):
            return [cls.serialize_one(cl) for cl in clothes]
        else:
            return cls.serialize_one(clothes)

    @classmethod
    def serialize_one(cls, clothes: Clothes) -> dict:
        image_url = f'{config.MEDIA_URL}{clothes.image_path}'

        return {
            'id': clothes.id,
            'name': clothes.name,
            'image_path': image_url,
            'parent_id': clothes.parent_id
        }

    @classmethod
    def serialize_primary_only(
        cls,
        primary_clothes: list[Clothes]
    ) -> list[dict]:
        result = []
        for clothes in primary_clothes:
            if clothes.parent_id:
                continue

            serialized = cls.serialize_one(clothes)
            children = cls._get_children(clothes, primary_clothes)

            serialized['children'] = [
                cls.serialize_one(child) for child in children
            ]

            result.append(serialized)

        return result

    @classmethod
    def _get_children(
        cls,
        clothes: Clothes,
        clothing_list: list[Clothes]
    ) -> list[Clothes]:
        children = list(
            filter(lambda x: x.parent_id == clothes.id, clothing_list)
        )

        return children


class CharactersSerializer():
    @classmethod
    def serialize(cls, characters) -> Union[dict, list]:
        if isinstance(characters, list) or isinstance(characters, tuple):
            return [cls.serialize_one(character) for character in characters]
        else:
            return cls.serialize_one(characters)

    @classmethod
    def serialize_one(cls, character: Character) -> dict:
        image_url = f'{config.MEDIA_URL}{character.image_path}'

        output_data = {
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

        if character.is_favorite is not None:
            output_data['is_favorite'] = character.is_favorite

        return output_data


class CharactersWithClothesSerializer():
    @classmethod
    def serialize_one(cls, character: Character) -> dict:
        serialized_character = CharactersSerializer.serialize_one(character)
        serialized_clothes = ClothesSerializer.serialize(character.clothes)
        serialized_character['clothes'] = serialized_clothes

        return serialized_character

    @classmethod
    def serialize(cls, characters) -> Union[dict, list]:
        if (isinstance(characters, list) or
                isinstance(characters, tuple)):
            return [
                cls.serialize_one(character) for character in characters
            ]
        else:
            return cls.serialize_one(characters)
