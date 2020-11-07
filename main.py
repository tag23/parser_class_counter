import math
import os
from os import listdir
import re
import configparser

config = configparser.ConfigParser()
config.read('./path_config.ini')

path_to_parse = config['PARSER']['GLOBAL_PATH']
class_regex = config['PARSER']['CLASS_REGEX']
file_extension = config['PARSER']['FILE_EXTENSION']


class ABC:
    def __init__(self, lul):
        self.lul = lul


class ClassA(ABC):
    def say_hello(self):
        print(f'Hello {self.lul}')


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return {'size': s, 'type': size_name[i]}


def get_dir_to_ignore():
    dir_list = []
    with open('ignore_dir.txt', 'r') as file:
        body = file.read()

        for line in body.split():
            dir_list.append(line)

    file.close()
    return dir_list


def main():
    dir_list_to_ignore = get_dir_to_ignore()

    for project in listdir(str(path_to_parse)):
        general_class_count = 0
        project_size = 0

        for path, dir_list, file_list in os.walk(f'{path_to_parse}/{project}', topdown=True):
            dir_list[:] = [dir_name for dir_name in dir_list if dir_name not in dir_list_to_ignore]

            for file_name in file_list:
                file_path = os.path.join(path, file_name)

                if re.search(rf'{file_extension}$', file_name):
                    with open(f'{path}/{file_name}', 'r') as file:
                        file_body = file.read()
                        class_count = len(re.findall(rf'{class_regex}', file_body))

                        general_class_count += class_count
                        print(f'    File named \'{file_name}\' has {class_count} classes')

                    file.close()

                if not os.path.islink(file_path):
                    project_size += os.path.getsize(file_path)

        project_size = convert_size(project_size)
        print(f'Project {project} has {general_class_count} classes with {project_size["size"]}{project_size["type"]} '
              f'size')


if __name__ == '__main__':
    main()
