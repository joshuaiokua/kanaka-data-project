"""
datacore/formatting.py

Functionality for formatting data, as distinct from transforming it. That is, this module is for changing the format the data might presented in or organized (e.g. column names), but not the data itself.

TODO:
- Revisit formatting given changes to string cleaning functions (i.e. use of SUBSTITUTION_MAP).

Functions:
- format_column_name: Format a singular column name.
- format_column_names: Format a list of column names.
- infer_column_types: Infer the data types of a DataFrame's columns.
"""

import re
from typing import Optional

from pandas import DataFrame, isna, to_datetime, to_numeric

from src.constants.mappings import SUBSTITUTION_MAP

### --- CONSTANTS --- ###
IGNORED_WORDS = ("census", "estimates")


### --- FUNCTIONS --- ###
def format_column_name(
    name: str,
    ignored: list = IGNORED_WORDS,
    substitutions: Optional[dict] = None,
) -> str:
    """
    Format a singular column name.

    Args:
        name (str): The name of the column to format.
        ignored (list): A list of words to ignore when formatting the column name.
        substitutions (dict): A dictionary of words to substitute when formatting the column name.

    Returns:
        str: The formatted column name.
    """
    formatted_list = []

    if substitutions is None:
        substitutions = SUBSTITUTION_MAP

    str_list = re.split(r"[\. ]+", name.lower())  # handle multiple delimiters
    for word in str_list:
        if word in ignored:
            continue

        # Appends sub word if in `substitutions` else original word
        formatted_list.append(substitutions.get(word, word))

    return "_".join(formatted_list).strip("_")


def format_column_names(
    df: DataFrame,
    inplace: bool = False,
    flag_word: str = "Unnamed",
    min_rows: int = 2,
) -> list:
    """
    Format a list of column names.

    Args:
        df (DataFrame): The DataFrame containing the column names to format.
        inplace (bool): Whether to modify the DataFrame in place.
        flag_word (str): A word that indicates the column name is invalid.
        min_rows (int): The minimum number of rows required to format the column names.

    Returns:
        list: The formatted column names
    """
    if df.empty:
        raise ValueError("DataFrame is empty.")

    if df.shape[0] < min_rows:
        msg = f"DataFrame has fewer than {min_rows} rows."
        raise ValueError(msg)

    curr_names, new_names = df.columns, []
    last_valid_column_idx = 0

    for col_idx, col in enumerate(curr_names):
        if (isna(col)) or (flag_word in col):
            row_idx = 1 if isna(df.iloc[0, col_idx]) else 0
            prev_col = curr_names[last_valid_column_idx]
            col = f"{prev_col} {df.iloc[row_idx, col_idx]}"
        else:
            last_valid_column_idx = col_idx

        new_names.append(format_column_name(col))

    if inplace:
        df.columns = new_names
        return df  # Return the DataFrame for method chaining
    return new_names


def infer_column_types(
    df: DataFrame,
    return_modified_df: bool = False,
    category_ceiling: float = 0.05,
) -> dict:
    """
    Infer the data types of a DataFrame's columns.

    Args:
        df (DataFrame): The DataFrame to infer the column types of.
        return_modified_df (bool): Whether to return the modified DataFrame with the inferred data types.
        category_ceiling (float): The maximum ratio of unique values to total values for a column to be considered a category.

    Returns:
        dict: A dictionary mapping column names to their inferred data types.
    """
    inferred_types = {}

    for col in df.columns:
        sample = df[col].dropna()

        if to_numeric(sample, errors="coerce").notna().all():
            if (sample.astype(float) % 1 == 0).all():  # all values whole numbers
                inferred_types[col] = "int"
            else:
                inferred_types[col] = "float"
        elif to_datetime(sample, errors="coerce").notna().all():
            inferred_types[col] = "datetime"
        elif sample.nunique() / len(sample) < category_ceiling:
            inferred_types[col] = "category"
        else:
            inferred_types[col] = "str"

    if return_modified_df:
        return df.astype(inferred_types)

    return inferred_types
