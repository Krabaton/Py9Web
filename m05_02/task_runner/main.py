import asyncio
from aiofile import async_open
from aiopath import AsyncPath


async def consumer(filename: str, queue: asyncio.Queue):
    async with async_open(filename, 'w', encoding='utf-8') as afr:
        while True:
            file, data = await queue.get()
            print(f'operation with file {file.name}')
            await afr.write(f'{data}\n')
            queue.task_done()


async def producer(file: AsyncPath, queue: asyncio.Queue):
    async with async_open(file, 'r', encoding='utf-8') as afr:
        data = []
        async for line in afr:
            data.append(str(line))
        data_all = ''.join(data)
        await queue.put((file, data_all))


async def run():
    files = AsyncPath('.').joinpath('files').glob('*.js')
    files_queue = asyncio.Queue()

    producers = [asyncio.create_task(producer(file, files_queue)) async for file in files]
    task_consumer = asyncio.create_task(consumer('main.js', files_queue))

    await asyncio.gather(*producers)
    await files_queue.join()
    task_consumer.cancel()
    print('Completed')


if __name__ == '__main__':
    asyncio.run(run())
