# src/data_processing.py
import pandas as pd
import numpy as np
import logging

# Configure basic logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Loads historical Brent crude oil price data from a CSV file, sanitizes headers,
    standardizes mixed date formats, and handles structural missing trading data.

    Parameters:
    -----------
    file_path : str
        The local or absolute file path to the input CSV dataset.

    Returns:
    --------
    pd.DataFrame
        A chronologically sorted DataFrame containing clean 'Date' (datetime64)
        and 'Price' (float64) columns with handled missing records.

    Raises:
    -------
    FileNotFoundError
        If the data file path does not point to a valid file.
    Exception
        For unforeseen data type parsing or format structure anomalies.
    """
    try:
        logging.info(f"Attempting to load dataset from: {file_path}")
        df = pd.read_csv(file_path)
        
        # Clean column names by stripping trailing and leading whitespaces
        df.columns = [col.strip() for col in df.columns]
        
        if 'Date' not in df.columns or 'Price' not in df.columns:
            raise KeyError("Dataset must contain explicitly labeled 'Date' and 'Price' columns.")

        # Handle mixed text representations of calendar dates (e.g., '20-May-87' vs 'Apr 22, 2020')
        df['Date'] = pd.to_datetime(df['Date'], format='mixed')
        
        # Enforce numeric conversion on pricing data, marking letters/symbols as NaN
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        
        # Sort values chronologically to protect structural time series ordering
        df = df.sort_values('Date').reset_index(drop=True)
        
        # Resolve weekend and market holiday gaps using multi-directional imputation filling
        missing_count = df['Price'].isna().sum()
        if missing_count > 0:
            logging.warning(f"Detected {missing_count} null fields in raw prices. Executing forward/backward imputation.")
            df['Price'] = df['Price'].ffill().bfill()
            
        logging.info("Data ingestion and processing completed successfully.")
        return df

    except FileNotFoundError as fnf_error:
        logging.error(f"File I/O Operation failed: {fnf_error}")
        raise fnf_error
    except Exception as e:
        logging.error(f"Critical error encountered during data ingestion: {e}")
        raise e

def calculate_log_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw nominal price points into continuous log returns to stabilize
    variance over time and force time series stationarity.
    Formula: Log_Return = log(Price_t) - log(Price_{t-1})

    Parameters:
    -----------
    df : pd.DataFrame
        A sanitized DataFrame containing a valid numeric 'Price' column.

    Returns:
    --------
    pd.DataFrame
        A modified DataFrame copy containing an added 'Log_Return' column,
        with the initial boundary NaN row dropped cleanly.
    """
    try:
        if 'Price' not in df.columns or df['Price'].empty:
            raise ValueError("Input DataFrame must possess a valid, non-empty numeric 'Price' field.")
            
        df_copy = df.copy()
        
        # Compute continuous daily log differences
        df_copy['Log_Return'] = np.log(df_copy['Price']) - np.log(df_copy['Price'].shift(1))
        
        # Cleanly drop initial baseline shift observation containing empty reference cell
        return df_copy.dropna().reset_index(drop=True)
        
    except Exception as e:
        logging.error(f"Failed to generate log return transformations: {e}")
        raise e