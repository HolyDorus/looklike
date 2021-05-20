from flask import Blueprint, jsonify

from looklike.db_helper import ClothesDBHelper
from looklike.serializers import ClothesSerializer


url_prefix = '/api/v1/clothes/'
clothes_bp = Blueprint('clothes_bp', __name__, url_prefix=url_prefix)


@clothes_bp.route('', methods=['GET'])
def get_clothes():
    # URL example:  /api/v1/clothes
    all_clothes = ClothesDBHelper.get_all_clothes()
    return jsonify(ClothesSerializer.serialize(all_clothes))


@clothes_bp.route('primary', methods=['GET'])
def get_primary_clothes_only():
    # URL example:  /api/v1/clothes/primary
    primary_clothes = ClothesDBHelper.get_primary_clothes()
    return jsonify(ClothesSerializer.serialize_primary_only(primary_clothes))


@clothes_bp.route('by-parent-id/<int:parent_id>', methods=['GET'])
def get_clothes_by_parent_id(parent_id: int):
    # URL example:  /api/v1/clothes/by-parent-id/10
    clothes_by_parent = ClothesDBHelper.get_clothes_by_parent_id(parent_id)
    return jsonify(ClothesSerializer.serialize(clothes_by_parent))
