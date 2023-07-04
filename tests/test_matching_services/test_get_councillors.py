import unittest  # type: ignore
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from src.matching_service.main import app


class TestCouncillorsAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    @patch("src.matching_service.main.matching_councillors")
    def test_get_councillors(self, mock_matching_councillors: MagicMock) -> None:
        report_id = 123

        # Mock the matching_councillors function
        mock_matching_councillors.return_value = [{"name": "John", "avr_rating": 4.5}]

        response = self.client.get(f"/councillors/{report_id}/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [{"name": "John", "avr_rating": 4.5}])

        mock_matching_councillors.assert_called_once_with(report_id)

    @patch("src.matching_service.main.matching_councillors")
    def test_get_specific_councillors(
        self, mock_matching_councillors: MagicMock
    ) -> None:
        report_id = 123
        number_of_councillors = 5

        # Mock the matching_councillors function
        mock_matching_councillors.return_value = [
            {"name": "John", "avr_rating": 4.5},
            {"name": "Jane", "avr_rating": 3.8},
            {"name": "Alice", "avr_rating": 4.2},
            {"name": "Bob", "avr_rating": 4.9},
            {"name": "Eve", "avr_rating": 4.0},
        ]

        response = self.client.get(f"/councillors/{report_id}/{number_of_councillors}")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), number_of_councillors)

        mock_matching_councillors.assert_called_once_with(
            report_id, number_of_councillors
        )

    @patch("src.matching_service.main.matching_councillors")
    def test_get_specific_councillors_default_number(
        self, mock_matching_councillors: MagicMock
    ) -> None:
        report_id = 123

        # Mock the matching_councillors function
        mock_matching_councillors.return_value = [
            {"name": "John", "avr_rating": 4.5},
            {"name": "Jane", "avr_rating": 3.8},
            {"name": "Alice", "avr_rating": 4.2},
        ]

        response = self.client.get(f"/councillors/{report_id}/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)  # Default number of councillors is 3

        mock_matching_councillors.assert_called_once_with(report_id)


if __name__ == "__main__":
    unittest.main()
