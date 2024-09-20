"""
Database Functionality

Functionality for working with local databases (i.e. `data/databases/`) primarily as it relates to simple demonstrations and prototyping rather than production-level applications.

Functions:
    load_local_database: Load a local SQLite database as a LangChain SQLDatabase object.
"""

from langchain_community.utilities import SQLDatabase
from pandas import DataFrame, read_sql
from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import StaticPool

from src.constants.sources import DB_PATH

from .utils import is_valid_table_name


### --- FUNCTIONS --- ###
def create_local_engine(
    database_file_path: str,
    connect_args: dict | None = None,
    poolclass: type = StaticPool,
    **kwargs,
) -> Engine:
    """
    Create a SQLAlchemy engine for a local SQLite database.

    Args:
        database_file_path (str): The path to the .db file.
        connect_args (dict, optional): Additional connection arguments to pass to the `create_engine` function. If `None`, defaults to `{"check_same_thread": False}`.
        poolclass (type, optional): The class to use for pooling connections. Defaults to `StaticPool`.
        kwargs: Additional keyword arguments to pass to the `create_engine` function.
    """
    return create_engine(
        f"sqlite:///{database_file_path}",
        connect_args=connect_args or {"check_same_thread": False},
        poolclass=poolclass,
        **kwargs,
    )


def load_local_database(
    database_name: str,
    database_path: str = DB_PATH,
    connect_args: dict | None = None,
    **kwargs,
) -> SQLDatabase:
    """
    Load a local SQLite database as a LangChain SQLDatabase object.

    Args:
        database_name (str): The name of the .db file.
        database_path (str, optional): The path to the .db file. Defaults to `DB_PATH` (i.e. "data/databases/").
        connect_args (dict, optional): Additional connection arguments to pass to the `create_engine` function. If `None`, defaults to `{"check_same_thread": False}`.
        kwargs: Additional keyword arguments to pass to the `create_engine` function.

    Returns:
        SQLDatabase: The database object.
    """
    return SQLDatabase(
        create_local_engine(
            f"{database_path}/{database_name}.db",
            connect_args=connect_args or {"check_same_thread": False},
            poolclass=StaticPool,
            **kwargs,
        ),
    )


def load_df_from_local_database(
    database_name: str,
    query: str | None = None,
    table_name: str | None = None,
    database_path: str = DB_PATH,
) -> DataFrame:
    """
    Load a pandas DataFrame from a local SQLite database.

    Args:
        database_name (str): The name of the .db file.
        query (str, optional): A custom SQL query to execute to load the data; presumably a subset of the table. Defaults to `None`.
        table_name (str, optional): The name of the table to load. Defaults to `None`.
        database_path (str, optional): The path to the .db file. Defaults to `DB_PATH` (i.e. "data/databases/").

    Returns:
        DataFrame: The loaded DataFrame.
    """
    # Validate table name
    if table_name and not is_valid_table_name(table_name):
        msg = f"Invalid table name: {table_name}"
        raise ValueError(msg)

    # Validate query and table name
    shared_msg = "Use `query` to load a subset of the table and `table_name` to load the table in its entirety."
    if query and table_name:
        msg = f"Cannot specify both `query` and `table_name`. {shared_msg}"
        raise ValueError(msg)
    if not query and not table_name:
        msg = f"Must specify either `query` or `table_name`. {shared_msg}"
        raise ValueError(msg)

    engine = create_local_engine(
        database_file_path=f"{database_path}/{database_name}.db",
    )

    with engine.connect() as connection:
        return read_sql(
            f"SELECT * FROM {table_name}" if query is None else query,  # noqa: S608
            connection,
        )
