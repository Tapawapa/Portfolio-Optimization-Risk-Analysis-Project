import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

RESULTS_DIR = 'results'
VISUALS_DIR = 'visuals'
SIM_FILE = os.path.join(RESULTS_DIR, 'monte_carlo_simulation.csv')
OPTIMAL_FILE = os.path.join(RESULTS_DIR, 'optimal_portfolios.json')
HIGH_RETURN_FILE = os.path.join(RESULTS_DIR, 'high_return_portfolio.json')
LOW_RISK_FILE = os.path.join(RESULTS_DIR, 'low_risk_portfolio.json')

def visualize_results():
    """ Generates visualizations for the Monte Carlo simulation results as well as the generated portfolios"""
    required_files = [SIM_FILE, OPTIMAL_FILE, HIGH_RETURN_FILE, LOW_RISK_FILE]
    if not all(os.path.exists(f) for f in required_files):
        print("Not all files found.")
        print("Run optimization.py to generate them.")
        return
    
    os.makedirs(VISUALS_DIR, exist_ok=True)
    sim_results = pd.read_csv(SIM_FILE)
    #Load portfolio data
    with open(OPTIMAL_FILE, 'r') as f:
        optimal_data = json.load(f)
    with open(HIGH_RETURN_FILE, 'r') as f:
        high_return_data = json.load(f)
    with open(LOW_RISK_FILE, 'r') as f:
        low_risk_data = json.load(f)
    #Efficient Frontier Plot 
    plt.style.use('seaborn-v0_8-darkgrid') #Custom style or theme
    plt.figure(figsize=(12,8)) #dimensions of frontier plot

    #Scatter plot of all simulated portfolios
    scatter = plt.scatter (
        sim_results['Volatility'],
        sim_results['Return'],
        c=sim_results['Sharpe Ratio'],
        cmap='viridis',
        marker='o',
        s=10,
        alpha=0.3
    )
    
 

    



