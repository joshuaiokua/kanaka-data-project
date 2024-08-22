"""
general_utils.py

General utility functions that either don't fit into a specific category or else do not require their own module due to their simplicity.

Functions:
- load_json: Load a JSON file into a dictionary.
- load_aws_variables: Load AWS credentials and other variables listed in a .env file.

"""
from json import loads

### --- FUNCTIONS --- ###
def load_json(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return loads(file.read())