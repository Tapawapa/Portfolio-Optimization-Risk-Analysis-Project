import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

# --- Configuration ---
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JNJ', 'TSLA', 'SPY']
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365*10)

OUTPUT_DIR = 'data'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'historical_prices.csv')

def fetch_data():
    """
    Fetches historical stock prices and saves a clean CSV
    containing only the 'Adj Close' prices.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Fetching data for tickers: {', '.join(TICKERS)}")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")

    try:
        # Auto adjust set to false so we can manually take only the adjusted close column from the data
        full_data = yf.download(TICKERS, start=START_DATE, end=END_DATE, auto_adjust=False)
        #selects only the adj close colummn
        data = full_data['Adj Close']
        #full fill moves previous values forward when a value is null
        data.fillna(method='ffill', inplace=True)
        data.dropna(inplace=True)
        data.to_csv(OUTPUT_FILE)
        print(f"\nSuccess! Clean data saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"\nAn error occurred while fetching data: {e}")

if __name__ == "__main__":
    fetch_data()