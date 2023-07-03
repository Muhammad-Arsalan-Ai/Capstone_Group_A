import json  # type: ignore
import os  # type: ignore
import unittest  # type: ignore
from unittest.mock import MagicMock, Mock, patch

import requests  # type: ignore
from matching import get_report_category, matching_councillors


class TestCouncillors(unittest.TestCase):
    @patch("requests.get")
    def test_get_report_category_success(self, mock_get: MagicMock) -> None:
        report_id = 123
        category = "Some Category"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"category": category}
        mock_get.return_value = mock_response

        result = get_report_category(report_id)

        mock_get.assert_called_once_with(f"{os.getenv('BASE_URL')}/report/{report_id}")
        self.assertEqual(result, category)

    @patch("requests.get")
    def test_get_report_category_http_error(self, mock_get: MagicMock) -> None:
        report_id = 123

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        with self.assertRaises(requests.HTTPError):
            get_report_category(report_id)

        mock_get.assert_called_once_with(f"{os.getenv('BASE_URL')}/report/{report_id}")

    @patch("matching.get_report_category")
    @patch("matching.get_redis_client")
    def test_matching_councillors(
        self, mock_get_redis_client: MagicMock, mock_get_report_category: MagicMock
    ) -> None:
        report_id = 123
        number_of_councillors = 5
        report_category = "Some Category"
        councillors_with_ratings = [
            json.dumps({"name": "John", "avr_rating": 4.5}),
            json.dumps({"name": "Jane", "avr_rating": 3.8}),
            json.dumps({"name": "Alice", "avr_rating": 4.2}),
            json.dumps({"name": "Bob", "avr_rating": 4.9}),
            json.dumps({"name": "Eve", "avr_rating": 4.0}),
        ]
        expected_top_councillors = [
            {"name": "John", "avr_rating": 4.5},
            {"name": "Jane", "avr_rating": 3.8},
            {"name": "Alice", "avr_rating": 4.2},
            {"name": "Bob", "avr_rating": 4.9},
            {"name": "Eve", "avr_rating": 4.0},
        ]

        mock_get_report_category.return_value = report_category

        mock_redis_client = Mock()
        mock_redis_client.get.return_value = json.dumps(councillors_with_ratings)
        mock_get_redis_client.return_value = mock_redis_client

        result = matching_councillors(report_id, number_of_councillors)

        mock_get_report_category.assert_called_once_with(report_id)
        mock_get_redis_client.assert_called_once_with()
        mock_redis_client.get.assert_called_once_with(report_category)
        self.assertEqual(result, expected_top_councillors)


if __name__ == "__main__":
    unittest.main()
