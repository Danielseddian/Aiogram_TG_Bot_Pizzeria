import json

from source.core import config


def make_json_list(filepath=config.MEDIA_ROOT, text_filename="temp.txt", json_filename="temp.json"):
    try:
        with open(filepath/text_filename, encoding="UTF-8") as text:
            array = [cleared_line for line in text if (cleared_line := line.lower().split("\n")[0])]
    except FileNotFoundError:
        print(f'Файл "{text_filename}" или директория "{filepath}" не существует')
        array = []
    if array:
        with open(filepath/json_filename, "w", encoding="UTF-8") as json_list:
            json.dump(array, json_list)
            print(f'Файл "{json_filename}" успешно создан, данные добавлены.')
    else:
        print(f'Файл "{json_filename}" не создан, так как список пуст.')


if __name__ == '__main__':
    make_json_list(json_filename="cenz.json")
