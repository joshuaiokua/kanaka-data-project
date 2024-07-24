from json import loads

def load_json(file_path):
    with open(file_path, 'r') as file:
        return loads(file.read())
    
