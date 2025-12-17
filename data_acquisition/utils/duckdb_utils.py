from pathlib import Path

import duckdb
import pandas as pd

# Path to your DuckDB database
DB_FILE = Path(__file__).parent.parent / "events.duckdb"

def get_connection():
    """
    Return a DuckDB connection to the events.duckdb file.
    """
    con = duckdb.connect(database=str(DB_FILE))
    return con

def run_query(query: str) -> pd.DataFrame:
    """
    Run a SQL query and return a pandas DataFrame.
    """
    con = get_connection()
    df = con.execute(query).fetchdf()
    con.close()
    return df

def export_table_to_csv(table_name: str, output_file: str):
    """
    Export a DuckDB table to a CSV file.
    """
    con = get_connection()
    con.execute(f"COPY {table_name} TO '{output_file}' (HEADER, DELIMITER ',')")
    con.close()
