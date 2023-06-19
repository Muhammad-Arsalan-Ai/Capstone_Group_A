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
    Calculates the average rating for each specialization based on the joined dataframe.

    Returns a dataframe containing the specialization, a list of councillor IDs, and the average ratings.

    Preconditions:
    - The `join()` function should be called prior to invoking this function to obtain the joined dataframe.

    Postconditions:
    - Returns a dataframe with the following columns:
        - 'specialization': The specialization of the councillors.
        - 'councillor_ids': A list of councillor IDs associated with the specialization.
        - 'average_value': A list of average ratings per specialization.


    """
    joined_df = join()

    # Group by specialization and calculate the average rating
    average_df = (
        joined_df.groupBy("specialization")
        .agg(
            F.collect_set("councillor_id").alias("councillor_ids"),
            F.collect_list("value").alias("average_value"),
        )
        .withColumn(
            "average_value", F.expr("transform(average_value, x -> CAST(x AS FLOAT))")
        )
        .withColumn("average_value", F.sort_array("average_value", asc=False))
        .orderBy("specialization")
    )

    return average_df
