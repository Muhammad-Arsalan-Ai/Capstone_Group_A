import requests  # type: ignore
from fastapi import FastAPI
from match import get_10_records

app = FastAPI()


@app.get("/{id}")
def get_category(id: int):
    """
    A FastAPI application that retrieves data from an external API and passes the category to the `get_10_records()` function.

    Endpoints:
    - GET "/{id}": Retrieves the category from an external API based on the provided ID and passes it to the `get_10_records()` function.

    Parameters:
    - id (int): The ID used to fetch data from the external API.

    Returns:
    - list: A list of dictionaries representing the first 10 records for the retrieved category.

    Note:
    - The `get_10_records()` function assumes a Redis connection is established using the `get_redis_client()` function from the `redis_connector` module.
    - The Redis data for the category should be a JSON-encoded list of dictionaries.
    - If the Redis value is in bytes format, it will be decoded into a string before parsing as JSON.
    - If any JSON parsing error occurs, the `get_10_records()` function may raise a `json.JSONDecodeError`.
    - If fewer than 10 records are available in the Redis data, the function will return all available records.
    """

    url = f"https://xloop-dummy.herokuapp.com/report/{id}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # return data['category']
        return get_10_records(data["category"])

    else:
        return f"Error: {response.status_code} - {response.text}"
