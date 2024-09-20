"""
DataCore Package

This package contains the modules that are responsible for data-related tasks, such as loading data from various sources, managing dataframes, and interacting with databases.

NOTE: (9/24) Extensive work on this package has been paused in favor of focusing on building out LLMCore functionality. The data-related tasks will be resumed, and this package will be further developed, after the initial LLMCore tasks are completed.
"""

from .database import load_df_from_local_database, load_local_database
from .df_manager import DataFrameManager, load_dataframe_from_db, load_json

__all__ = [
    "DataFrameManager",
    "load_dataframe_from_db",
    "load_json",
    "load_local_database",
    "load_df_from_local_database",
]
