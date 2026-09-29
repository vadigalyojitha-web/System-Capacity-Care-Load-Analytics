#  System Capacity & Care Load Analytics

##  Project Overview

System Capacity & Care Load Analytics is a data analytics dashboard designed to analyze the care pipeline of Unaccompanied Children (UAC), from CBP custody to HHS care.

The project uses historical data to understand system load, transfers, discharges, backlog patterns, and changes in care capacity over time.

---

##  Project Objective

The main objective of this project is to:

- Analyze the overall system care load
- Identify peak and lowest system load periods
- Compare CBP custody and HHS care
- Analyze transfers and discharges
- Monitor backlog patterns
- Understand changes in system capacity
- Provide interactive data filtering
- Allow users to download filtered data

---

##  Technologies Used

- Python
- Pandas
- Streamlit
- Data Visualization
- Jupyter Notebook
- CSV Dataset

---

##  Dashboard Features

###  Interactive Filters
Users can select a specific date range to analyze a particular period.

###  Key Performance Indicators

The dashboard displays:

- Reporting Days
- Highest System Load
- Lowest System Load
- Average System Load
- Total Transfers
- Total Discharges
- Net Care Load Change
- Discharge Offset Ratio

###  Visualizations

The dashboard includes:

- System Load Trend
- Transfers vs Discharges
- CBP Custody vs HHS Care
- Backlog Analysis

###  Automated Insights

The dashboard automatically identifies:

- Peak system load
- Lowest system load
- Transfer and discharge patterns
- Capacity variation

###  Data Download

Users can download the currently filtered records as a CSV file.

---

##  Data Pipeline

```text
Raw Dataset
     ↓
Data Cleaning
     ↓
Data Analysis
     ↓
Derived Metrics
     ↓
Interactive Dashboard
     ↓
Insights & Visualizations
     ↓
Filtered Data Download
