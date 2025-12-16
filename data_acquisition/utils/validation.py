"""Data validation utilities."""

import pandas as pd
from utils.logging_config import get_logger

logger = get_logger(__name__)

REQUIRED_FIELDS = ['venue', 'start_date_time', 'ticket_url']


def validate_records(df: pd.DataFrame) -> pd.DataFrame:
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
    removed_count = initial_count - len(df_clean)
    
    if removed_count > 0:
        logger.warning(f"Removed {removed_count} records with missing required fields")
    
    logger.info(f"Validation complete: {len(df_clean)}/{initial_count} records valid")
    
    return df_clean
