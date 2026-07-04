"""
Customer Segmentation & Churn Pattern Analytics in European Banking
Step 1: Data Ingestion & Validation
Step 2: Data Cleaning & Preparation

Usage:
    python app.py

Expects "European_Bank.csv" in the same folder (or update RAW_PATH below).
Outputs "European_Bank_clean.csv" ready for EDA / the Streamlit dashboard.
"""

import os
import pandas as pd
import numpy as np

# Build paths relative to this script's own location, so it works
# no matter which folder you run it from (fixes FileNotFoundError).
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.join(SCRIPT_DIR, "European_Bank.csv")
CLEAN_PATH = os.path.join(SCRIPT_DIR, "European_Bank_clean.csv")


# =========================================================
# STEP 1: DATA INGESTION & VALIDATION
# =========================================================

def load_data(path: str = RAW_PATH) -> pd.DataFrame:
    """Load the raw dataset."""
    df = pd.read_csv(path)
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


def validate_data(df: pd.DataFrame) -> None:
    """Run validation checks on raw data before cleaning."""
    print("\n--- Step 1: Validation ---")

    # Strip whitespace from column names first so checks are reliable
    df.columns = [c.strip() for c in df.columns]

    # Missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if missing.empty:
        print("No missing values found.")
    else:
        print("Missing values found:")
        print(missing)

    # Duplicate rows / IDs
    print(f"Duplicate rows: {df.duplicated().sum()}")
    print(f"Duplicate Customer IDs: {df['Customer ID'].duplicated().sum()}")

    # Binary field consistency
    for col in ["Has Credit Card", "Is Active Member", "Exited"]:
        values = sorted(df[col].unique())
        status = "OK" if values == [0, 1] else "CHECK THIS"
        print(f"{col} unique values: {values} -> {status}")

    # Product field range
    print(f"No Of Products range: {df['No Of Products'].min()}-{df['No Of Products'].max()}")

    # Geography values
    print(f"Geography values: {df['Geography'].unique().tolist()}")

    # Churn label distribution
    churn_rate = df["Exited"].mean()
    print(f"Churn label distribution -> churned: {churn_rate:.2%}, retained: {1 - churn_rate:.2%}")


# =========================================================
# STEP 2: DATA CLEANING & PREPARATION
# =========================================================

def clean_currency(value) -> float:
    """Convert strings like ' $101,348.88 ' or ' $-   ' into floats."""
    if pd.isna(value):
        return np.nan
    text = str(value).strip().replace("$", "").replace(",", "").strip()
    if text in ("-", ""):
        return 0.0
    return float(text)


def age_segment(age: int) -> str:
    if age < 30:
        return "<30"
    elif age <= 45:
        return "30-45"
    elif age <= 60:
        return "46-60"
    else:
        return "60+"


def credit_score_band(score: int) -> str:
    if score < 580:
        return "Low"
    elif score < 700:
        return "Medium"
    else:
        return "High"


def tenure_group(tenure: int) -> str:
    if tenure <= 2:
        return "New"
    elif tenure <= 6:
        return "Mid-term"
    else:
        return "Long-term"


def balance_segment(balance: float) -> str:
    if balance == 0:
        return "Zero-balance"
    elif balance < 100_000:
        return "Low-balance"
    else:
        return "High-balance"


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean fields and create derived segmentation columns."""
    print("\n--- Step 2: Cleaning ---")

    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    # Clean currency fields
    df["Balance"] = df["Balance"].apply(clean_currency)
    df["Estimated Salary"] = df["Estimated Salary"].apply(clean_currency)

    # Remove non-analytical fields
    df = df.drop(columns=["Surname"])

    # Derived segmentation fields
    df["Age Segment"] = df["Age"].apply(age_segment)
    df["Credit Score Band"] = df["Credit Score"].apply(credit_score_band)
    df["Tenure Group"] = df["Tenure"].apply(tenure_group)
    df["Balance Segment"] = df["Balance"].apply(balance_segment)

    # Readable labels (useful later for the Streamlit dashboard)
    df["Has Credit Card Label"] = df["Has Credit Card"].map({1: "Yes", 0: "No"})
    df["Is Active Member Label"] = df["Is Active Member"].map({1: "Yes", 0: "No"})
    df["Churn Status"] = df["Exited"].map({1: "Churned", 0: "Retained"})

    print(f"Cleaned dataset shape: {df.shape}")
    print("Columns after cleaning:", df.columns.tolist())

    return df


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    raw_df = load_data()
    validate_data(raw_df)
    clean_df = clean_data(raw_df)
    clean_df.to_csv(CLEAN_PATH, index=False)
    print(f"\nSaved cleaned dataset to {CLEAN_PATH}")