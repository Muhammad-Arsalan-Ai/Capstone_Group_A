from Apis import fetch_data_from_apis, api_urls
from pyspark.sql import SparkSession

def extract():
    
    data = {}

    for k, v in api_urls.items():
        data[k] = fetch_data_from_apis(v)
        
    spark = SparkSession.builder.getOrCreate()

    df1 = spark.createDataFrame(data["Appointment_API"])
    df2 = spark.createDataFrame(data["Councillor_API"])
    df3 = spark.createDataFrame(data["Patient_Councillor_API"])
    df4 = spark.createDataFrame(data["Rating_API"])

    return df1, df2, df3, df4
    spark.stop()

def fetch_all_data():
    
    df1, df2, df3, df4 = extract()
    return df1, df2, df3, df4

    # Show the dataframes
    df1.show(2)
    df2.show(2)
    df3.show(2)
    df4.show(2)