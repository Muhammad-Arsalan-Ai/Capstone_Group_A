import unittest  # type: ignore
from unittest.mock import Mock, patch

from src.etl_service.load import load_data_to_redis


class TestLoadDataToRedis(unittest.TestCase):
    def test_load_data_to_redis(self) -> None:
        # Mock the required dependencies
        redis_client_mock = Mock()
        specializations_dfs_mock = {
            "specialization1": {"key1": "value1"},
            "specialization2": {"key2": "value2"},
        }
        # Patch the necessary functions for mocking
        with patch(
            "src.etl_service.load.get_redis_client", return_value=redis_client_mock
        ), patch(
            "src.etl_service.transform.data_transformations",
            return_value=specializations_dfs_mock,
        ):
            # Call the function to be tested
            result = load_data_to_redis(redis_client_mock, specializations_dfs_mock)
            # Assertions
            redis_client_mock.set.assert_called()
            self.assertEqual(result, specializations_dfs_mock)


if __name__ == "__main__":
    unittest.main()
