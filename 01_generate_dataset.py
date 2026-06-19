"""
=============================================================================
E-COMMERCE SALES ANALYSIS PROJECT
Script 01: Dataset Generation
Author: [Your Name]
Date: 2024
Description: Generates a realistic e-commerce dataset with 5,000+ records
             for analysis, simulating real-world data patterns.
=============================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set seed for reproducibility (same "random" data every time you run)
np.random.seed(42)
random.seed(42)

print("=" * 60)
print("  E-COMMERCE DATASET GENERATOR")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION - Define all master data
# ─────────────────────────────────────────────────────────────────────────────

# Number of records to generate
NUM_RECORDS = 5500

# Date range: 2 full years of data (great for trend analysis)
START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2023, 12, 31)

# Product catalog: category → list of (product_name, base_price, cost_price)
PRODUCT_CATALOG = {
    "Electronics": [
        ("Wireless Headphones",   3499,  1800),
        ("Bluetooth Speaker",     1999,   900),
        ("Smart Watch",           8999,  4500),
        ("USB-C Hub",             1299,   550),
        ("Laptop Stand",          1499,   650),
        ("Mechanical Keyboard",   4999,  2200),
        ("Webcam HD",             2499,  1100),
        ("Phone Charger 65W",      999,   400),
    ],
    "Clothing": [
        ("Men's Casual T-Shirt",   599,   180),
        ("Women's Kurti",          899,   280),
        ("Denim Jeans",           1499,   520),
        ("Sports Shorts",          699,   220),
        ("Winter Jacket",         2999,  1100),
        ("Cotton Saree",          1999,   700),
        ("Running Shoes",         2499,   900),
        ("Kids Dress",             799,   260),
    ],
    "Home & Kitchen": [
        ("Air Fryer",             4999,  2400),
        ("Dinner Set (6 pcs)",    1799,   700),
        ("Coffee Maker",          3499,  1600),
        ("Pressure Cooker",       1999,   850),
        ("Non-stick Pan Set",     1299,   520),
        ("Water Purifier",        8999,  4200),
        ("Room Heater",           2499,  1100),
        ("Mixer Grinder",         3999,  1800),
    ],
    "Books": [
        ("Python Programming",     599,   180),
        ("Data Science Handbook",  799,   240),
        ("Business Strategy",      449,   130),
        ("Self-Help Bestseller",   349,   100),
        ("Indian History",         499,   150),
        ("Children Story Book",    299,    85),
        ("Cookbook Delights",      549,   165),
        ("Finance for Beginners",  399,   115),
    ],
    "Sports & Fitness": [
        ("Yoga Mat",               999,   380),
        ("Resistance Bands Set",   799,   280),
        ("Dumbbell Pair 5kg",     1499,   650),
        ("Cycling Helmet",        1999,   850),
        ("Cricket Bat",           2499,  1050),
        ("Badminton Racket Set",  1299,   530),
        ("Fitness Tracker Band",  2999,  1350),
        ("Jump Rope",              399,   120),
    ],
    "Beauty & Personal Care": [
        ("Face Wash 150ml",        399,   120),
        ("Sunscreen SPF50",        599,   190),
        ("Hair Dryer",            1999,   850),
        ("Electric Trimmer",      1499,   620),
        ("Moisturizer Cream",      799,   255),
        ("Perfume 100ml",         2499,  1000),
        ("Lip Balm Pack",          199,    55),
        ("Body Lotion 200ml",      449,   140),
    ],
}

# Regions with weighted distribution (Metro cities buy more)
REGIONS = {
    "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh", "Agra"],
    "South": ["Bangalore", "Chennai", "Hyderabad", "Kochi", "Coimbatore"],
    "East":  ["Kolkata", "Bhubaneswar", "Patna", "Guwahati", "Ranchi"],
    "West":  ["Mumbai", "Pune", "Ahmedabad", "Surat", "Nagpur"],
}

REGION_WEIGHTS = {"North": 0.30, "South": 0.28, "West": 0.27, "East": 0.15}

# Customer segments
CUSTOMER_SEGMENTS = ["Regular", "Premium", "VIP", "New"]
SEGMENT_WEIGHTS   = [0.45,      0.30,      0.15,  0.10]

# Payment methods
PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery", "EMI"]
PAYMENT_WEIGHTS = [0.25, 0.20, 0.30, 0.10, 0.10, 0.05]

# Order statuses (realistic: most orders complete)
ORDER_STATUSES = ["Delivered", "Delivered", "Delivered", "Returned", "Cancelled"]

# Discount tiers by segment
DISCOUNT_RANGES = {
    "VIP":     (0.15, 0.30),
    "Premium": (0.08, 0.20),
    "Regular": (0.02, 0.12),
    "New":     (0.05, 0.15),
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def generate_random_date(start, end):
    """Generate a random date between start and end."""
    delta = (end - start).days
    random_days = np.random.randint(0, delta)
    date = start + timedelta(days=int(random_days))
    # Add seasonality: Nov-Dec and Jan get 40% more records
    # (handled by weighted sampling in main generation loop)
    return date

def generate_order_id(index):
    """Generate a formatted Order ID like ORD-2022-000001."""
    return f"ORD-{1000000 + index}"

def generate_customer_id():
    """Generate a Customer ID. Repeat some IDs to simulate repeat customers."""
    # Create a pool of ~1500 unique customers (repeat purchases are realistic)
    return f"CUST-{np.random.randint(10000, 11500):05d}"

def apply_seasonal_weight(date):
    """Returns multiplier for seasonal shopping patterns."""
    month = date.month
    # Festive season: Oct-Dec gets higher sales
    if month in [10, 11, 12]:
        return 1.8
    # New Year / Budget season: Jan-Feb moderate boost
    elif month in [1, 2]:
        return 1.2
    # Summer slump: May-Jun slight dip
    elif month in [5, 6]:
        return 0.85
    else:
        return 1.0

# ─────────────────────────────────────────────────────────────────────────────
# MAIN DATA GENERATION
# ─────────────────────────────────────────────────────────────────────────────

print(f"\n[INFO] Generating {NUM_RECORDS} records...")

records = []

# Flatten product catalog for easy sampling
all_products = []
for category, products in PRODUCT_CATALOG.items():
    for product_name, base_price, cost_price in products:
        all_products.append({
            "category": category,
            "product_name": product_name,
            "base_price": base_price,
            "cost_price": cost_price,
        })

# Category weights: Electronics & Clothing sell more
category_list = list(PRODUCT_CATALOG.keys())
category_weights = [0.22, 0.20, 0.18, 0.12, 0.14, 0.14]

# Pre-generate all dates with seasonal skewing
# Generate more dates in festive months
date_pool = []
for _ in range(NUM_RECORDS * 3):  # Large pool
    d = generate_random_date(START_DATE, END_DATE)
    weight = apply_seasonal_weight(d)
    if np.random.random() < weight / 2:
        date_pool.append(d)
    if len(date_pool) >= NUM_RECORDS:
        break

# If pool is small, fill the rest uniformly
while len(date_pool) < NUM_RECORDS:
    date_pool.append(generate_random_date(START_DATE, END_DATE))

date_pool = date_pool[:NUM_RECORDS]

for i in range(NUM_RECORDS):
    # ── Pick a category (weighted) ──────────────────────────────────────────
    chosen_category = np.random.choice(category_list, p=category_weights)
    
    # ── Pick a product from that category ───────────────────────────────────
    category_products = PRODUCT_CATALOG[chosen_category]
    product = random.choice(category_products)
    product_name, base_price, cost_price = product

    # ── Customer info ────────────────────────────────────────────────────────
    customer_id = generate_customer_id()
    segment = np.random.choice(CUSTOMER_SEGMENTS, p=SEGMENT_WEIGHTS)

    # ── Region & City ────────────────────────────────────────────────────────
    region = np.random.choice(
        list(REGION_WEIGHTS.keys()),
        p=list(REGION_WEIGHTS.values())
    )
    city = random.choice(REGIONS[region])

    # ── Date ─────────────────────────────────────────────────────────────────
    order_date = date_pool[i]
    
    # Delivery takes 1-7 days (VIP gets faster delivery)
    if segment == "VIP":
        delivery_days = np.random.randint(1, 3)
    elif segment == "Premium":
        delivery_days = np.random.randint(2, 5)
    else:
        delivery_days = np.random.randint(3, 8)
    
    delivery_date = order_date + timedelta(days=int(delivery_days))

    # ── Quantity & Pricing ───────────────────────────────────────────────────
    quantity = np.random.choice([1, 1, 1, 2, 2, 3, 4, 5], p=[0.35, 0.25, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01])

    # Price variation: ±10% from base price (realistic market fluctuation)
    price_variation = np.random.uniform(0.90, 1.10)
    unit_price = round(base_price * price_variation, 2)

    # Discount
    min_disc, max_disc = DISCOUNT_RANGES[segment]
    discount_pct = round(np.random.uniform(min_disc, max_disc), 4)
    
    # Occasionally introduce no-discount records
    if np.random.random() < 0.15:
        discount_pct = 0.0

    discount_amount = round(unit_price * quantity * discount_pct, 2)
    
    # Shipping fee (free for orders above 499)
    gross_amount = unit_price * quantity
    if gross_amount > 499 or segment in ["VIP", "Premium"]:
        shipping_fee = 0.0
    else:
        shipping_fee = np.random.choice([49, 59, 79, 99])

    # Final sales amount
    sales_amount = round(gross_amount - discount_amount + shipping_fee, 2)
    
    # Profit calculation
    total_cost = cost_price * quantity
    profit = round(sales_amount - total_cost - shipping_fee * 0.3, 2)
    profit_margin = round((profit / sales_amount) * 100, 2) if sales_amount > 0 else 0

    # ── Order status ─────────────────────────────────────────────────────────
    status = random.choice(ORDER_STATUSES)
    
    # Returned/cancelled orders have 0 profit (business impact!)
    if status in ["Returned", "Cancelled"]:
        profit = round(-cost_price * quantity * 0.15, 2)  # Handling loss
        profit_margin = round((profit / sales_amount) * 100, 2)

    # ── Payment & Rating ─────────────────────────────────────────────────────
    payment_method = np.random.choice(PAYMENT_METHODS, p=PAYMENT_WEIGHTS)
    
    # Customer rating 1-5 (delivered orders rated higher)
    if status == "Delivered":
        rating = np.random.choice([3, 4, 4, 5, 5], p=[0.10, 0.25, 0.30, 0.20, 0.15])
    else:
        rating = np.random.choice([1, 2, 3], p=[0.40, 0.40, 0.20])

    # ── Introduce intentional data quality issues ────────────────────────────
    # ~3% missing ratings (customer didn't rate)
    if np.random.random() < 0.03:
        rating = None
    
    # ~2% missing shipping fee records
    if np.random.random() < 0.02:
        shipping_fee = None

    # ── Append record ────────────────────────────────────────────────────────
    records.append({
        "order_id":        generate_order_id(i + 1),
        "order_date":      order_date.strftime("%Y-%m-%d"),
        "delivery_date":   delivery_date.strftime("%Y-%m-%d"),
        "customer_id":     customer_id,
        "customer_segment": segment,
        "region":          region,
        "city":            city,
        "category":        chosen_category,
        "product_name":    product_name,
        "quantity":        quantity,
        "unit_price":      unit_price,
        "discount_pct":    discount_pct,
        "discount_amount": discount_amount,
        "shipping_fee":    shipping_fee,
        "sales_amount":    sales_amount,
        "cost_price":      cost_price,
        "profit":          profit,
        "profit_margin":   profit_margin,
        "payment_method":  payment_method,
        "order_status":    status,
        "customer_rating": rating,
    })

# ─────────────────────────────────────────────────────────────────────────────
# CREATE DATAFRAME & SAVE
# ─────────────────────────────────────────────────────────────────────────────

df = pd.DataFrame(records)

# Sort by date (realistic chronological order)
df["order_date"] = pd.to_datetime(df["order_date"])
df = df.sort_values("order_date").reset_index(drop=True)

# Introduce ~1% duplicate rows (realistic dirty data)
num_duplicates = int(NUM_RECORDS * 0.01)
duplicate_rows = df.sample(n=num_duplicates, random_state=42)
df = pd.concat([df, duplicate_rows], ignore_index=True)

print(f"[INFO] Dataset created: {len(df):,} rows × {len(df.columns)} columns")
print(f"[INFO] Date range: {df['order_date'].min()} → {df['order_date'].max()}")

# Save to CSV
output_path = os.path.join(os.path.dirname(__file__), "data", "ecommerce_raw.csv")
df.to_csv(output_path, index=False)
print(f"\n[SUCCESS] Raw dataset saved to: {output_path}")

# Quick preview
print("\n── Sample Records ──────────────────────────────────────────")
print(df[["order_id", "order_date", "category", "product_name",
          "sales_amount", "profit", "order_status"]].head(5).to_string(index=False))

print("\n── Dataset Info ────────────────────────────────────────────")
print(f"  Total Records  : {len(df):,}")
print(f"  Total Columns  : {len(df.columns)}")
print(f"  Missing Values : {df.isnull().sum().sum()}")
print(f"  Duplicate Rows : {df.duplicated().sum()}")
print(f"  Total Revenue  : ₹{df['sales_amount'].sum():,.2f}")
print(f"  Total Profit   : ₹{df['profit'].sum():,.2f}")
