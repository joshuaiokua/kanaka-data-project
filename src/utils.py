"""
utils.py

Utility functions for cleaning strings and other miscellaneous tasks.

Functions:
- apply_string_cleaning_patterns: Clean a string with a series of regex and replacements.
- clean_string_with_patterns: Clean a string with patterns from PATTERN_MAP.
- extract_years_from_string: Extract all years from a string.
"""

# External Imports
import re
from typing import Pattern

# Local Imports
from src.constants.mappings import PATTERN_MAP


### --- FUNCTIONS --- ###
def apply_string_cleaning_patterns(string: str, *patterns: tuple[Pattern, str]) -> str:
    """
    Clean a string by applying a series of regular expressions and replacements.

    Args:
        string (str): The string to clean.
        *patterns (tuple): A tuple of regular expressions and their corresponding replacements.

    Returns:
        str: The cleaned string.
    """
    for pattern, replacement in patterns:
        string = re.sub(pattern, replacement, string)
    return string


def clean_string_with_patterns(string: str, *pattern_keys: str) -> str:
    """
    Clean a string using a set of predefined patterns from the PATTERN_MAP.

    Args:
        string (str): The string to clean.
        *pattern_keys (str): One or more keys to retrieve specific patterns from PATTERN_MAP.

    Returns:
        str: The cleaned string.

    Raises:
        KeyError: If any of the pattern_keys are not found in PATTERN_MAP.
    """
    for pattern_key in pattern_keys:
        if pattern_key not in PATTERN_MAP:
            raise KeyError(f"Pattern key '{pattern_key}' not found in PATTERN_MAP.")

        # Retrieve the pattern-replacement tuple and apply it
        pattern, replacement = PATTERN_MAP[pattern_key]
        string = apply_string_cleaning_patterns(string, (pattern, replacement))

    return string


def extract_years_from_string(title: str) -> list:
    """
    Extracts all years from a string for formats listed below:
    - Single year: "Title 2006"
    - Year range: "Title: 2006-2010"
    - Mixed: "Title 2006, 2008-2010, 2012"

    Args:
        title (str): The title string containing years or ranges of years.

    Returns:
        list: A list of all years that could be extracted from the title, including all years in any ranges.
    """
    # Regex to find all year ranges (e.g., 2006-2010) or single years
    year_ranges = re.findall(r"(\d{4})\s*-\s*(\d{4})|\b(\d{4})\b", title)

    if not year_ranges:
        return []

    years = set()

    for year_range in year_ranges:
        if year_range[0] and year_range[1]:  # If range of years
            start_year = int(year_range[0])
            end_year = int(year_range[1])
            years.update(range(start_year, end_year + 1))
        elif year_range[2]:  # If single year
            years.add(int(year_range[2]))

    return sorted(years)
