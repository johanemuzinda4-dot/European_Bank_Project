import os
import pandas as pd
import streamlit as st

# 1. Page Configuration & Premium Theming Styling
st.set_page_config(
    page_title="European Bank | Portfolio Intelligence Group", 
    page_icon="🏦",
    layout="wide"
)

# Executive Hex Color Palette Codes
COLOR_PRIMARY = "#1E3A8A"    # Deep Navy
COLOR_SECONDARY = "#0284C7"  # Slate Blue
COLOR_ACCENT = "#E11D48"     # Risk Crimson / Accent
COLOR_MUTED = "#94A3B8"      # Cool Grey

# 2. File Ingestion Pipeline
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_PATH = os.path.join(SCRIPT_DIR, "European_Bank_clean.csv")

@st.cache_data
def load_clean_data():
    return pd.read_csv(CLEAN_PATH)

df = load_clean_data()
BASELINE_CHURN = 0.2037

# 3. Master Multi-Page Navigation Bar
st.title("🏦 European Bank Customer Analytics Framework")
navigation_mode = st.radio(
    "Select Analysis Workspace Navigation:",
    ["📊 Executive Overview Summary", "🔍 Deep-Dive Segment Analytics Workspace"],
    horizontal=True
)
st.markdown("---")

# 4. Global Top Filter Grid Dashboard Component
st.markdown("#### 🛠️ Master Filter Options")
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    selected_geo = st.multiselect("Geography / Region", options=df["Geography"].unique(), default=df["Geography"].unique())
with filter_col2:
    selected_gender = st.multiselect("Gender Demographic", options=df["Gender"].unique(), default=df["Gender"].unique())
with filter_col3:
    selected_credit = st.multiselect("Credit Score Band", options=df["Credit Score Band"].unique(), default=df["Credit Score Band"].unique())

# Filter data dynamically based on selections
filtered_df = df[
    (df["Geography"].isin(selected_geo)) & 
    (df["Gender"].isin(selected_gender)) &
    (df["Credit Score Band"].isin(selected_credit))
]

# Total metrics processing logic
total_customers = len(filtered_df)
churn_pct = filtered_df["Exited"].mean() if total_customers > 0 else 0
capital_lost = filtered_df[filtered_df["Exited"] == 1]["Balance"].sum()
total_portfolio_value = filtered_df["Balance"].sum()
churn_delta = churn_pct - BASELINE_CHURN


# =========================================================================
# WORKSPACE PAGE 1: EXECUTIVE OVERVIEW SUMMARY
# =========================================================================
if navigation_mode == "📊 Executive Overview Summary":
    
    # KPI Scorecard Metrics Row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(label="Active Portfolio Cohort", value=f"{total_customers:,}")
    with kpi2:
        st.metric(label="Cohort Churn Rate", value=f"{churn_pct:.2%}", delta=f"{churn_delta:+.2%} vs Baseline", delta_color="inverse")
    with kpi3:
        st.metric(label="Total Capital Lost via Churn", value=f"€{capital_lost:,.2f}")
    with kpi4:
        st.metric(label="Total Retained Assets", value=f"€{(total_portfolio_value - capital_lost):,.2f}")
        
    st.markdown("---")
    
    # Base Layout Visuals
    col_left, col_right = st.columns(2)
    with col_left:
        st.write("**Churn Rate by Age Segment (%)**")
        if total_customers > 0:
            age_chart_data = filtered_df.groupby("Age Segment", observed=False)["Exited"].mean() * 100
            st.bar_chart(age_chart_data, color=COLOR_PRIMARY)
            
    with col_right:
        st.write("**Churn Rate by Balance Segment (%)**")
        if total_customers > 0:
            bal_chart_data = filtered_df.groupby("Balance Segment", observed=False)["Exited"].mean() * 100
            st.bar_chart(bal_chart_data, color=COLOR_SECONDARY)

    st.markdown("---")
    st.markdown("#### 🚨 Priority Action Item: High-Risk Retention List")
    high_risk_condition = (filtered_df["Exited"] == 0) & (filtered_df["Balance"] > 0) & ((filtered_df["Age Segment"] == "46-60") | (filtered_df["Geography"] == "Germany"))
    action_list = filtered_df[high_risk_condition][["Customer ID", "Geography", "Gender", "Age", "Credit Score", "Balance"]].sort_values(by="Balance", ascending=False)
    st.dataframe(action_list.head(100), use_container_width=True)


# =========================================================================
# WORKSPACE PAGE 2: DEEP-DIVE SEGMENT ANALYTICS WORKSPACE (5 NEW CHARTS)
# =========================================================================
else:
    st.markdown("### 🔍 Advanced Portfolio Drilldown & Matrix Visuals")
    st.markdown("> *This dashboard segment focuses heavily on checking specific behavioral metrics to isolate systemic churn trends.*")
    
    if total_customers == 0:
        st.warning("Please adjust your top filters to populate deep-dive matrix charts.")
    else:
        # Layout Split Rows for the 5 charts
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_col1 = st.columns(1)[0]
        
        # --- CHART 1: Product Utilization Churn Profile ---
        with row1_col1:
            st.write("📈 **1. Churn Rate vs Number of Products Held (%)**")
            prod_churn = filtered_df.groupby("No Of Products")["Exited"].mean() * 100
            st.bar_chart(prod_churn, color=COLOR_ACCENT)
            st.caption("Notice: Customers holding 3 or 4 banking products present a critical risk anomaly profile.")

        # --- CHART 2: Activity vs Inactivity Risk Spread ---
        with row1_col2:
            st.write("📊 **2. Churn Distribution by Account Activity Status (%)**")
            act_churn = filtered_df.groupby("Is Active Member Label")["Exited"].mean() * 100
            st.bar_chart(act_churn, color=COLOR_PRIMARY)
            st.caption("Inactive account profiles show roughly double the risk footprint compared to active tiers.")

        # --- CHART 3: Credit Score Band Volatility ---
        with row2_col1:
            st.write("💳 **3. Credit Score Band Attrition Mapping (%)**")
            credit_churn = filtered_df.groupby("Credit Score Band", observed=False)["Exited"].mean() * 100
            st.bar_chart(credit_churn, color=COLOR_SECONDARY)
            st.caption("Isolating whether lower credit scoring bands trigger accelerated churn trends.")

        # --- CHART 4: Tenure Cohort Churn Timeline ---
        with row2_col2:
            st.write("⏳ **4. Churn Trajectory by Tenure Cohorts (%)**")
            tenure_churn = filtered_df.groupby("Tenure Group", observed=False)["Exited"].mean() * 100
            st.bar_chart(tenure_churn, color=COLOR_MUTED)
            st.caption("Tracks account lifecycle stability metrics from incoming clients to legacy accounts.")

        # --- CHART 5: Financial Matrix Value Comparison ---
        with row3_col1:
            st.write("💰 **5. Asset Capital Volume Context: Average Balances by Country (€)**")
            geo_balances = filtered_df.groupby("Geography")["Balance"].mean()
            st.bar_chart(geo_balances, color=COLOR_PRIMARY)
            st.caption("Compares total cross-border capitalization balances to verify risk revenue exposures.")

