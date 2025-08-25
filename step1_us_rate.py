import pandas as pd
from pandas_datareader.data import DataReader
from datetime import datetime
from pathlib import Path


def fetch_fedfunds(start: str, end: str) -> pd.DataFrame:
    """Fetch monthly Effective Federal Funds Rate (FEDFUNDS) from FRED."""
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    df = DataReader("FEDFUNDS", "fred", start_dt, end_dt)
    df = df.rename(columns={"FEDFUNDS": "fedfunds"})
    df.index.name = "date"

    # Debug prints
    print(f"\n📊 Retrieved FEDFUNDS data from {start} to {end}")
    print(f"Rows: {len(df)}, Columns: {list(df.columns)}")
    print("First 5 rows:")
    print(df.head())
    print("Last 5 rows:")
    print(df.tail())
    return df


def to_quarterly(df: pd.DataFrame, method: str = "mean") -> pd.DataFrame:
    """Convert monthly FEDFUNDS to quarterly frequency.

    method: 'mean' (quarterly average) or 'last' (end-of-quarter)
    """
    if method == "last":
        q = df.resample("Q").last()
    else:
        q = df.resample("Q").mean()
    q.index.name = "quarter"

    # Debug prints
    print(f"\n📈 Converted to quarterly data using method='{method}'")
    print(f"Rows: {len(q)}, Columns: {list(q.columns)}")
    print("First 5 rows:")
    print(q.head())
    print("Last 5 rows:")
    print(q.tail())
    return q
