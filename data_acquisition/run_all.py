import pandas as pd
from typing import Callable, Tuple
from utils.logging_config import get_logger
from utils.validation import validate_records
from utils.staging_utils import save_raw_csv
from utils.incremental import should_update, set_last_run
from staging.paradiso import paradiso
from staging.melkweg import melkweg
from staging.de_balie import de_balie
from staging.fchyena import fchyena
from staging.studiok import studiok
from staging.concertgebouw import concertgebouw
from staging.carre import carre
from mapping.paradiso_mapping import map_paradiso
from mapping.melkweg_mapping import map_melkweg
from mapping.de_balie_mapping import map_de_balie
from mapping.fchyena_mapping import map_fchyena
from mapping.studiok_mapping import map_studiok
from mapping.concertgebouw_mapping import map_concertgebouw
from mapping.carre_mapping import map_carre
from core.transform import write_core_records

logger = get_logger(__name__)

# List of scrapers and their corresponding mapping functions
SCRAPERS: list[Tuple[Callable, Callable, str]] = [
    (paradiso, map_paradiso, "Paradiso"),
    (melkweg, map_melkweg, "Melkweg"),
    (de_balie, map_de_balie, "De Balie"),
    (fchyena, map_fchyena, "FCHYENA"),
    (studiok, map_studiok, "Studio K"),
    (concertgebouw, map_concertgebouw, "Concertgebouw"),
    (carre, map_carre, "Carré"),
]


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
    run_all_scrapers()