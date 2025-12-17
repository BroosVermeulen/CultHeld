# core/write_core_records.py
from datetime import date
from pathlib import Path

import duckdb
import pandas as pd

from utils.logging_config import get_logger

logger = get_logger(__name__)

DB_FILE = Path("data/core/events.duckdb")


def write_core_records(df: pd.DataFrame, as_of_date: str | None = None, table_name: str = "events") -> None:
    """
    Write a DataFrame to DuckDB, adding as_of_date.
    Overwrites existing rows for the same venue + as_of_date.
    Assumes df already has a 'venue' column.
    
    Args:
        df: DataFrame with event records
        as_of_date: ISO format date string (defaults to today)
        table_name: DuckDB table name
    """
    if as_of_date is None:
        as_of_date = date.today().isoformat()

    df = df.copy()
    df["as_of_date"] = as_of_date

    # Ensure required columns exist and enforce desired column order
    desired_cols = ['venue', 'event_name', 'start_date_time', 'ticket_url', 'price', 'as_of_date']
    for col in desired_cols:
        if col not in df.columns:
            df[col] = None

    # Move desired columns to front in the requested order, keep extras after
    other_cols = [c for c in df.columns if c not in desired_cols]
    df = df[desired_cols + other_cols]

    # Ensure DB folder exists
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(database=str(DB_FILE))

    # Create table if it doesn't exist
    try:
        con.execute(f"SELECT 1 FROM {table_name} LIMIT 1")
    except duckdb.CatalogException:
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df LIMIT 0")

    # Delete existing rows for each venue in this batch
    for v in df["venue"].unique():
        con.execute(f"""
            DELETE FROM {table_name} 
            WHERE venue = '{v}' AND as_of_date = '{as_of_date}'
        """)

    # Insert new rows
    con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    con.close()

    logger.info(f"Written {len(df)} rows for venues={df['venue'].unique().tolist()}, as_of_date={as_of_date}")
