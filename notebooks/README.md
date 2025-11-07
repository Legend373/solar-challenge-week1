Notebook Workflow

Each country notebook follows this end-to-end EDA workflow:

1. Load Dataset

Load raw dataset from data/raw/<country>.csv.

Inspect shape, column types, and sample rows.

2. Summary Statistics & Missing-Value Report

Use df.describe() on numeric columns.

Report missing values per column (df.isna().sum()) and highlight any column with >5% nulls.

3. Outlier Detection & Basic Cleaning

Identify outliers in key columns: GHI, DNI, DHI, ModA, ModB, WS, WSgust.

Compute Z-scores and flag rows with |Z|>3.

Handle missing values using median imputation or drop remaining NAs.

Save cleaned dataset to data/cleaned/<country>_clean.csv (ignored in Git).

4. Time Series Analysis

Line/bar plots of GHI, DNI, DHI, Tamb vs. Timestamp.

Monthly averages to observe seasonal trends and anomalies.

5. Cleaning Impact

Group by Cleaning flag and visualize the effect on ModA and ModB.

6. Correlation & Relationship Analysis

Heatmaps of correlations for GHI, DNI, DHI, TModA, TModB.

Scatter plots: WS, WSgust, WD vs GHI and RH vs Tamb / RH vs GHI.

7. Wind & Distribution Analysis

Wind rose or radial bar plots for wind speed (WS) and direction (WD).

Histograms for GHI and other variables (WS).

8. Temperature Analysis

Examine relationships between relative humidity (RH), temperature (Tamb), and solar radiation.

9. Bubble Chart

Scatter plot of GHI vs Tamb with bubble size representing RH or BP to visualize combined effects.

⚡ Key Guidelines

Data Handling

Never commit cleaned datasets (data/cleaned/) to Git.

Always work from raw datasets for reproducibility.

Reusability

Notebooks are country-specific but structured identically.

Use benin_eda.ipynb as a template for other countries.

Visualization

Charts provide actionable insights into solar irradiance, wind, temperature, and humidity.

Color maps, bubble sizes, and transparency (alpha) are used for clarity.

Dependencies

Python ≥ 3.11

Key packages: pandas, numpy, matplotlib, seaborn, scipy

Installed via pip install -r requirements.txt

🔄 Workflow for New Country

Create a new branch: eda-<country>.

Copy benin_eda.ipynb to <country>_eda.ipynb.

Update the notebook to load data/raw/<country>.csv.

Run all cells to clean, analyze, and visualize the dataset.

Export cleaned dataset to data/cleaned/<country>_clean.csv.

Commit notebook changes and push the branch for PR/merge.

📊 Outcome

After completing a country notebook, you will have:

A cleaned dataset ready for comparison.

Comprehensive EDA visualizations (time series, correlations, wind analysis, temperature effects).

Insights to rank regions based on solar irradiance, wind, and environmental conditions.