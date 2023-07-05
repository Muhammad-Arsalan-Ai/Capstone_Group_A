import unittest
from unittest import mock
from unittest.mock import patch

from src.matching_service.main import get_councillors, get_specific_councillors


class TestGetCouncillors(unittest.TestCase):
    def test_matching_councillors_success(self):
        # Mock the matching_councillors function to return a predefined result
        with mock.patch(
            "src.matching_service.main.matching_councillors"
        ) as mock_matching_councillors:
            mock_matching_councillors.return_value = ["Councillor A", "Councillor B"]

            # Call the get_councillors function with a test report_id
            result = get_councillors(123)

            # Assert that the result matches the expected value
            self.assertEqual(result, ["Councillor A", "Councillor B"])

    def test_matching_councillors_error(self):
        # Mock the matching_councillors function to raise an exception
        with mock.patch(
            "src.matching_service.main.matching_councillors"
        ) as mock_matching_councillors:
            mock_matching_councillors.side_effect = Exception("An error occurred")

            # Call the get_councillors function with a test report_id
            with self.assertRaises(Exception):
                get_councillors(123)

    def test_matching_councillors_return(self):
        # Mock the matching_councillors function to return a specific result
        with mock.patch(
            "src.matching_service.main.matching_councillors"
        ) as mock_matching_councillors:
            mock_matching_councillors.return_value = ["Councillor X", "Councillor Y"]

            # Call the get_councillors function with a test report_id
            result = get_councillors(123)

            # Assert that the result matches the expected value
            self.assertEqual(result, ["Councillor X", "Councillor Y"])

    @patch("src.matching_service.main.matching_councillors")
    def test_successful_result(self, mock_matching_councillors):
        # Mock the return value of matching_councillors
        mock_matching_councillors.return_value = [
            {"name": "John"},
            {"name": "Jane"},
            {"name": "Alice"},
        ]

        # Call the function under test
        result = get_specific_councillors(123, 3)

        # Assertions
        self.assertEqual(
            result, [{"name": "John"}, {"name": "Jane"}, {"name": "Alice"}]
        )
        mock_matching_councillors.assert_called_once_with(123, 3)

    @patch("src.matching_service.main.matching_councillors")
    def test_error_occurred(self, mock_matching_councillors):
        # Mock an exception being raised in matching_councillors
        mock_matching_councillors.side_effect = Exception("An error occurred")

        # Call the function under test using a try-except block
        try:
            # result = get_specific_councillors(123, 3)
            self.fail("Exception not raised")
        except Exception as e:
            self.assertEqual(str(e), "An error occurred")

        mock_matching_councillors.assert_called_once_with(123, 3)

    @patch("src.matching_service.main.matching_councillors")
    def test_successful_result_details(self, mock_matching_councillors):
        # Mock the return value of matching_councillors
        mock_matching_councillors.return_value = [
            {"name": "John"},
            {"name": "Jane"},
            {"name": "Alice"},
        ]

        # Call the function under test
        result = get_specific_councillors(123, 3)

        # Assertions
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "John")
        self.assertEqual(result[1]["name"], "Jane")
        self.assertEqual(result[2]["name"], "Alice")
        mock_matching_councillors.assert_called_once_with(123, 3)


if __name__ == "__main__":
    unittest.main()
