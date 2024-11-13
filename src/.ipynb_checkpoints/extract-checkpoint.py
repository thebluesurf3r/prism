# src/extract.py

import pandas as pd
from utils.config import load_config
import logging

# Initialize configurations and logging
config = load_config()
logging.basicConfig(level=config['logging']['level'])

def load_data(file_path=None):
    """
    Loads data from a CSV file into a DataFrame.
    Applies initial data cleaning steps like handling missing values and setting data types.
    """
    if file_path is None:
        file_path = config['data']['source_file']

    try:
        logging.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)

        # Apply data type conversions and handle missing values
        df = handle_missing_values(df)
        df = set_column_dtypes(df)

        logging.info("Data loaded successfully")
        return df

    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there is an error

def handle_missing_values(df: pd.DataFrame):
    """
    Fills or drops missing values based on configuration settings.
    """
    # Example: Fill numeric columns with mean and drop rows with missing categorical values
    for col in df.columns:
        if df[col].dtype in [float, int]:
            df[col].fillna(df[col].mean(), inplace=True)
        else:
            df[col].fillna("Unknown", inplace=True)

    logging.info("Handled missing values")
    return df

def set_column_dtypes(df: pd.DataFrame):
    """
    Sets column data types based on configuration or inferred data types.
    """
    date_format = config['data'].get('date_format', None)

    # Set columns to datetime format if date_format is provided
    for col in df.columns:
        if "date" in col.lower() and date_format:
            try:
                df[col] = pd.to_datetime(df[col], format=date_format)
            except Exception as e:
                logging.warning(f"Failed to parse dates in column {col}: {e}")

    logging.info("Data types set according to configuration")
    return df

def validate_data(df: pd.DataFrame):
    """
    Validates the data to ensure it meets basic quality criteria.
    Example: Check if critical columns exist and have no missing values.
    """
    required_columns = config['data'].get('required_columns', [])
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logging.error(f"Missing required columns: {missing_columns}")
        return False

    # Additional custom validations could be added here
    logging.info("Data validation passed")
    return True
