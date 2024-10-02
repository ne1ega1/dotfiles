import orjson


def load_json(path_to_file):
    with path_to_file.open(mode='rb') as reading_file:
        data = orjson.loads(reading_file.read())

    return data


def dump_json(path_to_file, data):
    path_to_file.write_bytes(
        orjson.dumps(
            data,
            option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
        )
    )


def read_file(path_to_file) -> str:
    """Чтение файла"""
    with path_to_file.open(mode='r', encoding='UTF-8', errors='ignore') as _file:
        return _file.read()


def dump_file(path_to_file, data):
    with open(path_to_file, 'w') as _file:
        _file.write(data)
