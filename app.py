import logging
import streamlit as st
import pandas as pd
from src.extract import load_data, standardize_column_names, validate_data
from src.feature_engineering import (
    convert_salary_to_numeric,
    add_salary_band,
    compute_avg_salary_by_group,
    add_salaries_per_reported,
    extract_job_seniority,
)
from utils.config import load_config
from src.visualizations import plot_avg_salary_by_company, plot_salary_band_distribution
import re

# Initialize configurations and logging
config = load_config()
logging.basicConfig(level=config['logging']['level'])


def main():
    st.title("Salary Dataset Analysis")

    # Remove file uploader as data is loaded from the default path
    file_path = config['data']['source_file']
    logging.info(f"Using data from {file_path}")

    # Load and preprocess data using the specified file path
    df = load_data(file_path)  # Pass file_path directly to load_data

    if df.empty:
        st.error("Failed to load data. Please check the file path and try again.")
        return

    # Standardize column names
    df = standardize_column_names(df, case=config['data']['column_name_case'])

    # Validate data
    if not validate_data(df):
        st.error("Data validation failed. Please check the dataset.")
        return

    # Feature Engineering
    df = convert_salary_to_numeric(df)
    df = add_salary_band(df)
    df = compute_avg_salary_by_group(df, group_col='company_name')
    df = add_salaries_per_reported(df)
    df = extract_job_seniority(df)

    # Sidebar Filters
    st.sidebar.header("Filters")

    # Regex Match for Designation
    designation_pattern = st.sidebar.text_input("Regex match for Designation", "")

    # Double Slider for Salary Range
    min_salary, max_salary = st.sidebar.slider(
        "Select Salary Range",
        min_value=int(df['salary_numeric'].min()),
        max_value=int(df['salary_numeric'].max()),
        value=(int(df['salary_numeric'].min()), int(df['salary_numeric'].max())),
    )

    # Search Box for Company Name
    company_name_search = st.sidebar.text_input("Search by Company Name", "")

    # Dropdown for Location Selector
    locations = df['location'].unique()
    location_filter = st.sidebar.selectbox("Select Location", options=locations, index=0)

    # Apply Filters
    if designation_pattern:
        df = df[df['job_title'].str.contains(designation_pattern, regex=True, na=False)]

    df = df[(df['salary_numeric'] >= min_salary) & (df['salary_numeric'] <= max_salary)]

    if company_name_search:
        df = df[df['company_name'].str.contains(company_name_search, regex=False, na=False)]

    if location_filter:
        df = df[df['location'] == location_filter]

    # Display processed data
    st.subheader("Processed Data")
    st.write(df.head())

    # Data Analysis and Visualization
    st.subheader("Average Salary by Company")
    avg_salary_fig = plot_avg_salary_by_company(df)
    st.plotly_chart(avg_salary_fig)

    st.subheader("Salary Band Distribution")
    salary_band_fig = plot_salary_band_distribution(df)
    st.plotly_chart(salary_band_fig)


if __name__ == "__main__":
    main()
