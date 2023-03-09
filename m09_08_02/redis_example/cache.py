import timeit

import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@cache
def fibonacci_cache(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_cache(n - 1) + fibonacci_cache(n - 2)


if __name__ == '__main__':
    start = timeit.default_timer()
    fibonacci(35)
    print(f"Result 35: {timeit.default_timer() - start}")

    start = timeit.default_timer()
    fibonacci_cache(135)
    print(f"Result 135: {timeit.default_timer() - start}")
