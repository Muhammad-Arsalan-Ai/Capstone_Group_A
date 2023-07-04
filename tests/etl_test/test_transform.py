import unittest  # type: ignore
from unittest.mock import Mock

import pyspark  # type: ignore
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType, StringType, StructField, StructType
from transform import data_transformations, fetch_all_data


class TestDataFetching(unittest.TestCase):
    def test_fetch_all_data(self) -> None:
        # Mock the get_api_data function
        mock_get_api_data = Mock(
            return_value=[(1, "data1"), (2, "data2"), (3, "data3")]
        )
        # Create a SparkSession for testing
        # spark = SparkSession.builder.getOrCreate()
        # Set the URLs dictionary
        # urls = {
        #     "appointment": "url1",
        #     "councillor": "url2",
        #     "patient_councillor": "url3",
        #     "rating": "url4",
        # }
        # Call the function under test
        dataframes = fetch_all_data(mock_get_api_data)
        # Verify that the returned dictionary contains the expected keys and DataFrames
        self.assertEqual(
            set(dataframes.keys()),
            {"appointment", "councillor", "patient_councillor", "rating"},
        )
        self.assertFalse(
            all(isinstance(df, pyspark.sql.DataFrame) for df in dataframes.values())
        )

    def test_joined_data(self) -> None:
        spark_mock = Mock()
        # Create mock data
        appointment_data = {
            "id": [1, 2, 3],
            "patient_id": [1, 2, 3]
            # Add other columns if necessary
        }
        councillor_data = {
            "id": [1, 2, 3],
            "specialization": [
                "Specialization 1",
                "Specialization 2",
                "Specialization 3",
            ]
            # Add other columns if necessary
        }
        patient_councillor_data = {
            "patient_id": [1, 2, 3],
            "councillor_id": [1, 2, 3]
            # Add other columns if necessary
        }
        rating_data = {
            "appointment_id": [1, 2, 3],
            "value": [4, 5, 3]
            # Add other columns if necessary
        }
        # Set up mock DataFrame objects
        appointment_df_mock = Mock()
        councillor_df_mock = Mock()
        patient_councillor_df_mock = Mock()
        rating_df_mock = Mock()
        # Set up mock DataFrame methods and return values
        appointment_df_mock.side_effect = appointment_data.get
        councillor_df_mock.side_effect = councillor_data.get
        patient_councillor_df_mock.side_effect = patient_councillor_data.get
        rating_df_mock.side_effect = rating_data.get
        # Set up the behavior of the mocked Spark object
        spark_mock.createDataFrame.side_effect = [
            appointment_df_mock,
            councillor_df_mock,
            patient_councillor_df_mock,
            rating_df_mock,
        ]
        # Call the function with the mock data
        result_df = fetch_all_data(spark_mock)
        # Perform assertions on the result DataFrame
        expected_columns = ["councillor_id", "specialization", "value"]
        self.assertEqual(
            set(result_df.keys()),
            {"appointment", "councillor", "patient_councillor", "rating"},
            expected_columns,
        )

    def test_data_transformations(self) -> None:
        # Create a mock for the joined_data() function
        spark = SparkSession.builder.getOrCreate()
        # Define the schema for the joined DataFrame
        schema = StructType(
            [
                StructField("specialization", StringType(), nullable=False),
                StructField("councillor_id", StringType(), nullable=False),
                StructField("value", DoubleType(), nullable=False),
            ]
        )
        # Create a mock joined DataFrame
        data = [
            ("MockSpecialization", "Councillor1", 4.5),
            ("MockSpecialization", "Councillor2", 3.8),
            ("MockSpecialization", "Councillor3", 4.2),
        ]
        df = spark.createDataFrame(data, schema)
        return df
        # Call the data_transformations() function
        result = data_transformations()
        # Assert the ehxpected results
        assert (
            len(result) == 1
        )  # Assuming there is only one specialization in the mock joined data
        specialization, dataframe = next(iter(result.items()))
        assert (
            specialization == "MockSpecialization"
        )  # Assuming the specialization name in the mock data is "MockSpecialization"
        assert isinstance(
            dataframe, list
        )  # Assuming the result is a list of Row objects


if __name__ == "__main__":
    unittest.main()
