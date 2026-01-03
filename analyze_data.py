import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load the data
print("Loading data...")
control = pd.read_csv('data/control_group.csv', sep=';')
test = pd.read_csv('data/test_group.csv', sep=';')

# Add campaign type column
control['Campaign Type'] = 'Control'
test['Campaign Type'] = 'Test'

# Combine datasets
df = pd.concat([control, test], ignore_index=True)

print(f"\nDataset loaded successfully!")
print(f"Total rows: {len(df)}")
print(f"Control group: {len(control)} days")
print(f"Test group: {len(test)} days")
print(f"\nColumns: {list(df.columns)}")
print(f"\nFirst few rows:")
print(df.head())

# Calculate key metrics
print("\n" + "="*70)
print("KEY METRICS ANALYSIS")
print("="*70)

metrics = df.groupby('Campaign Type').agg({
    'Spend [USD]': 'sum',
    '# of Impressions': 'sum',
    'Reach': 'sum',
    '# of Website Clicks': 'sum',
    '# of Searches': 'sum',
    '# of View Content': 'sum',
    '# of Add to Cart': 'sum',
    '# of Purchase': 'sum'
}).reset_index()

# Calculate rates
metrics['CTR (%)'] = (metrics['# of Website Clicks'] / metrics['# of Impressions'] * 100).round(2)
metrics['Conversion Rate (%)'] = (metrics['# of Purchase'] / metrics['Reach'] * 100).round(2)
metrics['CPA (USD)'] = (metrics['Spend [USD]'] / metrics['# of Purchase']).round(2)
metrics['ROAS'] = (metrics['# of Purchase'] * 50 / metrics['Spend [USD]']).round(2)  # Assuming $50 per purchase

print(metrics)

# Save metrics
metrics.to_csv('results/metrics_summary.csv', index=False)
print("\n✓ Metrics saved to results/metrics_summary.csv")

