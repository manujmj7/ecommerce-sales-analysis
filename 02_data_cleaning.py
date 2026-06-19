"""
=============================================================================
E-COMMERCE SALES ANALYSIS PROJECT
Script 02: Data Cleaning & Validation
Author: [Your Name]
Date: 2024
Description: Cleans raw e-commerce data following industry-standard
             data quality practices. Outputs a clean dataset for EDA.
=============================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

print("=" * 60)
print("  DATA CLEANING & VALIDATION PIPELINE")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: LOAD RAW DATA
# ─────────────────────────────────────────────────────────────────────────────
print("\n[STEP 1] Loading raw dataset...")

# Resolve path relative to this script's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
raw_path = os.path.join(BASE_DIR, "data", "ecommerce_raw.csv")
df = pd.read_csv(raw_path)

print(f"  ✓ Loaded {len(df):,} rows × {len(df.columns)} columns")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: DATA QUALITY ASSESSMENT (before cleaning)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[STEP 2] Initial Data Quality Assessment")
print("-" * 50)

initial_rows = len(df)

# Missing values report
missing_report = df.isnull().sum()
missing_pct    = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    "Missing Count": missing_report,
    "Missing %":     missing_pct
}).query("`Missing Count` > 0")

print("\n  Missing Values Report:")
if len(missing_df) > 0:
    print(missing_df.to_string())
else:
    print("  No missing values found.")

# Duplicates
dup_count = df.duplicated().sum()
print(f"\n  Duplicate rows: {dup_count:,}")

# Data types
print("\n  Data Types:")
print(df.dtypes.to_string())

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: FIX DATA TYPES
# ─────────────────────────────────────────────────────────────────────────────
print("\n[STEP 3] Fixing Data Types...")

# Convert date columns to datetime
df["order_date"]    = pd.to_datetime(df["order_date"],    errors="coerce")
df["delivery_date"] = pd.to_datetime(df["delivery_date"], errors="coerce")

# Ensure numeric columns are correct type
numeric_cols = ["quantity", "unit_price", "discount_pct", "discount_amount",
                "shipping_fee", "sales_amount", "cost_price", "profit",
                "profit_margin", "customer_rating"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print(f"  ✓ Date columns converted to datetime")
print(f"  ✓ Numeric columns validated")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: REMOVE DUPLICATES
# ─────────────────────────────────────────────────────────────────────────────
print("\n[STEP 4] Removing Duplicate Records...")

before = len(df)
df = df.drop_duplicates(subset=["order_id"], keep="first")
after = len(df)

print(f"  ✓ Removed {before - after:,} duplicate order IDs")
print(f"  ✓ Records remaining: {after:,}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5: HANDLE MISSING VALUES
# ─────────────────────────────────────────────────────────────────────────────
print("\n[STEP 5] Handling Missing Values...")

# Strategy: Impute based on business logic, not blindly with mean

# 5a. Customer Rating: fill with median rating per category
#     (unrated doesn't mean bad — impute with category median)
before_missing = df["customer_rating"].isnull().sum()
df["customer_rating"] = df.groupby("category")["customer_rating"] \
                           .transform(lambda x: x.fillna(x.median()))
# If still null (edge case), fill with overall median
df["customer_rating"] = df["customer_rating"].fillna(df["customer_rating"].median())
after_missing = df["customer_rating"].isnull().sum()
print(f"  ✓ customer_rating: {before_missing} nulls → {after_missing} nulls "
      f"(filled with category median)")

# 5b. Shipping Fee: fill with 0 if sales_amount > 499 else with median
before_missing = df["shipping_fee"].isnull().sum()
df["shipping_fee"] = df.apply(
    lambda row: 0.0
    if pd.isnull(row["shipping_fee"]) and row["sales_amount"] > 499
    else (row["shipping_fee"] if pd.notna(row["shipping_fee"]) else 59.0),
    axis=1
)
after_missing = df["shipping_fee"].isnull().sum()
print(f"  ✓ shipping_fee: {before_missing} nulls → {after_missing} nulls "
      f"(business-logic fill)")

# Drop rows where critical columns are null
critical_cols = ["order_id", "order_date", "customer_id", "sales_amount",
                 "product_name", "category"]
before = len(df)
df = df.dropna(subset=critical_cols)
print(f"  ✓ Dropped {before - len(df):,} rows with null critical columns")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 6: DATA VALIDATION CHECKS
# ─────────────────────────────────────────────────────────────────────────────
print("\n[STEP 6] Data Validation Checks...")

issues_found = 0

# 6a. Negative sales amounts are invalid
neg_sales = df[df["sales_amount"] < 0]
if len(neg_sales) > 0:
    print(f"  ⚠ Found {len(neg_sales)} records with negative sales_amount → removing")
    df = df[df["sales_amount"] >= 0]
    issues_found += len(neg_sales)
else:
    print("  ✓ No negative sales amounts")

# 6b. Quantity must be >= 1
invalid_qty = df[df["quantity"] < 1]
if len(invalid_qty) > 0:
    print(f"  ⚠ Found {len(invalid_qty)} records with quantity < 1 → removing")
    df = df[df["quantity"] >= 1]
    issues_found += len(invalid_qty)
else:
    print("  ✓ All quantities are valid (≥ 1)")

# 6c. Unit price must be > 0
invalid_price = df[df["unit_price"] <= 0]
if len(invalid_price) > 0:
    print(f"  ⚠ Found {len(invalid_price)} records with unit_price ≤ 0 → removing")
    df = df[df["unit_price"] > 0]
    issues_found += len(invalid_price)
else:
    print("  ✓ All unit prices are valid (> 0)")

# 6d. Delivery date should be >= order date
invalid_dates = df[df["delivery_date"] < df["order_date"]]
if len(invalid_dates) > 0:
    print(f"  ⚠ Found {len(invalid_dates)} records where delivery < order date → fixing")
    # Fix: set delivery = order + 3 days
    df.loc[df["delivery_date"] < df["order_date"], "delivery_date"] = \
        df.loc[df["delivery_date"] < df["order_date"], "order_date"] + pd.Timedelta(days=3)
    issues_found += len(invalid_dates)
else:
    print("  ✓ All delivery dates are valid")

# 6e. Customer rating must be between 1 and 5
invalid_rating = df[~df["customer_rating"].between(1, 5)]
if len(invalid_rating) > 0:
    print(f"  ⚠ Found {len(invalid_rating)} invalid ratings → clipping to [1,5]")
    df["customer_rating"] = df["customer_rating"].clip(1, 5)
else:
    print("  ✓ All customer ratings are valid (1–5)")

# 6f. Discount % must be between 0 and 1
df["discount_pct"] = df["discount_pct"].clip(0, 1)
print("  ✓ Discount percentages clamped to [0, 1]")

print(f"\n  Total validation issues fixed: {issues_found}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 7: OUTLIER DETECTION & TREATMENT
# ─────────────────────────────────────────────────────────────────────────────
print("\n[STEP 7] Outlier Detection (IQR Method)...")

def detect_outliers_iqr(series, col_name):
    """Detect outliers using Interquartile Range (IQR) method.
    
    Logic: Any value below Q1 - 1.5×IQR or above Q3 + 1.5×IQR is an outlier.
    This is the industry-standard method for detecting outliers.
    """
    Q1  = series.quantile(0.25)
    Q3  = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound  = Q1 - 1.5 * IQR
    upper_bound  = Q3 + 1.5 * IQR
    outliers     = series[(series < lower_bound) | (series > upper_bound)]
    print(f"  {col_name:20s}: {len(outliers):4d} outliers "
          f"[bounds: {lower_bound:.2f} — {upper_bound:.2f}]")
    return lower_bound, upper_bound

# Check key numeric columns for outliers
for col in ["sales_amount", "profit", "quantity", "unit_price"]:
    lower, upper = detect_outliers_iqr(df[col], col)
    # Strategy: Cap (Winsorize) rather than remove — we don't lose data
    df[col] = df[col].clip(lower, upper)

print("  ✓ Outliers capped using Winsorization (IQR method)")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 8: FEATURE ENGINEERING (ADD USEFUL DERIVED COLUMNS)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[STEP 8] Feature Engineering...")

# Time-based features (essential for trend analysis)
df["order_year"]    = df["order_date"].dt.year
df["order_month"]   = df["order_date"].dt.month
df["order_quarter"] = df["order_date"].dt.quarter
df["order_day"]     = df["order_date"].dt.day
df["order_weekday"] = df["order_date"].dt.day_name()
df["month_name"]    = df["order_date"].dt.strftime("%b")  # Jan, Feb, ...

# Delivery time in days (useful for logistics analysis)
df["delivery_days"] = (df["delivery_date"] - df["order_date"]).dt.days

# Revenue per unit
df["revenue_per_unit"] = (df["sales_amount"] / df["quantity"]).round(2)

# Flag: Is this a high-value order? (Above 75th percentile)
high_value_threshold = df["sales_amount"].quantile(0.75)
df["is_high_value"] = (df["sales_amount"] >= high_value_threshold).astype(int)

# Flag: Was a discount applied?
df["has_discount"] = (df["discount_pct"] > 0).astype(int)

# Season based on month (useful for seasonal analysis)
def get_season(month):
    if month in [12, 1, 2]:  return "Winter"
    elif month in [3, 4, 5]: return "Spring"
    elif month in [6, 7, 8]: return "Summer"
    else:                     return "Autumn"  # Festive season in India

df["season"] = df["order_month"].apply(get_season)

print("  ✓ Added: order_year, order_month, order_quarter, order_day")
print("  ✓ Added: order_weekday, month_name, season")
print("  ✓ Added: delivery_days, revenue_per_unit, is_high_value, has_discount")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 9: FINAL QUALITY REPORT
# ─────────────────────────────────────────────────────────────────────────────
print("\n[STEP 9] Final Data Quality Report")
print("-" * 50)
print(f"  Original records  : {initial_rows:,}")
print(f"  Final records     : {len(df):,}")
print(f"  Records removed   : {initial_rows - len(df):,} ({(initial_rows-len(df))/initial_rows*100:.1f}%)")
print(f"  Columns           : {len(df.columns)}")
print(f"  Missing values    : {df.isnull().sum().sum()}")
print(f"  Duplicate orders  : {df['order_id'].duplicated().sum()}")
print(f"\n  Data Summary:")
print(f"    Total Revenue  : ₹{df['sales_amount'].sum():>12,.2f}")
print(f"    Total Profit   : ₹{df['profit'].sum():>12,.2f}")
print(f"    Avg Order Value: ₹{df['sales_amount'].mean():>12,.2f}")
print(f"    Unique Customers: {df['customer_id'].nunique():,}")
print(f"    Unique Products : {df['product_name'].nunique():,}")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 10: SAVE CLEAN DATASET
# ─────────────────────────────────────────────────────────────────────────────
clean_path = os.path.join(BASE_DIR, "data", "ecommerce_clean.csv")
df.to_csv(clean_path, index=False)
print(f"\n[SUCCESS] Clean dataset saved to: {clean_path}")
print(f"[INFO] Ready for Exploratory Data Analysis!")
