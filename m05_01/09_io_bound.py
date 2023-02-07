import asyncio
from concurrent.futures import ThreadPoolExecutor
from time import time

import requests
from requests.exceptions import RequestException, MissingSchema

from libs import async_timed

urls = ['http://www.google.com', 'http://www.python.org', 'http://duckduckgo.com', 'http://www.google.com',
        'http://www.python.org', 'http://duckduckgo.com', 'http://www.google.com', 'http://www.python.org',
        'http://duckduckgo.com', 'http://www.google.com', 'http://www.python.org', 'http://duckduckgo.com',
        'cat_dog']


def get_data_from_url(url) -> (str, str):
    r = requests.get(url)
    return url, r.text[:100]


@async_timed()
async def async_worker():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(3) as pool:
        futures = [loop.run_in_executor(pool, get_data_from_url, url) for url in urls]
        result = await asyncio.gather(*futures, return_exceptions=True)
        return result


if __name__ == '__main__':
    start = time()
    results = []
    for url in urls:
        try:
            results.append(get_data_from_url(url))
        except (RequestException, MissingSchema) as err:
            print(err)
    print(results)
    print(time() - start)

    r = asyncio.run(async_worker())
    print(r)

