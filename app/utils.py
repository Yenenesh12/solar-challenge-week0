import pandas as pd
import os

def load_data(country, base_path=None):
    # Build data path relative to project structure
    if base_path is None:
        current_dir = os.path.dirname(__file__)
        base_path = os.path.abspath(os.path.join(current_dir, '..', 'data'))
    
    path_map = {
        'Benin': os.path.join(base_path, 'benin-malanville_clean.csv'),
        'Sierra Leone': os.path.join(base_path, 'sierraleone-bumbuna_clean.csv'),
        'Togo': os.path.join(base_path, 'togo-dapaong_qc.csv')
    }

    file_path = path_map.get(country)
    if not file_path:
        raise ValueError(f"Unknown country: {country}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at expected location: {file_path}. Please ensure your data folder is correctly structured.")

    df = pd.read_csv(file_path, parse_dates=['Timestamp'])
    return df