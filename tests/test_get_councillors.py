import unittest
from unittest.mock import patch
from fast_api import get_councillors, get_specific_councillors


class TestGetCouncillors(unittest.TestCase):

    @patch("match.matching_councillors")
    def test_get_councillors(self, mock_matching_councillors):
        report_id = 123
        expected_result = [
            {
                "name": "Councillor 1",
                "avr_rating": 4.5
            },
            {
                "name": "Councillor 2",
                "avr_rating": 4.2
            },
            # Add more expected results as needed
        ]

        mock_matching_councillors.return_value = expected_result

        result = get_councillors(report_id)
        self.assertEqual(result, expected_result)
        mock_matching_councillors.assert_called_once_with(report_id)

    @patch("match.matching_councillors")
    def test_get_specific_councillors(self, mock_matching_councillors):
        report_id = 123
        number_of_councillors = 5
        expected_result = [
            {
                "name": "Councillor 1",
                "avr_rating": 4.5
            },
            {
                "name": "Councillor 2",
                "avr_rating": 4.2
            },
            # Add more expected results as needed
        ]

        mock_matching_councillors.return_value = expected_result

        result = get_specific_councillors(report_id, number_of_councillors)
        self.assertEqual(result, expected_result)
        mock_matching_councillors.assert_called_once_with(report_id, number_of_councillors)


if __name__ == "__main__":
    unittest.main()