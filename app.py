import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="UAC Care Load Analytics",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("UAC_Care_Load_Cleaned.csv")
df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# Header
# -----------------------------

st.title("System Capacity & Care Load Analytics")

st.markdown(
    "An interactive dashboard for analyzing system load, care capacity, "
    "transfers, discharges, backlog patterns, and operational trends "
    "within the Unaccompanied Children care system."
)

st.caption(
    f"Data period: {df['Date'].min().strftime('%d %B %Y')} "
    f"to {df['Date'].max().strftime('%d %B %Y')}"
)

st.divider()

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Dashboard Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Reporting Period",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

granularity = st.sidebar.selectbox(
    "Time Granularity",
    ["Daily", "Weekly", "Monthly"]
)

st.sidebar.subheader("Metric Selection")

selected_metrics = st.sidebar.multiselect(
    "Select Metrics to Display",
    [
        "Total System Load",
        "Children in CBP custody",
        "Children in HHS Care",
        "Net Daily Intake",
        "7-Day Rolling Load",
        "14-Day Rolling Load"
    ],
    default=["Total System Load"]
)


if len(date_range) == 2:
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    filtered_df = df[
        (df["Date"] >= start_date) &
        (df["Date"] <= end_date)
    ].copy()
else:
    filtered_df = df.copy()

# -----------------------------
# Empty Data Check
# -----------------------------

if filtered_df.empty:
    st.warning(
        "No data is available for the selected reporting period. "
        "Please choose a different date range."
    )
    st.stop()

# -----------------------------
# KPI Calculations
# -----------------------------

reporting_days = len(filtered_df)

highest_load = filtered_df["Total System Load"].max()
lowest_load = filtered_df["Total System Load"].min()

average_load = filtered_df["Total System Load"].mean()

total_transfers = filtered_df[
    "Children transferred out of CBP custody"
].sum()

total_discharges = filtered_df[
    "Children discharged from HHS Care"
].sum()

backlog_days = (
    filtered_df["Backlog Indicator"] == 1
).sum()

backlog_rate = (
    backlog_days / reporting_days * 100
    if reporting_days > 0 else 0
)

discharge_ratio = (
    total_discharges / total_transfers
    if total_transfers > 0 else 0
)

volatility = filtered_df["Total System Load"].std()

# -----------------------------
# Key Performance Indicators
# -----------------------------

st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Reporting Days",
    f"{reporting_days:,}"
)

col2.metric(
    "Highest System Load",
    f"{highest_load:,.0f}"
)

col3.metric(
    "Lowest System Load",
    f"{lowest_load:,.0f}"
)

col4.metric(
    "Average System Load",
    f"{average_load:,.0f}"
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Total Transfers",
    f"{total_transfers:,.0f}"
)

col6.metric(
    "Total Discharges",
    f"{total_discharges:,.0f}"
)

col7.metric(
    "Backlog Rate",
    f"{backlog_rate:.2f}%"
)

col8.metric(
    "Discharge Offset Ratio",
    f"{discharge_ratio:.2f}"
)

st.divider()

# -----------------------------
# Key Insights
# -----------------------------

st.header("Key Insights")

highest_row = filtered_df.loc[
    filtered_df["Total System Load"].idxmax()
]

lowest_row = filtered_df.loc[
    filtered_df["Total System Load"].idxmin()
]

insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.info(
        f"**Average System Load**\n\n"
        f"{average_load:,.0f} children were recorded on average "
        f"during the selected reporting period."
    )

    st.info(
        f"**Highest System Load**\n\n"
        f"{highest_load:,.0f} children were recorded on "
        f"{highest_row['Date'].strftime('%d %B %Y')}."
    )

    st.info(
        f"**Total Transfers**\n\n"
        f"{total_transfers:,.0f} transfers out of CBP custody "
        f"were recorded during the selected period."
    )

with insight_col2:

    st.info(
        f"**Backlog Pattern**\n\n"
        f"Backlog conditions were recorded on "
        f"{backlog_days:,} of {reporting_days:,} reporting days "
        f"({backlog_rate:.2f}%)."
    )

    st.info(
        f"**Total Discharges**\n\n"
        f"{total_discharges:,.0f} children were discharged "
        f"from HHS care during the selected period."
    )

    st.info(
        f"**Load Volatility**\n\n"
        f"The standard deviation of system load was "
        f"{volatility:,.2f}."
    )

st.divider()

# -----------------------------
# System Load Overview
# -----------------------------

st.header("System Load Overview")

load_data = filtered_df[
    ["Date"] + selected_metrics
].set_index("Date")

if granularity == "Weekly":
    load_data = load_data.resample("W").mean()

elif granularity == "Monthly":
    load_data = load_data.resample("ME").mean()

st.line_chart(load_data)

# -----------------------------
# CBP and HHS Comparison
# -----------------------------

st.header("CBP Custody and HHS Care Load")

comparison = filtered_df[
    [
        "Date",
        "Children in CBP custody",
        "Children in HHS Care"
    ]
].set_index("Date")

if granularity == "Weekly":
    comparison = comparison.resample("W").mean()

elif granularity == "Monthly":
    comparison = comparison.resample("ME").mean()

st.line_chart(comparison)

# -----------------------------
# Net Intake Analysis
# -----------------------------

st.header("Net Daily Intake")

net_intake = filtered_df[
    ["Date", "Net Daily Intake"]
].set_index("Date")

if granularity == "Weekly":
    net_intake = net_intake.resample("W").sum()

elif granularity == "Monthly":
    net_intake = net_intake.resample("ME").sum()

st.line_chart(net_intake)

# -----------------------------
# Rolling Load Analysis
# -----------------------------

st.header("Rolling Care Load")

rolling_load = filtered_df[
    [
        "Date",
        "Total System Load",
        "7-Day Rolling Load",
        "14-Day Rolling Load"
    ]
].set_index("Date")

st.line_chart(rolling_load)

# -----------------------------
# Transfers and Discharges
# -----------------------------

st.header("Transfers and Discharges")

flow_data = filtered_df[
    [
        "Date",
        "Children transferred out of CBP custody",
        "Children discharged from HHS Care"
    ]
].set_index("Date")

if granularity == "Weekly":
    flow_data = flow_data.resample("W").sum()

elif granularity == "Monthly":
    flow_data = flow_data.resample("ME").sum()

st.line_chart(flow_data)

# -----------------------------
# Backlog Analysis
# -----------------------------

st.header("Backlog Indicator")

backlog_data = filtered_df[
    ["Date", "Backlog Indicator"]
].set_index("Date")

st.line_chart(backlog_data)

# -----------------------------
# Load Extremes
# -----------------------------

st.header("System Load Extremes")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Highest Recorded Load")

    st.write(
        f"**Date:** "
        f"{highest_row['Date'].strftime('%d %B %Y')}"
    )

    st.write(
        f"**Total System Load:** "
        f"{highest_row['Total System Load']:,.0f}"
    )

    st.write(
        f"**CBP Custody:** "
        f"{highest_row['Children in CBP custody']:,.0f}"
    )

    st.write(
        f"**HHS Care:** "
        f"{highest_row['Children in HHS Care']:,.0f}"
    )

with col2:

    st.subheader("Lowest Recorded Load")

    st.write(
        f"**Date:** "
        f"{lowest_row['Date'].strftime('%d %B %Y')}"
    )

    st.write(
        f"**Total System Load:** "
        f"{lowest_row['Total System Load']:,.0f}"
    )

    st.write(
        f"**CBP Custody:** "
        f"{lowest_row['Children in CBP custody']:,.0f}"
    )

    st.write(
        f"**HHS Care:** "
        f"{lowest_row['Children in HHS Care']:,.0f}"
    )

st.divider()

# -----------------------------
# Filtered Dataset
# -----------------------------

st.header("Filtered Dataset")

st.caption(
    f"Showing {len(filtered_df):,} records for the selected reporting period."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Download
# -----------------------------

st.subheader("Export Data")

st.write(
    "Download the currently filtered dataset for further analysis "
    "in Excel, Python, or other data analysis tools."
)

csv_data = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv_data,
    file_name="UAC_Filtered_Data.csv",
    mime="text/csv"
)

st.divider()

# -----------------------------
# About the Dashboard
# -----------------------------

with st.expander("About This Dashboard"):

    st.write(
        "This dashboard analyzes system capacity and care load patterns "
        "using historical operational data."
    )

    st.write(
        "**Key areas analyzed:**"
    )

    st.write(
        "- Overall system load\n"
        "- CBP custody and HHS care load\n"
        "- Net daily intake\n"
        "- Rolling care load trends\n"
        "- Transfers and discharges\n"
        "- Backlog patterns\n"
        "- High and low system load periods"
    )

    st.write(
        "**Time Granularity:** Daily, Weekly, and Monthly views "
        "are available for selected trend analyses."
    )

# -----------------------------
# Footer
# -----------------------------

st.caption(
    "System Capacity & Care Load Analytics | "
    "Data Analysis and Monitoring Dashboard"
)