"""
data_processing/formatting.py

Functionality for formatting data, as distinct from transforming it. That is, this module is for changing the format the data might presented in or organized (e.g. column names), but not the data itself.

Functions:
- format_column_name: Format a singular column name.
- format_column_names: Format a list of column names.
"""
from src.constants.mappings import SUBSTITUTION_MAP

import re
from pandas import isna, DataFrame

### --- CONSTANTS --- ###
IGNORED_WORDS = ('census', 'estimates')

### --- FUNCTIONS --- ###
def format_column_name(name: str, ignored_words: list[str] = IGNORED_WORDS, substitution_map: dict[str] = SUBSTITUTION_MAP) -> str:
    """
    Format a singular column name.

    Args:
        name (str): The name of the column to format.
        ignored_words (tuple): A tuple of words to ignore when formatting the column name.

    Returns:
        str: The formatted column name.
    """
    formatted_list = []

    str_list = re.split(r'[\. ]+', name.lower())  # handle multiple delimiters
    for word in str_list:
        if word in ignored_words:
            continue

        if word in substitution_map:
            word = substitution_map[word]

        formatted_list.append(word)

    return '_'.join(formatted_list).strip('_')

def format_column_names(df: DataFrame, inplace: bool = False, flag_word: str = 'Unnamed') -> list:
    """
    Format a list of column names.

    Args:
        df (DataFrame): The DataFrame containing the column names to format.
        inplace (bool): Whether to modify the DataFrame in place.
        flag_word (str): A word that indicates the column name is invalid.

    Returns:
        list: The formatted column names
    """
    if df.empty:
        raise ValueError('DataFrame is empty.')

    if df.shape[0] < 2:
        raise ValueError('DataFrame must have at least two rows to check for NaN.')

    curr_names, new_names = df.columns, []
    last_valid_column_idx = 0

    for col_idx, col in enumerate(curr_names):
        if (isna(col)) or (flag_word in col):
            row_idx = 1 if isna(df.iloc[0, col_idx]) else 0
            prev_col = curr_names[last_valid_column_idx]
            col = f'{prev_col} {df.iloc[row_idx, col_idx]}'
        else:
            last_valid_column_idx = col_idx

        new_names.append(format_column_name(col))

    if inplace:
        df.columns = new_names
        return df  # Return the DataFrame for method chaining
    else:
        return new_names