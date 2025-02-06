import pandas as pd
import os

CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "fuel_prices.csv")

def load_fuel_data():
    df = pd.read_csv(CSV_FILE_PATH)
    fuel_stations = df.to_dict(orient="records")
    return fuel_stations
