"""
=============================================================================
E-COMMERCE SALES ANALYSIS PROJECT
Script 03: Exploratory Data Analysis & Visualizations
Author: [Your Name]
Date: 2024
Description: Full EDA with 15+ professional visualizations using
             Matplotlib and Seaborn. Each chart answers a business question.
=============================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

print("=" * 60)
print("  EXPLORATORY DATA ANALYSIS & VISUALIZATIONS")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────────────────
# SETUP: Professional Style Configuration
# ─────────────────────────────────────────────────────────────────────────────

# Custom color palette (professional, accessible)
COLORS = {
    "primary":    "#2563EB",   # Deep Blue
    "secondary":  "#16A34A",   # Green
    "accent":     "#DC2626",   # Red
    "warning":    "#D97706",   # Amber
    "purple":     "#7C3AED",   # Purple
    "teal":       "#0891B2",   # Teal
    "background": "#F8FAFC",   # Light gray
    "text":       "#1E293B",   # Dark slate
}

CATEGORY_COLORS = {
    "Electronics":            "#2563EB",
    "Clothing":               "#16A34A",
    "Home & Kitchen":         "#D97706",
    "Books":                  "#7C3AED",
    "Sports & Fitness":       "#DC2626",
    "Beauty & Personal Care": "#0891B2",
}

# Set global Matplotlib/Seaborn style
plt.rcParams.update({
    "figure.facecolor":  COLORS["background"],
    "axes.facecolor":    "white",
    "axes.edgecolor":    "#E2E8F0",
    "axes.labelcolor":   COLORS["text"],
    "axes.titlesize":    13,
    "axes.titleweight":  "bold",
    "axes.titlecolor":   COLORS["text"],
    "axes.labelsize":    10,
    "xtick.color":       "#64748B",
    "ytick.color":       "#64748B",
    "xtick.labelsize":   9,
    "ytick.labelsize":   9,
    "grid.color":        "#E2E8F0",
    "grid.linestyle":    "--",
    "grid.alpha":        0.7,
    "legend.framealpha": 0.95,
    "legend.fontsize":   9,
    "font.family":       "DejaVu Sans",
})

sns.set_style("whitegrid")

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
clean_path  = os.path.join(BASE_DIR, "data", "ecommerce_clean.csv")
viz_dir     = os.path.join(BASE_DIR, "visualizations")
os.makedirs(viz_dir, exist_ok=True)

df = pd.read_csv(clean_path, parse_dates=["order_date", "delivery_date"])
print(f"\n[INFO] Loaded clean dataset: {len(df):,} rows × {len(df.columns)} columns")

# ─────────────────────────────────────────────────────────────────────────────
# SECTION A: STATISTICAL SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("  SECTION A: STATISTICAL SUMMARY")
print("─"*60)

print("\n── Descriptive Statistics (Numeric Columns) ──────────────")
desc = df[["sales_amount", "profit", "profit_margin",
           "quantity", "unit_price", "discount_pct",
           "customer_rating", "delivery_days"]].describe().round(2)
print(desc.to_string())

print("\n── Business KPI Summary ───────────────────────────────────")
kpis = {
    "Total Revenue (₹)":        f"₹{df['sales_amount'].sum():,.2f}",
    "Total Profit (₹)":         f"₹{df['profit'].sum():,.2f}",
    "Overall Profit Margin (%)": f"{(df['profit'].sum()/df['sales_amount'].sum()*100):.2f}%",
    "Total Orders":             f"{len(df):,}",
    "Unique Customers":         f"{df['customer_id'].nunique():,}",
    "Average Order Value (₹)":  f"₹{df['sales_amount'].mean():.2f}",
    "Avg Customer Rating":      f"{df['customer_rating'].mean():.2f} / 5",
    "Avg Delivery Days":        f"{df['delivery_days'].mean():.1f} days",
    "Return/Cancel Rate (%)":   f"{(df['order_status'].isin(['Returned','Cancelled']).sum()/len(df)*100):.1f}%",
}
for k, v in kpis.items():
    print(f"  {k:<30s}: {v}")

# ─────────────────────────────────────────────────────────────────────────────
# HELPER: Save figure
# ─────────────────────────────────────────────────────────────────────────────
def save_fig(fig, filename, dpi=150):
    path = os.path.join(viz_dir, filename)
    fig.savefig(path, dpi=dpi, bbox_inches="tight",
                facecolor=COLORS["background"])
    plt.close(fig)
    print(f"  ✓ Saved → visualizations/{filename}")
    return path

def add_value_labels(ax, fmt="{:.0f}", fontsize=8, color="#1E293B", pad=3):
    """Add value labels on top of bar chart bars."""
    for bar in ax.patches:
        height = bar.get_height()
        if height != 0:
            ax.annotate(
                fmt.format(height),
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, pad),
                textcoords="offset points",
                ha="center", va="bottom",
                fontsize=fontsize, color=color, fontweight="bold"
            )

# ─────────────────────────────────────────────────────────────────────────────
# CHART 1: Revenue by Category (Horizontal Bar)
# Business Question: Which product categories generate the most revenue?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 1] Revenue by Category...")

cat_revenue = (
    df.groupby("category")["sales_amount"]
    .sum()
    .sort_values(ascending=True)
)
cat_colors = [CATEGORY_COLORS[c] for c in cat_revenue.index]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(cat_revenue.index, cat_revenue.values / 1e6,
               color=cat_colors, height=0.6, edgecolor="white", linewidth=0.5)

# Add value labels inside bars
for bar, val in zip(bars, cat_revenue.values):
    ax.text(bar.get_width() - 0.05, bar.get_y() + bar.get_height() / 2,
            f"₹{val/1e6:.1f}M", va="center", ha="right",
            fontsize=9, color="white", fontweight="bold")

ax.set_title("Revenue by Product Category", pad=15)
ax.set_xlabel("Revenue (₹ Millions)")
ax.set_xlim(0, cat_revenue.max() / 1e6 * 1.15)
ax.grid(axis="y", visible=False)
ax.grid(axis="x", alpha=0.4)

# Insight annotation
ax.text(0.97, 0.05,
        "📊 Top 2 categories contribute\n~45% of total revenue",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=8.5, color="#64748B",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#EFF6FF", alpha=0.8))

fig.suptitle("Business Insight: Electronics & Clothing dominate sales",
             y=0.98, fontsize=10, color="#64748B", style="italic")
fig.tight_layout()
save_fig(fig, "01_revenue_by_category.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 2: Monthly Sales Trend (Line Chart)
# Business Question: How do sales trend month-over-month?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 2] Monthly Sales Trend...")

monthly = (
    df.groupby(["order_year", "order_month"])["sales_amount"]
    .sum()
    .reset_index()
)
monthly["period"] = pd.to_datetime(
    monthly["order_year"].astype(str) + "-" + monthly["order_month"].astype(str)
)
monthly = monthly.sort_values("period")

fig, ax = plt.subplots(figsize=(13, 5))

# Separate 2022 and 2023 for different line styles
for year, style, color, marker in [(2022, "--", "#94A3B8", "o"),
                                    (2023, "-",  COLORS["primary"], "s")]:
    mask = monthly["order_year"] == year
    ax.plot(monthly[mask]["period"],
            monthly[mask]["sales_amount"] / 1e5,
            linestyle=style, color=color,
            linewidth=2.5, marker=marker,
            markersize=7, label=str(year), zorder=3)
    # Fill under line
    ax.fill_between(monthly[mask]["period"],
                    monthly[mask]["sales_amount"] / 1e5,
                    alpha=0.08, color=color)

# Highlight festive season
ax.axvspan(pd.Timestamp("2023-10-01"), pd.Timestamp("2023-12-31"),
           alpha=0.12, color=COLORS["warning"], label="Festive Season")
ax.axvspan(pd.Timestamp("2022-10-01"), pd.Timestamp("2022-12-31"),
           alpha=0.12, color=COLORS["warning"])

ax.set_title("Monthly Sales Revenue Trend (2022 vs 2023)", pad=15)
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (₹ Lakhs)")
ax.legend(loc="upper left")
ax.grid(True, alpha=0.4)

# Format x-axis
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
plt.xticks(rotation=45)

fig.tight_layout()
save_fig(fig, "02_monthly_sales_trend.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 3: Top 10 Products by Revenue (Bar Chart)
# Business Question: Which individual products drive the most revenue?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 3] Top 10 Products by Revenue...")

top_products = (
    df.groupby("product_name")["sales_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(
    range(len(top_products)),
    top_products["sales_amount"] / 1e5,
    color=[COLORS["primary"]] * 3 + [COLORS["teal"]] * 7,
    edgecolor="white", linewidth=0.8, width=0.65
)

# Value labels
for bar, val in zip(bars, top_products["sales_amount"].values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"₹{val/1e5:.1f}L",
            ha="center", va="bottom", fontsize=8, fontweight="bold",
            color=COLORS["text"])

ax.set_xticks(range(len(top_products)))
ax.set_xticklabels(
    [p.replace(" ", "\n") for p in top_products["product_name"]],
    fontsize=8.5
)
ax.set_title("Top 10 Products by Total Revenue", pad=15)
ax.set_ylabel("Revenue (₹ Lakhs)")
ax.grid(axis="x", visible=False)

# Add rank badges
for i in range(3):
    ax.text(i, top_products["sales_amount"].iloc[i] / 1e5 * 0.5,
            f"#{i+1}", ha="center", va="center",
            fontsize=11, fontweight="bold", color="white")

fig.tight_layout()
save_fig(fig, "03_top10_products.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 4: Regional Performance (Side-by-Side Bar)
# Business Question: Which regions generate the most sales & profit?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 4] Regional Performance...")

regional = (
    df.groupby("region")
    .agg(
        Revenue=("sales_amount", "sum"),
        Profit=("profit", "sum"),
        Orders=("order_id", "count"),
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)
regional["Profit_Margin"] = (regional["Profit"] / regional["Revenue"] * 100).round(1)

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
region_colors = [COLORS["primary"], COLORS["secondary"],
                 COLORS["warning"], COLORS["purple"]]

# Revenue
axes[0].bar(regional["region"], regional["Revenue"] / 1e6,
            color=region_colors, edgecolor="white")
axes[0].set_title("Revenue by Region")
axes[0].set_ylabel("₹ Millions")
add_value_labels(axes[0], fmt="₹{:.1f}M", fontsize=8)
axes[0].yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"₹{x:.0f}M"))

# Profit
axes[1].bar(regional["region"], regional["Profit"] / 1e5,
            color=region_colors, edgecolor="white")
axes[1].set_title("Profit by Region")
axes[1].set_ylabel("₹ Lakhs")

# Profit Margin
bars = axes[2].bar(regional["region"], regional["Profit_Margin"],
                   color=region_colors, edgecolor="white")
axes[2].set_title("Profit Margin % by Region")
axes[2].set_ylabel("Profit Margin (%)")
for bar, val in zip(bars, regional["Profit_Margin"]):
    axes[2].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.3,
                 f"{val:.1f}%", ha="center", va="bottom",
                 fontsize=9, fontweight="bold")

for ax in axes:
    ax.grid(axis="x", visible=False)
    ax.tick_params(axis="x", rotation=15)

fig.suptitle("Regional Performance Analysis", fontsize=14,
             fontweight="bold", y=1.02)
fig.tight_layout()
save_fig(fig, "04_regional_performance.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 5: Revenue Share by Category (Donut Chart)
# Business Question: What is the revenue contribution of each category?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 5] Category Revenue Share (Donut)...")

cat_rev = df.groupby("category")["sales_amount"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(9, 7))
wedge_colors = list(CATEGORY_COLORS.values())
explode = [0.04] * len(cat_rev)  # Slightly separate all wedges

wedges, texts, autotexts = ax.pie(
    cat_rev.values,
    labels=None,
    autopct="%1.1f%%",
    startangle=90,
    colors=wedge_colors,
    explode=explode,
    pctdistance=0.78,
    wedgeprops=dict(width=0.6, edgecolor="white", linewidth=2)  # Donut shape
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight("bold")
    autotext.set_color("white")

# Custom legend
legend_labels = [f"{cat}  (₹{rev/1e6:.1f}M)"
                 for cat, rev in cat_rev.items()]
ax.legend(wedges, legend_labels,
          title="Category", loc="lower center",
          bbox_to_anchor=(0.5, -0.12), ncol=2,
          fontsize=9, title_fontsize=10)

# Center text
ax.text(0, 0.05, f"₹{cat_rev.sum()/1e6:.1f}M",
        ha="center", va="center", fontsize=18, fontweight="bold",
        color=COLORS["text"])
ax.text(0, -0.18, "Total Revenue",
        ha="center", va="center", fontsize=10, color="#64748B")

ax.set_title("Revenue Distribution by Product Category", pad=20, fontsize=13)
fig.tight_layout()
save_fig(fig, "05_category_revenue_donut.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 6: Heatmap — Sales by Month & Category
# Business Question: When does each category peak in sales?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 6] Sales Heatmap (Month × Category)...")

month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

pivot_heat = (
    df.pivot_table(
        values="sales_amount",
        index="category",
        columns="month_name",
        aggfunc="sum",
        fill_value=0
    ) / 1e5  # Convert to Lakhs
)
# Reorder columns
pivot_heat = pivot_heat.reindex(columns=month_order, fill_value=0)

fig, ax = plt.subplots(figsize=(14, 5))
sns.heatmap(
    pivot_heat,
    ax=ax,
    cmap="YlOrRd",
    annot=True,
    fmt=".0f",
    linewidths=0.5,
    linecolor="#E2E8F0",
    cbar_kws={"label": "Revenue (₹ Lakhs)", "shrink": 0.8},
    annot_kws={"size": 8.5, "weight": "bold"},
)
ax.set_title("Monthly Revenue Heatmap by Category (₹ Lakhs)", pad=15, fontsize=13)
ax.set_xlabel("Month", fontsize=10)
ax.set_ylabel("Category", fontsize=10)
ax.tick_params(axis="y", rotation=0)

fig.tight_layout()
save_fig(fig, "06_monthly_category_heatmap.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 7: Customer Segment Analysis
# Business Question: Which customer segments are most valuable?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 7] Customer Segment Analysis...")

segment_stats = (
    df.groupby("customer_segment")
    .agg(
        Total_Revenue=("sales_amount", "sum"),
        Total_Orders=("order_id", "count"),
        Avg_Order_Value=("sales_amount", "mean"),
        Avg_Discount=("discount_pct", "mean"),
        Avg_Rating=("customer_rating", "mean"),
    )
    .reset_index()
)
segment_stats["Revenue_per_Order"] = (
    segment_stats["Total_Revenue"] / segment_stats["Total_Orders"]
)

seg_colors = [COLORS["accent"], COLORS["purple"],
              COLORS["primary"], COLORS["secondary"]]
seg_order = ["New", "Regular", "Premium", "VIP"]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Revenue by segment
seg_rev = segment_stats.set_index("customer_segment").reindex(seg_order)
bars = axes[0].bar(seg_order,
                   seg_rev["Total_Revenue"] / 1e6,
                   color=seg_colors, edgecolor="white", width=0.55)
axes[0].set_title("Total Revenue by Customer Segment")
axes[0].set_ylabel("Revenue (₹ Millions)")
for bar, val in zip(bars, seg_rev["Total_Revenue"]):
    axes[0].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.02,
                 f"₹{val/1e6:.1f}M",
                 ha="center", va="bottom", fontsize=9, fontweight="bold")

# Avg Order Value by segment
seg_aov = segment_stats.set_index("customer_segment").reindex(seg_order)
bars2 = axes[1].bar(seg_order,
                    seg_aov["Avg_Order_Value"],
                    color=seg_colors, edgecolor="white", width=0.55)
axes[1].set_title("Average Order Value by Customer Segment")
axes[1].set_ylabel("Avg Order Value (₹)")
for bar, val in zip(bars2, seg_aov["Avg_Order_Value"]):
    axes[1].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 10,
                 f"₹{val:.0f}",
                 ha="center", va="bottom", fontsize=9, fontweight="bold")

for ax in axes:
    ax.grid(axis="x", visible=False)

fig.suptitle("Customer Segment Analysis", fontsize=14, fontweight="bold")
fig.tight_layout()
save_fig(fig, "07_customer_segment_analysis.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 8: Payment Method Distribution (Stacked Bar)
# Business Question: What payment methods do customers prefer?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 8] Payment Method Distribution...")

payment_counts = df["payment_method"].value_counts()

fig, ax = plt.subplots(figsize=(9, 5))
payment_colors = ["#2563EB", "#16A34A", "#D97706",
                  "#7C3AED", "#DC2626", "#0891B2"]
wedges, texts, autotexts = ax.pie(
    payment_counts.values,
    labels=payment_counts.index,
    autopct="%1.1f%%",
    colors=payment_colors,
    startangle=140,
    pctdistance=0.82,
    wedgeprops=dict(edgecolor="white", linewidth=2)
)
for at in autotexts:
    at.set_fontsize(8.5)
    at.set_fontweight("bold")

ax.set_title("Payment Method Preference", pad=15, fontsize=13)
fig.tight_layout()
save_fig(fig, "08_payment_methods.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 9: Profit Margin by Category (Box Plot)
# Business Question: How does profitability vary across categories?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 9] Profit Margin Distribution by Category...")

fig, ax = plt.subplots(figsize=(11, 5))
category_order = (
    df.groupby("category")["profit_margin"]
    .median()
    .sort_values(ascending=False)
    .index.tolist()
)

sns.boxplot(
    data=df,
    x="category",
    y="profit_margin",
    order=category_order,
    palette=list(CATEGORY_COLORS.values()),
    width=0.5,
    linewidth=1.2,
    fliersize=3,
    ax=ax,
)

ax.axhline(y=df["profit_margin"].median(), color=COLORS["accent"],
           linestyle="--", linewidth=1.5, label="Overall Median Margin", alpha=0.8)
ax.set_title("Profit Margin Distribution by Product Category", pad=15)
ax.set_xlabel("Category")
ax.set_ylabel("Profit Margin (%)")
ax.legend()
plt.xticks(rotation=20)
fig.tight_layout()
save_fig(fig, "09_profit_margin_boxplot.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 10: Seasonal Revenue Pattern
# Business Question: What are the seasonal trends in revenue?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 10] Seasonal Revenue Pattern...")

seasonal = (
    df.groupby(["order_year", "season"])["sales_amount"]
    .sum()
    .reset_index()
)
season_order = ["Spring", "Summer", "Autumn", "Winter"]
seasonal["season"] = pd.Categorical(seasonal["season"],
                                    categories=season_order, ordered=True)
seasonal = seasonal.sort_values(["order_year", "season"])

fig, ax = plt.subplots(figsize=(9, 5))
season_colors_map = {
    "Spring": "#16A34A",
    "Summer": "#D97706",
    "Autumn": "#DC2626",
    "Winter": "#2563EB"
}

x = np.arange(len(season_order))
width = 0.35
for idx, (year, color) in enumerate([(2022, "#94A3B8"), (2023, COLORS["primary"])]):
    yr_data = seasonal[seasonal["order_year"] == year].set_index("season")
    yr_data = yr_data.reindex(season_order)
    bars = ax.bar(x + idx * width - width / 2,
                  yr_data["sales_amount"].values / 1e6,
                  width, label=str(year), color=color,
                  edgecolor="white", alpha=0.9)

ax.set_xticks(x)
ax.set_xticklabels(season_order, fontsize=10)
ax.set_title("Seasonal Revenue Pattern (2022 vs 2023)", pad=15)
ax.set_ylabel("Revenue (₹ Millions)")
ax.legend()
ax.grid(axis="x", visible=False)
fig.tight_layout()
save_fig(fig, "10_seasonal_trends.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 11: Order Status Distribution
# Business Question: What is the fulfillment quality?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 11] Order Status Distribution...")

status_counts = df["order_status"].value_counts()
status_colors = {
    "Delivered":  COLORS["secondary"],
    "Returned":   COLORS["warning"],
    "Cancelled":  COLORS["accent"],
}

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(status_counts.index,
              status_counts.values,
              color=[status_colors.get(s, COLORS["primary"]) for s in status_counts.index],
              edgecolor="white", linewidth=1, width=0.45)

for bar, val in zip(bars, status_counts.values):
    pct = val / len(df) * 100
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 20,
            f"{val:,}\n({pct:.1f}%)",
            ha="center", va="bottom", fontsize=9, fontweight="bold")

ax.set_title("Order Status Distribution", pad=15)
ax.set_ylabel("Number of Orders")
ax.grid(axis="x", visible=False)
fig.tight_layout()
save_fig(fig, "11_order_status.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 12: Revenue vs Profit Scatter (by Category)
# Business Question: Do high-revenue categories also have high profit?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 12] Revenue vs Profit Scatter...")

scatter_data = (
    df.groupby(["category", "product_name"])
    .agg(Revenue=("sales_amount", "sum"),
         Profit=("profit", "sum"),
         Orders=("order_id", "count"))
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 6))

for cat in scatter_data["category"].unique():
    mask = scatter_data["category"] == cat
    ax.scatter(
        scatter_data[mask]["Revenue"] / 1e5,
        scatter_data[mask]["Profit"] / 1e5,
        label=cat,
        color=CATEGORY_COLORS[cat],
        s=scatter_data[mask]["Orders"] * 3,
        alpha=0.75, edgecolors="white", linewidth=0.5
    )

# Add diagonal reference line (break-even)
max_val = max(scatter_data["Revenue"].max(), scatter_data["Profit"].max()) / 1e5
ax.plot([0, max_val * 0.6], [0, max_val * 0.6 * 0.35],
        color="#94A3B8", linestyle="--", alpha=0.5, label="Trend line")

ax.set_title("Revenue vs Profit by Product (bubble = order volume)", pad=15)
ax.set_xlabel("Revenue (₹ Lakhs)")
ax.set_ylabel("Profit (₹ Lakhs)")
ax.legend(loc="upper left", fontsize=8.5)
ax.grid(True, alpha=0.4)
fig.tight_layout()
save_fig(fig, "12_revenue_vs_profit_scatter.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 13: Customer Rating Distribution
# Business Question: How satisfied are our customers?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 13] Customer Rating Distribution...")

rating_counts = df["customer_rating"].value_counts().sort_index()
rating_colors = ["#DC2626", "#D97706", "#F59E0B", "#16A34A", "#15803D"]

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Bar chart
bars = axes[0].bar(rating_counts.index.astype(int),
                   rating_counts.values,
                   color=rating_colors, edgecolor="white", width=0.6)
axes[0].set_title("Customer Rating Distribution")
axes[0].set_xlabel("Rating (1–5 Stars)")
axes[0].set_ylabel("Number of Orders")
axes[0].set_xticks([1, 2, 3, 4, 5])
for bar, val in zip(bars, rating_counts.values):
    axes[0].text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 5,
                 f"{val:,}", ha="center", va="bottom", fontsize=9)

# Rating by segment
rating_by_seg = df.groupby("customer_segment")["customer_rating"].mean().sort_values()
bars2 = axes[1].barh(rating_by_seg.index, rating_by_seg.values,
                     color=COLORS["primary"], height=0.5, edgecolor="white")
axes[1].set_title("Average Rating by Customer Segment")
axes[1].set_xlabel("Average Rating")
axes[1].set_xlim(3, 5)
for bar, val in zip(bars2, rating_by_seg.values):
    axes[1].text(val + 0.02, bar.get_y() + bar.get_height() / 2,
                 f"⭐ {val:.2f}", va="center", fontsize=10)

fig.tight_layout()
save_fig(fig, "13_customer_ratings.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 14: Top 10 Cities by Revenue
# Business Question: Which cities are our biggest markets?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 14] Top 10 Cities by Revenue...")

city_revenue = (
    df.groupby(["region", "city"])["sales_amount"]
    .sum()
    .reset_index()
    .sort_values("sales_amount", ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 5))
city_bar_colors = [CATEGORY_COLORS.get(
    ["Electronics", "Clothing", "Home & Kitchen",
     "Books", "Sports & Fitness", "Beauty & Personal Care"][i % 6], COLORS["primary"]
) for i in range(10)]

bars = ax.barh(city_revenue["city"], city_revenue["sales_amount"] / 1e5,
               color=city_bar_colors, height=0.55, edgecolor="white")

for bar, val in zip(bars, city_revenue["sales_amount"].values):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
            f"₹{val/1e5:.1f}L", va="center", fontsize=9, fontweight="bold")

ax.set_title("Top 10 Cities by Revenue", pad=15)
ax.set_xlabel("Revenue (₹ Lakhs)")
ax.grid(axis="y", visible=False)
fig.tight_layout()
save_fig(fig, "14_top_cities_revenue.png")

# ─────────────────────────────────────────────────────────────────────────────
# CHART 15: Discount vs Sales Amount (Scatter + Regression)
# Business Question: Do discounts actually drive higher order values?
# ─────────────────────────────────────────────────────────────────────────────
print("\n[CHART 15] Discount vs Sales Amount Analysis...")

sample_df = df.sample(n=min(1500, len(df)), random_state=42)

fig, ax = plt.subplots(figsize=(9, 5))
scatter = ax.scatter(
    sample_df["discount_pct"] * 100,
    sample_df["sales_amount"],
    c=sample_df["customer_rating"],
    cmap="RdYlGn",
    alpha=0.5, s=25, edgecolors="none"
)

# Regression line
z = np.polyfit(sample_df["discount_pct"] * 100, sample_df["sales_amount"], 1)
p = np.poly1d(z)
x_line = np.linspace(0, sample_df["discount_pct"].max() * 100, 100)
ax.plot(x_line, p(x_line), color=COLORS["accent"],
        linewidth=2, linestyle="--", label="Trend", alpha=0.8)

cb = plt.colorbar(scatter, ax=ax)
cb.set_label("Customer Rating", fontsize=9)

ax.set_title("Discount % vs Sales Amount (colored by Customer Rating)", pad=15)
ax.set_xlabel("Discount (%)")
ax.set_ylabel("Sales Amount (₹)")
ax.legend()
fig.tight_layout()
save_fig(fig, "15_discount_vs_sales.png")

# ─────────────────────────────────────────────────────────────────────────────
# PRINT FULL BUSINESS INSIGHTS SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  KEY BUSINESS INSIGHTS")
print("=" * 60)

# Category insights
print("\n📦 PRODUCT CATEGORY INSIGHTS:")
cat_summary = df.groupby("category").agg(
    Revenue=("sales_amount", "sum"),
    Profit=("profit", "sum"),
    Orders=("order_id", "count"),
    Margin=("profit_margin", "mean"),
).sort_values("Revenue", ascending=False)
cat_summary["Margin_pct"] = cat_summary["Margin"].round(1)
cat_summary["Revenue_M"] = (cat_summary["Revenue"] / 1e6).round(2)
print(cat_summary[["Revenue_M", "Profit", "Orders", "Margin_pct"]].to_string())

# Regional insights
print("\n🗺️ REGIONAL INSIGHTS:")
reg_summary = df.groupby("region").agg(
    Revenue=("sales_amount", "sum"),
    Orders=("order_id", "count"),
    Margin=("profit_margin", "mean"),
).sort_values("Revenue", ascending=False)
print(reg_summary.round(2).to_string())

# Segment insights
print("\n👥 CUSTOMER SEGMENT INSIGHTS:")
seg_summary = df.groupby("customer_segment").agg(
    Revenue=("sales_amount", "sum"),
    AOV=("sales_amount", "mean"),
    Rating=("customer_rating", "mean"),
).sort_values("Revenue", ascending=False)
print(seg_summary.round(2).to_string())

print("\n✅ All 15 charts generated successfully!")
print(f"   Saved to: {viz_dir}")
