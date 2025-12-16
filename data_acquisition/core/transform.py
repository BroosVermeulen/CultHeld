# core/write_core_records.py
import duckdb
from pathlib import Path

DB_FILE = Path("data/core/events.duckdb")

def write_core_records(df, as_of_date=None, table_name="events"):
    """
    Write a DataFrame to DuckDB, adding as_of_date.
    Overwrites existing rows for the same venue + as_of_date.
    Assumes df already has a 'venue' column.
    """
    from datetime import date

    if as_of_date is None:
        as_of_date = date.today().isoformat()

    df = df.copy()
    df["as_of_date"] = as_of_date

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

    print(f"Written {len(df)} rows for venues={df['venue'].unique().tolist()}, as_of_date={as_of_date}")
