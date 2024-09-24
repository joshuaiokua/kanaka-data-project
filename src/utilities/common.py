"""
Common Utilities

Utility functions that do not fit into any other specific category or else are the sole function of what could be understood as their categorical kind (e.g. path utilities, type casting, etc.).

Functions:
    can_cast_to_int: Check if a string can be cast to an integer.
    create_random_identifier: Create a pseudo-random identifier string.
    find_project_root: Find the project root directory.
"""

from pathlib import Path
from random import randint


### --- FUNCTIONS --- ###
def can_cast_to_int(s: str) -> bool:
    """
    Check if the given string can be cast to an integer.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string can be cast to an int, False otherwise.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def create_random_identifier(
    prefix: str = "",
    separator: str = "_",
    ceiling: int = 1000,
) -> str:
    """
    Create a pseudo-random identifier string. Should not be used for cryptographic purposes.
    """
    return f"{prefix}{separator}{randint(0, ceiling)}"  # noqa: S311


def find_project_root(start_path: Path | None = None) -> Path:
    """
    Programmatically find the project root by searching for a known directory or file (e.g., '.git' or 'pyproject.toml').

    Args:
        start_path (Path): The starting directory to begin the search. Defaults to the current file's directory.

    Returns:
        Path: The absolute path to the project root.
    """
    if start_path is None:
        start_path = Path(__file__).resolve()

    # Traverse up the directory tree until we find a known project root indicator
    for parent in start_path.parents:
        if (parent / ".git").exists() or (parent / "pyproject.toml").exists():
            return parent
    # If no project root is found, assume the start_path is the project root
    return start_path.parent


def get_attribute(obj: object, attr: str) -> object:
    """
    Get an attribute from an object, checking for various attribute naming conventions.
    """
    variations = [attr, f"_{attr}", f"__{attr}__"]
    for var in variations:
        if hasattr(obj, var):
            return getattr(obj, var)

    msg = f"Object {obj} has no attribute {attr}."
    raise AttributeError(msg)
