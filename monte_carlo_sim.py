import pandas as pd
import numpy as np
import os

DATA_DIR = 'data'
RESULTS_DIR = 'results'
RETURNS_FILE = os.path.join(DATA_DIR, 'returns.csv')
COV_MATRIX_FILE = os.path.join(DATA_DIR, 'cov_matrix.csv')
OUTPUT_FILE = os.path.join(RESULTS_DIR, 'monte_carlo_simulation.csv')

#Simulated portfolios
NUM_PORTFOLIOS = 50000
#ROI on an investment that is considered risk-free
RISK_FREE_RATE = 0.02

def monte_carlo_simulation():
    """ Runs a Monte Carlo simulation to generate random portfolios and calculate their performance metrics."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    #load returns and covariance matrix into dataframes
    returns = pd.read_csv(RETURNS_FILE, index_col='Date')
    
    # --- THIS IS THE FIX ---
    # The covariance matrix's index is the first column (the tickers), not 'Date'.
    covariance_matrix = pd.read_csv(COV_MATRIX_FILE, index_col=0)

    #get mean annual return for each stock
    mean_returns = returns.mean() * 252

    tickers = mean_returns.index
    #gets the number of tickers len calcs amount of an object
    num_assets = len(tickers)
    #prepare lists to store results
    portfolio_returns = []
    portfolio_volatility = []
    portfolio_weights = []

    print(f"Running Monte Carlo simulation with {NUM_PORTFOLIOS} portfolios...")
    for i in range(NUM_PORTFOLIOS):
        #generate random weights
        weights = np.random.random(num_assets)
        #normalize to sum to 1
        weights /= np.sum(weights)
        portfolio_weights.append(weights)

        #calculate annual return of portfolio
        port_return = np.dot(weights, mean_returns)
        portfolio_returns.append(port_return)

        #calculate annual volitility of portfolio
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))
        portfolio_volatility.append(port_volatility)

    #Create a dictionary to hold results
    data = {
            'Return': portfolio_returns,
            'Volatility': portfolio_volatility
            }
    #add weights for each stock to dictionary
    for counter, symbol in enumerate(tickers):
        data[symbol + ' Weight'] = [w[counter] for w in portfolio_weights]

    #Create final df from reuslts dictionary
    results_df = pd.DataFrame(data)
    #calculate Sharpe ratio for each portfolio
    results_df['Sharpe Ratio'] = (results_df['Return'] - RISK_FREE_RATE) / results_df['Volatility']

    print("Simulation complete. Saving results...")

    #save results to csv
    results_df.to_csv(OUTPUT_FILE, index=False)

if __name__ == "__main__":
    monte_carlo_simulation()