import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from datetime import datetime
import plotly.express as px
import re

def load_data():
    """
    Load CSV data using Streamlit's file uploader.
    Returns:
        pandas.DataFrame: The loaded data or None if no file is uploaded.
    """
    st.sidebar.header("Upload Data")

    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload your auto dealership data in CSV format"
    )

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)            
            st.sidebar.success(f"Successfully loaded data with {data.shape[0]} rows and {data.shape[1]} columns")
            return data
        except Exception as e:
            st.sidebar.error(f"Error loading data: {e}")
            return None
    else:
        st.sidebar.info("Please upload a CSV file to begin analysis")
        return None

def file_explorer(data):
    """
    Display the raw data table with options to sort and filter.

    Args:
        data (pandas.DataFrame): The dataframe to display
    """
    if data is not None:
        st.header("Data Explorer")

        with st.expander("Show Raw Data", expanded=False):
            # Display dataframe with column configuration
            st.dataframe(
                data,
                use_container_width=True,
                height=400
            )

def filter_values(data):
    """
    Provide filtering capabilities for the dataframe.

    Args:
        data (pandas.DataFrame): The dataframe to filter

    Returns:
        pandas.DataFrame: The filtered dataframe
    """
    if data is None:
        return None

    st.header("Data Filtering")

    filtered_data = data.copy()

    with st.expander("Filter Data", expanded=True):
        # Create columns for filter layout
        cols = st.columns(3)

        # Process each column in the dataframe
        filter_count = 0
        for i, column in enumerate(data.columns):
            # Determine column type
            is_numeric = pd.api.types.is_numeric_dtype(data[column])
            is_datetime = pd.api.types.is_datetime64_dtype(data[column])
            is_categorical = (not is_numeric and not is_datetime) or (is_numeric and data[column].nunique() < 20)

            # Place in appropriate column (cycling through the 3 columns)
            with cols[filter_count % 3]:
                if is_categorical:
                    # For categorical data or numeric with few unique values
                    # Handle mixed types by converting to strings before sorting
                    unique_values = data[column].unique()
                    try:
                        unique_values = sorted(unique_values)
                    except TypeError:
                        # If sorting fails due to mixed types, convert to strings
                        unique_values = sorted(unique_values.astype(str))

                    selected_values = st.multiselect(
                        f"Select {column}",
                        options=unique_values,
                        default=[]
                    )

                    if selected_values:
                        filtered_data = filtered_data[filtered_data[column].isin(selected_values)]

                elif is_datetime:
                    # For datetime columns
                    min_date = data[column].min().date()
                    max_date = data[column].max().date()

                    date_range = st.date_input(
                        f"Filter {column}",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date
                    )

                    if len(date_range) == 2:
                        start_date, end_date = date_range
                        filtered_data = filtered_data[
                            (filtered_data[column].dt.date >= start_date) & 
                            (filtered_data[column].dt.date <= end_date)
                        ]

                else:
                    # For continuous numeric data
                    min_val = float(data[column].min())
                    max_val = float(data[column].max())

                    value_range = st.slider(
                        f"Filter {column}",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val),
                        step=(max_val - min_val) / 100
                    )

                    filtered_data = filtered_data[
                        (filtered_data[column] >= value_range[0]) & 
                        (filtered_data[column] <= value_range[1])
                    ]

                filter_count += 1

    # Show filtering stats
    if len(filtered_data) < len(data):
        st.info(f"Filtered data: {len(filtered_data)} rows (from {len(data)} total)")

    return filtered_data

def main():
    """
    Main application function that orchestrates the dashboard.
    """
    try:
        # Set page config
        st.set_page_config(
            page_title="Analytics Dashboard",
            page_icon="🚗",
            layout="wide"
        )

        # Add title and description
        st.title("Analytics Dashboard")
        st.markdown("""
        This is your starting point for any analytical project.
        """)

        # Load data
        data = load_data()

        if data is not None:
            # Filter data
            filtered_data = filter_values(data)

            # Display data explorer
            file_explorer(filtered_data)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.exception(e)

if __name__ == "__main__":
    main()