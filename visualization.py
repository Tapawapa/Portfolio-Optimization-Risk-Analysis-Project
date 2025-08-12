import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

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
        cmap='viridis', #color scheme
        marker='o', #style of points, circle.
        s=10, #parameter to control size of points, 
        alpha=0.3 #Opacity of points
    )
    #add color bar legend to label sharpe ratio
    plt.colorbar(scatter, label='Sharpe Ratio')

    #Highlight the optimal, aggressive, and conservative portfolios
    plt.scatter(
        low_risk_data['Low Risk Metrics']['Volatility'],
        low_risk_data['Low Risk Metrics']['Return'],
        c='blue', marker='X', s=250, edgecolors='black', label='Min Volatility'
    )

    plt.scatter(
        high_return_data['High Return Metrics']['Volatility'],
        high_return_data['High Return Metrics']['Return'],
        c='red', marker='P', s=250, edgecolors='black', label='Max Return'
    )
    
    plt.scatter (
        optimal_data['Optimal Metrics']['Volatility'],
        optimal_data['Optimal Metrics']['Return'],
        c='green', marker='*', s=250, edgecolors='black', label='Max Sharpe Ratio'
    )
    
    plt.title('Efficient Frontier: Portfolio Optimization', fontweight='bold')
    #Label for x and y axes
    plt.xlabel('Annualized Volatility (Risk)')
    plt.ylabel('Annualized Return')
    plt.legend(markerscale=0.7)

    #Make a PNG
    frontier_path = os.path.join(VISUALS_DIR, 'efficient_frontier.png')
    plt.savefig(frontier_path)

    plt.close()
    print(f"Efficient Frontier plot saved to {frontier_path}")

    print("Making allocation pie charts...")

    #Optimal portfolio pie chart
    allocation = optimal_data['Optimal Weights']
    labels = allocation.keys()
    sizes = allocation.values()
    plt.figure(figsize=(10,10))
    plt.pie(sizes, labels=labels, autopct='%1.2f%%', pctdistance=0.85, labeldistance=1.15)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Optimal Portfolio Asset Allocation (Max Sharpe Ratio)', pad=40, fontweight='bold')
    plt.axis('equal')
    pie_path = os.path.join(VISUALS_DIR, 'optimal_allocation_pie.png')
    plt.savefig(pie_path)
    plt.close()
    print(f"Optimal allocation pie chart saved to {pie_path}")

    # Low risk portfolio pie chart
    allocation_low_risk = low_risk_data['Low Risk Weights']
    labels_low_risk = allocation_low_risk.keys()
    sizes_low_risk = allocation_low_risk.values()
    plt.figure(figsize=(10,10))
    plt.pie(sizes_low_risk, labels=labels_low_risk, autopct='%1.2f%%', pctdistance=0.85, labeldistance=1.15)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title('Low Risk Portfolio Asset Allocation (Min Volatility)', pad=40, fontweight='bold')
    plt.axis('equal')
    pie_path_low_risk = os.path.join(VISUALS_DIR, 'low_risk_allocation_pie.png')
    plt.savefig(pie_path_low_risk)
    plt.close()
    print(f"Low risk allocation pie chart saved to {pie_path_low_risk}")

    # High return portfolio pie chart
    allocation_high_return = high_return_data['High Return Weights']
    
    # tickers to annotate
    tickers_to_annotate = ['PG Weight', 'QQQ Weight', 'SPY Weight']
    
    # get labels and sizes
    all_labels = list(allocation_high_return.keys())
    all_sizes = list(allocation_high_return.values())

    # create modified labels
    # empty string for annotated tickers
    labels_for_pie = [label if label not in tickers_to_annotate else '' for label in all_labels]

    fig, ax = plt.subplots(figsize=(12, 10))
    
    # plot pie chart
    wedges, texts, autotexts = ax.pie(
        all_sizes, 
        labels=labels_for_pie, 
        autopct='%1.2f%%', # show all percentages
        pctdistance=0.85, 
        labeldistance=1.05
    )

    # iterate autotexts
    for i, autotext in enumerate(autotexts):
        # find slice to annotate
        if all_labels[i] in tickers_to_annotate:
            # hide percentage
            autotext.set_visible(False)
    
    # donut chart
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    ax.add_artist(centre_circle)
    
    ax.set_title('High Return Portfolio Asset Allocation (Max Return)', pad=40, fontweight='bold')
    ax.axis('equal')

    # create annotation box
    annotation_text = "Specific Allocations:\n\n"
    for stock, weight in allocation_high_return.items():
        if stock in tickers_to_annotate:
            annotation_text += f"{stock}: {weight:.2%}\n"

    # place text box
    ax.text(1.1, 0.5, annotation_text.strip(), transform=ax.transAxes, fontsize=10,
            verticalalignment='center', bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.7))

    pie_path_high_return = os.path.join(VISUALS_DIR, 'high_return_allocation_pie.png')
    # ensure all elements fit
    plt.savefig(pie_path_high_return, bbox_inches='tight')
    plt.close()
    print(f"High return allocation pie chart saved to {pie_path_high_return}")


if __name__ == "__main__":
    visualize_results()
