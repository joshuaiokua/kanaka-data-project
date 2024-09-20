"""
DataFrameManager Parsing Module

Functionality for parsing data from various sources, primarily for use in the DataFrameManager class.

TODO:
- Revisit extensive use of **kwargs
- Robust and customizable use of clean_string_with_named_patterns function
- Functionality to parse specific types of metadata (e.g. annotations, commentary, source)

Functions:
    extract_metadata: Extract metadata from a DataFrame.
    extract_section_ranges: Extract the start and end index ranges for sections in the DataFrame based on a given label.
"""

# External Libraries
from itertools import pairwise

from pandas import DataFrame

# Local Libraries
from src.utilities.string import clean_string_with_named_patterns


### --- FUNCTIONS --- ###
def extract_metadata(
    df: DataFrame,
    column_idx: int = 0,
    remove_rows: bool = True,
) -> tuple[set[str], DataFrame]:
    """
    Extract metadata (e.g. annotations, commentary, source) from a DataFrame.
    NOTE: Assumes that metadata rows have all NaN except in the specified column.

    Args:
        df (pd.DataFrame): The DataFrame from which to extract metadata.
        column_idx (int): The index of the column expected to contain non-NaN values in metadata rows.
        remove_rows (bool): Whether to return the DataFrame with the metadata rows removed.

    Returns:
        tuple[set[str], pd.DataFrame]: A set containing the extracted metadata and the DataFrame with metadata rows removed (if specified).
    """
    # Find rows where all NaN except specified column
    mask = df.iloc[:, 1:].isna().all(axis=1)

    # Extract unique metadata values from specified column
    metadata = set(
        df.loc[mask, df.columns[column_idx]]
        .dropna()
        .str.strip()
        .apply(
            lambda x: clean_string_with_named_patterns(
                x,
                "glottal_stop",
                "bullet",
                "newline",
                "non_breaking_space",
            ),
        ),
    )

    # Optionally remove metadata rows from original DataFrame
    return metadata, df[~mask].reset_index(drop=True) if remove_rows else df


def extract_section_ranges(
    dataframe: DataFrame,
    section_label: str,
) -> list[tuple[int, int]]:
    """
    Extract the start and end index ranges for sections in the DataFrame based on a given label.

    NOTE: Ranges should be passed to a DataFrame using iloc.

    Args:
        dataframe (pd.DataFrame): The DataFrame to process.
        section_label (str): The label used to identify the sections.

    Returns:
        list: A list of tuples, where each tuple contains the start and end index for the identified subsets.
    """
    return pairwise([
        *dataframe.index[dataframe.iloc[:, 0] == section_label].tolist(),
        dataframe.shape[0],  # Add the final row as the end of the last section
    ])
