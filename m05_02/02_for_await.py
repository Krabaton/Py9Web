import asyncio
from time import sleep, time
from typing import Iterable, Awaitable, List, Coroutine, Any

from faker import Faker

fake = Faker('uk-UA')


async def get_user_async(uuid: int):
    await asyncio.sleep(0.5)
    return {'id': uuid, 'name': fake.name(), 'company': fake.company(), 'email': fake.email()}


async def get_users(uuids: List[int]) -> List[Coroutine[Any, dict, Any]]:
    return [get_user_async(uuid) for uuid in uuids]


async def main(users: Coroutine[Any, List[Coroutine[Any, dict, Any]], Any]):
    result = []
    for user in await users:
        result.append(user)
    return await asyncio.gather(*result)


if __name__ == '__main__':
    start = time()
    uuids = [1, 2, 3]
    users = asyncio.run(main(get_users(uuids)))
    print(users)
    print(time() - start)
