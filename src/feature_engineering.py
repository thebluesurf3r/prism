# src/feature_engineering.py


import pandas as pd
import re
import logging
import os


def convert_salary_to_numeric(df):
    """
    Converts the 'salary' column to a numeric format (removes currency symbols, commas, and other non-numeric text).
    """
    # Remove all non-numeric characters including '₹', '/yr', 'mo', 'k' etc.
    df['salary_numeric'] = df['salary'].replace(
        {r'₹': '', r'/yr': '', r',': '', r'mo': '', r'k': '000'}, regex=True
    )

    # Now attempt to convert the cleaned strings to float
    df['salary_numeric'] = pd.to_numeric(df['salary_numeric'], errors='coerce')

    return df



def add_salary_band(df):
    """
    Adds a salary band column for easier grouping.
    """
    bins = [0, 500000, 1000000, 1500000, 2000000, float('inf')]
    labels = ['<5L', '5-10L', '10-15L', '15-20L', '20L+']
    df['salary_band'] = pd.cut(df['salary_numeric'], bins=bins, labels=labels)
    return df


def compute_avg_salary_by_group(df, group_col):
    """
    Computes the average salary grouped by a specified column.
    """
    avg_salary = df.groupby(group_col)['salary_numeric'].transform('mean')
    df[f'avg_salary_by_{group_col}'] = avg_salary
    return df


def add_salaries_per_reported(df: pd.DataFrame):
    """
    Add a new column for salaries per reported.
    This divides the salary by the number of reports (if available).
    """
    if 'salaries_reported' in df.columns:  # Column name in snake_case
        df['salaries_per_reported'] = df['salary'] / df['salaries_reported']
    else:
        logging.warning("Column 'salaries_reported' is missing, defaulting to NaN")
        df['salaries_per_reported'] = None  # Or some default value

    return df


def extract_job_seniority(df):
    """
    Extracts job seniority level from job title.
    """

    def seniority_level(title):
        if 'junior' in title.lower():
            return 'Junior'
        elif 'senior' in title.lower() or 'lead' in title.lower() or 'manager' in title.lower():
            return 'Senior'
        else:
            return 'Mid-level'

    df['job_seniority'] = df['job_title'].apply(seniority_level)
    return df
