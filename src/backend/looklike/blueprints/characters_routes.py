from typing import Optional

from flask import Blueprint, request, json as flask_json

from looklike.configs import config
from looklike.db_helper import CharactersDBHelper
from looklike.exceptions import (
    ObjectNotFoundException,
    CharacterAlreadyInFavorites
)
from looklike.serializers import CharactersWithClothesSerializer
from looklike.redis_client import redis_client, format_cache_key
from looklike.routes_decorators import authorized_required, authorized_optional
from looklike.utils import get_ids_from_string, jsoning


url_prefix = '/api/v1/characters/'
characters_bp = Blueprint('characters_bp', __name__, url_prefix=url_prefix)


@characters_bp.route('', methods=['GET'])
@authorized_optional
def get_characters(user_id: Optional[int] = None):
    # URL example:  /api/v1/characters
    all_characters = CharactersDBHelper.get_all_characters(
        user_id=user_id,
        with_clothes=True
    )
    return jsoning(CharactersWithClothesSerializer.serialize(all_characters))


@characters_bp.route('<int:character_id>', methods=['GET'])
def get_character(character_id):
    # URL example:  /api/v1/characters/15
    try:
        character = CharactersDBHelper.get_character_by_id(
            character_id=character_id,
            with_clothes=True
        )
    except ObjectNotFoundException as e:
        return jsoning({'message': str(e)}), 404

    return jsoning(CharactersWithClothesSerializer.serialize(character))


@characters_bp.route('favorites', methods=['GET'])
@authorized_required
def get_favorite_characters(user_id: int):
    # URL example:  /api/v1/characters/favorites
    try:
        characters = CharactersDBHelper.get_favorites(
            user_id=user_id,
            with_clothes=True
        )
    except ObjectNotFoundException as e:
        return jsoning({'message': str(e)}), 404

    return jsoning(CharactersWithClothesSerializer.serialize(characters))


@characters_bp.route('filter', methods=['GET'])
@authorized_optional
def get_filtered_characters(user_id: Optional[int] = None):
    # URL example:  /api/v1/characters/filter?type=newness&limit=10
    filter_type = request.args.get('type')
    filter_limit = request.args.get('limit')

    if filter_type == 'newness':
        if filter_limit:
            try:
                filter_limit = int(filter_limit)
            except ValueError:
                return jsoning(
                    {'message': 'Argument \'filter_limit\' must be integer!'}
                ), 400

            filtered_characters = CharactersDBHelper.get_newest_characters(
                user_id=user_id,
                limit=filter_limit,
                with_clothes=True
            )
        else:
            filtered_characters = CharactersDBHelper.get_newest_characters(
                user_id=user_id,
                with_clothes=True
            )

        return jsoning(
            CharactersWithClothesSerializer.serialize(filtered_characters)
        )

    return jsoning({'message': 'Filter type not allowed!'})


@characters_bp.route('find', methods=['GET'])
@authorized_optional
def find_characters_by_clothes(user_id: Optional[int] = None):
    # URL example:  /api/v1/characters/find?clothes=[2,9]
    clothes_list = request.args.get('clothes')

    if clothes_list:
        try:
            clothes_ids = get_ids_from_string(clothes_list)
        except ValueError:
            return jsoning({
                'message':
                    'Argument \'clothes\' must be array of integers!'
            }), 400

        try:
            if config.REDIS_CACHING:
                cache_key = format_cache_key(clothes_ids)
                cache_value = redis_client.get(cache_key)
                if cache_value:
                    response_text = cache_value.decode('utf-8')
                    return response_text, 200, {
                        'Content-Type': 'application/json'
                    }

            characters = CharactersDBHelper.get_characters_by_clothes(
                clothes_ids=clothes_ids,
                user_id=user_id,
                with_clothes=True
            )
        except ObjectNotFoundException as e:
            return jsoning({'message': str(e)}), 404

        serialized = CharactersWithClothesSerializer.serialize(characters)

        if config.REDIS_CACHING:
            new_cache_value = flask_json.dumps(serialized)
            redis_client.set(
                name=cache_key,
                value=new_cache_value,
                ex=config.REDIS_CACHE_EXPIRE
            )

        return jsoning(serialized)

    return jsoning({
        'message': ('You must add query parameter \'clothes\' with array of '
                    'clothes IDs!')
    })


@characters_bp.route('<int:character_id>/add-to-favorites', methods=['POST'])
@authorized_required
def add_character_to_favorites(character_id: int, user_id: int):
    # URL example:  /api/v1/characters/17/add-to-favorites
    try:
        CharactersDBHelper.add_to_favorites(
            character_id=character_id,
            user_id=user_id
        )
    except ObjectNotFoundException as e:
        return jsoning({'message': str(e)}), 404
    except CharacterAlreadyInFavorites as e:
        return jsoning({'message': str(e)}), 400

    return jsoning({'message': 'Character added to favorites'})


@characters_bp.route(
    '<int:character_id>/remove-from-favorites',
    methods=['POST']
)
@authorized_required
def remove_character_from_favorites(character_id: int, user_id: int):
    # URL example:  /api/v1/characters/17/remove-from-favorites
    try:
        CharactersDBHelper.remove_from_favorites(
            character_id=character_id,
            user_id=user_id
        )
    except ObjectNotFoundException as e:
        return jsoning({'message': str(e)}), 404

    return jsoning({'message': 'Character removed from favorites'})
