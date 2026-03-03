import pandas as pd
import matplotlib.pyplot as plt

print("EDA Started...")

# ======================================
# 1. Load Cleaned Dataset
# ======================================

df = pd.read_csv('data/cleaned_retail_data.csv')

# Clean column names (removes hidden spaces)
df.columns = df.columns.str.strip()

print("\nDataset Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

# ======================================
# 2. Basic Validation
# ======================================

required_columns = ['InvoiceDate', 'TotalRevenue', 'Country', 'Description']

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Required column '{col}' not found in dataset")

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# ======================================
# 3. Revenue by Country
# ======================================

country_revenue = (
    df.groupby('Country')['TotalRevenue']
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Countries by Revenue:")
print(country_revenue.head(10))

plt.figure()
country_revenue.head(10).plot(kind='bar')
plt.title("Top 10 Countries by Revenue")
plt.xticks(rotation=75)
plt.tight_layout()
plt.savefig('outputs/top_countries.png')
plt.close()

print("Top Countries chart saved.")

# ======================================
# 4. Monthly Revenue Trend
# ======================================

df['Month'] = df['InvoiceDate'].dt.to_period('M')

monthly_revenue = (
    df.groupby('Month')['TotalRevenue']
    .sum()
)

print("\nMonthly Revenue:")
print(monthly_revenue)

plt.figure()
monthly_revenue.plot()
plt.title("Monthly Revenue Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/monthly_trend.png')
plt.close()

print("Monthly trend chart saved.")

# ======================================
# 5. Top 10 Products
# ======================================

top_products = (
    df.groupby('Description')['TotalRevenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Revenue:")
print(top_products)

plt.figure()
top_products.plot(kind='bar')
plt.title("Top 10 Products by Revenue")
plt.xticks(rotation=75)
plt.tight_layout()
plt.savefig('outputs/top_products.png')
plt.close()

print("Top products chart saved.")

# ======================================
# 6. Top 10 Customers (If Available)
# ======================================

if 'CustomerID' in df.columns:
    top_customers = (
        df.groupby('CustomerID')['TotalRevenue']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print("\nTop 10 Customers by Revenue:")
    print(top_customers)
else:
    print("\nCustomerID column not found. Skipping customer analysis.")

print("\nEDA Completed Successfully.")