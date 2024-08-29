"""
datacore/loaders.py

Functionality for loading data from various sources.

TODO:
- Revisit logic for renaming columns

Functions:
- load_json: Load a JSON file into a dictionary.
- load_data_from_url: Load data from a URL.
"""

import json
from io import BytesIO

import requests


### --- FUNCTIONS --- ###
def load_json(file_path: str, encoding: str = "utf-8") -> dict:
    """
    Load a JSON file into a dictionary.

    Args:
        file_path (str): The path to the JSON file.
        encoding (str): The encoding of the file.

    Returns:
        dict: The JSON data as a dictionary.
    """
    with open(file_path, encoding=encoding, mode="r") as file:
        return json.loads(file.read())


def load_data_from_url(url: str, timeout: int = 10) -> BytesIO:
    """
    Load data from given a URL.

    Args:
        url (str): The URL of the data to load.
        timeout (int): The number of seconds to wait before timing out.

    Returns:
        BytesIO: The retrieved data as a BytesIO object.
    """
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return BytesIO(response.content)
