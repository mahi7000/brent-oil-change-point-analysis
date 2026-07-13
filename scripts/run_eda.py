# scripts/run_eda.py
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing import load_and_clean_data, calculate_log_returns

def perform_adf_test(series, name):
    print(f"\n--- Augmented Dickey-Fuller Test for: {name} ---")
    result = adfuller(series)
    print(f"ADF Statistic: {result[0]:.4f}")
    print(f"p-value: {result[1]:.4e}")
    print("Critical Values:")
    for key, value in result[4].items():
        print(f"   {key}: {value:.4f}")
    
    if result[1] <= 0.05:
        print(f"Result: Reject the null hypothesis. The {name} series is STATIONARY.")
    else:
        print(f"Result: Fail to reject the null hypothesis. The {name} series is NON-STATIONARY.")

def main():
    data_path = "data/raw/BrentOilPrices.csv" 
    
    if not os.path.exists(data_path):
        print(f"⚠️ Data file not found at {data_path}. Please place your BrentOilPrices.csv there.")
        return

    # 1. Ingest and Clean
    df = load_and_clean_data(data_path)
    df_returns = calculate_log_returns(df)
    
    # 2. Run Diagnostics
    perform_adf_test(df['Price'], "Raw Price")
    perform_adf_test(df_returns['Log_Return'], "Log Returns")
    
    # 3. Visual Analysis Setup
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=False)
    
    # Plot 1: Raw Price Trend & Rolling Windows
    df['Rolling_Mean_Yearly'] = df['Price'].rolling(window=365).mean()
    axes[0].plot(df['Date'], df['Price'], label='Daily Spot Price', color='steelblue', alpha=0.6)
    axes[0].plot(df['Date'], df['Rolling_Mean_Yearly'], label='365-Day Rolling Average', color='darkorange', linewidth=2)
    axes[0].set_title('Historical Brent Crude Oil Prices (USD/Barrel) & Macro Trend', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Price (USD)')
    axes[0].legend()
    
    # Plot 2: Log Returns & Volatility Clustering
    axes[1].plot(df_returns['Date'], df_returns['Log_Return'], color='crimson', alpha=0.5, linewidth=0.5)
    axes[1].set_title('Log Returns demonstrating Volatility Clustering (Stationary Transformation)', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Log Return')
    axes[1].set_xlabel('Date')
    
    plt.tight_layout()
    
    # Save output visualization for Interim Report
    output_plot = "notebooks/eda_price_returns.png"
    plt.savefig(output_plot, dpi=300)
    print(f"\n📈 Visualizations saved successfully to {output_plot}")

if __name__ == "__main__":
    main()