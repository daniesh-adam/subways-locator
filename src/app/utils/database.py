"""
Helper functions to perform database operations
"""

from typing import List, Dict
import sqlite3
from contextlib import closing


def create_table(db_path: str, table_name: str) -> None:
    """
    Creates a new table in the SQLite database.

    Args:
        db_path (str): The path to the SQLite database file.
        table_name (str): The name of the table to be created.
    """
    with closing(sqlite3.connect(db_path)) as conn:
        with conn as cur:
            cur.execute(f"""CREATE TABLE {table_name} (
                    name text,
                    address text,
                    operating_hours text,
                    waze_link text,
                    latitude real,
                    longitude real
                )""")


def get_all(db_path: str, table_name: str) -> List[Dict]:
    """
    Queries the SQLite database and returns all records.

    Args:
        db_path (str): The path to the SQLite database file.
        table_name (str): The name of the table to query.

    Returns:
        List[Dict]: A list of dictionaries representing the rows in the table.
    """
    with closing(sqlite3.connect(db_path)) as conn:
        conn.row_factory = sqlite3.Row
        with conn as cur:
            # Select all records from defined table
            records = cur.execute(f"SELECT * FROM {table_name}").fetchall()
            # Convert records to list of dictionaries
            records = [dict(record) for record in records]
    return records


def add_many_to_table(db_path: str, table_name: str, data: list) -> None:
    """
    Inserts multiple records into a table in the SQLite database.

    Args:
        db_path (str): The path to the SQLite database file.
        table_name (str): The name of the table to insert data into.
        data (list): A list of tuples representing the records to insert.
    """
    with closing(sqlite3.connect(db_path)) as conn:
        with conn as cur:
            query = f"INSERT INTO {table_name} VALUES (?,?,?,?,?,?)"
            cur.executemany(query, data)


def delete_table(db_path: str, table_name: str) -> None:
    """
    Deletes a table from the SQLite database.

    Args:
        db_path (str): The path to the SQLite database file.
        table_name (str): The name of the table to delete.
    """
    with closing(sqlite3.connect(db_path)) as conn:
        with conn as cur:
            # Delete a Table
            cur.execute(f"""DROP TABLE IF EXISTS {table_name}""")
