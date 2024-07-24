"""

Functionality for loading data from various sources.

"""

from requests import get
from io import BytesIO

def load_data_from_url(url: str) -> bytes:
    """
    Load data from a URL.
    """
    response = get(url)
    response.raise_for_status()

    return BytesIO(response.content)