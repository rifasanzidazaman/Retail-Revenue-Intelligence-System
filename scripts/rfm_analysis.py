import pandas as pd
import numpy as np

print("RFM Analysis Started...")

# ======================================
# 1. Load Cleaned Dataset
# ======================================

df = pd.read_csv('data/cleaned_retail_data.csv')

# Clean column names (removes hidden spaces)
df.columns = df.columns.str.strip()

print("Columns in dataset:")
print(df.columns)

# ======================================
# 2. Convert InvoiceDate to datetime
# ======================================

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# ======================================
# 3. Define Customer Column
# ======================================

customer_column = 'Customer ID'

if customer_column not in df.columns:
    raise ValueError("Customer ID column not found in dataset")

# ======================================
# 4. Define Reference Date
# ======================================

reference_date = df['InvoiceDate'].max()

print("Reference Date:", reference_date)

# ======================================
# 5. Create RFM Table
# ======================================

rfm = df.groupby(customer_column).agg({
    'InvoiceDate': lambda x: (reference_date - x.max()).days,
    'Invoice': 'nunique',
    'TotalRevenue': 'sum'
})

rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'Invoice': 'Frequency',
    'TotalRevenue': 'Monetary'
}, inplace=True)

print("\nRFM Table:")
print(rfm.head())

# ======================================
# 6. RFM Scoring
# ======================================

rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M_score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])

rfm['RFM_Score'] = (
    rfm['R_score'].astype(str) +
    rfm['F_score'].astype(str) +
    rfm['M_score'].astype(str)
)

print("\nRFM Scores:")
print(rfm.head())

# ======================================
# 7. Best Customers
# ======================================

best_customers = rfm[rfm['RFM_Score'] == '444']

print("\nBest Customers (RFM = 444):")
print(best_customers.head())

# ======================================
# 8. Save RFM Table
# ======================================

rfm.to_csv('outputs/rfm_table.csv')

print("\nRFM Analysis Completed Successfully.")

# ======================================
# 9. Customer Segmentation Labels
# ======================================

def segment_customer(row):
    if row['RFM_Score'] == '444':
        return 'VIP'
    elif row['F_score'] == 4:
        return 'Loyal'
    elif row['R_score'] == 1:
        return 'At Risk'
    else:
        return 'Regular'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

print("\nCustomer Segment Distribution:")
print(rfm['Segment'].value_counts())

# Save updated table
rfm.to_csv('outputs/rfm_table.csv')

print("\nUpdated RFM Table Saved with Segments.")