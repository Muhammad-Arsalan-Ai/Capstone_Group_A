import requests # type: ignore
import json # type: ignore
import os # type: ignore
from redis_connector import get_redis_client
from base_logger import logger
from dotenv import load_dotenv

load_dotenv()

def fetch_report_category(report_id: int):
    
    """
    This function fetches the report category based on the provided report ID by making a GET request to the API.

    Parameters:
    - report_id (int): The ID of the report for which the category is to be fetched.

    Returns:
    - str: The category of the report.

    Usage:
    - Call this function with the desired report ID.
    - The function sends a GET request to the API endpoint, appending the report ID to the URL.
    - If the response status code is 200, the category is extracted from the response JSON and returned.
    - If the response status code is not 200, an error message is logged, and an exception is raised.
    """
    api_url = f"{os.getenv('BASE_URL')}/report/{report_id}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        logger.info('Report category received')
        return data['category']
    else:
        err_msg = f"Error {response.status_code} occurred while accessing {api_url}"
        logger.error(err_msg)
        response.raise_for_status()

def find_top_councillors(report_id: int, num_councillors: int = 10):
    """
    This function retrieves the top councillors based on a report ID and the number of councillors.

    Parameters:
    - report_id (int): The ID of the report for which the top councillors are to be retrieved.
    - num_councillors (int): The number of top councillors to retrieve. Defaults to 10 if not specified.

    Returns:
    - list: A list of the top councillors based on the given report ID and number of councillors.

    Usage:
    - Call this function with the desired report ID and optionally specify the number of councillors.
    - The function internally calls the "fetch_report_category" function to retrieve the report category based on the report ID.
    - The report category is used to retrieve councillor ratings from a Redis client using the "get_redis_client" function.
    - The councillor ratings are parsed and stored in the "councillor_ratings" list.
    - The function selects the top councillors based on the provided number of councillors.
    - The top councillors are returned as the result.
    """
    
    get_category = fetch_report_category(report_id)
    councillor_ratings = json.loads(get_redis_client(get_category).decode())
    top_councillors = [json.loads(item) for item in councillor_ratings[:num_councillors]]
    logger.info("Returning top councillors")
    return top_councillors

if __name__ == "__main__":
    find_top_councillors()