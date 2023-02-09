import asyncio
from time import sleep, time
from typing import Iterable, Awaitable, List

from faker import Faker

fake = Faker('uk-UA')


async def get_user_async(uuid: int):
    await asyncio.sleep(0.5)
    return {'id': uuid, 'name': fake.name(), 'company': fake.company(), 'email': fake.email()}


def get_users(uuids: List[int]) -> Iterable[Awaitable]:
    return [get_user_async(uuid) for uuid in uuids]


async def main(users: Iterable[Awaitable]):
    return await asyncio.gather(*users)


if __name__ == '__main__':
    start = time()
    uuids = [1, 2, 3]
    users = asyncio.run(main(get_users(uuids)))
    print(users)
    print(time() - start)
