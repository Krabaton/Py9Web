#  Awaitable -> Coroutine
#  Awaitable -> Future -> Task

import asyncio
from asyncio import Future
from time import sleep, time

from faker import Faker

from libs import async_timed

fake = Faker('uk-UA')


async def get_user_async_db(uuid: int, future: Future):
    await asyncio.sleep(0.5)
    future.set_result({'id': uuid, 'name': fake.name(), 'company': fake.company(), 'email': fake.email()})


def make_request(uuid: int):
    future = Future()
    asyncio.create_task(get_user_async_db(uuid, future))
    return future


@async_timed()
async def main():
    u1_future = make_request(1)
    u2_future = make_request(2)
    u3_future = make_request(3)
    print(u1_future, u2_future, u3_future)
    print(u1_future.done(), u2_future.done(), u3_future.done())
    result = await asyncio.gather(u1_future, u2_future, u3_future)
    print(u1_future.done(), u2_future.done(), u3_future.done())
    return result


if __name__ == '__main__':
    users = asyncio.run(main())
    print(users)
