import importlib
import os
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from core.transform import write_core_records
from utils.incremental import set_last_run, should_update
from utils.logging_config import get_logger
from utils.staging_utils import save_raw_csv
from utils.validation import validate_records

logger = get_logger(__name__)

def discover_scrapers(staging_pkg: str = 'staging', mapping_pkg: str = 'mapping') -> list[tuple[Callable, Callable, str]]:
    """Auto-discover staging modules and corresponding mapping functions.

    For each module `staging.<name>`, attempts to import `mapping.<name>_mapping`
    and retrieve `map_<name>` as the mapping function. The venue name is
    derived by calling the mapping function with an empty row (most mapping
    functions set a static `venue` field).
    """
    scrapers = []
    base = Path(__file__).parent / staging_pkg
    for f in sorted(os.listdir(base)):
        if not f.endswith('.py') or f.startswith('_'):
            continue
        mod_name = f[:-3]
        staging_module_path = f"{staging_pkg}.{mod_name}"
        mapping_module_path = f"{mapping_pkg}.{mod_name}_mapping"
        try:
            sm = importlib.import_module(staging_module_path)
        except Exception:
            logger = get_logger(__name__)
            logger.warning('Failed to import staging module %s', staging_module_path)
            continue

        # choose scraper callable: prefer `scrape`, else fallback to function named after module
        if hasattr(sm, 'scrape') and callable(getattr(sm, 'scrape')):
            scraper_callable = getattr(sm, 'scrape')
        elif hasattr(sm, mod_name) and callable(getattr(sm, mod_name)):
            scraper_callable = getattr(sm, mod_name)
        else:
            logger = get_logger(__name__)
            logger.warning('No scraper callable found in %s', staging_module_path)
            continue

        try:
            mm = importlib.import_module(mapping_module_path)
        except Exception:
            logger = get_logger(__name__)
            logger.warning('No mapping module for %s; skipping', mod_name)
            continue

        map_func_name = f"map_{mod_name}"
        if not hasattr(mm, map_func_name):
            logger = get_logger(__name__)
            logger.warning('Mapping function %s not found in %s', map_func_name, mapping_module_path)
            continue
        map_callable = getattr(mm, map_func_name)

        # derive venue name by calling mapping function on an empty dict
        try:
            venue_name = map_callable({}).get('venue')
        except Exception:
            venue_name = mod_name.replace('_', ' ').title()

        scrapers.append((scraper_callable, map_callable, venue_name))

    return scrapers


# Discovered scrapers
SCRAPERS = discover_scrapers()


def run_all_scrapers(force_update: bool = False) -> None:
    """
    Run all scrapers with error isolation, validation, and incremental updates.
    
    Args:
        force_update: If True, skip incremental update checks and always scrape
    """
    logger.info("Starting data acquisition pipeline")
    
    successful_scrapers = 0
    failed_scrapers = 0
    skipped_scrapers = 0
    
    for scraper_func, map_func, venue_name in SCRAPERS:
        try:
            # Check if update is needed
            if not force_update and not should_update(venue_name):
                logger.info(f"Skipping {venue_name} - recently updated")
                skipped_scrapers += 1
                continue
            
            logger.info(f"Running scraper: {venue_name}")
            
            # Step 1: get raw data
            df_raw = scraper_func()
            logger.info(f"Scraped {len(df_raw)} rows from {venue_name}")
            save_raw_csv(df_raw, venue_name)

            # Step 2: apply mapping
            df_core = df_raw.apply(map_func, axis=1)
            df_core = pd.DataFrame(df_core.tolist())
            logger.info(f"Mapped rows to core schema for {venue_name}")
            
            # Step 3: validate data
            df_core = validate_records(df_core)
            if len(df_core) == 0:
                logger.error(f"No valid records after validation for {venue_name}")
                failed_scrapers += 1
                continue
            
            logger.debug(f"Sample data:\n{df_core.head()}")

            # Step 4: write to core DB
            write_core_records(df_core)
            set_last_run(venue_name)
            logger.info(f"Successfully processed {venue_name}")
            successful_scrapers += 1
            
        except Exception as e:
            logger.error(f"Error processing {venue_name}: {str(e)}", exc_info=True)
            failed_scrapers += 1
            continue
    
    logger.info(f"Pipeline complete: {successful_scrapers} successful, {failed_scrapers} failed, {skipped_scrapers} skipped")


# This ensures the function runs when the script is executed directly
if __name__ == "__main__":
    run_all_scrapers(True)