import pandas as pd

from utils.staging_utils import save_raw_csv
from staging.paradiso import paradiso
from mapping.paradiso_mapping import map_paradiso
from core.transform import write_core_records

# List of scrapers and their corresponding mapping functions
SCRAPERS = [
    (paradiso, map_paradiso),
    # (scrape_other, map_other),
]


def run_all_scrapers():
    for scraper_func, map_func in SCRAPERS:
        print(f"Running scraper: {scraper_func.__name__}")

        # Step 1: get raw data
        df_raw = scraper_func()
        print(f"Scraped {len(df_raw)} rows")
        save_raw_csv(df_raw, scraper_func.__name__)

        # Step 2: apply mapping
        df_core = df_raw.apply(map_func, axis=1)
        df_core = pd.DataFrame(df_core.tolist())
        print("Mapped rows to core schema")
        print(df_core.head())

        # Step 3: write to core DB (uncomment when ready)
        write_core_records(df_core)

# This ensures the function runs when the script is executed directly
if __name__ == "__main__":
    run_all_scrapers()