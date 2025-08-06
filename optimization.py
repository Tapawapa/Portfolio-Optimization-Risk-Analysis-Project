import pandas as pd
import os
import json

RESULTS_DIR = 'results'
SIM_FILE = os.path.join(RESULTS_DIR, 'monte_carlo_simulation.csv')
OUTPUT_FILE = os.path.join(RESULTS_DIR, 'optimal_portfolios.json')

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
    # FIX: Identify weight columns by excluding the metric columns.
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

if __name__ == "__main__":
    find_optimal_portfolios()
