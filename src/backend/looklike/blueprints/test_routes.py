from flask import Blueprint, request, jsonify


test_bp = Blueprint('testBP', __name__, url_prefix='/test/')


@test_bp.route('', methods=['POST'])
def get_test_route():
    """Returns message"""
    print(request.data)
    print('JSON?: ', request.is_json)
    print(request.get_json())
    return jsonify({'message': "test"})
