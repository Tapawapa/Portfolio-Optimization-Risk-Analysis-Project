import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA','NVDA','META','JPM','V','JNJ','WMT','PG','CVX','MA', 'SPY', 'QQQ']
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365*10)

OUTPUT_DIR = 'data'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'historical_prices.csv')

def fetch_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Fetching data for tickers: {', '.join(TICKERS)}")
    print(f"Date range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")

    try:
        full_data = yf.download(TICKERS, start=START_DATE, end=END_DATE, auto_adjust=False)
        prices = full_data['Adj Close']
        
        print(f"Initial download complete. Shape of data: {prices.shape}")

        if prices.empty:
            print("Error: No data was downloaded.")
            return

        print("Cleaning data...")
        prices.fillna(method='ffill', inplace=True)
        prices.dropna(inplace=True)
        
        print(f"Data cleaning complete. Final shape of data: {prices.shape}")

        prices.to_csv(OUTPUT_FILE)
        print(f"\nSuccess! Clean data has been saved to: {OUTPUT_FILE}")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    fetch_data()