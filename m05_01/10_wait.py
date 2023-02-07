import asyncio
from concurrent.futures import ThreadPoolExecutor
from time import time

import requests
from requests.exceptions import RequestException, MissingSchema

from libs import async_timed

urls = ['http://www.google.com', 'http://www.python.org', 'http://duckduckgo.com', 'https://goit.global']


def get_data_from_url(url) -> (str, str):
    r = requests.get(url)
    return url, r.text[:100]


@async_timed()
async def async_worker():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(3) as pool:
        futures = [loop.run_in_executor(pool, get_data_from_url, url) for url in urls]
        done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
        print('Done: ', done)
        print('Pending: ', pending)

        [p.cancel() for p in pending]

        results = []
        for future in done:
            results.append(await future)
        return results


if __name__ == '__main__':
    r = asyncio.run(async_worker())
    print(r)

