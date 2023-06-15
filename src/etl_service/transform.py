from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from extract import fetch_all_data,api_urls


def join():
    appointment_df, councillor_df, patient_councillor_df, rating_df = fetch_all_data()

    joined_df = appointment_df.join(patient_councillor_df, appointment_df["patient_id"] == patient_councillor_df["patient_id"]) \
        .join(rating_df, appointment_df["id"] == rating_df["appointment_id"]) \
        .join(councillor_df, councillor_df["id"] == patient_councillor_df["councillor_id"]) \
        .select(appointment_df["patient_id"], councillor_df["id"].alias("councillor_id"), councillor_df["specialization"], rating_df["value"])

    return joined_df

def calculate_average():
    joined_df = join()
    
    
    # Group by specialization and calculate the average rating
    average_df = joined_df.groupBy("specialization") \
        .agg(F.collect_set("councillor_id").alias("councillor_ids"),
             F.collect_list("value").alias("average_value")) \
        .withColumn("average_value", F.expr("transform(average_value, x -> CAST(x AS FLOAT))")) \
        .withColumn("average_value", F.sort_array("average_value", asc=False)) \
        .orderBy("specialization")
            
    return average_df
