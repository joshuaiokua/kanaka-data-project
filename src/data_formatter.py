"""

Functionality for formatting data, as distinct from transforming it. That is, this module is for changing the format the data might presented in or organized (e.g. column names), but not the data itself.

"""

# Local Imports
from src.utils.dicts import abbreviation_map

# External Imports
from re import split
from pandas import isna, DataFrame

### --- CONSTANTS --- ###
IGNORED_WORDS = ('census', 'estimates')


### --- FUNCTIONS --- ###
def format_column_name(name: str, conversion_map: dict = abbreviation_map, ignored_words = IGNORED_WORDS) -> str:
    """
    Format a singular column name using a conversion map to standardize column names and make them more readable, accessible, and consistent.
    """
    # Split the string by '.' or ' ' and convert to lowercase
    str_list, formatted_list = split(r'[\. ]', name.lower()), []

    for word in str_list:
        if word in conversion_map:
            formatted_list.append(conversion_map[word])
        elif word not in ignored_words:
            formatted_list.append(word)

    return '_'.join(formatted_list)

def format_column_names(df: DataFrame, inplace: bool = False, flag_word: str = 'Unnamed') -> list:
    """
    Format a list of column names using a conversion map to standardize column names and make them more readable, accessible, and consistent.
    """
    if df.empty:
        raise ValueError('DataFrame is empty.')

    curr_names, new_names = df.columns, []
    last_valid_column_idx = 0

    for col_idx, col in enumerate(curr_names):
        if flag_word in col:
            # Determine if the first row value in this column is NaN
            row_idx = 1 if isna(df.iloc[0, col_idx]) else 0
            prev_col = curr_names[last_valid_column_idx]
            col = f'{prev_col} {df.iloc[row_idx, col_idx]}'
        else:
            last_valid_column_idx = col_idx
        
        new_names.append(format_column_name(col))

    if inplace:
        df.columns = new_names
        return None
    else:
        return new_names
