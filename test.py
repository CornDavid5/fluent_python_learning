

from tkinter.font import names


def get_creator(record: dict) -> list:
    match record:
        case {'type': 'book', 'authors': [*names]}:
            return names
        case {'type': 'book', 'author': name}:
            return [name]
        case {'type': 'book', **all}:
            print(all)
            return None

record = {'writes': ['a', 'b', 'c'], 'title': 'aa', 'type': 'book'}

print(get_creator(record))