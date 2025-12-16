from pathlib import Path
from datetime import datetime
import pandas as pd

RAW_CSV_DIR = Path("data/staging")
RAW_CSV_DIR.mkdir(parents=True, exist_ok=True)

def save_raw_csv(df: pd.DataFrame, scraper_name: str) -> Path:
    """Save raw scraped data to a timestamped CSV."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file = RAW_CSV_DIR / f"{scraper_name}_{timestamp}.csv"
    df.to_csv(csv_file, index=False)
    print(f"Saved raw CSV snapshot: {csv_file}")
    return csv_file
