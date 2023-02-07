import asyncio
from time import sleep, time

from faker import Faker

fake = Faker('uk-UA')


def get_user_from_db(uuid: int):
    sleep(0.5)
    return {'id': uuid, 'name': fake.name(), 'company': fake.company(), 'email': fake.email()}


async def get_user_async_db(uuid: int):
    await asyncio.sleep(0.5)
    return {'id': uuid, 'name': fake.name(), 'company': fake.company(), 'email': fake.email()}


async def main():
    result = await asyncio.gather(get_user_async_db(1), get_user_async_db(2), get_user_async_db(3))
    return result


if __name__ == '__main__':
    start = time()
    for uuid in [1, 2, 3]:
        user = get_user_from_db(uuid)
        print(user)
    print(time() - start)
    print('---------------')
    start = time()
    users = asyncio.run(main())
    print(users)
    print(time() - start)
