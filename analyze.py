import os
import pandas as pd

# Get path to our freshly cleaned dataset
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_PATH = os.path.join(SCRIPT_DIR, "European_Bank_clean.csv")

# Load the clean data
df = pd.read_csv(CLEAN_PATH)

print("\n==================================================")
print("     EUROPEAN BANK PROJECT: PHENOMENAL PROGRESS   ")
print("==================================================\n")

# 1. Overall Churn Base Rate
base_churn = df['Exited'].mean()
print(f"Overall Bank Churn Rate: {base_churn:.2%}\n")

# 2. Geographic Risk Index
print("--- GEOGRAPHIC RISK PROFILE ---")
geo_stats = df.groupby('Geography').agg(
    Total_Customers=('Customer ID', 'count'),
    Churn_Rate=('Exited', 'mean'),
    Total_Balance_Lost=('Balance', lambda x: x[df['Exited'] == 1].sum())
).sort_values(by='Churn_Rate', ascending=False)

print(geo_stats.to_string())

# 3. High-Value Customer Churn Analysis
print("\n--- HIGH-VALUE CUSTOMER ANALYSIS ---")
high_val_stats = df.groupby('Balance Segment', observed=False).agg(
    Total_Customers=('Customer ID', 'count'),
    Churn_Rate=('Exited', 'mean')
)
print(high_val_stats.to_string())

print("\n==================================================")