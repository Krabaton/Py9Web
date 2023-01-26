'''
Задача: Сортировка файлов в папке. Скопировать файлы из указанной папки и положить в новую папку с
расширениям этого файла.
'''

import argparse
from pathlib import Path
from shutil import copyfile
from multiprocessing import Pool, current_process, cpu_count

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('--source', '-s', required=True, help='Source folder')
parser.add_argument('--output', '-o', default='dist', help='Output folder')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')
output_folder = Path(output)  # dist


def read_folder(path: Path) -> list:
    result = []
    for el in path.iterdir():
        if el.is_dir():
            result.append(el)
            r = read_folder(el)
            if len(r):
                result = result + r
        else:
            pass
    return result


def copy_file(dir: Path) -> None:
    for el in dir.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_folder / ext
            new_path.mkdir(exist_ok=True, parents=True)
            copyfile(el, new_path / el.name)


if __name__ == '__main__':
    with Pool(cpu_count()) as pool:
        pool.map(copy_file, read_folder(Path(source)))
        pool.close()
        pool.join()

    print('Finished')
