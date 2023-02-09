'''
Задача: Сортировка файлов в папке. Скопировать файлы из указанной папки и положить в новую папку с
расширениям этого файла.
'''

import argparse
import asyncio

from aiopath import AsyncPath
from aioshutil import copyfile

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('--source', '-s', required=True, help='Source folder')
parser.add_argument('--output', '-o', default='dist', help='Output folder')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')
output_folder = AsyncPath(output)  # dist


async def read_folder(path: AsyncPath) -> None:
    async for el in path.iterdir():
        if await el.is_dir():
            await read_folder(el)
        else:
            await copy_file(el)


async def copy_file(file: AsyncPath) -> None:
    ext = file.suffix
    new_path = output_folder / ext
    await new_path.mkdir(exist_ok=True, parents=True)
    await copyfile(file, new_path / file.name)


if __name__ == '__main__':
    asyncio.run(read_folder(AsyncPath(source)))
    print('Finished')
