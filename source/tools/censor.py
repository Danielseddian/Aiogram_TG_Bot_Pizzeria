import json
import string

from source.core import config


def get_censorship(text: str) -> bool:
    def get_translate(word):
        return word.lower().translate(str.maketrans("", "", string.punctuation + string.digits))

    censor_json = "cenz.json"

    def get_censor_set():
        try:
            return set(json.load(open(config.MEDIA_ROOT/censor_json)))
        except FileNotFoundError:
            print(f'Файл "{censor_json}" в директории {config.MEDIA_ROOT} не найден')
            return ""

    if {get_translate(word) for word in text.split(" ")}.intersection(get_censor_set()) != set():
        return True
    return False


if __name__ == '__main__':
    print(get_censorship("Здесь есть м!ат"))
