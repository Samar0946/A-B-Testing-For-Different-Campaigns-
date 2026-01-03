import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300

# Load data
control = pd.read_csv('data/control_group.csv', sep=';')
test = pd.read_csv('data/test_group.csv', sep=';')
metrics = pd.read_csv('results/metrics_summary.csv')

# Visualization 1: Conversion Rate Comparison
fig, ax = plt.subplots(figsize=(10, 6))
campaigns = metrics['Campaign Type']
conv_rates = metrics['Conversion Rate (%)']
colors = ['#4C72B0', '#55A868']

bars = ax.bar(campaigns, conv_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_title('Conversion Rate Comparison: Control vs Test Campaign', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Campaign Type', fontsize=13, fontweight='bold')
ax.set_ylabel('Conversion Rate (%)', fontsize=13, fontweight='bold')
ax.set_ylim(0, max(conv_rates) * 1.3)

for i, (bar, rate) in enumerate(zip(bars, conv_rates)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
            f'{rate:.2f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('images/conversion_rate_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: conversion_rate_comparison.png")
plt.close()

# Visualization 2: Cost Per Acquisition (CPA)
fig, ax = plt.subplots(figsize=(10, 6))
cpa = metrics['CPA (USD)']

bars = ax.bar(campaigns, cpa, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
ax.set_title('Cost Per Acquisition (CPA) Comparison', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Campaign Type', fontsize=13, fontweight='bold')
ax.set_ylabel('CPA (USD)', fontsize=13, fontweight='bold')
ax.set_ylim(0, max(cpa) * 1.3)

for bar, cost in zip(bars, cpa):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
            f'${cost:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('images/cpa_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: cpa_comparison.png")
plt.close()

# Visualization 3: Funnel Analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

for idx, (campaign_type, color) in enumerate(zip(['Control', 'Test'], colors)):
    data = metrics[metrics['Campaign Type'] == campaign_type].iloc[0]
    
    stages = ['Reach', 'Clicks', 'Searches', 'View Content', 'Add to Cart', 'Purchase']
    values = [
        data['Reach'],
        data['# of Website Clicks'],
        data['# of Searches'],
        data['# of View Content'],
        data['# of Add to Cart'],
        data['# of Purchase']
    ]
    
    # Normalize to percentages
    percentages = [v / values[0] * 100 for v in values]
    
    ax = ax1 if idx == 0 else ax2
    y_pos = np.arange(len(stages))
    
    ax.barh(y_pos, percentages, color=color, alpha=0.7, edgecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages)
    ax.set_xlabel('Percentage of Initial Reach (%)', fontsize=11, fontweight='bold')
    ax.set_title(f'{campaign_type} Campaign Funnel', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 110)
    
    for i, (v, p) in enumerate(zip(values, percentages)):
        ax.text(p + 2, i, f'{p:.1f}%', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('images/funnel_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: funnel_analysis.png")
plt.close()

# Visualization 4: Key Metrics Dashboard
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Campaign Performance Dashboard', fontsize=18, fontweight='bold', y=0.995)

# Subplot 1: Total Spend
ax = axes[0, 0]
spend = metrics['Spend [USD]']
ax.bar(campaigns, spend, color=colors, alpha=0.8, edgecolor='black')
ax.set_title('Total Spend', fontsize=13, fontweight='bold')
ax.set_ylabel('USD', fontsize=11)
for bar, s in zip(ax.patches, spend):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1000,
            f'${s:,.0f}', ha='center', fontsize=10, fontweight='bold')

# Subplot 2: Total Purchases
ax = axes[0, 1]
purchases = metrics['# of Purchase']
ax.bar(campaigns, purchases, color=colors, alpha=0.8, edgecolor='black')
ax.set_title('Total Purchases', fontsize=13, fontweight='bold')
ax.set_ylabel('Count', fontsize=11)
for bar, p in zip(ax.patches, purchases):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 200,
            f'{p:,.0f}', ha='center', fontsize=10, fontweight='bold')

# Subplot 3: CTR
ax = axes[1, 0]
ctr = metrics['CTR (%)']
ax.bar(campaigns, ctr, color=colors, alpha=0.8, edgecolor='black')
ax.set_title('Click-Through Rate (CTR)', fontsize=13, fontweight='bold')
ax.set_ylabel('Percentage (%)', fontsize=11)
for bar, c in zip(ax.patches, ctr):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.2,
            f'{c:.2f}%', ha='center', fontsize=10, fontweight='bold')

# Subplot 4: ROAS
ax = axes[1, 1]
roas = metrics['ROAS']
ax.bar(campaigns, roas, color=colors, alpha=0.8, edgecolor='black')
ax.set_title('Return on Ad Spend (ROAS)', fontsize=13, fontweight='bold')
ax.set_ylabel('Ratio', fontsize=11)
for bar, r in zip(ax.patches, roas):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
            f'{r:.2f}x', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('images/performance_dashboard.png', dpi=300, bbox_inches='tight')
print("✓ Saved: performance_dashboard.png")
plt.close()

print("\n✓ All visualizations created successfully!")
