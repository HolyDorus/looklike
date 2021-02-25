from flask import Blueprint, request, jsonify

from looklike.database import get_db_cursor


test_bp = Blueprint('testBP', __name__, url_prefix='/test/')


@test_bp.route('', methods=['POST'])
def test_route():
    print('Test route (post)')

    with get_db_cursor() as cursor: 
        cursor.execute("SELECT * FROM all_clothes;") 
        data = cursor.fetchall()

        for item in data:
            print(item['id'], item['name'])

    return jsonify({'message': "test"})
