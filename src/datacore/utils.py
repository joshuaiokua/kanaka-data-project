"""
Data Utilities

Utility functions for specifically for working with data and data-related tasks.

Functions:
    is_valid_table_name: Guards against SQL injection by checking validity of table name.
"""

import re


### --- FUNCTIONS --- ###
def is_valid_table_name(table_name: str) -> bool:
    """
    Check if the provided table name is a valid SQL identifier.
    """
    return bool(re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", table_name))
