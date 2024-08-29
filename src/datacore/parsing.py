"""
datacore/parsing.py

Functionality for parsing data from various sources.

TODO: 
- Revisit consolidating the functions in this module.
- Naming conventions for functions (i.e. is sheet the best term to use).

Functions:
- get_sheet_text: Retrieve text elements from a specific sheet in the DataFrame dictionary.
"""

import re
from pandas import DataFrame, notna


### --- FUNCTIONS --- ###
def get_sheet_text(
    df_dict: dict[str, DataFrame],
    sheet_name: str,
    separator="\n",
    drop_na: bool = True,
    include_numbers: bool = False,
    ignore_key_error: bool = False,
) -> str:
    """
    Retrieves the text elements from a specific sheet in the DataFrame dictionary.

    Args:
        df_dict (dict): A dictionary of DataFrames.
        sheet_name (str): The name of the sheet to retrieve text from.
        separator (str): The separator to use when joining text elements.
        drop_na (bool): Whether to drop NaN values from the text.
        include_numbers (bool): Whether to include numbers in the text.
        ignore_key_error (bool): Whether to return an empty string if the specified sheet is not found.

    Returns:
        str: The text elements from the specified sheet.
    """
    if sheet_name not in df_dict:
        if ignore_key_error:
            return ""
        raise KeyError(f'Sheet "{sheet_name}" not found in DataFrame dictionary.')

    # Drop NaN values if specified
    content = (
        df_dict[sheet_name].dropna().to_numpy().flatten()
        if drop_na
        else df_dict[sheet_name].to_numpy().flatten()
    )

    # Filter out numbers if specified
    if not include_numbers:
        content = [item for item in content if isinstance(item, str)]
    else:
        content = [str(item) for item in content if notna(item)]

    # Join the text elements using the specified separator
    return separator.join(content).strip()


def get_sheet_titles(df_dict: dict) -> DataFrame:
    """
    Extract the titles of each sheet in the DataFrame dictionary.

    Args:
        df_dict (dict): A dictionary of DataFrames.

    Returns:
        pd.DataFrame: A DataFrame containing the sheet titles.
    """
    try:
        title_pairs = df_dict["Titles"].dropna().values.tolist()
    except KeyError as exc:
        raise KeyError(
            "The 'Titles' sheet is missing from the DataFrame dictionary."
        ) from exc

    table_name_pairs = []

    while title_pairs:
        table, title = title_pairs.pop(0)
        if "Table" in table and table != "Table":
            table_name_pairs.append(
                (
                    "0" + table.split(" ")[-1],
                    re.sub(r"Hawaiÿi|Hawai'i", "Hawaii", title),
                )
            )

    return table_name_pairs
