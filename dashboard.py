import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt


st.set_page_config(page_title="Data Analytics Dashboard",layout="wide")
st.title("E-commerce Sales & Product Analytics Dashboard")
st.write("Analyze your e-commerce sales data and product performance with this interactive dashboard.")

uploaded_files = st.file_uploader("Upload csv",type='csv',accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df= pd.read_csv(file)
        else:
            st.error("File format not supported")
            continue

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")
        st.write("Preview the head of DataFrame")
        st.dataframe(df.head(10))

        df["Order_Date"] = pd.to_datetime(df["Order_Date"])

        # 🟢 Show Basic Sales Metrics
        total_sales = df["Total_Amount"].sum()
        total_orders = df["Order_ID"].nunique()
        avg_order_value = total_sales / total_orders

        st.write(f"**🛒 Total Orders:** {total_orders}")
        st.write(f"**💰 Total Sales:** Rs. {total_sales:,}")
        st.write(f"**📦 Average Order Value:** Rs. {avg_order_value:.2f}")

        # 🟢 Sales Trend Over Time
        st.write("### 📈 Sales Over Time")
        sales_trend = df.groupby("Order_Date")["Total_Amount"].sum()
        fig, ax = plt.subplots()
        ax.plot(sales_trend.index, sales_trend.values, marker="o", linestyle="-")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Sales (Rs.)")
        ax.set_title("Sales Trend Over Time")
        st.pyplot(fig)

        st.write("### 🏷️ Category-wise Sales Distribution")
        category_sales = df.groupby("Category")["Total_Amount"].sum()
        fig, ax = plt.subplots()
        category_sales.plot(kind="bar", ax=ax)
        ax.set_ylabel("Total Sales (Rs.)")
        st.pyplot(fig)

        st.write("### 🏆 Top 5 Best-Selling Products")
        top_products = df.groupby("Product")["Total_Amount"].sum().nlargest(5)
        st.bar_chart(top_products)

        # 🟢 Top 5 Customers
        st.write("### 👑 Top 5 Customers")
        top_customers = df.groupby("Customer_Name")["Total_Amount"].sum().nlargest(5)
        st.bar_chart(top_customers)

    else:
        st.write("⏳ Please upload a CSV file to see analytics.")