import math
import sys
import os
from os import listdir
import re
import configparser
import json

os.chdir(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read('./path_config.ini')


class_regex = config['PARSER']['CLASS_REGEX']
file_extensions = config['PARSER']['FILE_EXTENSION']
path_to_parse = sys.argv[1]
project_name = sys.argv[2]

def convert_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    size_name = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return {'size': s, 'type': size_name[i], 'bytes': size_bytes}


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

    general_class_count = 0
    project_size = 0

    json_data = {'data': []}

    for path, dir_list, file_list in os.walk(f'{path_to_parse}/{project_name}', topdown=True):
        dir_list[:] = [dir_name for dir_name in dir_list if dir_name not in dir_list_to_ignore]

        for file_name in file_list:
            file_path = os.path.join(path, file_name)

            for extension in file_extensions.split():
                if re.search(rf'{extension}$', file_name):
                    with open(f'{path}/{file_name}', 'r', encoding='utf-8') as file:
                        print(f'    File {path}/{file_name} are ready for reading')
                        file_body = file.read()
                        class_count = len(re.findall(rf'{class_regex}', file_body))

                        general_class_count += class_count
                        print(f'    File named \'{file_name}\' has {class_count} amount')

                    file.close()

            if not ('result_data.json' in listdir('./')):
                with open('result_data.json', 'w') as json_file:
                    json.dump(json_data, json_file)
                json_file.close()
            else:
                with open('result_data.json', 'r') as json_file:
                    json_data = json.load(json_file)
                json_file.close()

            if not os.path.islink(file_path):
                project_size += os.path.getsize(file_path)

    project_size = convert_size(project_size)
    print(f'Project {project_name} has {general_class_count} amount with {project_size["size"]}{project_size["type"]} bytes {project_size["bytes"]} '
          f'size2')

    json_data['data'].append({
        'name': project_name,
        'count': general_class_count,
        'bytes': project_size['bytes'],
        'size': project_size['size'],
        'type': project_size['type']
    })

    with open('result.txt', 'a') as file:
        file.write(f'{project_name} {general_class_count} {project_size["bytes"]} {project_size["size"]}{project_size["type"]}\n')
    file.close()

    with open('result_data.json', 'w') as json_file:
        json.dump(json_data, json_file)
    json_file.close()


if __name__ == '__main__':
    main()
