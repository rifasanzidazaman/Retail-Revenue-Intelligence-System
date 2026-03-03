import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

print("System Started...")

# Load dataset
df = pd.read_csv('data/raw_retail_data.csv', encoding='ISO-8859-1')

# Clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

print("Original Shape:", df.shape)
print("Columns:", df.columns)

# Data cleaning
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)
df = df[df['Quantity'] > 0]

print("After Cleaning Shape:", df.shape)

# Convert date
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Revenue calculation (SAFE version)
if 'Price' in df.columns:
    df['TotalRevenue'] = df['Quantity'] * df['Price']
else:
    raise ValueError("Price column not found in dataset")

# Time features
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.to_period('M')

# Save cleaned dataset
df.to_csv('data/cleaned_retail_data.csv', index=False)
print("Cleaned Data Saved.")

# Monthly revenue
monthly_revenue = df.groupby('Month')['TotalRevenue'].sum()

plt.figure()
monthly_revenue.plot()
plt.title("Monthly Revenue Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/monthly_revenue.png')
plt.close()

print("Monthly Revenue Chart Saved.")

# Top 10 products
top_products = (
    df.groupby('Description')['TotalRevenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure()
top_products.plot(kind='bar')
plt.title("Top 10 Products by Revenue")
plt.xticks(rotation=75)
plt.tight_layout()
plt.savefig('outputs/top_products.png')
plt.close()

print("Top Products Chart Saved.")

# SQLite database
conn = sqlite3.connect('database/retail_database.db')
df.to_sql('retail_data', conn, if_exists='replace', index=False)

print("Database Created Successfully.")

query = """
SELECT Country, SUM(TotalRevenue) as Revenue
FROM retail_data
GROUP BY Country
ORDER BY Revenue DESC
LIMIT 5;
"""

result = pd.read_sql(query, conn)
print("\nTop 5 Countries by Revenue:")
print(result)

conn.close()

print("System Completed Successfully.")