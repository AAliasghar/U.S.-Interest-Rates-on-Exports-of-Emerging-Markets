import argparse
from datetime import datetime
import pandas as pd
from pandas_datareader.data import DataReader

def fetch_fedfunds(start: str, end: str) -> pd.DataFrame:
    """Fetch monthly Effective Federal Funds Rate (FEDFUNDS) from FRED."""
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end)
    df = DataReader('FEDFUNDS', 'fred', start_dt, end_dt)
    df = df.rename(columns={'FEDFUNDS': 'fedfunds'})
    df.index.name = 'date'
    return df

def to_quarterly(df: pd.DataFrame, method: str = 'mean') -> pd.DataFrame:
    """Convert monthly FEDFUNDS to quarterly frequency.

    method: 'mean' (quarterly average) or 'last' (end-of-quarter)
    """
    if method == 'last':
        q = df.resample('Q').last()
    else:
        q = df.resample('Q').mean()
    q.index.name = 'quarter'
    return q

def main():
    parser = argparse.ArgumentParser(description='Step 1: Fetch U.S. FEDFUNDS and convert to quarterly.')
    parser.add_argument('--start', default='1990-01-01', help='Start date YYYY-MM-DD')
    parser.add_argument('--end', default=datetime.today().strftime('%Y-%m-%d'), help='End date YYYY-MM-DD')
    parser.add_argument('--quarterly_method', default='mean', choices=['mean', 'last'], help='Aggregation method to quarterly')
    args = parser.parse_args()

    # Fetch
    monthly = fetch_fedfunds(args.start, args.end)

    # Convert to quarterly
    quarterly = to_quarterly(monthly, method=args.quarterly_method)

    # Save
    out_dir = pd.Path = None  # placeholder to appease linters
    out_dir = 'data'
    import os
    os.makedirs(out_dir, exist_ok=True)
    monthly.to_csv(f'{out_dir}/us_fedfunds_monthly.csv', index=True)
    quarterly.to_csv(f'{out_dir}/us_fedfunds_quarterly.csv', index=True)

    print('Saved:')
    print(f' - {out_dir}/us_fedfunds_monthly.csv (rows={len(monthly)})')
    print(f' - {out_dir}/us_fedfunds_quarterly.csv (rows={len(quarterly)})')

if __name__ == '__main__':
    main()
