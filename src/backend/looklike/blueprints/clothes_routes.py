from flask import Blueprint, request, jsonify

from looklike.db_helper import ClothesDBHelper
from looklike.serializers import ClothesSerializer


url_prefix = '/api/v1/clothes/'
clothes_bp = Blueprint('clothes_bp', __name__, url_prefix=url_prefix)


@clothes_bp.route('', methods=['GET'])
def get_clothes():
    # URL example:  /api/v1/clothes?primary_only
    if 'primary_only' in request.args:
        primary_clothes = ClothesDBHelper.get_primary_clothes()
        result = ClothesSerializer.serialize_primary_only(primary_clothes)
        return jsonify(result)

    # URL example:  /api/v1/clothes?parent_id=10
    parent_id = request.args.get('parent_id')
    if parent_id:
        try:
            parent_id = int(parent_id)
        except ValueError:
            return jsonify(
                {'message': 'Argument \'parent_id\' must be integer!'}
            ), 400

        clothes_by_parent = ClothesDBHelper.get_clothes_by_parent_id(parent_id)
        return jsonify(ClothesSerializer.serialize(clothes_by_parent))

    # URL example:  /api/v1/clothes
    all_clothes = ClothesDBHelper.get_all_clothes()
    return jsonify(ClothesSerializer.serialize(all_clothes))
