import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt


path = os.path.join(os.getcwd(), "data.csv")
main_data = pd.read_csv(
    path, 
    parse_dates=['order_purchase_timestamp', 'order_approved_at',
                 'order_delivered_customer_date', 'order_estimated_delivery_date']
)

st.title("Project Akhir Dicoding Analisis Data dengan Python")
intro = """
Ini adalah Project Akhir dari Course Dicoding,  
**Belajar Analisis Data Dengan Python**  
Dalam Project ini Saya _Muh Haikal Akbar_ akan menganalisis sebuah dataset yaitu **E-commerce Dataset**.  
Berikut Dashboard hasil analisis saya
"""
st.markdown(intro)

reviews_tab, transaction_tabs, product_sales_tab = st.tabs(["Reviews", "Transaction", "Product Sales"])

with reviews_tab:
    st.header("1. Kepuasan Pelanggan")
    st.metric("Rata-Rata Kepuasan Pelanggan", round(main_data["review_score"].mean(), 1), border=True)
    col1, col2 = st.columns(2)
    with col1:
        data_review = main_data[["review_score"]].copy()
        data_review["Date Review"] = main_data["order_delivered_customer_date"].dt.strftime('%Y-%m')
        data_line = data_review.groupby(["Date Review", "review_score"])["review_score"].value_counts().to_frame().reset_index()
        st.subheader("Trend Total Review")
        st.line_chart(data=data_line, x="Date Review", y="count", color="review_score")
    with col2:
        fig, ax = plt.subplots()
        ax.hist(data_review["review_score"], bins="auto")
        plt.figure(frameon= False)
        st.subheader("Distribusi Review Skor")
        st.pyplot(fig)
    data = main_data[["review_score", "payment_type"]].copy()
    data_bar = data.groupby("payment_type")["review_score"].mean().reset_index()
    st.subheader("Rata-Rata Skor Reviews berdasarkan Metode Pembayaran")
    st.bar_chart(data_bar, x="payment_type", y="review_score", x_label="Payment Method", y_label="Rata-Rata Reviews",color="payment_type")

with transaction_tabs:
    st.header("2. Transaksi")
    trans_col1, trans_col2, trans_col3 = st.columns(3)

    with trans_col1:
        higher_value = main_data["payment_value"].max()
        st.metric("Nilai Transaksi Tertinggi", value=f"${higher_value:,.0f}", border=True)

    with trans_col2:
        lowest_value = main_data["payment_value"].loc[main_data["payment_value"] > 0].min()
        st.metric("Nilai Transaksi Terendah", value=f"${lowest_value:,.0f}", border=True)

    with trans_col3:
        mean_value = main_data["payment_value"].mean()
        st.metric("Rata-Rata Nilai Transaksi", value=f"${mean_value:,.0f}", border=True)

    data_line = main_data[["order_delivered_customer_date", "payment_type", "payment_value"]].copy()
    data_line["Date"] = data_line["order_delivered_customer_date"].dt.strftime("%Y-%m")
    data_line["Payment Type"] = data_line["payment_type"]
    data_line.drop(columns=["order_delivered_customer_date", "payment_type"], inplace=True)
    data_line_grouped = data_line.groupby(["Date", "Payment Type"])["payment_value"].agg(["mean", "sum"]).round(2).reset_index().rename(columns={"mean":"Rata-Rata Transaksi", "sum":"Jumlah Transaksi"})
    
    st.subheader("Rata-Rata Nilai Transaksi Berdasarkan Jenis Pembayaran")
    st.line_chart(data=data_line_grouped, x="Date", y="Rata-Rata Transaksi", color="Payment Type")
    st.subheader("Total Nilai Transaksi Berdasarkan Jenis Pembayaran")
    st.line_chart(data=data_line_grouped, x="Date", y="Jumlah Transaksi", color="Payment Type")

    trans_col4, trans_col5 = st.columns(2)
    with trans_col4:
        st.subheader("Total Nilai Transaksi Berdasarkan Jenis Pembayaran")
        data_1 = main_data[["payment_type", "payment_value"]].copy()
        data_coba = data_1.groupby("payment_type")["payment_value"].sum().reset_index()
        st.bar_chart(data_coba, x="payment_type", y="payment_value", color="payment_type", x_label="Tipe Pembayaran", y_label="Total Jumlah Nilai")
    with trans_col5:
        st.subheader("Proporsi Jenis Pembayaran")
        data_pie = data_1.groupby("payment_type")["payment_type"].value_counts().reset_index()
        fig, ax = plt.subplots()
        ax.pie(data_pie["count"], labels=data_pie["payment_type"], autopct='%1.1f%%')
        st.pyplot(fig)

with product_sales_tab:
    st.header("3. Transaksi Produk")
    data_transaksi = main_data[["order_purchase_timestamp", "product_category_name_english", "payment_type", "payment_value"]].copy()
    data_transaksi.rename(columns={"order_purchase_timestamp":"Order Purchase Date", "product_category_name_english":"Product Category", "payment_type":"Payment Type", "payment_value":"Total Sales"}, inplace=True)
    data_transaksi["Order Purchase Date"] = data_transaksi["Order Purchase Date"].dt.strftime("%Y-%m")

    data_sales = data_transaksi[["Product Category", "Total Sales"]].copy()
    data_sales_bar = data_sales.groupby("Product Category")["Total Sales"].sum().sort_values(ascending=False).reset_index().head(5)
    
    st.subheader("5 Transaksi terbesar berdasarkan Kategori Product")
    st.bar_chart(data_sales_bar, x="Product Category", y="Total Sales")