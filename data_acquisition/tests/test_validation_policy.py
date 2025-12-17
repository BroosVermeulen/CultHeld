import sys
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd

from utils.validation import validate_records


def test_price_required_drops_missing_price():
    df = pd.DataFrame([
        {"venue": "Concertgebouw", "start_date_time": "2025-12-21 20:30", "ticket_url": "https://x", "price": None},
        {"venue": "Melkweg", "start_date_time": "2025-12-22 21:00", "ticket_url": "https://y", "price": None},
        {"venue": "Concertgebouw", "start_date_time": "2025-12-23 19:30", "ticket_url": "https://z", "price": 25.0},
    ])

    # Force only Concertgebouw to require price, independent of repo config
    validated = validate_records(df, price_required_venues=["Concertgebouw"])

    venues = validated["venue"].tolist()
    # Row 1 should be dropped (Concertgebouw with missing price)
    assert "Concertgebouw" in venues
    assert len(validated) == 2
    assert not validated[(validated["venue"] == "Concertgebouw") & (validated["price"].isna())].any().any()


def test_price_optional_keeps_missing_price_for_other_venues():
    df = pd.DataFrame([
        {"venue": "Melkweg", "start_date_time": "2025-12-22 21:00", "ticket_url": "https://y", "price": None},
    ])

    validated = validate_records(df, price_required_venues=["Concertgebouw"])  # Melkweg not required
    assert len(validated) == 1
    assert validated.iloc[0]["price"] is None
