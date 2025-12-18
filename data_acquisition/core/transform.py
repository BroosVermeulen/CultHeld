# core/write_core_records.py
from datetime import date
from pathlib import Path

import duckdb
import pandas as pd

from utils.logging_config import get_logger

logger = get_logger(__name__)

DB_FILE = Path("data/core/events.duckdb")


def write_core_records(
    df: pd.DataFrame, as_of_date: str | None = None, table_name: str = "events"
) -> None:
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
    desired_cols = [
        'venue', 'event_type', 'event_name', 'start_date_time', 'ticket_url', 'price', 'as_of_date'
    ]
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

    # Ensure schema has 'event_type'; add column if missing
    try:
        table_cols = [r[0] for r in con.execute(
            f"SELECT name FROM pragma_table_info('{table_name}')"
        ).fetchall()]
    except Exception:
        table_cols = []
    if 'event_type' not in table_cols:
        con.execute(f"ALTER TABLE {table_name} ADD COLUMN event_type VARCHAR")
        # refresh table_cols after schema change
        table_cols = [r[0] for r in con.execute(
            f"SELECT name FROM pragma_table_info('{table_name}')"
        ).fetchall()]

    # Delete existing rows for each venue in this batch
    for v in df["venue"].unique():
        con.execute(f"""
            DELETE FROM {table_name} 
            WHERE venue = '{v}' AND as_of_date = '{as_of_date}'
        """)

    # Insert new rows using explicit column list to avoid order mismatches
    insert_cols = ", ".join(table_cols)
    con.execute(f"INSERT INTO {table_name} ({insert_cols}) SELECT {insert_cols} FROM df")
    con.close()

    logger.info(
        f"Written {len(df)} rows for venues={df['venue'].unique().tolist()}, "
        f"as_of_date={as_of_date}"
    )
