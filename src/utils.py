"""
utils.py

Utility functions for cleaning strings and other miscellaneous tasks.

Functions:
- apply_string_cleaning_patterns: Clean a string with a series of regex and replacements.
- clean_string_with_named_patterns: Clean a string with patterns from PATTERN_MAP.
- extract_years_from_string: Extract all years from a string.
"""

# External Imports
import re
from typing import Pattern

# Local Imports
from src.constants.mappings import PATTERN_MAP


### --- FUNCTIONS --- ###
def apply_string_cleaning_patterns(
    string: str,
    attempt_cast_to_int: bool = False,
    *patterns: tuple[Pattern, str],
    **kwargs,
) -> str:
    """
    Clean a string by applying a series of regular expressions and replacements.

    Args:
        string (str): The string to clean.
        attempt_cast_to_int (bool): Whether to attempt to cast the cleaned string to an int.
        *patterns (tuple): A tuple of regular expressions and their corresponding replacements.
        **kwargs: Additional keyword arguments to pass to re.sub.

    Returns:
        str: The cleaned string.
    """
    input_type = type(string)

    # Convert to string if not already
    if input_type is not str:
        string = str(string)

    # Apply each pattern-replacement pair
    for pattern, replacement in patterns:
        string = re.sub(pattern, replacement, string, **kwargs)

    # Convert back to original type if necessary
    if input_type is not str:
        string = input_type(string)

    # Check if input can be cast to int
    if can_cast_to_int(string) and attempt_cast_to_int:
        string = int(string)

    return string


def clean_string_with_named_patterns(
    string: str,
    *pattern_keys: str,
    **kwargs,
) -> str:
    """
    Clean a string using a set of predefined named patterns that act as keys to retrieve regex and replacement pairs from PATTERN_MAP.

    Args:
        string (str): The string to clean.
        *pattern_keys (str): One or more keys to retrieve specific patterns from PATTERN_MAP.
        **kwargs: Additional keyword arguments to pass to apply_string_cleaning_patterns, such as `flags=re.IGNORECASE`.

    Returns:
        str: The cleaned string.

    Raises:
        KeyError: If any of the pattern_keys are not found in PATTERN_MAP.
    """
    attempt_cast_to_int = kwargs.pop("attempt_cast_to_int", False)

    for pattern_key in pattern_keys:
        if pattern_key not in PATTERN_MAP:
            msg = f"Pattern key '{pattern_key}' not found in PATTERN_MAP."
            raise KeyError(msg)

        # Retrieve the pattern-replacement tuple and apply it
        pattern, replacement = PATTERN_MAP[pattern_key]
        string = apply_string_cleaning_patterns(
            string,
            attempt_cast_to_int,
            (pattern, replacement),
        )

    return string


def extract_years_from_string(title: str) -> list:
    """
    Extract all years from a string for formats listed below:
    - Single year: "Title 2006"
    - Year range: "Title: 2006-2010"
    - Mixed: "Title 2006, 2008-2010, 2012"

    Args:
        title (str): The title string containing years or ranges of years.

    Returns:
        list: A list of all years and year ranges (as tuples) that could be extracted from the title.
    """
    # Regex to find all single years and year ranges, standardizing hyphens first
    year_matches = re.findall(
        r"(\d{4})\s*-\s*(\d{4})|\b(\d{4})\b",
        clean_string_with_named_patterns(title, "hyphens"),
    )

    years = []

    for match in year_matches:
        if match[0] and match[1]:  # If a range of years is matched
            start_year = int(match[0])
            end_year = int(match[1])
            years.append((start_year, end_year))  # Capture the range as a tuple
        elif match[2]:  # If a single year is matched
            years.append(int(match[2]))

    return years


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
