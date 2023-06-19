from extract import get_api_data, urls
from pyspark.sql import functions as F


def join():
    """
    Performs data joining based on appointment, councillor, patient-councillor, and rating dataframes.

    Returns a joined dataframe containing patient ID, councillor ID, councillor specialization, and rating value.

    Preconditions:
    - The `get_api_data()` function should be implemented and accessible to retrieve the required dataframes.
    - The `urls` dictionary should contain the appropriate URLs for fetching the dataframes.

    Parameters:
    - Returns a dataframe with the following columns:
        - 'patient_id': The ID of the patient associated with the appointment.
        - 'councillor_id': The ID of the councillor associated with the appointment.
        - 'specialization': The specialization of the councillor.
        - 'value': The rating value associated with the appointment.

    """
    appointment_df = get_api_data(urls["appointment"])
    councillor_df = get_api_data(urls["councillor"])
    patient_councillor_df = get_api_data(urls["patient_councillor"])
    rating_df = get_api_data(urls["rating"])

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
            appointment_df["patient_id"],
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
    - The join() function should be called prior to invoking this function to obtain the joined dataframe.

    Parameters:
    - Returns a dictionary of DataFrame tables with the following columns:
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
        )

        average_df = average_df.drop("specialization")

        specialization_tables[specialization] = average_df

    return specialization_tables
