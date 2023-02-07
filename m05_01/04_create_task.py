#  Awaitable -> Coroutine
#  Awaitable -> Future -> Task

import asyncio
from time import sleep, time

from faker import Faker

fake = Faker('uk-UA')


async def get_user_async_db(uuid: int):
    await asyncio.sleep(0.5)
    return {'id': uuid, 'name': fake.name(), 'company': fake.company(), 'email': fake.email()}


async def main():
    u1_task = asyncio.create_task(get_user_async_db(1))
    u2_task = asyncio.create_task(get_user_async_db(2))
    u3_task = asyncio.create_task(get_user_async_db(3))
    print(u1_task, u2_task, u3_task)

    result = await asyncio.gather(u1_task, u2_task, u3_task)
    return result


if __name__ == '__main__':
    # start = time()
    # users = asyncio.run(main())
    # print(users)
    # print(time() - start)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    users = loop.run_until_complete(main())
    print(users)
