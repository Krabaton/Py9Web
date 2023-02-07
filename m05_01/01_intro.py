import asyncio
from typing import Coroutine, Any


async def baz():
    await asyncio.sleep(1)
    return 'Hello world!'


async def main():
    cor = baz()
    print(cor)
    result = await cor
    print(result)
    return result


if __name__ == '__main__':
    r = asyncio.run(main())
    print(r)
