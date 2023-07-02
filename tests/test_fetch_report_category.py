import unittest
import mock
import json
from match import get_report_category, matching_councillors

class CouncillorsTestCase(unittest.TestCase):
    def test_get_report_category(self):
        report_id = 1
        expected_result = "transport"
        with mock.patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "category": expected_result
            }
            actual_result = get_report_category(report_id)
            assert actual_result == expected_result

    def test_matching_councillors(self):
        report_id = 1
        number_of_councillors = 2
        expected_result = [
            {
                "id": 1,
                "name": "John Smith",
                "avr_rating": 4.5,
            },
            {
                "id": 2,
                "name": "Jane Doe",
                "avr_rating": 3.5,
            },
        ]
        with mock.patch("councillors.get_report_category") as mock_get_report_category:
            mock_get_report_category.return_value = "transport"
            with mock.patch("redis.Redis.get") as mock_get:
                mock_get.return_value = (
                    b"["
                    + json.dumps(expected_result).encode()
                    + b"]"
                )
                actual_result = matching_councillors(report_id, number_of_councillors)
                assert actual_result == expected_result


if __name__ == "__main__":
    unittest.main()