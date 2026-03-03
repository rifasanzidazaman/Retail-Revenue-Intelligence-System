import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Retail Intelligence System",
    page_icon="🚀",
    layout="wide"
)

# ------------------ DARK THEME & SIDEBAR CSS ------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #1e1b4b, #000000);
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}
header {visibility: hidden;}
footer {visibility: hidden;}
.block-container {padding-top: 2rem; padding-left: 3rem; padding-right: 3rem;}
[data-testid="stSidebar"] {background: #0a0a1f; color: #ffffff;}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div[role="radiogroup"] label {
    color: #ffffff !important;
}
.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(139,92,246,0.3);
    box-shadow: 0 0 30px rgba(139,92,246,0.4);
    text-align: center;
    transition: 0.3s;
}
.metric-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 0 40px rgba(56,189,248,0.7);
}
.chart-card {
    background: rgba(255,255,255,0.04);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(99,102,241,0.2);
    box-shadow: 0 0 25px rgba(99,102,241,0.4);
    margin-bottom: 30px;
}
.stDataFrame div.row_heading, .stDataFrame th {
    color: #f1f5f9 !important;
    background-color: rgba(255,255,255,0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
rfm_path = os.path.join(ROOT_DIR, "outputs", "rfm_table.csv")

@st.cache_data
def load_data():
    if not os.path.exists(rfm_path):
        return None
    return pd.read_csv(rfm_path)

rfm = load_data()
if rfm is None:
    st.error("rfm_table.csv not found in outputs folder.")
    st.stop()

# ------------------ SIDEBAR ------------------
st.sidebar.markdown("<h2 style='font-weight:700;'>🚀 Performance Navigator</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p>Select Dashboard View</p>", unsafe_allow_html=True)
page = st.sidebar.radio("", ["Executive Overview", "RFM Deep Dive", "Customer Segments"])
st.sidebar.markdown("---")
st.sidebar.markdown("<p>Minimum Customer Spend</p>", unsafe_allow_html=True)
min_spend = st.sidebar.slider(
    "",
    int(rfm["Monetary"].min()),
    int(rfm["Monetary"].max()),
    int(rfm["Monetary"].min())
)

# ------------------ FILTER DATA ------------------
filtered_rfm = rfm[rfm["Monetary"] >= min_spend]

# ================= EXECUTIVE OVERVIEW =================
if page == "Executive Overview":
    st.title("📊 Executive Intelligence Dashboard")

    total_customers = filtered_rfm.shape[0]
    avg_monetary = filtered_rfm["Monetary"].mean()
    avg_frequency = filtered_rfm["Frequency"].mean()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Total Customers</h4>
            <h1>{total_customers}</h1>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Avg Customer Spend</h4>
            <h1>₹ {round(avg_monetary,2)}</h1>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Avg Purchase Frequency</h4>
            <h1>{round(avg_frequency,2)}</h1>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    colA, colB = st.columns(2)

    # Histogram with purple neon
    with colA:
        fig_hist = px.histogram(
            filtered_rfm,
            x="Monetary",
            nbins=40,
            color_discrete_sequence=["#a855f7"]  # bright purple
        )
        fig_hist.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#f1f5f9",
            title="Customer Spending Distribution"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    # Pie Chart with vibrant purple theme
    with colB:
        if "Segment" in filtered_rfm.columns:
            segment_counts = filtered_rfm["Segment"].value_counts().reset_index()
            segment_counts.columns = ["Segment", "Count"]
            fig_pie = px.pie(
                segment_counts,
                names="Segment",
                values="Count",
                hole=0.6,
                color_discrete_sequence=["#a855f7","#c084fc","#9333ea","#7c3aed","#d8b4fe","#e0d6fd"]
            )
            fig_pie.update_traces(textinfo="percent+label")
            fig_pie.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#f1f5f9",
                title="Customer Segment Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # Scatter Plot with purple gradient
    st.markdown("### 🔥 Customer Value Analysis")
    fig_scatter = px.scatter(
        filtered_rfm,
        x="Frequency",
        y="Monetary",
        color="Segment" if "Segment" in filtered_rfm.columns else None,
        size="Monetary",
        color_discrete_sequence=["#a855f7","#c084fc","#9333ea","#7c3aed"],
        hover_data=["Recency"]
    )
    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#f1f5f9"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ================= RFM DEEP DIVE =================
elif page == "RFM Deep Dive":
    st.title("📈 RFM Deep Analysis")
    for metric, color in zip(["Recency","Frequency","Monetary"], ["#ec4899","#22d3ee","#a855f7"]):
        fig = px.histogram(
            filtered_rfm,
            x=metric,
            color_discrete_sequence=[color]
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#f1f5f9",
            title=f"{metric} Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

# ================= CUSTOMER SEGMENTS =================
elif page == "Customer Segments":
    st.title("👥 Customer Intelligence")
    if "Segment" in filtered_rfm.columns:
        segment_counts = filtered_rfm["Segment"].value_counts().reset_index()
        segment_counts.columns = ["Segment", "Count"]
        fig_bar = px.bar(
            segment_counts,
            x="Segment",
            y="Count",
            color="Segment",
            color_discrete_sequence=["#a855f7","#c084fc","#9333ea","#7c3aed"]
        )
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#f1f5f9",
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.dataframe(filtered_rfm, use_container_width=True)

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("<h4>🚀 Built as a Premium Startup SaaS Analytics Product</h4>", unsafe_allow_html=True)