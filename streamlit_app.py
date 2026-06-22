import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", layout="wide")

DATA_PATH = "data/orders.csv"


@st.cache_data
def load_orders(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["order_date"].dt.strftime("%Y-%m")
    return df


orders = load_orders(DATA_PATH)

st.sidebar.header("Filters")

categories = sorted(orders["category"].unique())
selected_categories = st.sidebar.multiselect(
    "Category", categories, default=categories
)

min_date = orders["order_date"].min().date()
max_date = orders["order_date"].max().date()
date_range = st.sidebar.date_input(
    "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)
start_date, end_date = date_range if isinstance(date_range, tuple) else (min_date, max_date)

filtered = orders[
    orders["category"].isin(selected_categories)
    & (orders["order_date"].dt.date >= start_date)
    & (orders["order_date"].dt.date <= end_date)
]

st.title("Sales Dashboard")

if filtered.empty:
    st.warning("No orders match the selected filters.")
    st.stop()

total_revenue = filtered["revenue"].sum()
total_orders = filtered["order_id"].nunique()
aov = total_revenue / total_orders

monthly = (
    filtered.groupby("month")
    .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
    .reset_index()
    .sort_values("month")
)
best_month_row = monthly.loc[monthly["revenue"].idxmax()]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Avg Order Value", f"${aov:,.2f}")
col4.metric("Best Month", best_month_row["month"], f"${best_month_row['revenue']:,.2f}")

st.subheader("Revenue by Month")
st.bar_chart(monthly.set_index("month")["revenue"])
st.caption(
    "Revenue climbs through the second half of the year before a sharp post-holiday "
    "dip, then recovers steadily. Order counts track revenue closely, meaning swings "
    "are driven mainly by how many orders are placed rather than by changes in "
    "average order value."
)

st.subheader("Revenue by Category")
by_category = (
    filtered.groupby("category")
    .agg(revenue=("revenue", "sum"), orders=("order_id", "nunique"))
    .reset_index()
)
by_category["aov"] = by_category["revenue"] / by_category["orders"]
by_category = by_category.sort_values("revenue", ascending=False)

chart_col, table_col = st.columns([2, 1])
chart_col.bar_chart(by_category.set_index("category")["revenue"])
table_col.dataframe(
    by_category.rename(
        columns={"category": "Category", "revenue": "Revenue", "orders": "Orders", "aov": "AOV"}
    ).style.format({"Revenue": "${:,.2f}", "AOV": "${:,.2f}"}),
    hide_index=True,
    use_container_width=True,
)
