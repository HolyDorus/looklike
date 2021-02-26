from flask import Blueprint, request, jsonify

from looklike.db_helper import DBHelper
from looklike.serializers import ClothesSerializer
from looklike.models import Clothes


clothes_bp = Blueprint('clothes_bp', __name__, url_prefix='/api/v1/')


@clothes_bp.route('clothes/', methods=['GET'])
def get_clothes():
    # URL example:  /api/v1/clothes?primary_only
    if 'primary_only' in request.args:
        primary_clothes = DBHelper.get_primary_clothes()
        result = ClothesSerializer.serialize_primary_only(primary_clothes)
        return jsonify(result)

    # URL example:  /api/v1/clothes?parent_id=10
    parent_id = request.args.get('parent_id')
    if parent_id:
        if not parent_id.isdigit():
            return jsonify(
                {'message': 'Argument \'parent_id\' must be integer!'}
            ), 400

        clothes_by_parent = DBHelper.get_clothes_by_parent_id(parent_id)
        return jsonify(ClothesSerializer.serialize(clothes_by_parent))

    # URL example:  /api/v1/clothes
    all_clothes = DBHelper.get_all_clothes()
    return jsonify(ClothesSerializer.serialize(all_clothes))
