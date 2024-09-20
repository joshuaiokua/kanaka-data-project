"""
datacore/loaders.py

Functionality for loading data from various sources.

TODO:
- Revisit logic for renaming columns

Functions:
- load_json: Load a JSON file into a dictionary.
- load_data_from_url: Load data from a URL.
"""

### --- External Imports --- ###
import json
from io import BytesIO

import requests
from pandas import DataFrame


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
    with open(file_path, encoding=encoding) as file:
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


async def load_dataframe_from_db(
    table_name: str,
    db_manager: object,
) -> DataFrame:
    """
    Load a DataFrame from a CockroachDB table.

    Args:
        table_name (str): The name of the table in the database.
        db_manager (CockroachDBManager): The CockroachDBManager object.

    Returns:
        DataFrame: The loaded DataFrame.
    """
    # Connect to the database if not already connected
    if not db_manager.is_connected:
        await db_manager.connect()

    columns, rows = await db_manager.execute_query(
        "SELECT * FROM %s",
        (table_name,),
        return_columns=True,
    )

    return DataFrame(rows, columns=columns)
