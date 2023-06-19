from extract import get_api_data, urls
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def fetch_all_data():
    """
    Fetches data from the specified API URLs and returns the corresponding dataframes.

    Returns:
    - appointment_df: DataFrame containing appointment data.
    - councillor_df: DataFrame containing councillor data.
    - patient_councillor_df: DataFrame containing patient-councillor relationship data.
    - rating_df: DataFrame containing rating data.

    Preconditions:
    - The get_api_data() function should be implemented to fetch data from the API URLs.
    - The urls dictionary should contain the appropriate API URLs.

    """
    data = {}

    for k, v in urls.items():
        data[k] = get_api_data(v)

    spark = SparkSession.builder.getOrCreate()

    appointment_df = spark.createDataFrame(data["appointment"])
    councillor_df = spark.createDataFrame(data["councillor"])
    patient_councillor_df = spark.createDataFrame(data["patient_councillor"])
    rating_df = spark.createDataFrame(data["rating"])

    return appointment_df, councillor_df, patient_councillor_df, rating_df


def join():
    """
    Performs data joining based on appointment, councillor, patient-councillor, and rating dataframes.

    Returns a joined dataframe containing patient ID, councillor ID, councillor specialization, and rating value.

    Preconditions:
    - The `fetch_all_data()` function should be implemented and accessible to retrieve the required dataframes.

    Returns:
    - A dataframe with the following columns:
        - 'councillor_id': The ID of the councillor associated with the appointment.
        - 'specialization': The specialization of the councillor.
        - 'value': The rating value associated with the appointment.
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


def calculate_average():
    """
    Calculates the average rating for each councillor in each specialization based on the joined dataframe.

    Returns a dictionary of DataFrame tables, where each table represents the average rating for each councillor
    within a specialization. The tables are indexed by the specialization name.

    Preconditions:
    - The `join()` function should be called prior to invoking this function to obtain the joined dataframe.

    Returns:
    - A dictionary of DataFrame tables with the following columns:
        - 'councillor_id': The ID of the councillor.
        - 'average_value': The average rating for the councillor within the specialization.
    """

    joined_df = join()

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

    return specialization_tables


if __name__ == "__main__":
    specialization_tables = calculate_average()

    for specialization in specialization_tables:
        df = specialization_tables[specialization]
        print(f"Specialization: {specialization}")
        df.show()
