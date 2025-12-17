import sys
import pathlib
from pathlib import Path

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import duckdb
import pandas as pd

import core.transform as transform


def test_write_core_records_column_order(tmp_path):
    # Prepare DataFrame with shuffled columns and an extra field
    df = pd.DataFrame([
        {
            "ticket_url": "https://example/event",
            "venue": "Test Venue",
            "start_date_time": "2025-12-21 20:30",
            "event_name": "Example Event",
            "extra_col": "extra",
            "price": 12.5,
        }
    ])

    # Write to a temporary DuckDB file by monkeypatching the module constant
    db_file = tmp_path / "events.duckdb"
    original_db = transform.DB_FILE
    try:
        transform.DB_FILE = Path(db_file)
        transform.write_core_records(df, as_of_date="2025-12-16")
    finally:
        transform.DB_FILE = original_db

    # Verify column order in the created table
    con = duckdb.connect(database=str(db_file))
    cols = [r[1] for r in con.execute("PRAGMA table_info('events')").fetchall()]
    con.close()

    # Desired order must lead the table
    assert cols[:6] == [
        "venue",
        "event_name",
        "start_date_time",
        "ticket_url",
        "price",
        "as_of_date",
    ]
