
"""
This script performs a comprehensive A/B testing analysis on a marketing campaign dataset.
It compares a 'Control' campaign with a 'Test' campaign to determine which is more effective.

The analysis includes:
1. Data loading and cleaning.
2. Calculation of key performance indicators (KPIs) like CTR, Conversion Rate, CPA, and ROAS.
3. Statistical significance testing (t-test) on key metrics.
4. Generation of visualizations for comparison.
5. A full customer conversion funnel analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# --- Configuration ---
sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 300
RESULTS_DIR = "results"
IMAGES_DIR = "images"

# Create output directories if they don't exist
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# --- 1. Data Loading and Preparation ---
def load_and_prepare_data(control_path, test_path):
    """Loads, cleans, and merges the control and test group data."""
    try:
        control_df = pd.read_csv(control_path, sep=';')
        test_df = pd.read_csv(test_path, sep=';')
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure the data files are in the 'data/' directory.")
        return None

    # Add a campaign type identifier
    control_df['Campaign Type'] = 'Control'
    test_df['Campaign Type'] = 'Test'

    # Combine the datasets
    df = pd.concat([control_df, test_df], ignore_index=True)

    # Clean column names
    df.columns = [col.replace(' ', '_').replace('[USD]', '').replace('#_of_', '').strip('_') for col in df.columns]
    df = df.rename(columns={'Spend': 'Spend_USD'})

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

    # Handle potential missing values (e.g., fill with 0)
    df = df.fillna(0)

    print("Data loaded and prepared successfully.")
    print(f"Total records: {len(df)}")
    return df

# --- 2. KPI Calculation ---
def calculate_kpis(df):
    """Calculates aggregate KPIs for each campaign type."""
    # Aggregate totals
    kpis = df.groupby('Campaign_Type').agg(
        Total_Spend=('Spend_USD', 'sum'),
        Total_Impressions=('Impressions', 'sum'),
        Total_Reach=('Reach', 'sum'),
        Total_Clicks=('Website_Clicks', 'sum'),
        Total_Searches=('Searches', 'sum'),
        Total_View_Content=('View_Content', 'sum'),
        Total_Add_to_Cart=('Add_to_Cart', 'sum'),
        Total_Purchases=('Purchase', 'sum')
    ).reset_index()

    # Calculate rates and efficiency metrics
    kpis['CTR_%'] = (kpis['Total_Clicks'] / kpis['Total_Impressions'] * 100)
    kpis['Conversion_Rate_%'] = (kpis['Total_Purchases'] / kpis['Total_Reach'] * 100)
    kpis['CPA_USD'] = (kpis['Total_Spend'] / kpis['Total_Purchases'])
    # Assuming an average order value of $50 for ROAS calculation
    kpis['ROAS'] = (kpis['Total_Purchases'] * 50) / kpis['Total_Spend']

    print("\n--- Key Performance Indicators (KPIs) ---")
    print(kpis.round(2))
    kpis.to_csv(f"{RESULTS_DIR}/kpi_summary.csv", index=False)
    print(f"\nKPI summary saved to {RESULTS_DIR}/kpi_summary.csv")
    return kpis

# --- 3. Statistical Significance Testing ---
def perform_statistical_tests(df):
    """Performs t-tests to check for statistical significance between groups."""
    control_group = df[df['Campaign_Type'] == 'Control']
    test_group = df[df['Campaign_Type'] == 'Test']

    # We will test the daily purchases and daily clicks
    purchase_ttest = stats.ttest_ind(control_group['Purchase'], test_group['Purchase'], equal_var=False)
    clicks_ttest = stats.ttest_ind(control_group['Website_Clicks'], test_group['Website_Clicks'], equal_var=False)

    results = {
        "Metric": ["Daily Purchases", "Daily Website Clicks"],
        "T-Statistic": [purchase_ttest.statistic, clicks_ttest.statistic],
        "P-Value": [purchase_ttest.pvalue, clicks_ttest.pvalue],
        "Significant_at_alpha_0.05": [purchase_ttest.pvalue < 0.05, clicks_ttest.pvalue < 0.05]
    }
    results_df = pd.DataFrame(results)

    print("\n--- Statistical Significance Tests (T-Tests) ---")
    print(results_df.round(4))
    results_df.to_csv(f"{RESULTS_DIR}/statistical_tests.csv", index=False)
    print(f"\nStatistical test results saved to {RESULTS_DIR}/statistical_tests.csv")
    return results_df

# --- 4. Visualization ---
def create_visualizations(kpis, df):
    """Generates and saves all visualizations for the analysis."""
    colors = {"Control": "#4C72B0", "Test": "#55A868"}

    # Plot 1: KPI Dashboard
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Campaign Performance Dashboard', fontsize=18, fontweight='bold')

    # Subplot: Conversion Rate
    sns.barplot(ax=axes[0, 0], x='Campaign_Type', y='Conversion_Rate_%', data=kpis, palette=colors)
    axes[0, 0].set_title('Conversion Rate (Purchases / Reach)', fontweight='bold')
    axes[0, 0].set_ylabel('Conversion Rate (%)')

    # Subplot: Cost Per Acquisition (CPA)
    sns.barplot(ax=axes[0, 1], x='Campaign_Type', y='CPA_USD', data=kpis, palette=colors)
    axes[0, 1].set_title('Cost Per Acquisition (CPA)', fontweight='bold')
    axes[0, 1].set_ylabel('CPA (USD)')

    # Subplot: Click-Through Rate (CTR)
    sns.barplot(ax=axes[1, 0], x='Campaign_Type', y='CTR_%', data=kpis, palette=colors)
    axes[1, 0].set_title('Click-Through Rate (CTR)', fontweight='bold')
    axes[1, 0].set_ylabel('CTR (%)')

    # Subplot: Return on Ad Spend (ROAS)
    sns.barplot(ax=axes[1, 1], x='Campaign_Type', y='ROAS', data=kpis, palette=colors)
    axes[1, 1].set_title('Return on Ad Spend (ROAS)', fontweight='bold')
    axes[1, 1].set_ylabel('ROAS (Ratio)')

    for ax in axes.flat:
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=11, color='black', xytext=(0, 5),
                        textcoords='offset points')
        ax.set_xlabel('')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f"{IMAGES_DIR}/kpi_dashboard.png")
    print(f"\nVisualization saved: {IMAGES_DIR}/kpi_dashboard.png")
    plt.close()

    # Plot 2: Funnel Analysis
    funnel_stages = ['Impressions', 'Reach', 'Website_Clicks', 'Searches', 'View_Content', 'Add_to_Cart', 'Purchase']
    funnel_df = df.groupby('Campaign_Type')[funnel_stages].sum().reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(16, 7), sharex=True)
    fig.suptitle('Marketing Conversion Funnel Analysis', fontsize=18, fontweight='bold')

    for i, campaign in enumerate(['Control', 'Test']):
        ax = axes[i]
        campaign_data = funnel_df[funnel_df['Campaign_Type'] == campaign].iloc[0]
        values = campaign_data[funnel_stages].values
        percentages = (values / values[0] * 100)

        ax.barh(funnel_stages, percentages, color=colors[campaign], edgecolor='black')
        ax.set_title(f'{campaign} Campaign', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        ax.set_xlabel('Conversion from Impression (%)')

        for j, (p, v) in enumerate(zip(percentages, values)):
            ax.text(p + 1, j, f'{p:.1f}% ({v:,.0f})', va='center', fontsize=9)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f"{IMAGES_DIR}/funnel_analysis.png")
    print(f"Visualization saved: {IMAGES_DIR}/funnel_analysis.png")
    plt.close()

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Starting A/B Testing Analysis ---")
    main_df = load_and_prepare_data('data/control_group.csv', 'data/test_group.csv')
    if main_df is not None:
        kpi_summary = calculate_kpis(main_df)
        perform_statistical_tests(main_df)
        create_visualizations(kpi_summary, main_df)
        print("\n--- Analysis Complete ---")
