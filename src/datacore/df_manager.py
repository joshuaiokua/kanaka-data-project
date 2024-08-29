"""
datacore/df_manager.py

Module for managing separate DataFrame objects that originate, or are somehow related to, the same data source (e.g. a single Excel file with multiple sheets).

TODO: classmethods for loading data from various sources (e.g. URL, file, etc.).???

Classes:
- DataFrameEntry
- DataFrameManager
"""

# External Imports
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Pattern

import re
import pandas as pd

# Local Imports
from src.datacore.loaders import load_data_from_url
from src.constants.mappings import PATTERN_MAP


### --- UTILS --- ###
def clean_string(string: str, *args: tuple[Pattern, str]) -> str:
    """
    Clean a string by removing unwanted characters.

    Args:
        string (str): The string to clean.
        *args (tuple): A tuple of regular expressions and their corresponding replacements.

    Returns:
        str: The cleaned string.
    """
    for pattern, replacement in args:
        string = re.sub(pattern, replacement, string)
    return string


### --- CLASSES --- ###
@dataclass
class DataFrameEntry:
    dataframe: pd.DataFrame
    name: Optional[str] = None
    original_sheet_name: Optional[str] = None
    last_modified: datetime = field(default_factory=datetime.now)
    tags: set = field(default_factory=set)  # (e.g. 'drop', 'cleaned', etc.)
    
    def _repr_html_(self) -> str:
        """
        Return an HTML representation of the DataFrameEntry object without the need to call to dataframe attribute.
        """
        if self.dataframe is not None:
            return self.dataframe._repr_html_()
        else:
            return "<i>Empty DataFrameEntry</i>"

class DataFrameManager:
    def __init__(self, source_url: str = None):
        self.dataframes = {}

        if source_url:
            self.load_from_url(source_url)

    def load_from_url(self, source_url: str) -> None:
        """
        Load data from a URL and store it in a DataFrame object.
        """
        raw_dataframes = pd.read_excel(load_data_from_url(source_url), sheet_name=None)

        if len(self.dataframes) > 0:
            raise ValueError("DataFrames already exist.")

        sheet_titles = self.get_sheet_titles(raw_dataframes, drop_title_sheet=True)

        for key, df in raw_dataframes.items():
            df_entry = DataFrameEntry(
                name=sheet_titles.get(key),
                dataframe=df.dropna(how="all").reset_index(drop=True),
                original_sheet_name=key,
            )

            if key.startswith("0"):
                key = int(key.split(".")[-1])

            self.dataframes[key] = df_entry

    def get_sheet_titles(self, df_dict: dict, drop_title_sheet: bool = False) -> dict:
        """
        Extract the titles of each sheet in the DataFrame dictionary.

        Args:
            df_dict (dict): A dictionary of DataFrames.
            drop_title_sheet (bool): Whether to drop the sheet containing the titles after extracting them.

        Returns:
            dict: A dictionary of table names and their corresponding table numbers.
        """

        table_name_pairs = {}

        for _, (table, table_name) in df_dict["Titles"].dropna().iterrows():
            if "Table" in table and table != "Table":
                table = "0" + table.split(" ")[-1]
                table_name = clean_string(table_name, PATTERN_MAP["glottal"])
                table_name_pairs[table] = table_name

        if drop_title_sheet:
            df_dict.pop("Titles")

        return table_name_pairs

    def __len__(self) -> int:
        return len(self.dataframes)
