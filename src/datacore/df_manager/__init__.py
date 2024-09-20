"""
Dataframe Manager Package

This package contains the modules that are responsible for implementing the Dataframe Manager class. DataFrameManager is used for managing multiple DataFrame objects that originate, or are somehow related to, the same data source (e.g. a single Excel file with multiple sheets).

NOTE: (9/24) Work on this package, and the data-cleaning tasks it helps with, has been paused in favor of focusing on LLM interactivity with a subset of the data already cleaned and preprocessed. The data cleaning tasks will be resumed, and this package will be further developed, after the initial LLM interactivity tasks are completed.
"""

from loaders import load_data_from_url, load_dataframe_from_db, load_json

from .base import DataFrameManager
from .entry import DataFrameEntry

__all__ = [
    "DataFrameManager",
    "DataFrameEntry",
    "load_json",
    "load_data_from_url",
    "load_dataframe_from_db",
]
