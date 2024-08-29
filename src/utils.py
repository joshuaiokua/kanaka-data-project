"""
utils.py

Utility functions for cleaning strings and other miscellaneous tasks.

Functions:
- apply_string_cleaning_patterns: Clean a string with a series of regex and replacements.
- clean_string_with_patterns: Clean a string with patterns from PATTERN_MAP.
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

        # Retrieve the single pattern-replacement tuple
        pattern, replacement = PATTERN_MAP[pattern_key]

        # Apply the pattern using the existing function
        string = apply_string_cleaning_patterns(string, (pattern, replacement))

    return string
