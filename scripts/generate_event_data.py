# scripts/generate_event_data.py
import os
import pandas as pd
import logging

# Configure basic logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_historical_events_csv(output_path: str) -> None:
    """
    Programmatically builds and exports the curated dataset of 12 critical 
    geopolitical, economic, and OPEC policy shocks affecting the oil market.

    Parameters:
    -----------
    output_path : str
        The destination file path where the structured CSV will be saved.

    Returns:
    --------
    None
    """
    try:
        logging.info("Compiling historical macro-event raw matrix...")
        
        # Define the structural event rows
        events_data = [
            {"Date": "02-Aug-1990", "Event_Name": "Gulf War Outbreak", "Category": "Geopolitical Shock", 
             "Description": "Iraq invades Kuwait leading to immediate global energy security anxieties and supply premium hikes."},
            {"Date": "11-Sep-2001", "Event_Name": "9/11 Terror Attacks", "Category": "Geopolitical Shock", 
             "Description": "Triggers massive contraction in global aviation fuel consumption followed by premium pricing adjustments."},
            {"Date": "15-Sep-2008", "Event_Name": "Lehman Brothers Collapse", "Category": "Economic Core Shock", 
             "Description": "Catalyzes global financial crisis; widespread global industrial demand destruction."},
            {"Date": "15-Mar-2011", "Event_Name": "Arab Spring / Libyan War", "Category": "Geopolitical Shock", 
             "Description": "Widespread regional civil unrest halts sweet crude export flows across North Africa."},
            {"Date": "27-Nov-2014", "Event_Name": "OPEC Thanksgiving Decision", "Category": "Internal OPEC Policy", 
             "Description": "OPEC refuses to cut production targets despite expanding US shale output crashing global pricing regimes."},
            {"Date": "08-May-2018", "Event_Name": "US Iran Sanctions Return", "Category": "Political Mandate", 
             "Description": "US pulls out of JCPOA nuclear framework reimposing aggressive sanctions targeting Iranian crude exports."},
            {"Date": "14-Sep-2019", "Event_Name": "Abqaiq-Khurais Drone Attacks", "Category": "Geopolitical Shock", 
             "Description": "Drone strikes disable Saudi Aramco processing nodes knocking offline 5% of active global supply."},
            {"Date": "06-Mar-2020", "Event_Name": "OPEC+ Price War Collapse", "Category": "Internal OPEC Policy", 
             "Description": "Disagreements on production caps spark an aggressive volume war between Russia and Saudi Arabia."},
            {"Date": "11-Mar-2020", "Event_Name": "WHO COVID-19 Declaration", "Category": "Economic Core Shock", 
             "Description": "Enforced global structural lockdowns induce unprecedented historic drops in industrial fuel demand."},
            {"Date": "20-Apr-2020", "Event_Name": "WTI Negative Pricing Anomaly", "Category": "Economic Core Shock", 
             "Description": "Extreme domestic infrastructure storage shortages drop WTI below zero disrupting global spot benchmarks."},
            {"Date": "24-Feb-2022", "Event_Name": "Russian Invasion of Ukraine", "Category": "Geopolitical Shock", 
             "Description": "Outbreak of active European warfare and widespread Western economic sanctions send Brent soaring near 140 USD."},
            {"Date": "05-Oct-2022", "Event_Name": "OPEC+ 2 Million Barrel Output Cut", "Category": "Internal OPEC Policy", 
             "Description": "OPEC+ imposes aggressive production rollbacks to artificially defend falling baseline target lines."}
        ]
        
        # Convert list of dictionaries to a Pandas DataFrame
        df = pd.DataFrame(events_data)
        
        # Ensure target directory exists before writing
        target_dir = os.path.dirname(output_path)
        if target_dir and not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            logging.info(f"Created missing directory space at: {target_dir}")
            
        # Export data cleanly without the default index column
        df.to_csv(output_path, index=False)
        logging.info(f"✅ Success! Tabular event database generated at: {output_path}")
        
    except IOError as io_err:
        logging.error(f"File writing failure occurred: {io_err}")
        raise io_err
    except Exception as e:
        logging.error(f"An unexpected anomaly occurred during dataset generation: {e}")
        raise e

if __name__ == "__main__":
    # Define the delivery path targeting your notebooks directory
    target_csv = os.path.join("notebooks", "events.csv")
    generate_historical_events_csv(target_csv)