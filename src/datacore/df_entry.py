"""
datacore/df_entry.py

Module for DataFrame entry functionality.

TODO:
- Functionality to consolidate __str__ and __repr__ methods for DataFrameEntry

"""

# External Imports
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import pandas as pd


### --- CLASSES --- ###
@dataclass
class DataFrameEntry:
    """
    Dataclass for storing a DataFrame object along with metadata.
    """

    dataframe: pd.DataFrame
    name: Optional[str] = None
    original_sheet_name: Optional[str] = None
    years_covered: Optional[list[int]] = field(default_factory=list)
    metadata: Optional[dict] = field(default_factory=dict)
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

    def __repr__(self) -> str:
        return (
            f"DataFrameEntry(\n"
            f"    name='{self.name}',\n"
            f"    original_sheet_name='{self.original_sheet_name}',\n"
            f"    years_covered={self.years_covered},\n"
            f"    metadata={self.metadata},\n"
            f"    last_modified={self.last_modified},\n"
            f"    tags={self.tags}\n"
            f")"
        )

    def __str__(self) -> str:
        # Prepare metadata for printing
        if self.metadata:
            formatted_metadata = []
            for key, value in self.metadata.items():
                if isinstance(value, list):
                    formatted_items = "\n      - ".join(value)
                    formatted_metadata.append(f"{key.capitalize()}:\n      - {formatted_items}")
                else:
                    formatted_metadata.append(f"{key.capitalize()}: {value}")
            formatted_metadata = "\n    ".join(formatted_metadata)
        else:
            formatted_metadata = "None"

        return (
            f"DataFrameEntry: {self.name}\n"
            f"  Original Sheet: {self.original_sheet_name}\n"
            f"  Years Covered: {self.years_covered}\n"
            f"  Metadata: \n    {formatted_metadata}\n"
            f"  Last Modified: {self.last_modified}\n"
            f"  Tags: {', '.join(self.tags) if self.tags else 'None'}"
        )
        
    def info(self) -> None:
        """
        Print the DataFrameEntry object in a human-readable format.
        """
        print(self)
