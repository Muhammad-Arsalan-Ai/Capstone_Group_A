from extract import get_api_data, urls
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import json
from base_logger import logger

def fetch_all_data():
    """
    Fetches data from the specified API URLs and returns the corresponding Spark DataFrames.

    Returns:
    - appointment_df: DataFrame
        DataFrame containing appointment data.
    - councillor_df: DataFrame
        DataFrame containing councillor data.
    - patient_councillor_df: DataFrame
        DataFrame containing patient-councillor relationship data.
    - rating_df: DataFrame
        DataFrame containing rating data.

    Preconditions:
    - The `get_api_data()` function should be implemented to fetch data from the API URLs.
    - The `urls` dictionary should contain the appropriate API URLs.

    Returns:
    - Tuple of DataFrames:
        The appointment, councillor, patient-councillor, and rating DataFrames retrieved from the API URLs.
    """
    spark = SparkSession.builder.getOrCreate()

    dataframes = {}
    for key, url in urls.items():
        data = get_api_data(url)
        dataframes[key] = spark.createDataFrame(data)

    spark.stop()
    logger.info("Data received from endpoints")
    return dataframes['appointment'], dataframes['councillor'], dataframes['patient_councillor'], dataframes['rating']


def joined_data():
    """
    Performs data joining based on appointment, councillor, patient-councillor, and rating DataFrames.

    Returns:
    - joined_df: DataFrame
        Joined DataFrame containing the following columns:
        - 'councillor_id': The ID of the councillor associated with the appointment.
        - 'specialization': The specialization of the councillor.
        - 'value': The rating value associated with the appointment.

    Preconditions:
    - The `fetch_all_data()` function should be implemented and accessible to retrieve the required DataFrames.

    Returns:
    - DataFrame:
        The joined DataFrame containing the desired columns.
    """

    appointment_df, councillor_df, patient_councillor_df, rating_df = fetch_all_data()

    joined_df = (
        appointment_df.join(
            patient_councillor_df,
            appointment_df["patient_id"] == patient_councillor_df["patient_id"],
        )
        .join(rating_df, appointment_df["id"] == rating_df["appointment_id"])
        .join(
            councillor_df, councillor_df["id"] == patient_councillor_df["councillor_id"]
        )
        .select(
            councillor_df["id"].alias("councillor_id"),
            councillor_df["specialization"],
            rating_df["value"],
        )
    )
    return joined_df

def data_transformations():
    """
    Calculates the average rating for each councillor in each specialization based on the joined DataFrame.

    Returns:
    - json_data: str
        JSON representation of the average rating data. The data is a dictionary where each key represents a specialization,
        and the corresponding value is a list of JSON objects containing the average rating information for each councillor
        within that specialization.

    Preconditions:
    - The `joined_data()` function should be called prior to invoking this function to obtain the joined DataFrame.

    Returns:
    - str:
        JSON representation of the average rating data.
    """

    joined_df = joined_data()

    specializations = joined_df.select("specialization").distinct().collect()

    specialization_tables = {}

    for specialization_row in specializations:
        specialization = specialization_row["specialization"]

        filtered_df = joined_df.filter(joined_df["specialization"] == specialization)

        average_df = (
            filtered_df.groupBy("councillor_id")
            .agg(F.avg("value").alias("average_value"))
            .orderBy(F.desc("average_value"))
            .drop("specialization")
        )

        specialization_tables[specialization] = average_df

    json_data = json.dumps({
        specialization: table.toJSON().collect() for specialization, table in specialization_tables.items()
    })

    logger.info("Data has been transformed")
    return json_data


if __name__ == "__main__":
    data_transformations()
