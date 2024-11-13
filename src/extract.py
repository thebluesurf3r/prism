import logging
import os
import pandas as pd
from utils.config import load_config
from src.feature_engineering import (
    convert_salary_to_numeric,
    add_salary_band,
    compute_avg_salary_by_group,
    add_salaries_per_reported,
    extract_job_seniority
)
from utils.file_utils import to_snakecase

# Initialize configurations and logging
config = load_config()
logging.basicConfig(level=config['logging']['level'])


def load_data(file_path=None):
    """
    Loads data from a CSV file into a DataFrame.
    Applies initial data cleaning steps like handling missing values and setting data types.
    """
    if file_path is None:
        # Default path from config.yaml
        file_path = config['data']['source_file']

    logging.info(f"Attempting to load data from: {file_path}")

    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return pd.DataFrame()  # Return empty DataFrame if the file doesn't exist

        logging.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        df.columns = [to_snakecase(col) for col in df.columns]

        # Log columns in dataset for debugging
        logging.info(f"Columns in dataset: {df.columns.tolist()}")

        # Apply data type conversions and handle missing values
        df = handle_missing_values(df)
        df = set_column_dtypes(df)

        # Apply feature engineering
        df = convert_salary_to_numeric(df)
        df = add_salary_band(df)
        df = compute_avg_salary_by_group(df, group_col='company_name')
        df = add_salaries_per_reported(df)  # This function now checks for the column's existence
        df = extract_job_seniority(df)
        df = standardize_column_names(df, case=config['data']['column_name_case'])

        logging.info("Data loaded and feature engineering applied successfully")
        return df

    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Return empty DataFrame if there is an error


def handle_missing_values(df: pd.DataFrame):
    """
    Fills or drops missing values based on configuration settings.
    """
    for col in df.columns:
        if df[col].dtype in [float, int]:
            df[col] = df[col].fillna(df[col].mean())  # Direct assignment without inplace=True
        else:
            df[col] = df[col].fillna("Unknown")  # Direct assignment without inplace=True

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


def standardize_column_names(df: pd.DataFrame, case='title'):
    """
    Standardizes the column names of the DataFrame.
    This method will apply title case or lower case as per configuration.
    """
    if case == 'title':
        df.columns = df.columns.str.title()  # Apply title case to column names
    else:
        df.columns = df.columns.str.lower()  # You can also apply lowercase if needed

    logging.info(f"Columns after standardization: {df.columns.tolist()}")
    return df


def validate_data(df: pd.DataFrame):
    """
    Validates the data to ensure it meets basic quality criteria.
    Example: Check if critical columns exist and have no missing values.
    """
    # Adjust the required columns to match snake_case column names in the dataset
    required_columns = config['data'].get('required_columns',
                                          ['company_name', 'job_title', 'salaried_reported', 'location', 'salary'])

    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        logging.error(f"Missing required columns: {missing_columns}")
        return False

    # Additional custom validations could be added here
    logging.info("Data validation passed")
    return True
