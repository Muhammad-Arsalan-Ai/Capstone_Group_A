import unittest  # type: ignore
from unittest.mock import MagicMock, patch

from extract import get_api_data
from requests import HTTPError  # type: ignore


class TestGetApiData(unittest.TestCase):
    @patch("extract.requests.get")
    def test_get_api_data_success(self, mock_get: MagicMock) -> None:
        url = "https://example.com/api"
        expected_data = {"key": "value"}

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = expected_data
        mock_get.return_value = mock_response

        result = get_api_data(url)

        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with(url)
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_called_once()

    @patch("extract.requests.get")
    def test_get_api_data_http_error(self, mock_get: MagicMock) -> None:
        url = "https://xloop-dummy.herokuapp.com"

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_response.status_code = 404  # Set the status code manually
        mock_get.return_value = mock_response

        with self.assertRaises(HTTPError) as cm:
            get_api_data(url)

        self.assertEqual(str(cm.exception), "404 Not Found")
        mock_get.assert_called_once_with(url)
        mock_response.raise_for_status.assert_called_once()
        mock_response.json.assert_not_called()


if __name__ == "__main__":
    unittest.main()
