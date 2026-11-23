
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------------
# 1. LOAD DATASET
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "amazon_sales_dataset.csv"
OUTPUT_DIR = BASE_DIR / "analysis_output"

OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_FILE)

print("\n========== E-COMMERCE SALES ANALYSIS ==========")

# -----------------------------------
# 2. UNDERSTAND THE DATASET
# -----------------------------------

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset information:")
df.info()

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

# -----------------------------------
# 3. DATA QUALITY CHECKS
# -----------------------------------

print("\n========== DATA QUALITY ==========")

print("\nMissing values:")
print(df.isnull().sum())

print("\nTotal duplicate rows:")
print(df.duplicated().sum())

print("\nUnique order IDs:")
print(df["order_id"].nunique())

# -----------------------------------
# 4. EXPLORE CATEGORICAL DATA
# -----------------------------------

print("\n========== CATEGORY ANALYSIS ==========")

print("\nOrder status:")
print(df["order_status"].value_counts())

print("\nProduct categories:")
print(df["category"].value_counts())

print("\nSub-categories:")
print(df["sub_category"].value_counts())

print("\nPayment methods:")
print(df["payment_method"].value_counts())

# -----------------------------------
# 5. NUMERICAL SUMMARY
# -----------------------------------

print("\n========== NUMERICAL SUMMARY ==========")

print(df.describe())

# -----------------------------------
# 6. PREPARE DATE COLUMNS
# -----------------------------------

date_columns = ["order_date", "ship_date", "delivery_date"]

for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors="coerce")

print("\nOrder date range:")
print(df["order_date"].min(), "to", df["order_date"].max())

# -----------------------------------
# 7. VALIDATE TOTAL SALES
# -----------------------------------

df["calculated_sales"] = (
    df["quantity"] * df["unit_price"] * (1 - df["discount"])
    + df["shipping_cost"]
)

df["sales_difference"] = (
    df["total_sales"] - df["calculated_sales"]
)

print("\nSales formula validation:")
print(df["sales_difference"].describe())

if np.allclose(df["total_sales"], df["calculated_sales"]):
    print("Sales calculation is verified.")
else:
    print("Warning: Some sales calculations do not match.")

# -----------------------------------
# 8. DAILY SALES ANALYSIS
# -----------------------------------

daily_sales = (
    df.groupby("order_date")["total_sales"]
    .sum()
    .sort_index()
)

daily_sales.to_csv(OUTPUT_DIR / "daily_sales.csv")

print("\n========== DAILY SALES ==========")
print(daily_sales.head())

print("\nHighest sales day:")
print(daily_sales.idxmax(), daily_sales.max())

print("\nLowest sales day:")
print(daily_sales.idxmin(), daily_sales.min())

# -----------------------------------
# 9. CATEGORY-WISE SALES
# -----------------------------------

category_sales = (
    df.groupby("category")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

category_sales.to_csv(OUTPUT_DIR / "category_sales.csv")

print("\n========== CATEGORY SALES ==========")
print(category_sales)

# -----------------------------------
# 10. TOP 10 PRODUCTS
# -----------------------------------

top_products = (
    df.groupby(["product_id", "product_name"])["total_sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

top_products.to_csv(OUTPUT_DIR / "top_10_products.csv")

print("\n========== TOP 10 PRODUCTS ==========")
print(top_products)

# -----------------------------------
# 11. LOCATION-WISE SALES
# -----------------------------------

state_sales = (
    df.groupby("state")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

city_sales = (
    df.groupby("city")["total_sales"]
    .sum()
    .sort_values(ascending=False)
)

state_sales.to_csv(OUTPUT_DIR / "state_sales.csv")
city_sales.to_csv(OUTPUT_DIR / "city_sales.csv")

print("\n========== TOP 10 STATES ==========")
print(state_sales.head(10))

print("\n========== TOP 10 CITIES ==========")
print(city_sales.head(10))

# -----------------------------------
# 12. PAYMENT METHOD ANALYSIS
# -----------------------------------

payment_analysis = (
    df.groupby("payment_method")
    .agg(
        order_count=("order_id", "nunique"),
        total_sales=("total_sales", "sum")
    )
    .sort_values("total_sales", ascending=False)
)

payment_analysis.to_csv(OUTPUT_DIR / "payment_analysis.csv")

print("\n========== PAYMENT ANALYSIS ==========")
print(payment_analysis)

# -----------------------------------
# 13. DISCOUNT ANALYSIS
# -----------------------------------

df["discount_range"] = pd.cut(
    df["discount"],
    bins=[-0.001, 0.10, 0.20, 0.30],
    labels=["0-10%", "10-20%", "20-30%"]
)

discount_analysis = (
    df.groupby("discount_range", observed=False)
    .agg(
        order_count=("order_id", "nunique"),
        average_sales=("total_sales", "mean"),
        total_sales=("total_sales", "sum")
    )
)

discount_analysis.to_csv(OUTPUT_DIR / "discount_analysis.csv")

print("\n========== DISCOUNT ANALYSIS ==========")
print(discount_analysis)

# -----------------------------------
# 14. CREATE CHARTS
# -----------------------------------

# Daily sales trend
plt.figure(figsize=(12, 5))
plt.plot(daily_sales.index, daily_sales.values)
plt.title("Daily Sales Trend")
plt.xlabel("Order Date")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "daily_sales_trend.png")
plt.close()

# Category sales
plt.figure(figsize=(8, 5))
category_sales.plot(kind="bar")
plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "category_sales.png")
plt.close()

# Top 10 products
plt.figure(figsize=(10, 6))
top_products.sort_values().plot(kind="barh")
plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_10_products.png")
plt.close()

# Payment methods
plt.figure(figsize=(8, 5))
payment_analysis["order_count"].plot(kind="bar")
plt.title("Orders by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "payment_methods.png")
plt.close()

# -----------------------------------
# 15. FINAL BUSINESS SUMMARY
# -----------------------------------

print("\n========== FINAL BUSINESS SUMMARY ==========")

print("Total orders:", df["order_id"].nunique())

print("Total sales:", round(df["total_sales"].sum(), 2))

print("Average sales per order:", round(df["total_sales"].mean(), 2))

print("Best performing category:", category_sales.idxmax())

print("Highest sales state:", state_sales.idxmax())

print("Most used payment method:",
      df["payment_method"].value_counts().idxmax())

print("\nAnalysis completed successfully!")
print("Charts and CSV reports saved in:", OUTPUT_DIR)
