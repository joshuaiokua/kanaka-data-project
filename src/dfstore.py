""""

DataFrame Store

This module contains the DataFrameStore class and related functionality. The DataFrameStore is a dictionary-like object that extends the Collections module's MutableMapping class to provide additional functionality for storing and manipulating data in a pandas DataFrame.

Author's Note: idk might spin this off into its own package, but for now it's just a module in the project because the data sources i'm working with are annoyingly packaged in a way that makes it hard to work with them in a more modular way

"""

# Local Imports
from src.data_loader import load_data_from_url

# External Imports
from dataclasses import dataclass, field
from datetime import datetime
from copy import deepcopy
from pandas import DataFrame
import pickle
from collections.abc import MutableMapping
from typing import Union, Any, Optional

### --- CLASSES --- ###
@dataclass
class DataFrameEntry:
    """
    A class for storing a DataFrame and related metadata.

    TODO: Think about adding functionality for when user does not want working data to be created by default. This would be useful for very large datasets where the user may not want to store a copy of the data in memory.
    """
    name: str
    _original_data: bytes = field(init=False, repr=False)
    _working_data: bytes = field(init=False, repr=False)
    has_working_data: bool = field(init=False)
    last_modified: datetime = field(default_factory=datetime.now)
    source_url: Optional[str] = None

    def __init__(self, name: str, original_data: Union[DataFrame, bytes], source_url: Optional[str] = None):
        self.name = name
        self._original_data = original_data if isinstance(original_data, bytes) else pickle.dumps(original_data)
        self._working_data = deepcopy(self._original_data)
        self.has_working_data = bool(self._working_data)
        self.last_modified = datetime.now()
        self.source_url = source_url

    def __setattr__(self, key, value) -> None:
        if key == '_original_data' and '_original_data' in self.__dict__:
            raise AttributeError('Cannot modify original data once set. Please create a new DataFrameEntry.')
        super().__setattr__(key, value)

    @property
    def original_data(self) -> bytes:
        return self._original_data
    
    @property
    def working_data(self) -> bytes:
        return self._working_data
    
    def load_working_data(self) -> DataFrame:
        if self.has_working_data:
            return pickle.loads(self._working_data)
        else:
            raise ValueError(f'No working data exists for {self.name}.')
        
    def update_working_data(self, new_data: DataFrame) -> None:
        if not isinstance(new_data, DataFrame):
            raise ValueError('Input data must be a pandas DataFrame.')
        self._working_data = pickle.dumps(new_data)
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