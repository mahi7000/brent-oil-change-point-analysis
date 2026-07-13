# app.py
import os
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing to allow your local React server to fetch API models
CORS(app)

# Resolve local paths safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRICE_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "BrentOilPrices.csv")
EVENT_DATA_PATH = os.path.join(BASE_DIR, "notebooks", "events.csv")

def parse_and_load_data():
    """Ingests data models cleanly for API consumption."""
    if not os.path.exists(PRICE_DATA_PATH) or not os.path.exists(EVENT_DATA_PATH):
        return pd.DataFrame(), pd.DataFrame()
    
    df_prices = pd.read_csv(PRICE_DATA_PATH)
    df_prices['Date'] = pd.to_datetime(df_prices['Date'], format='mixed')
    df_prices = df_prices.sort_values('Date').dropna().reset_index(drop=True)
    
    df_events = pd.read_csv(EVENT_DATA_PATH)
    df_events['Date'] = pd.to_datetime(df_events['Date'], format='mixed')
    return df_prices, df_events

@app.route('/api/v1/historical-prices', methods=['GET'])
def get_historical_prices():
    """
    Endpoint 1: Returns complete historical price records.
    Supports optional query filtering arguments: start_date and end_date.
    Format: /api/v1/historical-prices?start_date=2020-01-01&end_date=2020-06-30
    """
    df_p, _ = parse_and_load_data()
    if df_p.empty:
        return jsonify({"error": "Dataset assets missing on workspace paths."}), 500
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        df_p = df_p[df_p['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df_p = df_p[df_p['Date'] <= pd.to_datetime(end_date)]
        
    # Format dates to string array output mapping to prevent JSON transformation crashes
    data_payload = [{
        "date": row['Date'].strftime('%Y-%m-%d'),
        "price": float(row['Price'])
    } for _, row in df_p.iterrows()]
    
    return jsonify(data_payload)

@app.route('/api/v1/change-points', methods=['GET'])
def get_change_points():
    """
    Endpoint 2: Provides pre-computed MCMC change point parameters 
    and quantified impact indicators discovered during Task 2 runs.
    """
    change_points = [
        {
            "id": 1,
            "date": "2020-03-09",
            "associated_event": "OPEC+ Price War Breakdown",
            "price_before": 53.64,
            "price_after": 29.11,
            "pct_change": -45.73,
            "regime_shift_type": "Volatility Shock Phase"
        },
        {
            "id": 2,
            "date": "2008-09-15",
            "associated_event": "Lehman Brothers Collapse",
            "price_before": 140.02,
            "price_after": 42.40,
            "pct_change": -69.71,
            "regime_shift_type": "Economic Demand Crushing Phase"
        }
    ]
    return jsonify(change_points)

@app.route('/api/v1/events', methods=['GET'])
def get_event_correlation_data():
    """
    Endpoint 3: Exposes the curated historical event catalog 
    containing descriptions and strategic macroeconomic tags.
    """
    _, df_e = parse_and_load_data()
    if df_e.empty:
        return jsonify({"error": "Events description file missing."}), 500
        
    events_payload = [{
        "date": row['Date'].strftime('%Y-%m-%d'),
        "name": row['Event_Name'],
        "category": row['Category'],
        "description": row['Description']
    } for _, row in df_e.iterrows()]
    
    return jsonify(events_payload)

if __name__ == '__main__':
    # Execute backend locally on standard development channel port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)