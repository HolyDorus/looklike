from datetime import datetime

import pytest

from looklike import create_app
from looklike.utils import (
    datetime_to_timestamp,
    get_ids_from_string,
    raw_json_to_response
)


class TestDatetimeToTimestamp:
    def test_valid_data(self) -> None:
        dt = datetime(2021, 5, 19, 18, 35, 10, 4)
        assert datetime_to_timestamp(dt) == 1621438510


class TestGetIdsFromString:
    @pytest.mark.parametrize('data,expected', [
        ('[1,2,3]', [1, 2, 3]),
        ('[1,5,0', [1, 5, 0]),
        ('2,7]', [2, 7]),
        ('-5,3', [-5, 3]),
        ('4', [4])
    ])
    def test_valid_strings(self, data: str, expected: list[int]) -> None:
        assert get_ids_from_string(data) == expected

    def test_empty_string(self) -> None:
        pytest.raises(ValueError, get_ids_from_string, '')

    def test_character(self) -> None:
        pytest.raises(ValueError, get_ids_from_string, 'a')


class TestRawJsonToResponse:
    def test_valid_data(self):
        app = create_app()

        with app.app_context():
            input_data = '[1, 2, 3]'
            response = raw_json_to_response(input_data)

            assert response.mimetype == app.config["JSONIFY_MIMETYPE"]
            assert response.data == input_data.encode()
            assert response.get_json() == [1, 2, 3]
