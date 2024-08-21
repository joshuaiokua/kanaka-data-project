"""

General utility functionality that does not neatly fit into other categories captured by any of the specifically named modules in the utils folder (e.g. string.py).

"""

from json import loads

def load_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return loads(file.read())
    
