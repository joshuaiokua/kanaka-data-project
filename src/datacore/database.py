"""
Functionality for working with local databases (i.e. `data/databases/`) primarily as it relates to simple demonstrations and prototyping rather than production-level applications.

Functions:
    load_local_database: Load a local SQLite database as a LangChain SQLDatabase object.
"""

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from src.constants.sources import DB_PATH


### --- FUNCTIONS --- ###
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
    engine = create_engine(
        f"sqlite:///{database_path}{database_name}.db",
        connect_args=connect_args or {"check_same_thread": False},
        poolclass=StaticPool,
        **kwargs,
    )
    return SQLDatabase(engine)
