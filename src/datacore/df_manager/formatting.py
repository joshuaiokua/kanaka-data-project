"""
DataFrameManager Formatting Functionality

Functionality for formatting data, as distinct from transforming it. That is, this module is for changing the format the data might presented in or organized (e.g. column names), but not the data itself. This module is primarily for use in the DataFrameManager class.

TODO:
- Clean up and consolidate functions for formatting column names and values.

Functions:
    format_column_name: Format a singular column name.
    format_column_names: Format a list of column names.
    format_column_values: Format column values in a DataFrame.
    apply_column_value_formatting: Apply named patterns to column values in a DataFrame.
    apply_column_formatting: Apply column formatting to a DataFrame.
    apply_functions_to_dataframe: Apply a list of functions to a DataFrame.
    replace_implicit_nan: Replace implicit NaN values in a DataFrame.
    rename_columns: Rename columns in a DataFrame.
    promote_first_row_to_header: Promote the first row of a DataFrame to be the column names.
"""

# External Libraries
import re

from pandas import DataFrame

# Local Libraries
from src.constants.patterns import SUBSTITUTION_MAP
from src.utilities.string import clean_string_with_named_patterns

### --- MODULE CONSTANTS --- ###
IGNORED_WORDS = ("census", "estimates")


### --- FUNCTIONS --- ###
def format_column_name(
    name: str,
    ignored: list = IGNORED_WORDS,
    substitutions: dict | None = None,
    named_patterns: list[str] | None = None,
    **kwargs,
) -> str:
    """
    Format a singular column name.

    Args:
        name (str): The name of the column to format.
        ignored (list): A list of words to ignore when formatting the column name.
        substitutions (dict): A dictionary of words to substitute when formatting the column name.
        named_patterns (list): A list of named patterns to apply to the column name.
        **kwargs: Additional keyword arguments to pass to `clean_string_with_named_patterns`.
            - `attempt_cast_to_int`: Whether to attempt to cast the cleaned string to an int. Default is False.

    Returns:
        str: The formatted column name.
    """
    formatted_list = []

    if substitutions is None:
        substitutions = SUBSTITUTION_MAP

    if named_patterns is None:
        named_patterns = [
            "slash",
            "parentheses",
            "comma",
            "hyphens",
            "glottal_stop",
            "apostrophe",
        ]

    str_list = re.split(r"[\. ]+", name.lower())  # handle multiple delimiters
    for word in str_list:
        if word in ignored:
            continue

        # Appends sub word if in `substitutions` else original word
        substituted_word = substitutions.get(word, word)

        # Apply named patterns to the word
        if named_patterns:
            substituted_word = clean_string_with_named_patterns(
                substituted_word,
                *named_patterns,
                **kwargs,
            )

        # Appends the formatted word to the list
        formatted_list.append(substituted_word)

    return "_".join(formatted_list).strip("_")


def format_column_names(
    dataframe: DataFrame,
    named_patterns: list | None = None,
    **kwargs,
) -> DataFrame:
    """
    Format a list of column names.

    NOTE: Calls to `format_column_name` and `rename_columns` functions.

    Args:
        dataframe (DataFrame): The DataFrame containing the column names to format.
        named_patterns (list): A list of named patterns to apply to the column names.
        **kwargs: Additional keyword arguments to pass to `format_column_name`.

    Returns:
        DataFrame: The DataFrame with formatted column names.
    """
    return rename_columns(
        dataframe,
        [
            format_column_name(name, named_patterns=named_patterns, **kwargs)
            for name in dataframe.columns
        ],
    )


def format_column_values(
    dataframe: DataFrame,
    column: str,
    named_patterns: list[str] | str,
    return_dataframe: bool = False,
    **kwargs,
) -> None | DataFrame:
    """
    Format column values in a DataFrame, either in place or by returning the formatted DataFrame.

    Args:
        dataframe (DataFrame): The DataFrame to format.
        column (str): The column to format.
        named_patterns (list): A list of named patterns to apply to the column values.
        return_dataframe (bool): Whether to return the formatted DataFrame.
        **kwargs: Additional keyword arguments to pass to `clean_string_with_named_patterns`.

    Returns:
        None | DataFrame: The formatted DataFrame.
    """
    named_patterns = (
        [named_patterns] if isinstance(named_patterns, str) else named_patterns
    )
    for pattern in named_patterns:
        dataframe[column] = dataframe[column].apply(
            lambda x, pattern_keys=pattern: clean_string_with_named_patterns(
                x,
                pattern,
                **kwargs,
            ),
        )

    return dataframe if return_dataframe else None


def apply_column_value_formatting(
    dataframe: DataFrame,
    columns: list[str] | dict | str,
    named_patterns: list[str] | dict | str | None = None,
    **kwargs,
) -> DataFrame:
    """
    Format column values in a DataFrame using named patterns. Supports passing columns and patterns
    either as: a list; a dictionary where keys are columns and values are patterns; or a single pattern; or a string.

    Args:
        dataframe (DataFrame): The DataFrame to format.
        columns (list | dict | str): The columns to format.
        named_patterns (list | dict | str | None): The named patterns to apply to the columns.
        **kwargs: Additional keyword arguments to pass to `format_column_values`.

    Returns:
        DataFrame: The formatted DataFrame.
    """
    match (columns, named_patterns):
        # Single column, single or many pattern(s)
        case str() as column, _:
            format_column_values(dataframe, column, named_patterns, **kwargs)

        # Many columns, single pattern
        case list() as columns, str() as pattern:
            for column in columns:
                format_column_values(dataframe, column, pattern, **kwargs)

        # Many columns, many patterns
        case list() as columns, list() as patterns:
            for column, pattern in zip(columns, patterns):
                format_column_values(dataframe, column, pattern, **kwargs)

        # Mapping of columns to pattern(s)
        case dict() as column_pattern_map, _:
            for column, pattern in column_pattern_map.items():
                format_column_values(dataframe, column, pattern, **kwargs)

        # Default case (catches invalid inputs)
        case _:
            raise ValueError("Invalid input for columns and/or named_patterns.")

    return dataframe


def apply_column_formatting(dataframe: DataFrame) -> DataFrame:
    """
    Apply column formatting to a DataFrame.

    Args:
        dataframe (DataFrame): The DataFrame to format.

    Returns:
        DataFrame: The formatted DataFrame.
    """
    # Use first row as column names
    dataframe = promote_first_row_to_header(dataframe)
    dataframe.columns = format_column_names(dataframe)

    return dataframe.iloc[1:].reset_index(drop=True)


def apply_functions_to_dataframe(
    dataframe: DataFrame,
    functions: list[callable, tuple[callable, dict]],
) -> DataFrame:
    """
    Apply a list of functions to a DataFrame.

    Args:
        dataframe (DataFrame): The DataFrame to apply the functions to.
        functions (list): A list of functions to apply, where items are:
            - A callable function.
            - A tuple containing a callable function and a dictionary of keyword arguments.

    Returns:
        DataFrame: The DataFrame with the functions applied.
    """
    for func in functions:
        if isinstance(func, tuple):
            func_with_args, kwargs = func
            dataframe = func_with_args(dataframe, **kwargs)
        else:
            dataframe = func(dataframe)

    return dataframe


def replace_implicit_nan(
    dataframe: DataFrame,
    implicit_nan_labels: str | list[str] | re.Pattern,
    replacements: str | list[str] | dict[str, str] | None = None,
    cast_dtypes: bool = True,
) -> DataFrame:
    """
    Replace implicit NaN values--that is values that are not explicitly NaN but are intended to represent missing data (e.g. "Missing", "X", etc.)--in a DataFrame. Acts as a wrapper for the DataFrame's `replace` method.

    NOTE: Assumes regular expressions are used for `implicit_nan_labels` if the string starts with a backslash.

    Args:
        dataframe (DataFrame): The DataFrame to replace implicit NaN values in.
        implicit_nan_labels (str | list[str] | re.Pattern): The label(s) for implicit NaN values.
        replacements (str | list[str] | dict[str, str] | None): The replacement value(s) for implicit NaN values.
        cast_dtypes (bool): Whether to cast the DataFrame's dtypes after replacing implicit NaN values.

    Returns:
        DataFrame: The DataFrame with implicit NaN values replaced.
    """
    # Check if `implicit_nan_labels` is a regular expression
    use_regex = bool(implicit_nan_labels.startswith("\\"))

    # Apply replacements
    dataframe_replaced = dataframe.replace(
        implicit_nan_labels,
        replacements,
        regex=use_regex,
    )

    return dataframe_replaced.convert_dtypes() if cast_dtypes else dataframe_replaced


def rename_columns(
    dataframe: DataFrame,
    column_map: dict[str | int, str] | list[str],
) -> DataFrame:
    """
    Rename columns in a DataFrame, using either the column name or index as the key in the `column_map`. Alternatively, pass a list of new column names to rename each column in order.

    Args:
        dataframe (DataFrame): The DataFrame to rename columns in.
        column_map (dict | list): A dictionary mapping the current column names or indices to the new column names, or a list of new column names.

    Returns:
        DataFrame: The DataFrame with renamed columns.
    """
    current_columns = dataframe.columns.to_list()

    if isinstance(column_map, list):
        if len(column_map) != len(current_columns):
            raise ValueError(
                "Length of column_map list does not match the number of columns.",
            )
        column_map = dict(enumerate(column_map))

    for index, new_name in column_map.items():
        if isinstance(index, int):
            current_columns[index] = new_name
        elif isinstance(index, str):
            current_columns[current_columns.index(index)] = new_name

    dataframe.columns = current_columns
    return dataframe


def promote_first_row_to_header(dataframe: DataFrame) -> DataFrame:
    """
    Promote the first row of a DataFrame to be the column names.

    Args:
        dataframe (DataFrame): The DataFrame to format.

    Returns:
        DataFrame: The formatted DataFrame with the first row as column names.
    """
    return (
        dataframe.rename(columns=dataframe.iloc[0])
        .drop(dataframe.index[0])
        .reset_index(drop=True)
    )


def transpose_and_reset_index(dataframe: DataFrame) -> DataFrame:
    """
    Transpose a DataFrame, remove the index name, and reset the index.

    Args:
        dataframe (DataFrame): The DataFrame to transpose.

    Returns:
        DataFrame: The transposed and transformed DataFrame.
    """
    return dataframe.T.rename_axis(None).reset_index(drop=True)


def remove_rows_with_values(
    dataframe: DataFrame,
    values: list[str | float],
) -> DataFrame:
    """
    Remove rows from a DataFrame where the specified value(s) occurs in any column.

    Args:
        dataframe (DataFrame): The DataFrame to filter.
        values (list): The value(s) to remove rows containing.

    Returns:
        DataFrame: The DataFrame with rows containing the specified value(s) removed.
    """
    return dataframe.loc[
        ~dataframe.applymap(lambda x: x in values).any(axis=1)
    ].reset_index(drop=True)


def remove_columns_with_values(
    dataframe: DataFrame,
    values: list[str | float],
    match_condition: str = "any",
) -> DataFrame:
    """
    Remove columns from a DataFrame where the specified value(s) occurs in any or all row(s), depending on the match condition.

    Args:
        dataframe (DataFrame): The DataFrame to filter.
        values (list): The value(s) to remove columns containing.
        match_condition (str): The condition to match the values against.
            - 'any': Remove columns where any row contains the value.
            - 'all': Remove columns where all rows contain the value.

    Returns:
        DataFrame: The DataFrame with columns containing the specified value(s) removed.
    """
    if match_condition == "all":
        return dataframe.loc[:, ~dataframe.isin(values).all()]
    if match_condition == "any":
        return dataframe.loc[:, ~dataframe.isin(values).any()]

    raise ValueError("Invalid match condition. Must be 'any' or 'all'.")


def fill_column_missing_values(
    dataframe: DataFrame,
    column: str,
    fill_value: str | float | None = None,
    fill_method: str | None = None,
) -> DataFrame:
    """
    Fill missing values in a DataFrame with a specified value. Wrapper for the DataFrame's `fillna` method.

    NOTE: Serves a similar function to `replace_implicit_nan` but is more specific to filling missing values. May be deprecated and consolidated in the future.

    Args:
        dataframe (DataFrame): The DataFrame to fill missing values in.
        column (str): The column to fill missing values in.
        fill_value (str | int | float): The value to fill missing values with.
        fill_method (str): The method to use for filling missing values.
            - 'ffill': Forward fill missing values.
            - 'bfill': Backward fill missing values.

    Returns:
        DataFrame: The DataFrame with missing values filled.
    """
    if fill_method == "ffill":
        dataframe[column] = dataframe[column].ffill(axis=0)
    if fill_method == "bfill":
        dataframe[column] = dataframe[column].bfill(axis=0)
    if fill_method is None:
        dataframe[column] = dataframe[column].fillna(fill_value)

    return dataframe
