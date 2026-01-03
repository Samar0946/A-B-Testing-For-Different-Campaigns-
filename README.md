# A/B Testing Analysis of Marketing Campaigns

![KPI Dashboard](./images/kpi_dashboard.png)

## 1. Business Problem & Objective

A marketing team ran two campaigns simultaneously to determine the most effective strategy for acquiring new customers. The **Control Campaign** used a traditional marketing approach, while the **Test Campaign** implemented a new, experimental strategy.

The objective of this analysis is to conduct a comprehensive A/B test to determine which campaign was more successful. The key success metrics are **Conversion Rate** (purchases per reach) and **Cost Per Acquisition (CPA)**. The final recommendation will guide future marketing spend.

## 2. Dataset

This project uses the "A/B Testing DataSet" from Kaggle, which contains daily performance data for two marketing campaigns over a 30-day period.

- **Source:** [Kaggle A/B Testing DataSet](https://www.kaggle.com/datasets/amirmotefaker/ab-testing-dataset)
- **Files:** `control_group.csv`, `test_group.csv`

Each file contains 10 columns, including `Spend`, `Impressions`, `Reach`, `Website Clicks`, and `Purchase`.

## 3. Methodology

My analysis followed a structured, multi-step approach:

1.  **Data Preparation:** Loaded both datasets, cleaned column names, and merged them into a single DataFrame for comparative analysis.
2.  **KPI Calculation:** Calculated key performance indicators (KPIs) for each campaign, including:
    -   Click-Through Rate (CTR)
    -   Conversion Rate (Purchases / Reach)
    -   Cost Per Acquisition (CPA)
    -   Return on Ad Spend (ROAS) (assuming a $50 average order value)
3.  **Statistical Significance:** Performed an independent t-test on daily purchases and website clicks to determine if the observed differences were statistically significant (using α = 0.05).
4.  **Funnel Analysis:** Visualized the entire customer journey for both campaigns, from initial impression to final purchase, to identify drop-off points.
5.  **Visualization:** Created a KPI dashboard and a funnel analysis chart to clearly communicate the findings.

## 4. Key Findings & Results

### Overall Performance

The analysis revealed a clear trade-off between the two campaigns:

| Metric | Control Campaign | Test Campaign | Winner |
| :--- | :--- | :--- | :--- |
| **Conversion Rate** | 0.59% | **0.97%** | **Test** (+64%) |
| **Click-Through Rate (CTR)** | 4.86% | **8.09%** | **Test** (+66%) |
| **Cost Per Acquisition (CPA)** | **$4.53** | $4.92 | **Control** (-8%) |
| **Return on Ad Spend (ROAS)** | **11.04x** | 10.17x | **Control** (+8.5%) |

-   The **Test Campaign** was significantly more effective at engaging users, achieving a **64% higher conversion rate** and a **66% higher CTR**.
-   However, the **Control Campaign** was more cost-efficient, with a **lower CPA** and a **higher ROAS**.

### Statistical Significance

The t-test results showed that the differences in daily purchases and clicks were **not statistically significant** (p-value > 0.05). This is likely due to the small sample size (30 days). While the overall trends are strong, the daily variations are too high to make a definitive statistical conclusion from this dataset alone.

### Funnel Analysis

![Funnel Analysis](./images/funnel_analysis.png)

The funnel analysis shows that the **Test Campaign** was much better at the top of the funnel (getting clicks from impressions). However, the **Control Campaign** was more effective at converting users who had already shown interest (e.g., from Add to Cart to Purchase).

## 5. Business Recommendation

Based on the analysis, I recommend a **hybrid approach**:

1.  **Adopt the Test Campaign's Strategy for Top-of-Funnel Activities:** The Test Campaign's creative and targeting strategy is clearly superior for generating impressions and clicks. This approach should be used for all awareness-focused marketing efforts.

2.  **Adopt the Control Campaign's Strategy for Mid-Funnel Activities:** The Control Campaign was more efficient at converting interested users. Its messaging and user experience should be analyzed and applied to the website and checkout process to improve conversion rates for users who have already clicked or added items to their cart.

**Conclusion:** Neither campaign is a clear winner on all fronts. The most profitable path forward is to combine the strengths of both campaigns. The Test Campaign is better for **acquisition**, while the Control Campaign is better for **conversion efficiency**.

## 6. How to Run This Project

1.  Clone this repository:
    ```bash
    git clone https://github.com/your-username/marketing-ab-testing.git
    cd marketing-ab-testing
    ```
2.  Create the data directory and download the data:
    ```bash
    mkdir data
    # Download control_group.csv and test_group.csv into the data/ folder
    ```
3.  Install the required libraries:
    ```bash
    pip install pandas matplotlib seaborn scipy
    ```
4.  Run the analysis script:
    ```bash
    python marketing_ab_analysis.py
    ```

**Technologies Used:**
- Python
- Pandas
- Matplotlib
- Seaborn
- SciPy
