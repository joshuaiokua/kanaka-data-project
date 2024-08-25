"""
data_processing/loaders.py

Functionality for loading data from various sources.

TODO:
- Revisit logic for renaming columns

Functions:
- load_json: Load a JSON file into a dictionary.
- load_data_from_url: Load data from a URL.
"""

import json
import requests
from io import BytesIO

### --- FUNCTIONS --- ###
def load_json(file_path: str) -> dict:
    """
    Load a JSON file into a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The JSON data as a dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f'File not found: {file_path}')
    except json.JSONDecodeError:
        raise ValueError(f'Invalid JSON file: {file_path}')

def load_data_from_url(url: str, timeout: int = 10) -> BytesIO:
    """
    Load data from given a URL.

    Args:
        url (str): The URL of the data to load.
        timeout (int): The number of seconds to wait before timing out.

    Returns:
        BytesIO: The retrieved data as a BytesIO object.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return BytesIO(response.content)
    except requests.exceptions.HTTPError as e:
        raise requests.exceptions.HTTPError(f"HTTP error occurred: {e.response.status_code} {e.response.reason}") from e
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f'Error loading data from URL: {e}')

