from flask import Blueprint, request, jsonify

from looklike.db_helper import DBHelper
from looklike.exceptions import ObjectNotFoundException
from looklike.serializers import CharactersWithClothesSerializer
from looklike.utils import get_ids_from_string


url_prefix = '/api/v1/characters/'
characters_bp = Blueprint('characters_bp', __name__, url_prefix=url_prefix)


@characters_bp.route('', methods=['GET'])
def get_characters():
    # URL example:  /api/v1/characters?id=7
    character_id = request.args.get('id')
    if character_id:
        try:
            character_id = int(character_id)
        except ValueError:
            return jsonify(
                {'message': 'Argument \'character_id\' must be integer!'}
            ), 400

        try:
            character = DBHelper.get_character_by_id(
                character_id,
                with_clothes=True
                )
        except ObjectNotFoundException as e:
            return jsonify({'message': str(e)}), 404

        return jsonify(CharactersWithClothesSerializer.serialize(character))

    # URL example:  /api/v1/characters?filter=newness&limit=10
    filter_type = request.args.get('filter')
    filter_limit = request.args.get('limit')

    if filter_type == 'newness':
        if filter_limit:
            try:
                filter_limit = int(filter_limit)
            except ValueError:
                return jsonify(
                    {'message': 'Argument \'filter_limit\' must be integer!'}
                ), 400

            filtered_characters = DBHelper.get_newest_characters(
                limit=filter_limit,
                with_clothes=True
            )
        else:
            filtered_characters = DBHelper.get_newest_characters(
                with_clothes=True
            )

        return jsonify(
            CharactersWithClothesSerializer.serialize(filtered_characters)
        )

    # URL example:  /api/v1/characters?clothes=[2,9]
    clothes_list = request.args.get('clothes')
    if clothes_list:
        try:
            clothes_ids = get_ids_from_string(clothes_list)
        except ValueError:
            return jsonify({
                'message':
                    'Argument \'clothes\' must be array of integers!'
            }), 400

        try:
            characters = DBHelper.get_characters_by_clothes(
                clothes_ids=clothes_ids,
                with_clothes=True
            )
        except ObjectNotFoundException as e:
            return jsonify({'message': str(e)}), 404

        return jsonify(CharactersWithClothesSerializer.serialize(characters))

    # URL example:  /api/v1/characters
    all_characters = DBHelper.get_all_characters(with_clothes=True)
    return jsonify(CharactersWithClothesSerializer.serialize(all_characters))
