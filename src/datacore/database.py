"""
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


def load_df_from_local_db(
    table_name: str,
    database_name: str,
    database_path: str = DB_PATH,
) -> DataFrame:
    """
    Load a pandas DataFrame from a local SQLite database.

    Args:
        table_name (str): The name of the table in the database.
        database_name (str): The name of the .db file.
        database_path (str, optional): The path to the .db file. Defaults to `DB_PATH` (i.e. "data/databases/").

    Returns:
        DataFrame: The loaded DataFrame.
    """
    # Validate table name
    if not is_valid_table_name(table_name):
        msg = f"Invalid table name: {table_name}"
        raise ValueError(msg)

    engine = create_local_engine(
        database_file_path=f"{database_path}/{database_name}.db",
    )

    with engine.connect() as connection:
        return read_sql(
            f"SELECT * FROM {table_name}",  # noqa: S608
            connection,
        )
