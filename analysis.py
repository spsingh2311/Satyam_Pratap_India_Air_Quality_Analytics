import pandas as pd
from pathlib import Path

DATA = Path(__file__).parent / "data" / "india_air_quality_12042_rows.csv"

def add_category(aqi):
    if pd.isna(aqi): return "Unknown"
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Satisfactory"
    if aqi <= 200: return "Moderate"
    if aqi <= 300: return "Poor"
    if aqi <= 400: return "Very Poor"
    return "Severe"

def load_data():
    df = pd.read_csv(DATA, parse_dates=["Date"])
    return df

def validate_data(df):
    numeric = ["AQI", "PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df[numeric].isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "negative_numeric_values": int((df[numeric] < 0).sum().sum()),
        "invalid_dates": int(df["Date"].isna().sum()),
    }

if __name__ == "__main__":
    df = load_data()
    print(df.head())
    print(validate_data(df))
    print(df.groupby("City")["AQI"].agg(["count","mean","min","max"]).sort_values("mean", ascending=False))
