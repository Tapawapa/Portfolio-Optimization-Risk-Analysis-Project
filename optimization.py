import pandas as pd
import os
import json

RESULTS_DIR = 'results'
SIM_FILE = os.path.join(RESULTS_DIR, 'monte_carlo_simulation.csv')
OUTPUT_FILE = os.path.join(RESULTS_DIR, 'optimal_portfolios.json')
OUTPUT_FILE_2 = os.path.join(RESULTS_DIR, 'high_return_portfolio.json')
OUTPUT_FILE_3 = os.path.join(RESULTS_DIR, 'low_risk_portfolio.json')

def find_optimal_portfolios():
    
    if not os.path.exists(SIM_FILE):
        print(f"{SIM_FILE} not found. Please run the Monte Carlo simulation first.")
        return
    sim_results = pd.read_csv(SIM_FILE)

    #locate the row with highest Sharpe Ratio
    optimal_portfolio = sim_results.loc[sim_results['Sharpe Ratio'].idxmax()]

    print("Optimal Portfolio based on Sharpe Ratio:")
    print(optimal_portfolio)
    #get the metrics for the optimal portfolio
    optimal_metrics = {
        'Return': optimal_portfolio['Return'],
        'Volatility': optimal_portfolio['Volatility'],
        'Sharpe Ratio': optimal_portfolio['Sharpe Ratio']
    }
    
    #get the weights for each stock in the optimal portfolio
    all_cols = sim_results.columns.tolist()
    weight_cols = [col for col in all_cols if col not in ['Return', 'Volatility', 'Sharpe Ratio']]
    optimal_weights = optimal_portfolio[weight_cols].to_dict()

    output_data = {
        'Optimal Metrics': optimal_metrics,
        'Optimal Weights': optimal_weights
    }
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output_data, f, indent=4)
    print(f"\nOptimal portfolio details saved to {OUTPUT_FILE}")

#locating the portfolio with the highest return
def high_return_portfolio():
    if not os.path.exists(SIM_FILE):
        print(f"{SIM_FILE} not found. Please run the Monte Carlo simulation first.")
        return
    sim_results = pd.read_csv(SIM_FILE)
    #locate the row with highest Return
    high_return_port = sim_results.loc[sim_results['Return'].idxmax()]
    print("Portfolio with Highest Return:")
    print(high_return_port)
    high_return_metrics = {
        'Return': high_return_port['Return'],
        'Volatility': high_return_port['Volatility'],
        'Sharpe Ratio': high_return_port['Sharpe Ratio']
    }

    all_cols = sim_results.columns.tolist()
    weight_cols = [col for col in all_cols if col not in ['Return', 'Volatility', 'Sharpe Ratio']]
    high_return_weights = high_return_port[weight_cols].to_dict()

    output_data_2 = {
        'High Return Metrics': high_return_metrics,
        'High Return Weights': high_return_weights
    }
    with open(OUTPUT_FILE_2, 'w') as f:
        json.dump(output_data_2, f, indent=4)
    print(f"\nHigh return portfolio details saved to {OUTPUT_FILE_2}")

#Identifying the portfolio with the lowest risk (volatility)
def low_risk_portfolio():

    if not os.path.exists(SIM_FILE):
        print(f"{SIM_FILE} not found. Please run the Monte Carlo simulation first.")
        return
    sim_results = pd.read_csv(SIM_FILE)
    #locate the row with lowest Volatility
    low_risk_port = sim_results.loc[sim_results['Volatility'].idxmin()]
    print("Portfolio with Lowest Risk (Volatility):")
    print(low_risk_port)

    low_risk_metrics = {
        'Return': low_risk_port['Return'],
        'Volatility': low_risk_port['Volatility'],
        'Sharpe Ratio': low_risk_port['Sharpe Ratio']
    }

    all_cols = sim_results.columns.tolist()
    weight_cols = [col for col in all_cols if col not in ['Return', 'Volatility', 'Sharpe Ratio']]
    low_risk_weights = low_risk_port[weight_cols].to_dict()

    output_data_3 = {
        'Low Risk Metrics': low_risk_metrics,
        'Low Risk Weights': low_risk_weights
    }
    with open(OUTPUT_FILE_3, 'w') as f:
        json.dump(output_data_3, f, indent=4)
    print(f"\nLow risk portfolio details saved to {OUTPUT_FILE_3}")


    
if __name__ == "__main__":
    find_optimal_portfolios()
    high_return_portfolio()
    low_risk_portfolio()

