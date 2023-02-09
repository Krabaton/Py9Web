import asyncio
from time import sleep, time
from typing import Iterable, Awaitable, List, Coroutine, Any, AsyncIterator

from faker import Faker

fake = Faker('uk-UA')


async def get_user_async(uuid: int):
    await asyncio.sleep(0.5)
    return {'id': uuid, 'name': fake.name(), 'company': fake.company(), 'email': fake.email()}


async def get_users(uuids: List[int]) -> AsyncIterator:
    for uuid in uuids:
        yield get_user_async(uuid)


async def main(users: AsyncIterator):
    result = []
    async for user in users:
        result.append(user)
    return await asyncio.gather(*result)


if __name__ == '__main__':
    start = time()
    uuids = [1, 2, 3]
    users = asyncio.run(main(get_users(uuids)))
    print(users)
    print(time() - start)
