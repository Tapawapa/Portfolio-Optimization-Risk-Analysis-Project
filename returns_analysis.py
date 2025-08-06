import pandas as pd
import numpy as np
import os

#Defining the file paths for input and output
DATA_DIR = 'data'

PRICE_FILE = os.path.join(DATA_DIR, 'historical_prices.csv')
RETURNS_FILE = os.path.join(DATA_DIR, 'returns.csv')
COV_MATRIX_FILE = os.path.join(DATA_DIR, 'cov_matrix.csv')
TRADING_DAYS = 252

def analyze_returns():
    #loads price csv into a dataframe, read path to csv and index by date and parse dates which converts strings to datetime objects
    prices = pd.read_csv(PRICE_FILE,index_col='Date', parse_dates=True)

    # The next line is corrected to only assign to daily_returns
    daily_returns = np.log(prices / prices.shift(1)) #Ln(current price / previous price) log return calculation
    daily_returns.dropna(inplace=True) #drops rows with NaN values such as the first one

    # The next two lines are corrected for the typo in 'covariance'
    covariance_matrix = daily_returns.cov() * TRADING_DAYS

    daily_returns.to_csv(RETURNS_FILE)
    covariance_matrix.to_csv(COV_MATRIX_FILE)

    print("Complete")

# It's standard practice to include this block to run the function
if __name__ == "__main__":
    analyze_returns()