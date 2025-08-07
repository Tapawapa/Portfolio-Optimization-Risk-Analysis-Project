import data_fetch
import returns_analysis
import monte_carlo_sim
import optimization
# import visualization 

def main():
    data_fetch.fetch_data()
    returns_analysis.analyze_returns()
    monte_carlo_sim.monte_carlo_simulation()
    optimization.find_optimal_portfolios()
    optimization.high_return_portfolio()
    optimization.low_risk_portfolio()
    # visualization.visualize_results()

if __name__ == '__main__':
    main()
