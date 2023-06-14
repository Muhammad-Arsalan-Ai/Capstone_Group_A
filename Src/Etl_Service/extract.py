import requests
from pyspark.sql import SparkSession

def fetch_data_from_apis(api_url):

    response = requests.get(api_url)
    
    if response.status_code==200:
        return response.json()
    else:
        raise Exception('API request failed with status code:',response.status_code)

# Define the API URLs with names
api_urls = {
    "appointment_api": "https://xloop-dummy.herokuapp.com/appointment",
    "councillor_api": "https://xloop-dummy.herokuapp.com/councillor",
    "patient_councillor_api": "https://xloop-dummy.herokuapp.com/patient_councillor",
    "rating_api": "https://xloop-dummy.herokuapp.com/rating"
}