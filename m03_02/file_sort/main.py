'''
Задача: Сортировка файлов в папке. Скопировать файлы из указанной папки и положить в новую папку с
расширениям этого файла.
'''

import argparse
from pathlib import Path
from shutil import copyfile
from multiprocessing import Process, current_process

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument('--source', '-s', required=True, help='Source folder')
parser.add_argument('--output', '-o', default='dist', help='Output folder')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')
output_folder = Path(output)  # dist


def read_folder(path: Path) -> None:
    print(f'Start: {current_process().name} in {path}')
    for el in path.iterdir():
        if el.is_dir():
            pr_rf = Process(target=read_folder, args=(el,))
            pr_rf.start()
        else:
            copy_file(el)
    print(f'Finish: {current_process().name} in {path}')


def copy_file(file: Path) -> None:
    ext = file.suffix
    new_path = output_folder / ext
    new_path.mkdir(exist_ok=True, parents=True)
    copyfile(file, new_path / file.name)


if __name__ == '__main__':
    # read_folder(Path(source))
    pr_rf = Process(target=read_folder, args=(Path(source), ))
    pr_rf.start()
    pr_rf.join()
    print('Finished')
