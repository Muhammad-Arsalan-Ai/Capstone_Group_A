import redis  # type: ignore

def get_redis_client():
    """
    Provides a Redis client instance for interacting with a Redis server.

    Functions:
    - get_redis_client(): Returns a Redis client instance connected to the specified Redis server.

    Returns:
    - redis.Redis: A Redis client instance.

    Note:
    - The Redis server connection details (host, port, and database) are hardcoded in the function. Adjust them as needed.
    - This module requires the `redis` package to be installed. Install it using `pip install redis`.
    - To establish a connection with the Redis server, ensure that the Redis server is running and accessible at the specified host and port.

    """
    redis_host = "localhost"
    redis_port = 6379
    redis_db = 0
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    return redis_client


if __name__ == "__main__":
    get_redis_client()