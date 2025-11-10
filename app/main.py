import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.append(project_root)

from scripts import comparison_utils as cu

# --- Streamlit page setup ---
st.set_page_config(
    page_title="Country Comparison Dashboard",
    layout="wide",
    page_icon="🌍"
)


st.title("🌍 Country Data Comparison Dashboard")
st.markdown(
    """
    This interactive dashboard allows you to:
    - Upload datasets for multiple countries  
    - Compare metrics (like **GHI**) across countries  
    - View summary statistics and statistical test results  
    """
)

# --- Sidebar: File Uploads ---
st.sidebar.header("📂 Upload Country CSV Files")

uploaded_files = st.sidebar.file_uploader(
    "Upload one or more CSV files (each representing a country)",
    type=["csv"],
    accept_multiple_files=True
)

if uploaded_files:
    dfs = []
    for file in uploaded_files:
        country_name = st.text_input(
            f"Enter country name for file `{file.name}`:",
            value=file.name.replace(".csv", "")
        )
        df = pd.read_csv(file)
        df['Country'] = country_name
        dfs.append(df)

    # Combine all data
    full_df = pd.concat(dfs, ignore_index=True)

    # --- Sidebar: Metric Selection ---
    numeric_cols = full_df.select_dtypes(include="number").columns.tolist()
    if not numeric_cols:
        st.warning("No numeric columns found in uploaded files.")
    else:
        st.sidebar.header("⚙️ Analysis Settings")
        selected_metrics = st.sidebar.multiselect(
            "Select metrics to analyze:",
            numeric_cols,
            default=["GHI"] if "GHI" in numeric_cols else numeric_cols[:1]
        )

        # --- Tabs for visualizations ---
        tab1, tab2, tab3 = st.tabs(["📊 Boxplots", "📈 Summary Statistics", "🧠 Statistical Tests"])

        # --- BOX PLOTS ---
        with tab1:
            st.subheader("Distribution by Country")
            for metric in selected_metrics:
                fig, ax = plt.subplots(figsize=(8, 5))
                cu.sns.boxplot(x='Country', y=metric, data=full_df, palette='Set2', ax=ax)
                ax.set_title(f"{metric} Distribution by Country")
                st.pyplot(fig)

        # --- SUMMARY STATS ---
        with tab2:
            st.subheader("Summary Statistics")
            summary_df = cu.summarize_metrics(full_df, selected_metrics)
            st.dataframe(summary_df)

            st.subheader("Average GHI (Ranking)")
            if "GHI" in full_df.columns:
                avg_ghi = full_df.groupby('Country')['GHI'].mean().sort_values(ascending=False)
                fig, ax = plt.subplots(figsize=(6, 4))
                cu.sns.barplot(x=avg_ghi.index, y=avg_ghi.values, palette='Blues_d', ax=ax)
                ax.set_title('Average GHI by Country')
                st.pyplot(fig)

        # --- STATISTICAL TESTS ---
        with tab3:
            st.subheader("One-way ANOVA & Kruskal–Wallis Tests")
            for metric in selected_metrics:
                st.write(f"### {metric}")
                results = cu.statistical_tests(full_df, metric)
                st.write(f"**ANOVA p-value:** {results['anova_p']:.5f}")
                st.write(f"**Kruskal–Wallis p-value:** {results['kruskal_p']:.5f}")
else:
    st.info("👈 Please upload CSV files from the sidebar to begin analysis.")
