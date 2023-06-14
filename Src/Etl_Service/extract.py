import requests
from pyspark.sql import SparkSession

def fetch_data_from_apis(api_url):

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None

def extract():
    
    data = {}

    for k, v in api_urls.items():
        data[k] = fetch_data_from_apis(v)
        
    spark = SparkSession.builder.getOrCreate()

    df1 = spark.createDataFrame(data["appointment_api"])
    df2 = spark.createDataFrame(data["councillor_api"])
    df3 = spark.createDataFrame(data["patient_councillor_api"])
    df4 = spark.createDataFrame(data["rating_api"])

    return df1, df2, df3, df4
    spark.stop()

# Define the API URLs with names
api_urls = {
    "appointment_api": "https://xloop-dummy.herokuapp.com/appointment",
    "councillor_api": "https://xloop-dummy.herokuapp.com/councillor",
    "patient_councillor_api": "https://xloop-dummy.herokuapp.com/patient_councillor",
    "rating_api": "https://xloop-dummy.herokuapp.com/rating"
}