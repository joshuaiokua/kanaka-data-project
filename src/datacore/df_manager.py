"""
datacore/df_manager.py

Module for managing separate DataFrame objects that originate, or are somehow related to, the same data source (e.g. a single Excel file with multiple sheets).

TODO:
- Revisit extensive use of **kwargs
- Summary information functionality of entries for the DataFrameManager class
- Implement a method to drop DataFrames from the DataFrameManager
- Implement a method to clean DataFrames in the DataFrameManager
- Loading from file path
- Loading from multiple URLs
- "Smart" recognition of DataFrameManager source (e.g. URL, file path, etc.) and source type (e.g. Excel, CSV, etc.)
- Revisit extract_years_from_string function for more robust year extraction


Class Method Overview:
- from_url(cls, source_url: str, **kwargs) -> "DataFrameManager": Create a DataFrameManager instance from a URL.
"""

# External Imports
import re
from collections import defaultdict
from functools import cached_property

import pandas as pd

from src.constants.mappings import THEME_MAP

# Local Imports
from src.datacore.df_entry import DataFrameEntry
from src.datacore.loaders import load_data_from_url
from src.datacore.parsing import extract_metadata
from src.utilities.string import (
    clean_string_with_named_patterns,
    extract_years_from_string,
)


### --- CLASSES --- ###
class DataFrameManager(dict):
    """
    DataFrameManager class for managing multiple DataFrame objects that originate, or are somehow related to, the same data source (e.g. a single Excel file with multiple sheets). Inherits from dict.
    """

    def __init__(self, dataframes: dict[str, DataFrameEntry] | None = None) -> None:
        """
        Initialize a DataFrameManager instance with an optional dictionary of DataFrameEntry objects.
        """
        super().__init__(dataframes or {})

    @classmethod
    def from_url(cls, source_url: str, **kwargs) -> "DataFrameManager":
        """
        Create a DataFrameManager instance from a URL.

        Args:
            source_url (str): The URL of the data source.
            kwargs: Additional keyword arguments.

        Returns:
            DataFrameManager: An instance of DataFrameManager populated with DataFrameEntry objects from the source.
        """
        instance = cls()
        instance.load_from_url(source_url, **kwargs)
        return instance

    @classmethod
    def from_excel(cls, file_path: str, **kwargs) -> "DataFrameManager":
        """
        Create a DataFrameManager instance from an Excel file.

        Args:
            file_path (str): The path to the Excel file.
            kwargs: Additional keyword arguments.

        Returns:
            DataFrameManager: An instance of DataFrameManager populated with DataFrameEntry objects from the Excel file.
        """
        instance = cls()
        instance.load_from_excel(file_path, **kwargs)
        return instance

    def load_from_url(self, source_url: str, overwrite: bool = False, **kwargs) -> None:
        """
        Load data from a URL and store it as a series of DataFrameEntry objects within the DataFrameManager.

        Args:
            source_url (str): The URL of the data source.
            overwrite (bool): Whether to overwrite existing DataFrames in the DataFrameManager.
            **kwargs: Additional keyword arguments.
        """
        if not overwrite and self:
            raise ValueError(
                "DataFrames already exist. Use 'overwrite=True' to replace them.",
            )

        # Load dataframes from URL
        raw_df_dict = pd.read_excel(
            pd.ExcelFile(load_data_from_url(source_url)),
            sheet_name=None,
        )
        self._process_raw_dataframes(raw_df_dict, **kwargs)

    def load_from_excel(
        self, excel_file: str, overwrite: bool = False, **kwargs
    ) -> None:
        """
        Load data from an Excel file and store it as a series of DataFrameEntry objects within the DataFrameManager.

        Args:
            excel_file (str): The path to the Excel file.
            overwrite (bool): Whether to overwrite existing DataFrames in the DataFrameManager.
            **kwargs: Additional keyword arguments.
        """
        if not overwrite and self:
            raise ValueError(
                "DataFrames already exist. Use 'overwrite=True' to replace them.",
            )

        # Load dataframes from Excel file
        raw_df_dict = pd.read_excel(
            pd.ExcelFile(excel_file),
            sheet_name=None,
        )
        self._process_raw_dataframes(raw_df_dict, **kwargs)

    def _process_raw_dataframes(self, raw_df_dict: dict, **kwargs) -> None:
        """
        Process raw dataframes and store them as DataFrameEntry objects in the DataFrameManager.

        Args:
            raw_df_dict (dict): Dictionary of raw DataFrames.
            kwargs: Additional keyword arguments.
        """
        # Extract table names and themes, handle title sheets, etc.
        titles_sheet_name = self.find_titles_sheet_name(raw_df_dict.keys(), **kwargs)
        table_names_and_themes = self.extract_table_names(
            raw_df_dict,
            titles_sheet_name,
            **kwargs,
        )

        if kwargs.get("drop_title_sheet", False) and titles_sheet_name:
            raw_df_dict.pop(titles_sheet_name, None)

        int_key = 1
        for key, df in raw_df_dict.items():
            table_info = table_names_and_themes.get(key, {})
            table_name = table_info.get("name", key)
            table_theme = table_info.get("theme", None)
            metadata, extracted_df = extract_metadata(
                df.dropna(how="all").reset_index(drop=True),
            )

            df_entry = DataFrameEntry(
                dataframe=extracted_df,
                name=table_name,
                original_sheet_name=key,
                years_covered=(
                    extract_years_from_string(table_name) if table_name else []
                ),
                metadata=self.categorize_metadata(metadata),
                tags={table_theme} if table_theme else set(),
            )

            if key != "Introduction":
                self[int_key] = df_entry
                int_key += 1
            else:
                self[key] = df_entry

    def extract_table_names(
        self,
        df_dict: dict[str, pd.DataFrame],
        titles_sheet_name: str,
        title_cleaning_patterns: list[str] | None = None,
        **kwargs,
    ) -> dict[str, str]:
        """
        Extract table names (i.e. sheet titles) from a dictionary of DataFrames if a 'Titles' sheet is present.

        Args:
            df_dict (dict[str, pd.DataFrame]): A dictionary of DataFrames as returned by pd.read_excel when sheet_name=None.
            titles_sheet_name (str): The name of the sheet containing the table names.
            title_cleaning_patterns (list[str]): A list of patterns mapped to PATTERN_MAP in constants/mappings.py.
            **kwargs: Additional keyword arguments.
                - title_sheet_type (str): The type of sheet containing the table names.

        Returns:
            dict[str, str]: A dictionary of sheet names and their corresponding titles.

        Raises:
            KeyError: If the title sheet name is None or is not found in the DataFrame dictionary.
        """

        # Define helper function to allow for vectorization
        def process_titles_row(row: pd.Series) -> pd.Series:
            table = row.iloc[0]
            table_name = row.iloc[1]

            # Handle normal title sheets
            if title_sheet_type == "normal":
                if "Table" in table and table != "Table":
                    table = "0" + table.split(" ")[-1]
                    if title_cleaning_patterns:
                        table_name = clean_string_with_named_patterns(
                            table_name,
                            *title_cleaning_patterns,
                        )
                    return pd.Series([table, None, table_name])
                if "Introduction" in table:
                    return pd.Series(["Introduction", None, table_name])

                return pd.Series([None, None, None])

            # Handle wiki-style title sheets
            if title_sheet_type == "wiki":
                theme_code = (
                    re.match(r"^[A-Z]+", table).group()
                    if re.match(r"^[A-Z]+", table)
                    else None
                )
                theme = THEME_MAP.get(theme_code, None)

                # Clean the table name if patterns are provided
                if title_cleaning_patterns:
                    table_name = clean_string_with_named_patterns(
                        table_name,
                        *title_cleaning_patterns,
                    )

                if "Introduction" in table:
                    table = "Introduction"
                else:
                    table = clean_string_with_named_patterns(table, "hyphens")

                return pd.Series([table, theme, table_name])

            # Return None if sheet type is unrecognized
            return pd.Series([None, None, None])

        # Extract table names from the titles sheet
        title_cleaning_patterns = (
            title_cleaning_patterns
            if title_cleaning_patterns
            else kwargs.get("title_cleaning_patterns")
        )
        title_sheet_type = kwargs.get("title_sheet_type", "normal")

        title_df = df_dict[titles_sheet_name].dropna()
        table_rows = title_df.iloc[
            title_df.iloc[:, 0].str.contains("Table", na=False).idxmax() - 2 :
        ]

        return (
            table_rows.apply(process_titles_row, axis=1)
            .set_index(0)
            .rename(columns={1: "theme", 2: "name"})
            .to_dict(orient="index")
        )

    @staticmethod
    def clean_key_format(key: str) -> str:
        """
        Clean up the key format if following "00.00" format.

        TODO: Maybe remove.

        Args:
            key (str): The key to clean.

        Returns:
            str: The cleaned key.
        """
        if re.match(r"^\d{2}\.\d{2}$", key):
            return int(key.split(".")[-1])
        return key

    @staticmethod
    def categorize_metadata(metadata_set: set[str]) -> dict:
        """
        Categorize metadata into 'source' and 'notes' based on content.

        Args:
            metadata_set (set[str]): A set of metadata strings to categorize.

        Returns:
            dict: A dictionary with keys 'source' and 'notes', where 'source' is a single string or list of sources, and 'notes' is a list of notes.
        """
        metadata_dict = defaultdict(list)

        while metadata_set:
            item = metadata_set.pop()
            if item.lower().startswith("source"):
                metadata_dict["source"].append(item.split(":", 1)[-1].strip())
            else:
                metadata_dict["notes"].append(item)

        # Convert source list to a single string if only one source is found
        if len(metadata_dict["source"]) == 1:
            metadata_dict["source"] = metadata_dict["source"][0]

        return dict(metadata_dict)

    @staticmethod
    def find_titles_sheet_name(df_dict_keys: list[str], **kwargs) -> str:
        """
        Find the title sheet name from a list of DataFrame dictionary keys or a specified keyword argument.

        NOTE: Assumes that title sheet is not case-sensitive. Need to revisit this assumption in the future.

        Args:
            df_dict_keys (list[str]): A list of keys from the DataFrame dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            str: The title sheet name if found, otherwise raises a KeyError.
        """
        # First handle kwarg for titles sheet name
        if "titles_sheet_name" in kwargs:
            return kwargs.get("titles_sheet_name")

        # Check for 'titles' or 'title' in the keys
        for key in df_dict_keys:
            if "Titles" in key or "Title" in key:
                return key

        raise KeyError("Title sheet name not found in the DataFrame dictionary.")

    def __iter__(self) -> iter:
        """
        Override the default iterator to return the DataFrameEntry objects instead of the keys.
        """
        return iter(self.values())

    @cached_property
    def dataframe_names(self) -> list:
        """
        Return a cached list of dataframe names in the DataFrameManager.
        NOTE: This property is cached to avoid recalculating the list each time it is accessed, however it will not update if DataFrames are added or removed.
        """
        return [df.name for df in self if df.name is not None]

    def list_dataframes(self) -> None:
        """
        Print a list of DataFrame names in the DataFrameManager.
        """
        for df in self.dataframe_names:
            print(df)
