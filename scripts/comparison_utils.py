# scripts/comparison_utils.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def load_country_data(country_name, filepath):
    """Load cleaned CSV and add country label."""
    df = pd.read_csv(filepath)
    df['Country'] = country_name
    return df


def summarize_metrics(df, metrics):
    """Return summary stats (mean, median, std) for selected metrics."""
    summary = (
        df.groupby('Country')[metrics]
        .agg(['mean', 'median', 'std'])
        .round(2)
    )
    return summary


def plot_boxplots(df, metrics):
    """Plot side-by-side boxplots for selected metrics by country."""
    for metric in metrics:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x='Country', y=metric, data=df, palette='Set2')
        plt.title(f'{metric} Distribution by Country')
        plt.xlabel('Country')
        plt.ylabel(metric)
        plt.tight_layout()
        plt.show()


def statistical_tests(df, metric='GHI'):
    """
    Run one-way ANOVA and Kruskal–Wallis tests across countries for a given metric.
    Returns both p-values and prints interpretation.
    """
    grouped = [g[metric].dropna() for _, g in df.groupby('Country')]

    # One-way ANOVA
    f_stat, p_anova = stats.f_oneway(*grouped)
    print(f"ANOVA F-statistic: {f_stat:.3f}, p-value: {p_anova:.5f}")

    # Kruskal–Wallis
    h_stat, p_kw = stats.kruskal(*grouped)
    print(f"Kruskal–Wallis H-statistic: {h_stat:.3f}, p-value: {p_kw:.5f}")

    if p_anova < 0.05:
        print("✅ ANOVA indicates significant differences among countries.")
    else:
        print("❌ ANOVA shows no significant difference.")

    if p_kw < 0.05:
        print("✅ Kruskal–Wallis indicates significant differences among countries.")
    else:
        print("❌ Kruskal–Wallis shows no significant difference.")

    return {"anova_p": p_anova, "kruskal_p": p_kw}


def plot_avg_ghi_bar(df):
    """Plot bar chart ranking countries by average GHI."""
    avg_ghi = df.groupby('Country')['GHI'].mean().sort_values(ascending=False)
    plt.figure(figsize=(6,4))
    sns.barplot(x=avg_ghi.index, y=avg_ghi.values, palette='Blues_d')
    plt.title('Average GHI by Country')
    plt.ylabel('Mean GHI')
    plt.xlabel('Country')
    plt.tight_layout()
    plt.show()
    return avg_ghi
