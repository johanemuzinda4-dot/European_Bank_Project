import os
import pandas as pd
import streamlit as st

# 1. Page Configuration & Premium Layout Styling
st.set_page_config(
    page_title="European Bank | Executive Intelligence", 
    page_icon="🏦",
    layout="wide"
)

# Executive Color Palette Definitions
COLOR_PRIMARY = "#1E3A8A"    # Deep Corporate Navy
COLOR_SECONDARY = "#0284C7"  # Slate Blue Accent
COLOR_RISK = "#E11D48"       # Risk Crimson
COLOR_MUTED = "#64748B"      # Neutral Charcoal

# 2. Secure File Ingestion Pipeline
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_PATH = os.path.join(SCRIPT_DIR, "European_Bank_clean.csv")

@st.cache_data
def load_clean_data():
    return pd.read_csv(CLEAN_PATH)

df = load_clean_data()
BASELINE_CHURN = 0.2037

# 3. Modern Sticky Top Header System
st.title("🏦 European Bank | Executive Portfolio Analytics")
st.markdown("##### Performance Metrics, Segment Risk Matrix, and Capital Volatility")
st.markdown("---")

# 4. Filter Navigation Block (Modern Clean Top Row Filter Layout)
st.markdown("#### 🛠️ Portfolio Management Filter Settings")
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    selected_geo = st.multiselect("Region / Country Focus", options=df["Geography"].unique(), default=df["Geography"].unique())
with f_col2:
    selected_gender = st.multiselect("Demographic Split", options=df["Gender"].unique(), default=df["Gender"].unique())
with f_col3:
    selected_credit = st.multiselect("Credit Rating Class", options=df["Credit Score Band"].unique(), default=df["Credit Score Band"].unique())

# Filter data dynamically based on your selections
filtered_df = df[
    (df["Geography"].isin(selected_geo)) & 
    (df["Gender"].isin(selected_gender)) &
    (df["Credit Score Band"].isin(selected_credit))
]

# Calculate Global Summary Indicators
total_customers = len(filtered_df)
churn_pct = filtered_df["Exited"].mean() if total_customers > 0 else 0
capital_lost = filtered_df[filtered_df["Exited"] == 1]["Balance"].sum()
total_portfolio_value = filtered_df["Balance"].sum()
churn_delta = churn_pct - BASELINE_CHURN

st.markdown("---")

# 5. Master Executive Workspaces Navigation (Horizontal Select)
navigation_mode = st.segmented_control(
    "Select Interface View",
    options=["📊 Executive Overview Dashboard", "🔍 Deep-Dive Behavioral Insights"],
    default="📊 Executive Overview Dashboard"
)
st.markdown("<br>", unsafe_allow_html=True)

# =========================================================================
# WORKSPACE 1: EXECUTIVE OVERVIEW DASHBOARD (Premium Structured Layout)
# =========================================================================
if navigation_mode == "📊 Executive Overview Dashboard":
    
    # Clean Row of Top KPI Cards
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.markdown(f"<div style='border-left: 5px solid {COLOR_PRIMARY}; padding-left: 10px;'><p style='color:{COLOR_MUTED}; margin:0; font-size:14px;'>Active Account Cohort</p><h2>{total_customers:,}</h2></div>", unsafe_allow_html=True)
    with kpi_col2:
        # Use inverse delta coloring logic (Red is bad for churn increases)
        delta_label = f"{churn_delta:+.2%} vs Bank Baseline"
        st.metric(label="Portfolio Churn Rate", value=f"{churn_pct:.2%}", delta=delta_label, delta_color="inverse")
    with kpi_col3:
        st.markdown(f"<div style='border-left: 5px solid {COLOR_RISK}; padding-left: 10px;'><p style='color:{COLOR_MUTED}; margin:0; font-size:14px;'>Capital Outflow Lost</p><h2 style='color:{COLOR_RISK};'>€{capital_lost:,.2f}</h2></div>", unsafe_allow_html=True)
    with kpi_col4:
        st.markdown(f"<div style='border-left: 5px solid {COLOR_SECONDARY}; padding-left: 10px;'><p style='color:{COLOR_MUTED}; margin:0; font-size:14px;'>Total Retained Capital</p><h2>€{(total_portfolio_value - capital_lost):,.2f}</h2></div>", unsafe_allow_html=True)
        
    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    # 2-Column Professional Visual Balance Layout Split
    layout_left, layout_right = st.columns(2)
    
    with layout_left:
        st.markdown("📊 **Churn Risk Index by Age Cohorts**")
        if total_customers > 0:
            age_chart = filtered_df.groupby("Age Segment", observed=False)["Exited"].mean() * 100
            st.bar_chart(age_chart, color=COLOR_PRIMARY, use_container_width=True)
        else:
            st.caption("No data selected.")
            
    with layout_right:
        st.markdown("💰 **Capital Concentration: Total Assets by Country**")
        if total_customers > 0:
            geo_balances = filtered_df.groupby("Geography")["Balance"].sum()
            st.bar_chart(geo_balances, color=COLOR_SECONDARY, use_container_width=True)
        else:
            st.caption("No data selected.")

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Automated Action Priority Row
    st.markdown("#### 🚨 Priority Action Target: High-Risk Retention Workspace")
    st.markdown("> *The target data engine below automatically filters active high-value accounts matching critical churn patterns (Age 46–60 or Based in Germany).*")
    
    high_risk_flag = (filtered_df["Exited"] == 0) & (filtered_df["Balance"] > 0) & ((filtered_df["Age Segment"] == "46-60") | (filtered_df["Geography"] == "Germany"))
    action_table = filtered_df[high_risk_flag][["Customer ID", "Geography", "Gender", "Age", "Balance", "No Of Products"]].sort_values(by="Balance", ascending=False)
    
    st.dataframe(action_table.head(100), use_container_width=True)


# =========================================================================
# WORKSPACE 2: DEEP-DIVE BEHAVIORAL INSIGHTS (5 Advanced Analytical Charts)
# =========================================================================
else:
    st.markdown("### 🔍 Strategic Metric Analysis Workspace")
    
    if total_customers == 0:
        st.warning("Please adjust your master filters to generate deep-dive visual graphs.")
    else:
        # Constructing a clean 2x2 Layout Matrix for structural charts
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        row3_full = st.columns(1)[0]
        
        with row1_col1:
            st.markdown("📈 **1. Product Holding Vulnerability Index**")
            prod_data = filtered_df.groupby("No Of Products")["Exited"].mean() * 100
            st.bar_chart(prod_data, color=COLOR_RISK, use_container_width=True)
            st.caption("Critical Alert: Customers cross-sold into 3 or 4 accounts have near-total attrition scores.")
            
        with row1_col2:
            st.markdown("👥 **2. Engagement Attrition Gap: Active vs Inactive Tiers**")
            active_data = filtered_df.groupby("Is Active Member Label")["Exited"].mean() * 100
            st.bar_chart(active_data, color=COLOR_PRIMARY, use_container_width=True)
            st.caption("Inactive statuses present double the baseline systemic operational threat profile.")
            
        with row2_col1:
            st.markdown("💳 **3. Credit Class Attrition Index**")
            credit_data = filtered_df.groupby("Credit Score Band", observed=False)["Exited"].mean() * 100
            st.bar_chart(credit_data, color=COLOR_SECONDARY, use_container_width=True)
            st.caption("Identifies baseline performance stability across individual customer credit bands.")
            
        with row2_col2:
            st.markdown("⏳ **4. Churn Spread Across Tenure Lifecycle Years**")
            tenure_data = filtered_df.groupby("Tenure Group", observed=False)["Exited"].mean() * 100
            st.bar_chart(tenure_data, color=COLOR_MUTED, use_container_width=True)
            st.caption("Evaluates long-term customer life cycles against account drop-off velocity.")
            
        with row3_full:
            st.markdown("💵 **5. Revenue Volatility Mapping: Capital Balances vs Age Demographics**")
            # Aggregating average balance across age demographics
            age_balances = filtered_df.groupby("Age Segment", observed=False)["Balance"].mean()
            st.bar_chart(age_balances, color=COLOR_PRIMARY, use_container_width=True)
            st.caption("Highlights specific age categories that represent the single largest financial weight inside bank portfolios.")
