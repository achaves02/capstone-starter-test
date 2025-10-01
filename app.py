import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Sales Dashboard", layout="wide")

@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    # parse dates
    for col in ["Order Date", "Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    # ensure Sales numeric
    if "Sales" in df.columns:
        df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce").fillna(0.0)
    return df

DATA_PATH = "data/sales.csv"

df = load_data(DATA_PATH)

# --- Sidebar filters
st.sidebar.header("Filters")
min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date))
region_opts = df["Region"].dropna().unique().tolist()
region = st.sidebar.multiselect("Region", options=region_opts, default=region_opts)
category_opts = df["Category"].dropna().unique().tolist()
category = st.sidebar.multiselect("Category", options=category_opts, default=category_opts)
ship_modes = df["Ship Mode"].dropna().unique().tolist()
ship_mode = st.sidebar.multiselect("Ship Mode", options=ship_modes, default=ship_modes)

# Apply filters
filtered = df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = filtered[(filtered["Order Date"] >= start) & (filtered["Order Date"] <= end)]

if region:
    filtered = filtered[filtered["Region"].isin(region)]
if category:
    filtered = filtered[filtered["Category"].isin(category)]
if ship_mode:
    filtered = filtered[filtered["Ship Mode"].isin(ship_mode)]

# --- KPIs
col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
with col1:
    st.metric("Total Sales", f"${filtered['Sales'].sum():,.2f}")
with col2:
    st.metric("Orders", filtered['Order ID'].nunique())
with col3:
    # avg order value
    order_sums = filtered.groupby('Order ID')['Sales'].sum()
    st.metric("Avg Order Value", f"${order_sums.mean():,.2f}")
with col4:
    st.metric("Rows", filtered.shape[0])

st.markdown("---")

# --- Sales over time
st.header("Sales over time")
if "Order Date" in filtered.columns:
    time_df = filtered.set_index('Order Date').resample('M')['Sales'].sum().reset_index()
    chart = alt.Chart(time_df).mark_line(point=True).encode(
        x=alt.X('Order Date:T', title='Order Date'),
        y=alt.Y('Sales:Q', title='Sales')
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

# --- Sales by Region
st.header("Sales by Region")
region_df = filtered.groupby('Region', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
bar = alt.Chart(region_df).mark_bar().encode(
    x=alt.X('Sales:Q'),
    y=alt.Y('Region:N', sort='-x')
)
st.altair_chart(bar, use_container_width=True)

# --- Top products
st.header("Top products")
top_products = filtered.groupby('Product Name', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False).head(10)
prod_bar = alt.Chart(top_products).mark_bar().encode(
    x=alt.X('Sales:Q'),
    y=alt.Y('Product Name:N', sort='-x')
)
st.altair_chart(prod_bar, use_container_width=True)

# --- Category breakdown
st.header("Sales by Category")
cat_df = filtered.groupby('Category', as_index=False)['Sales'].sum().sort_values('Sales', ascending=False)
cat_chart = alt.Chart(cat_df).mark_bar().encode(
    x=alt.X('Category:N', sort='-y', title='Category'),
    y=alt.Y('Sales:Q', title='Sales')
)
st.altair_chart(cat_chart, use_container_width=True)

# --- Data and download
st.header("Filtered data")
st.dataframe(filtered.reset_index(drop=True))

@st.cache_data
def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = to_csv(filtered)
st.download_button("Download filtered data as CSV", csv, file_name='filtered_sales.csv', mime='text/csv')
