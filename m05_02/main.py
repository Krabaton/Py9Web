import asyncio
import platform
import logging

import aiohttp

urls = ['https://www.google.com.ua/', 'https://duckduckgo.com/', 'https://docs.aiohttp.org/',
        'https://goit.global/ua/asdf', 'https://mail.ru']


async def main():
    async with aiohttp.ClientSession() as session:
        for url in urls:
            logging.info(f'Starting: {url}')
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        print(html[:100])
                    else:
                        logging.error(f"Error status {response.status} for {url}")
            except aiohttp.ClientConnectorError as e:
                logging.error(f"Connection error {url}: {e}")


async def custom_main(url):
    session = aiohttp.ClientSession()
    logging.info(f'Starting: {url}')
    try:
        response = await session.get(url)
        if response.status == 200:
            html = await response.text()
            await session.close()
            return html[:150]
        else:
            logging.error(f"Error status {response.status} for {url}")
    except aiohttp.ClientConnectorError as e:
        logging.error(f"Connection error {url}: {e}")
    await session.close()


async def run():
    r = []
    for url in urls:
        r.append(custom_main(url))

    result = await asyncio.gather(*r)
    return result


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    r = await response.json()
                    return r
                logging.error(f"Error status {response.status} for {url}")
        except aiohttp.ClientConnectorError as e:
            logging.error(f"Connection error {url}: {e}")
        return None


async def get_exchange():
    res = await request('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
    return res


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # asyncio.run(main())
    # r = asyncio.run(run())
    # print(r)
    r = asyncio.run(get_exchange())
    print(r)
