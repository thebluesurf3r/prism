# src/analysis.py

import pandas as pd
import numpy as np
import yaml
import logging
import os

# Load configurations
from utils.config import load_config

# Initialize configurations
config = load_config()


def calculate_numerical_summary(df: pd.DataFrame):
    """
    Calculates summary statistics for numerical columns in the DataFrame.
    """
    metrics = config['analysis']['numerical_summary_metrics']
    summary = df.describe(percentiles=[])

    # Only keep required metrics
    summary = summary.loc[metrics]
    return summary


def calculate_correlation_matrix(df: pd.DataFrame):
    """
    Computes the correlation matrix for numerical columns in the DataFrame.
    """
    correlation_threshold = config['analysis']['correlation_threshold']
    correlation_matrix = df.corr()

    # Highlight strong correlations
    strong_correlation = correlation_matrix[
        (correlation_matrix >= correlation_threshold) |
        (correlation_matrix <= -correlation_threshold)
        ]

    return strong_correlation.fillna(0)


def detect_outliers(df: pd.DataFrame):
    """
    Detects outliers in numerical columns based on the method specified in config.
    """
    method = config['analysis']['outlier_detection_method']
    threshold = config['analysis']['outlier_threshold']
    outliers = pd.DataFrame()

    if method == "iqr":
        for col in df.select_dtypes(include=[np.number]).columns:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            outliers[col] = df[col][(df[col] < lower_bound) | (df[col] > upper_bound)]
    elif method == "Z-score":
        for col in df.select_dtypes(include=[np.number]).columns:
            mean = df[col].mean()
            std_dev = df[col].std()
            outliers[col] = df[col][(np.abs(df[col] - mean) > threshold * std_dev)]

    return outliers.dropna(how='all')


def top_categorical_counts(df: pd.DataFrame):
    """
    Calculates the top N categories for categorical columns in the DataFrame.
    """
    top_n = config['analysis']['top_n_categories']
    top_counts = {}

    for col in df.select_dtypes(include=['object']).columns:
        top_counts[col] = df[col].value_counts().nlargest(top_n).to_dict()

    return top_counts

