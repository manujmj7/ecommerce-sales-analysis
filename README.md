# 🛒 E-Commerce Sales Analysis Dashboard

> **A complete, portfolio-ready Data Analysis project built with Python, Pandas, Matplotlib, Seaborn, and Power BI**  
> Analyzing 5,500+ real-world e-commerce transactions to surface business insights on sales performance, customer behavior, and regional profitability.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Business Objectives & KPIs](#-business-objectives--kpis)
- [Dataset Description](#-dataset-description)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [How to Run](#-how-to-run)
- [Visualizations](#-visualizations)
- [Key Business Insights](#-key-business-insights)
- [Power BI Dashboard](#-power-bi-dashboard)
- [Skills Demonstrated](#-skills-demonstrated)
- [Interview Q&A](#-interview-qa)

---

## 🎯 Project Overview

### Business Problem
An e-commerce company sells products across 6 categories and 4 regions in India. Management needs to understand:
- Which products and categories generate the most revenue and profit
- How sales trend across seasons and months
- Which customer segments are most valuable
- Where regional opportunities and gaps exist

### Business Objectives
1. Identify top-performing products and underperforming categories
2. Understand monthly and seasonal revenue trends
3. Analyze regional sales performance and profitability
4. Profile customer segments by purchasing behavior
5. Provide data-driven recommendations to increase revenue by 15%

### Expected Outcomes
- A clean, analysis-ready dataset from raw transactional data
- 15 professional visualizations answering key business questions
- An interactive Power BI dashboard for executive decision-making
- Actionable business recommendations backed by data

---

## 📊 Business Objectives & KPIs

| KPI | Value | Target |
|-----|-------|--------|
| Total Revenue | ₹1.21 Crore | ₹1.4 Crore |
| Overall Profit Margin | 27.47% | 30%+ |
| Average Order Value | ₹2,209 | ₹2,500 |
| Customer Satisfaction (Rating) | 3.31 / 5 | 4.0+ |
| Avg Delivery Time | 3.8 days | ≤ 3 days |
| Return/Cancel Rate | 39.8% | < 15% |

---

## 🗃️ Dataset Description

**File:** `data/ecommerce_clean.csv`  
**Records:** 5,500 orders | **Columns:** 32 | **Period:** Jan 2022 – Dec 2023

### Column Dictionary

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| `order_id` | String | Unique order identifier | ORD-1001234 |
| `order_date` | DateTime | Date the order was placed | 2022-03-15 |
| `delivery_date` | DateTime | Actual delivery date | 2022-03-18 |
| `customer_id` | String | Anonymized customer identifier | CUST-10045 |
| `customer_segment` | String | Customer tier (New/Regular/Premium/VIP) | Premium |
| `region` | String | Geographic region (North/South/East/West) | South |
| `city` | String | Customer city | Bangalore |
| `category` | String | Product category | Electronics |
| `product_name` | String | Name of the product sold | Smart Watch |
| `quantity` | Integer | Number of units ordered | 2 |
| `unit_price` | Float | Price per unit in ₹ | 8999.00 |
| `discount_pct` | Float | Discount applied (0.0–0.30) | 0.12 |
| `discount_amount` | Float | Total discount in ₹ | 2159.76 |
| `shipping_fee` | Float | Shipping cost in ₹ (0 if free) | 0.0 |
| `sales_amount` | Float | **Final revenue** (after discount + shipping) | 15998.24 |
| `cost_price` | Float | Product cost to company | 4500.00 |
| `profit` | Float | Profit per order (sales - cost) | 6998.24 |
| `profit_margin` | Float | Profit as % of sales | 43.75 |
| `payment_method` | String | How the customer paid | UPI |
| `order_status` | String | Delivery outcome | Delivered |
| `customer_rating` | Float | 1–5 star rating given by customer | 4.0 |
| `order_year` | Integer | Year extracted from order_date | 2023 |
| `order_month` | Integer | Month number (1–12) | 3 |
| `order_quarter` | Integer | Quarter (1–4) | 1 |
| `month_name` | String | Short month name | Mar |
| `order_weekday` | String | Day of week | Tuesday |
| `season` | String | Season (Spring/Summer/Autumn/Winter) | Spring |
| `delivery_days` | Integer | Days from order to delivery | 3 |
| `revenue_per_unit` | Float | Sales amount ÷ quantity | 7999.12 |
| `is_high_value` | Integer | 1 if order is in top 25% by value | 1 |
| `has_discount` | Integer | 1 if any discount was applied | 1 |

---

## 📁 Project Structure

```
ecommerce_analysis/
│
├── 📂 data/
│   ├── ecommerce_raw.csv          # Raw generated dataset (dirty)
│   └── ecommerce_clean.csv        # Cleaned & feature-engineered dataset
│
├── 📂 scripts/
│   ├── 01_generate_dataset.py     # Generate realistic synthetic data
│   ├── 02_data_cleaning.py        # Full cleaning & validation pipeline
│   └── 03_eda_visualization.py    # EDA + 15 professional charts
│
├── 📂 visualizations/
│   ├── 01_revenue_by_category.png
│   ├── 02_monthly_sales_trend.png
│   ├── 03_top10_products.png
│   ├── 04_regional_performance.png
│   ├── 05_category_revenue_donut.png
│   ├── 06_monthly_category_heatmap.png
│   ├── 07_customer_segment_analysis.png
│   ├── 08_payment_methods.png
│   ├── 09_profit_margin_boxplot.png
│   ├── 10_seasonal_trends.png
│   ├── 11_order_status.png
│   ├── 12_revenue_vs_profit_scatter.png
│   ├── 13_customer_ratings.png
│   ├── 14_top_cities_revenue.png
│   └── 15_discount_vs_sales.png
│
├── 📂 powerbi/
│   └── dashboard_guide.md         # Power BI setup instructions
│
├── 📂 docs/
│   └── project_guide.md           # Full project documentation
│
└── README.md                      # This file
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

---

## ▶️ How to Run

Run the scripts **in order** from the project root directory:

```bash
# Step 1: Generate the raw dataset (creates data/ecommerce_raw.csv)
python scripts/01_generate_dataset.py

# Step 2: Clean and validate the data (creates data/ecommerce_clean.csv)
python scripts/02_data_cleaning.py

# Step 3: Run EDA and generate all 15 visualizations
python scripts/03_eda_visualization.py
```

Each script prints its progress to the console. All outputs are saved automatically.

---

## 📈 Visualizations

| # | Chart | Business Question Answered |
|---|-------|---------------------------|
| 1 | Revenue by Category (Bar) | Which categories generate the most revenue? |
| 2 | Monthly Sales Trend (Line) | How do sales trend month-over-month? |
| 3 | Top 10 Products (Bar) | Which products drive the most revenue? |
| 4 | Regional Performance (Multi-Bar) | Which regions perform best? |
| 5 | Category Share (Donut) | What is each category's revenue contribution? |
| 6 | Month × Category Heatmap | When does each category peak? |
| 7 | Customer Segment Analysis | Which segments are most valuable? |
| 8 | Payment Methods (Pie) | How do customers prefer to pay? |
| 9 | Profit Margin Box Plot | How does profitability vary by category? |
| 10 | Seasonal Trends (Bar) | What are seasonal revenue patterns? |
| 11 | Order Status Distribution | What is the order fulfillment rate? |
| 12 | Revenue vs Profit Scatter | Do high-revenue products also have high profit? |
| 13 | Customer Ratings | How satisfied are customers? |
| 14 | Top 10 Cities (Bar) | Which cities are the biggest markets? |
| 15 | Discount vs Sales Scatter | Do discounts drive higher order values? |

---

## 💡 Key Business Insights

### 1. Electronics Leads in Revenue but Not Margin
Electronics generates the highest revenue (₹38.7L) but has a lower profit margin (27%) than Books (38%) and Clothing (36%). **Recommendation:** Push clothing bundles and book subscriptions to improve overall margins.

### 2. Festive Season (Oct–Dec) Drives 35%+ of Annual Revenue
Q4 consistently outperforms other quarters by 35–40%. **Recommendation:** Build inventory surplus by August; launch targeted marketing campaigns from September.

### 3. North Region Leads, East Region Underperforms
North (₹36.2L) and South (₹33.6L) dominate. East region contributes only 15% of revenue despite being a large market. **Recommendation:** Invest in targeted regional campaigns and faster delivery infrastructure in East India.

### 4. VIP Customers Have Lowest Average Order Value
Counterintuitively, VIP customers (₹2,073 AOV) spend less per order than Regular customers (₹2,300 AOV). This suggests VIP discounts may be too generous. **Recommendation:** Review VIP discount tiers; introduce exclusive product lines instead.

### 5. UPI is the Dominant Payment Method (30%)
UPI leads payment methods, reflecting India's digital payments revolution. **Recommendation:** Offer UPI-exclusive cashback to boost conversion.

### 6. Return/Cancellation Rate is Critically High (39.8%)
This is a major revenue leakage issue. **Recommendation:** Improve product descriptions, images, and implement a "try before you buy" pilot for high-return categories.

---

## 📊 Power BI Dashboard

See `powerbi/dashboard_guide.md` for:
- Step-by-step connection to CSV data
- KPI card setup
- Slicer and filter configuration
- DAX measures for calculated metrics
- Dashboard layout wireframe

### Dashboard Pages
1. **Executive Summary** — KPI cards, total revenue, profit, order volume
2. **Product Performance** — Category breakdown, top products, margin analysis
3. **Regional Analysis** — Map visual, city-level drill-down
4. **Customer Insights** — Segment analysis, payment methods, ratings
5. **Trend Analysis** — Monthly/seasonal line charts with year-over-year comparison

---

## 🛠️ Skills Demonstrated

| Skill Area | Specific Skills |
|-----------|----------------|
| **Data Engineering** | Synthetic data generation, realistic pattern simulation |
| **Data Cleaning** | Missing value imputation, duplicate removal, outlier detection (IQR), Winsorization |
| **Feature Engineering** | Date extraction, derived KPIs, business flags |
| **Exploratory Data Analysis** | Descriptive statistics, distribution analysis, correlation |
| **Data Visualization** | Matplotlib, Seaborn, bar/line/scatter/heatmap/box/donut charts |
| **Business Thinking** | KPI design, insight extraction, actionable recommendations |
| **Python** | Pandas, NumPy, OOP practices, modular scripting |
| **BI Tools** | Power BI dashboard design, DAX basics |
| **Documentation** | README writing, code commenting, project structuring |

---

## 🎤 Interview Q&A

**Q: Why did you use synthetic data instead of a real dataset?**  
A: Synthetic data allowed me to control the quality, structure, and complexity of the dataset, and to intentionally introduce real-world data issues (nulls, duplicates, outliers) to practice cleaning. It also demonstrates my ability to understand business logic well enough to simulate realistic patterns — seasonal trends, segment behavior, and regional variation.

**Q: How did you handle missing values?**  
A: I used business-logic-driven imputation rather than blindly applying mean/median. For customer ratings, I filled nulls with the category median (not the overall median), because satisfaction differs by category. For shipping fees, I applied free shipping logic — orders above ₹499 got ₹0 shipping.

**Q: What was the most important business finding?**  
A: The 39.8% return/cancellation rate. This is a major revenue leakage issue — every returned order incurs a handling loss. Before pushing for more sales, the company should address why customers are returning products.

**Q: How would you improve this project?**  
A: I'd add customer lifetime value (CLV) analysis using RFM segmentation, cohort analysis to track customer retention, and a machine learning model to predict which orders are likely to be returned or cancelled.

**Q: What is the difference between profit and profit margin?**  
A: Profit is an absolute number (₹) — the actual money earned. Profit margin is a percentage — it shows efficiency. A product earning ₹500 profit on ₹1,000 revenue (50% margin) is more efficient than one earning ₹1,000 profit on ₹5,000 revenue (20% margin), even though it earns less in absolute terms.

---

## 👤 Author

**[Your Name]**  
Aspiring Data Analyst | Python · SQL · Power BI  
📧 your.email@example.com  
🔗 [LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/yourusername)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built as a portfolio project to demonstrate end-to-end Data Analysis skills.*
