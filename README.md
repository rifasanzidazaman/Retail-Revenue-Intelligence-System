## 🚀 Retail Revenue Intelligence Dashboard

The **Retail Revenue Intelligence Dashboard** is an AI-powered business analytics platform designed to transform retail transaction data into meaningful business insights using advanced analytical and machine learning techniques.

The project focuses on analyzing customer purchasing behavior, revenue distribution patterns, and behavioral segmentation using **RFM (Recency, Frequency, Monetary) customer segmentation methodology**.

The dashboard provides interactive analytics tools that allow users to explore customer-level analytics, business performance indicators, and automated insight generation.

The system integrates **data preprocessing, exploratory data analysis (EDA), visualization engineering, and predictive modeling** to support intelligent business decision-making.

---

## 📁 Project Directory Structure

RETAIL-REVENUE-INTELLIGENCE-SYSTEM

│  
├── dashboard/  
│ ├── app.py  
│ └── dist/  

│  
├── data/  
│ ├── cleaned_retail_data.csv  
│ ├── raw_retail_data.csv  

│  
├── database/  
│ └── retail_database.db  

│  
├── notebooks/  

│  
├── outputs/  
│ ├── monthly_revenue.png  
│ ├── monthly_trend.png  
│ ├── rfm_table.csv  
│ ├── top_countries.png  
│ └── top_products.png  

│  
├── report/  
│ └── rfm_insights.txt  

│  
├── scripts/  
│ ├── eda_analysis.py  
│ ├── main_analysis.py  
│ └── rfm_analysis.py  

│  
├── venv/  
├── .gitignore  
├── README.md  
└── requirements.txt  

---

## 📊 Dataset Description

The retail dataset used in this project is stored inside the **data/** folder of the repository.

The dataset is processed from raw transaction records and converted into structured analytical format suitable for segmentation modeling and business intelligence visualization.

### ⭐ Features Used

- **CustomerID** — Unique customer identifier assigned to each customer  
- **Recency** — Time difference since the customer's last purchase  
- **Frequency** — Number of purchase transactions made by customer  
- **Monetary** — Total spending value per customer  
- **Segment** — Customer behavioral cluster label generated through RFM segmentation methodology  

---

## 🧠 Technical Pipeline

The project follows a structured data science workflow:

1. Data Cleaning and Preprocessing  
2. Exploratory Data Analysis (EDA)  
3. Customer Segmentation Modeling  
4. Machine Learning Classification Prediction  
5. Business Insight Automation  
6. Visualization-Based Reporting System  

---

## 📈 Dashboard Functionalities

✅ Interactive customer segmentation filtering system  
✅ Revenue contribution analytics across segments  
✅ Customer behavioral distribution visualization  
✅ Top revenue generating customer ranking table  
✅ Customer churn risk detection indicator  
✅ Automated business insight summary generator  
✅ Machine learning-based customer segment prediction interface  
✅ Dataset report download functionality  

---

## 🤖 Machine Learning Component

A **Random Forest Classification Model** is used to predict customer segment categories.

### Input Features

- Recency  
- Frequency  
- Monetary Value  

The model helps identify customer purchasing behavior patterns and supports targeted marketing strategies.

---

## 🛠️ Technologies Used

- Python  
- Streamlit  
- Pandas  
- Matplotlib  
- Scikit-learn  

Install dependencies using:

pip install -r requirements.txt  

---

## 🎯 Project Objective

The main objective of this project is to develop an intelligent retail analytics dashboard that helps businesses understand customer behavior patterns, optimize marketing campaigns, and support data-driven business decision-making.

---

## 👩‍💻 Author

**Rifa Sanzida Zaman**

LinkedIn:  
https://www.linkedin.com/in/rifasanzidazaman/

GitHub Repository:  
https://github.com/rifasanzidazaman/Retail-Revenue-Intelligence-System
```

