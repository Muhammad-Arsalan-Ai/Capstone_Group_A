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

# Define the API URLs with names
api_urls = {
    "appointment_api": "https://xloop-dummy.herokuapp.com/appointment",
    "councillor_api": "https://xloop-dummy.herokuapp.com/councillor",
    "patient_councillor_api": "https://xloop-dummy.herokuapp.com/patient_councillor",
    "rating_api": "https://xloop-dummy.herokuapp.com/rating"
}