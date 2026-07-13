import pandas as pd
import numpy as np

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df.columns = [col.strip() for col in df.columns]

    df['Date'] = pd.to_datetime(df['Date'], format='mixed')

    df = df.sort_values('Date').reset_index(drop=True)

    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Price'] = df['Price'].ffill().bfill()

    return df

def calculate_log_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['Log_Return'] = np.log(df['Price']) - np.log(df['Price'].shift(1))

    return df.dropna().reset_index(drop=True)
