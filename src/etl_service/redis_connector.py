import redis  # type: ignore


def get_redis_client():
    redis_host = "localhost"
    redis_port = 6379
    redis_db = 0
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    return redis_client


if __name__ == "__main__":
    get_redis_client()
