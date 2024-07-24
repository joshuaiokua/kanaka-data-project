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
from pandas import DataFrame, ExcelFile, read_excel
import pickle
from collections.abc import MutableMapping
from typing import Union, Any, Optional, List

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
    """
    A dictionary-like object for storing DataFrameEntry objects.

    TODO: Listed below.
        - Figure out a way list all the keys in the store without using KeysView object and maybe making provide useful information about the data stored in the store
        - Updating entries in the store in a more user-friendly way
    """

    def __init__(self, data_source: Union[str, dict] = None, **kwargs):
        self._store = {}

        if data_source:
            self.load_data(data_source, **kwargs)

    def __setitem__(self, key: str, value: DataFrameEntry) -> None:
        if not isinstance(value, DataFrameEntry):
            raise ValueError('Value must be a DataFrameEntry object.')
        self._store[key] = value

    def __getitem__(self, key: str) -> DataFrameEntry:
        return self._store[key]
    
    def __delitem__(self, key: str) -> None:
        del self._store[key]

    def __iter__(self):
        return iter(self._store)
    
    def __len__(self) -> int:
        return len(self._store)
    
    def __repr__(self) -> str:
        return repr(self._store)
    
    def load_data(self, data_source: Union[str, dict], sheet_name_pairs: List[tuple] = None) -> None:
        """
        TODO: Listed below.
            - Add various data loading methods (e.g. from URL, from file, etc.). Currently defaults to loading excel file from URL given that's what I'm working with at OHA
            - Add support for loading data from a dictionary
            - Add func for getting specific sheet source
            - Add ability to preprocess working data upon loading while keeping original data intact
        """
        excel_file = ExcelFile(
            load_data_from_url(data_source)
            )
        
        if sheet_name_pairs:
            for sheet, name in sheet_name_pairs:
                self._store[name] = DataFrameEntry(name, read_excel(excel_file, sheet_name=sheet))
        else:
            for sheet in excel_file.sheet_names:
                self._store[sheet] = DataFrameEntry(sheet, read_excel(excel_file, sheet_name=sheet))
        
