import streamlit as st
import pandas as pd

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Retail Revenue Intelligence Dashboard",
    layout="wide"
)

st.title("Retail Revenue Intelligence Dashboard")

# ==========================================================
# LOAD DATA
# ==========================================================

# IMPORTANT:
# Since you are running the app from the main project folder
# using: streamlit run dashboard/app.py
# the correct path is:

rfm = pd.read_csv("outputs/rfm_table.csv")

# ==========================================================
# SIDEBAR FILTER
# ==========================================================

st.sidebar.header("Customer Segment Filter")

segments = rfm["Segment"].unique()

selected_segments = st.sidebar.multiselect(
    "Select Segment",
    options=segments,
    default=segments
)

# Filter data based on selection
filtered_data = rfm[rfm["Segment"].isin(selected_segments)]

# ==========================================================
# KPI SECTION
# ==========================================================

total_customers = len(filtered_data)
total_revenue = filtered_data["Monetary"].sum()

vip_revenue = filtered_data[
    filtered_data["Segment"] == "VIP"
]["Monetary"].sum()

if total_revenue != 0:
    vip_percentage = (vip_revenue / total_revenue) * 100
else:
    vip_percentage = 0

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", total_customers)
col2.metric("Total Revenue", round(total_revenue, 2))
col3.metric("VIP Revenue %", round(vip_percentage, 2))

st.markdown(" ")

# ==========================================================
# CHART 1 — SEGMENT DISTRIBUTION
# ==========================================================

st.subheader("Customer Segment Distribution")

segment_counts = filtered_data["Segment"].value_counts()

if not segment_counts.empty:
    st.bar_chart(segment_counts)
else:
    st.warning("No data available for selected filter.")

# ==========================================================
# CHART 2 — REVENUE CONTRIBUTION
# ==========================================================

st.subheader("Revenue Contribution by Segment")

revenue_by_segment = (
    filtered_data
    .groupby("Segment")["Monetary"]
    .sum()
)

if not revenue_by_segment.empty:
    st.bar_chart(revenue_by_segment)
else:
    st.warning("No revenue data available.")

# ==========================================================
# TOP 10 CUSTOMERS TABLE
# ==========================================================

st.subheader("Top 10 Customers by Revenue")

top_customers = (
    filtered_data
    .sort_values(by="Monetary", ascending=False)
    .head(10)
)

st.dataframe(top_customers)


# ==========================================================
# BUSINESS INSIGHT AUTOMATIC SUMMARY
# ==========================================================

st.markdown("---")
st.subheader("🧠 Business Insight Summary")

if not filtered_data.empty:

    insight = ""

    mean_revenue = filtered_data["Monetary"].mean()
    global_mean = rfm["Monetary"].mean()

    if mean_revenue > global_mean:
        insight += "✅ Selected segment customers generate higher than average revenue. "

    churn_risk = len(
        filtered_data[filtered_data["Recency"] >
        filtered_data["Recency"].median()]
    )

    if churn_risk > len(filtered_data) * 0.3:
        insight += "⚠ High customer churn risk detected in this segment. "

    if len(filtered_data) > len(rfm) * 0.5:
        insight += "📊 This segment covers majority customer base. "

    st.info(insight)
    
# ==========================================================
# Download Dataset Button
# ==========================================================


st.markdown("---")
st.subheader("Download Filtered Data")

csv_data = filtered_data.to_csv(index=False)

st.download_button(
    label="Download Report CSV",
    data=csv_data,
    file_name="customer_segment_report.csv",
    mime="text/csv"
)