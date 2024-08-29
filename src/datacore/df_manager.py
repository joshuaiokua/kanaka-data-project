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


Class Method Overview:
- 
"""

# External Imports
import re
import pandas as pd
from functools import cached_property

# Local Imports
from src.datacore.df_entry import DataFrameEntry
from src.datacore.loaders import load_data_from_url
from src.datacore.parsing import extract_metadata
from src.utils import clean_string_with_patterns, extract_years_from_string


### --- CLASSES --- ###
class DataFrameManager(dict):
    """
    DataFrameManager class for managing multiple DataFrame objects that originate, or are somehow related to, the same data source (e.g. a single Excel file with multiple sheets). Inherits from dict.
    """

    def __init__(self, dataframes: dict[str, DataFrameEntry] = None) -> None:
        super().__init__(dataframes or {})

    @classmethod
    def from_url(cls, source_url: str, **kwargs) -> "DataFrameManager":
        """
        Create a DataFrameManager instance from a URL.

        Args:
            source_url (str): The URL of the data source.

        Returns:
            DataFrameManager: An instance of DataFrameManager populated with DataFrameEntry objects from the source.
        """
        instance = cls()
        instance.load_from_url(source_url, **kwargs)
        return instance

    def load_from_url(self, source_url: str, overwrite: bool = False, **kwargs) -> None:
        """
        Load data from a URL and store it as a series of DataFrameEntry objects within the DataFrameManager.

        Args:
            source_url (str): The URL of the data source.
            overwrite (bool): Whether to overwrite existing DataFrames in the DataFrameManager.
            **kwargs: Additional keyword arguments.
                - titles_sheet_name (str): The name of the sheet containing the table names.
                - title_cleaning_patterns (list[str]): List regex patterns.
                - drop_title_sheet (bool): Flag to drop title sheet after extracting table names.

        Raises:
            ValueError: If DataFrames already exist and overwrite is set to False.
        """
        if not overwrite and self:
            raise ValueError(
                "DataFrames already exist. Use 'overwrite=True' to replace them."
            )

        # Load dataframes, lowercasing the keys
        raw_df_dict = {
            key.lower(): value
            for key, value in pd.read_excel(
                pd.ExcelFile(load_data_from_url(source_url)), sheet_name=None
            ).items()
        }

        # Extract table names given kwarg or 'title(s)' as titles_sheet_name
        titles_sheet_name = self.find_titles_sheet_name(raw_df_dict.keys(), **kwargs)
        table_names = self.extract_table_names(raw_df_dict, titles_sheet_name, **kwargs)

        # Drop the titles sheet if specified
        if kwargs.get("drop_title_sheet", False) and titles_sheet_name:
            raw_df_dict.pop(titles_sheet_name, None)

        for key, df in raw_df_dict.items():
            
            table_name = table_names.get(key)
            metadata, df = extract_metadata(
                df.dropna(how="all").reset_index(drop=True), **kwargs
            )
            
            df_entry = DataFrameEntry(
                dataframe=df,
                name=table_name,
                original_sheet_name=key,
                years_covered=(
                    extract_years_from_string(table_name) if table_name else []
                ),
                metadata=metadata,
            )

            # Clean up the key if following "00.00" format
            key = self.clean_key_format(key)

            self[key] = df_entry

    def extract_table_names(
        self,
        df_dict: dict[str, pd.DataFrame],
        titles_sheet_name: str,
        title_cleaning_patterns: list[str] = None,
        **kwargs,
    ) -> dict[str, str]:
        """
        Extract table names (i.e. sheet titles) from a dictionary of DataFrames if a 'Titles' sheet is present.

        Args:
            df_dict (dict[str, pd.DataFrame]): A dictionary of DataFrames as returned by pd.read_excel when sheet_name=None.
            title_sheet_name (str): The name of the sheet containing the table names.
            title_cleaning_patterns (list[str]): A list of patterns mapped to PATTERN_MAP in constants/mappings.py.
            **kwargs: Additional keyword arguments.
                - title_cleaning_patterns (list[str]): A list of patterns mapped to PATTERN_MAP in constants/mappings.py.

        Returns:
            dict[str, str]: A dictionary of sheet names and their corresponding titles.

        Raises:
            KeyError: If the title sheet name is None or is not found in the DataFrame dictionary.
        """

        # Define helper function to allow for vectorization
        def process_titles_row(row):
            cleaning_patterns = (
                kwargs.get("title_cleaning_patterns") or title_cleaning_patterns
            )

            table = row.iloc[0]
            table_name = row.iloc[1]  # Assuming table name is in next column

            if "Table" in table and table != "Table":
                table = "0" + table.split(" ")[-1]
                if cleaning_patterns:
                    table_name = clean_string_with_patterns(
                        table_name, *cleaning_patterns
                    )
                return pd.Series([table, table_name])
            return pd.Series([None, None])

        if not titles_sheet_name or df_dict.get(titles_sheet_name) is None:
            raise KeyError("Title sheet name not found in the DataFrame dictionary.")

        title_df = df_dict[titles_sheet_name].dropna(how="all")
        table_rows = title_df[title_df.iloc[:, 0].str.contains("Table", na=False)]

        return (
            table_rows.apply(process_titles_row, axis=1)
            .dropna()
            .set_index(0)
            .squeeze()
            .to_dict()
        )

    @staticmethod
    def clean_key_format(key: str) -> str:
        """
        Clean up the key format if following "00.00" format.

        Args:
            key (str): The key to clean.

        Returns:
            str: The cleaned key.
        """
        if re.match(r"^\d{2}\.\d{2}$", key):
            return int(key.split(".")[-1])
        return key

    @staticmethod
    def find_titles_sheet_name(df_dict_keys: list[str], **kwargs) -> str:
        """
        Find the title sheet name from a list of DataFrame dictionary keys or a specified keyword argument.

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
            if "titles" in key or "title" in key:
                return key

        raise KeyError("Title sheet name not found in the DataFrame dictionary.")

    @cached_property
    def dataframe_names(self) -> list:
        """
        Return a cached list of dataframe names in the DataFrameManager.
        NOTE: This property is cached to avoid recalculating the list each time it is accessed, however it will not update if DataFrames are added or removed.
        """
        return [df.name for df in self.values() if df.name is not None]

    def list_dataframes(self) -> None:
        """
        Print a list of DataFrame names in the DataFrameManager.
        """
        for df in self.dataframe_names:
            print(df)
