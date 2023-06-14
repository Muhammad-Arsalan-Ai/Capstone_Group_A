#requests library is necessary for making HTTP requests
import requests

def fetch_data_from_apis(api_url):
    
    #Function to fetch data from the specified API URL
    response = requests.get(api_url)
    
    if response.status_code==200:
        return response.json() # Return JSON data for successful API request
    else:
        # Raise an exception with an informative error message
        raise Exception('API request failed with status code:',response.status_code)

# Define the API URLs with names
api_urls = {
    "appointment_api": "https://xloop-dummy.herokuapp.com/appointment",
    "councillor_api": "https://xloop-dummy.herokuapp.com/councillor",
    "patient_councillor_api": "https://xloop-dummy.herokuapp.com/patient_councillor",
    "rating_api": "https://xloop-dummy.herokuapp.com/rating"
}