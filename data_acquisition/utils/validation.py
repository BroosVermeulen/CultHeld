"""Data validation utilities."""

import pandas as pd
from typing import Iterable
from config import PRICE_REQUIRED_VENUES
from utils.logging_config import get_logger

logger = get_logger(__name__)

REQUIRED_FIELDS = ['venue', 'start_date_time', 'ticket_url']


def validate_records(df: pd.DataFrame, price_required_venues: Iterable[str] | None = None) -> pd.DataFrame:
    """
    Validate that required fields exist and have valid data.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Validated DataFrame (rows with missing required fields are removed)
    """
    initial_count = len(df)
    
    # Check all required fields exist
    missing_fields = [f for f in REQUIRED_FIELDS if f not in df.columns]
    if missing_fields:
        logger.warning(f"Missing fields in data: {missing_fields}")
        return pd.DataFrame()
    
    # Remove rows with null values in required fields
    df_clean = df.dropna(subset=REQUIRED_FIELDS)

    # If price is required for certain venues, enforce non-null price for those rows
    venues_requiring_price = set(price_required_venues) if price_required_venues is not None else set(PRICE_REQUIRED_VENUES)
    if 'price' in df_clean.columns and 'venue' in df_clean.columns and venues_requiring_price:
        before = len(df_clean)
        mask = df_clean['venue'].isin(venues_requiring_price)
        df_with_price = df_clean[~mask | (~df_clean['price'].isna())]
        dropped = before - len(df_with_price)
        if dropped > 0:
            logger.warning(f"Removed {dropped} records missing price for venues requiring price: {sorted(venues_requiring_price)}")
        df_clean = df_with_price
    removed_count = initial_count - len(df_clean)
    
    if removed_count > 0:
        logger.warning(f"Removed {removed_count} records with missing required fields")
    
    logger.info(f"Validation complete: {len(df_clean)}/{initial_count} records valid")
    
    return df_clean
