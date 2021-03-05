from flask import Blueprint, request, jsonify

from looklike.db_helper import DBHelper
from looklike.exceptions import ObjectNotFoundException
from looklike.serializers import CharactersSerializer
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
            character = DBHelper.get_character_by_id(character_id)
        except ObjectNotFoundException as e:
            return jsonify({'message': str(e)}), 404

        return jsonify(CharactersSerializer.serialize(character))

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
            characters_with_their_clothes = []
            characters = DBHelper.get_characters_by_clothes(clothes_ids)

            for character in characters:
                clothes = DBHelper.get_character_clothes(character)
                characters_with_their_clothes.append({
                    'character': character,
                    'clothes': clothes
                })
        except ObjectNotFoundException as e:
            return jsonify({'message': str(e)}), 404
            
        return jsonify(
            CharactersSerializer.serialize_characters_with_clothes(
                characters_with_their_clothes
            )
        )

    # URL example:  /api/v1/characters
    all_characters = DBHelper.get_all_characters()
    return jsonify(CharactersSerializer.serialize(all_characters))
