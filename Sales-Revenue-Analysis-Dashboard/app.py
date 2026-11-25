import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Sales & Revenue Dashboard", page_icon="📊", layout="wide")
st.title("📊 Sales & Revenue Analysis Dashboard")
st.caption("Interactive business dashboard | Educational project using synthetic sales data")

DEFAULT_FILE = Path(__file__).parent / "data" / "sales_data.csv"

@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")
    for col in ["Quantity", "Unit_Price", "Discount", "Revenue"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")
    data = data.drop_duplicates(subset=["Order_ID"])
    data = data.dropna(subset=["Order_Date", "Product", "Revenue", "Quantity"])
    data["Region"] = data["Region"].fillna("Unknown")
    data["Category"] = data["Category"].fillna("Unknown")
    data["Month"] = data["Order_Date"].dt.to_period("M").astype(str)
    return data

st.sidebar.header("Data and filters")
uploaded = st.sidebar.file_uploader("Upload sales CSV or Excel file", type=["csv", "xlsx", "xls"])
if uploaded is not None:
    if uploaded.name.lower().endswith(".csv"):
        raw = pd.read_csv(uploaded)
    else:
        raw = pd.read_excel(uploaded)
    # Normalize required column names and parse dates
    required = ["Order_ID","Order_Date","Product","Category","Quantity","Unit_Price","Discount","Revenue","Region"]
    missing = [c for c in required if c not in raw.columns]
    if missing:
        st.error("Uploaded file is missing required columns: " + ", ".join(missing))
        st.stop()
    raw.to_csv("/tmp/uploaded_sales.csv", index=False)
    data = load_data("/tmp/uploaded_sales.csv")
else:
    data = load_data(DEFAULT_FILE)

if data.empty:
    st.warning("No valid sales records found.")
    st.stop()

min_date, max_date = data["Order_Date"].min().date(), data["Order_Date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

regions = sorted(data["Region"].dropna().unique())
categories = sorted(data["Category"].dropna().unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
filtered = data[
    data["Order_Date"].dt.date.between(start_date, end_date)
    & data["Region"].isin(selected_regions)
    & data["Category"].isin(selected_categories)
].copy()

st.sidebar.caption(f"Showing {len(filtered):,} of {len(data):,} cleaned orders")
if filtered.empty:
    st.info("No records match the selected filters. Change the filters to see results.")
    st.stop()

total_revenue = filtered["Revenue"].sum()
total_orders = filtered["Order_ID"].nunique()
total_units = filtered["Quantity"].sum()
avg_order = total_revenue / total_orders if total_orders else 0

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Units Sold", f"{total_units:,.0f}")
c4.metric("Average Order Value", f"₹{avg_order:,.0f}")

st.divider()
left,right = st.columns(2)
monthly = filtered.groupby("Month", as_index=False)["Revenue"].sum()
with left:
    st.subheader("Revenue trend")
    fig = px.line(monthly, x="Month", y="Revenue", markers=True, title="Monthly revenue")
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue (₹)")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Revenue by category")
    cat = filtered.groupby("Category", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    fig = px.bar(cat, x="Category", y="Revenue", color="Category", title="Category performance")
    st.plotly_chart(fig, use_container_width=True)

left,right = st.columns(2)
with left:
    st.subheader("Top-performing products")
    prod = filtered.groupby("Product", as_index=False).agg(Revenue=("Revenue","sum"), Units=("Quantity","sum"))
    prod = prod.sort_values("Revenue", ascending=False).head(8)
    fig = px.bar(prod, x="Revenue", y="Product", orientation="h", color="Revenue", title="Top products by revenue")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Revenue by region")
    reg = filtered.groupby("Region", as_index=False)["Revenue"].sum()
    fig = px.pie(reg, names="Region", values="Revenue", hole=.4, title="Regional revenue share")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Sales data")
st.dataframe(filtered.sort_values("Order_Date", ascending=False), use_container_width=True, hide_index=True)
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", csv, "filtered_sales_data.csv", "text/csv")

st.info("Dataset note: The bundled sales dataset is synthetic and created for educational demonstration. Upload a real dataset with the required columns to analyze actual business performance.")
