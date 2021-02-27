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

    # URL example:  /api/v1/characters?by_clothes=[2,9]
    by_clothes = request.args.get('by_clothes')
    if by_clothes:
        try:
            clothes_ids = get_ids_from_string(by_clothes)
        except ValueError:
            return jsonify({
                'message': 
                    'Argument \'by_clothes\' must be array of integers!'
            }), 400

        try:
            characters = DBHelper.get_characters_by_clothes(clothes_ids)
        except ObjectNotFoundException as e:
            return jsonify({'message': str(e)}), 404
            
        return jsonify(CharactersSerializer.serialize(characters))

    # URL example:  /api/v1/characters
    all_characters = DBHelper.get_all_characters()
    return jsonify(CharactersSerializer.serialize(all_characters))
