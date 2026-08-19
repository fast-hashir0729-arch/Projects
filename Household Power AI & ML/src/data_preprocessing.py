"""
data_preprocessing.py
----------------------
Handles loading, cleaning, and feature engineering for the
Household Power Consumption dataset (UCI Machine Learning Repository).

Skills demonstrated:
    - Reading large, messy real-world CSV/TXT data with pandas
    - Missing-value detection and handling
    - Duplicate removal
    - Datetime parsing and feature extraction
    - Outlier treatment using the IQR method
"""

import pandas as pd
import numpy as np


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the raw household power consumption dataset.

    The original UCI file is semicolon-separated and uses '?' to mark
    missing readings, so both are handled explicitly here.

    Parameters
    ----------
    filepath : str
        Path to household_power_consumption.txt

    Returns
    -------
    pd.DataFrame
        Raw dataframe as read from disk.
    """
    df = pd.read_csv(
        filepath,
        sep=";",
        low_memory=False,
        na_values=["?"],
    )
    return df


def report_missing_values(df: pd.DataFrame) -> pd.Series:
    """Print and return the count and percentage of missing values per column."""
    missing_counts = df.isnull().sum()
    missing_percentage = (missing_counts / len(df) * 100).round(1)

    print("Missing Values:\n", missing_counts)
    print("\nPercentage of missing values:\n", missing_percentage)

    return missing_counts


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop missing values and duplicate rows.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe (missing rows and duplicates removed).
    """
    df = df.dropna().copy()

    n_duplicates = df.duplicated().sum()
    print("Number of duplicated rows:", n_duplicates)

    df = df.drop_duplicates()
    return df


def engineer_datetime_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combine the separate Date and Time columns into a single Datetime
    column and extract Hour / Day / Month / Weekday features that the
    models use to capture temporal usage patterns.
    """
    df = df.copy()
    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    df["Hour"] = df["Datetime"].dt.hour
    df["Day"] = df["Datetime"].dt.day
    df["Month"] = df["Datetime"].dt.month
    df["Weekday"] = df["Datetime"].dt.dayofweek
    df = df.drop(["Date", "Time"], axis=1)

    print("\nData types:\n", df.dtypes)
    return df


def cap_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Cap outliers in `column` using the IQR (Interquartile Range) method
    instead of removing them, to keep the dataset size intact.

    Any value below Q1 - 1.5*IQR or above Q3 + 1.5*IQR is clipped to
    the respective bound.
    """
    df = df.copy()
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    df[column] = np.clip(df[column], lower_bound, upper_bound)
    return df


def preprocess_pipeline(filepath: str, target_column: str = "Global_active_power") -> pd.DataFrame:
    """
    End-to-end preprocessing pipeline: load -> report missing ->
    clean -> engineer datetime features -> cap outliers.

    Parameters
    ----------
    filepath : str
        Path to the raw dataset file.
    target_column : str
        Column to apply IQR outlier capping on.

    Returns
    -------
    pd.DataFrame
        Fully preprocessed dataframe, ready for EDA / modelling.
    """
    df = load_data(filepath)
    report_missing_values(df)
    df = clean_data(df)
    df = engineer_datetime_features(df)
    df = cap_outliers_iqr(df, target_column)
    return df
