import json  # type: ignore

from redis_connector import get_redis_client


def get_10_records(category):
    """
    Retrieve the first 10 records from Redis for a given category.

    Parameters:
    - category (str): The category key used to retrieve the data from Redis.

    Returns:
    - list: A list of dictionaries representing the first 10 records. Each dictionary contains the parsed JSON data from Redis.

    Note:
    - The function assumes the Redis connection is established using the `get_redis_client()` function from the `redis_connector` module.
    - The Redis data for the given category should be a JSON-encoded list of dictionaries.
    - If the Redis value is in bytes format, it will be decoded into a string before parsing as JSON.
    - If any JSON parsing error occurs, the function may raise a `json.JSONDecodeError`.
    - If fewer than 10 records are available in the Redis data, the function will return all available records.

    """

    r = get_redis_client()

    value = r.get(category)

    if isinstance(value, bytes):
        value = value.decode()  # Convert bytes to string

    json_data = json.loads(value)

    formatted_data = []
    for item in json_data[:10]:
        record = json.loads(item)
        formatted_data.append(record)

    return formatted_data
