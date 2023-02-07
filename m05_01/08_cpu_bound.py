import asyncio
from concurrent.futures import ProcessPoolExecutor
from time import time


def cpu_bound_task(counter):
    init = counter
    while counter > 0:
        counter -= 1
    print(f'Completed cpu_bound_task with: {init}')
    return f'Completed cpu_bound_task with: {init}'


async def send_data():
    while True:
        await asyncio.sleep(1)
        print(f'Send to https://for.me: {time()}')


async def async_worker():
    loop = asyncio.get_running_loop()
    sd = loop.create_task(send_data())

    with ProcessPoolExecutor(2) as pool:
        futures = [loop.run_in_executor(pool, cpu_bound_task, num) for num in [60_000_000, 70_000_000, 80_000_000]]
        result = await asyncio.gather(*futures)
        sd.cancel()
        return result


async def main():
    r = await async_worker()
    return r


if __name__ == '__main__':
    r = asyncio.run(main())
    print(r)
