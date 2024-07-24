""""

DataFrame Store

This module contains the DataFrameStore class and related functionality. The DataFrameStore is a dictionary-like object that extends the Collections module's MutableMapping class to provide additional functionality for storing and manipulating data in a pandas DataFrame.

"""

# Local Imports
from src.data_loader import load_data_from_url

# External Imports
from dataclasses import dataclass, field
from datetime import datetime
from copy import deepcopy
import pandas as pd
import pickle
from collections.abc import MutableMapping
from typing import Union, Any

### --- CLASSES --- ###
@dataclass
class DataFrameEntry:
    """
    A class for storing a DataFrame and related metadata.
    """
    name: str
    original_data: bytes = field(repr=False)
    working_data: bytes = field(init=False, repr=False)
    has_working_data: bool = field(init=False)
    last_modified: datetime = field(default_factory=datetime.now)
    source_url: str = None

    def __post_init__(self):
        self.working_data = deepcopy(self.original_data)
        self.has_working_data = bool(self.working_data)

    def load_original_data(self) -> pd.DataFrame:
        return pickle.loads(self.original_data)
    
    def load_working_data(self) -> pd.DataFrame:
        if self.has_working_data:
            return pickle.loads(self.working_data)
        else:
            raise ValueError(f'No modified data exists for {self.name}.')
        
    def update_working_data(self, new_data: pd.DataFrame) -> None:
        self.working_data = pickle.dumps(new_data)
        self.last_modified = datetime.now()

    def export_working_data(self, file_path: str) -> None:
        with open(file_path, 'wb') as file:
            file.write(self.working_data)


class DataFrameStore(MutableMapping):

    def __init__(self, data_source: Union[str, dict] = None):
        self._store = {}

        if data_source:
            self.load_data(data_source)

    def __setitem__(self, key: Any, value: Any) -> None:
        return super().__setitem__(key, value)