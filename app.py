import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="India Air Quality Analytics",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA = Path(__file__).parent / "data" / "india_air_quality_12042_rows.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA, parse_dates=["Date"])
    return df

def category(aqi):
    if pd.isna(aqi): return "Unknown"
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Satisfactory"
    if aqi <= 200: return "Moderate"
    if aqi <= 300: return "Poor"
    if aqi <= 400: return "Very Poor"
    return "Severe"

df = load_data()

st.markdown("""
<style>
.main-title {font-size: 2.4rem; font-weight: 700; margin-bottom: 0;}
.subtitle {font-size: 1rem; opacity: .75; margin-bottom: 1.2rem;}
.kpi {padding: 1rem; border-radius: 14px; border: 1px solid rgba(128,128,128,.25);}
.small {font-size:.82rem; opacity:.7;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌫️ India Air Quality Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Interactive analysis of AQI and estimated pollutant levels for five major Indian cities.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Filters")
    cities = st.multiselect("City", sorted(df["City"].unique()), default=sorted(df["City"].unique()))
    min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
    date_range = st.date_input("Date range", [min_date, max_date], min_value=min_date, max_value=max_date)
    cats = st.multiselect(
        "AQI category",
        ["Good","Satisfactory","Moderate","Poor","Very Poor","Severe"],
        default=["Good","Satisfactory","Moderate","Poor","Very Poor","Severe"]
    )

if len(date_range) != 2:
    st.warning("Please select a start and end date.")
    st.stop()

f = df[
    df["City"].isin(cities) &
    (df["Date"].dt.date >= date_range[0]) &
    (df["Date"].dt.date <= date_range[1]) &
    (df["AQI_Category"].isin(cats))
].copy()

if f.empty:
    st.error("No records match the selected filters.")
    st.stop()

avg_aqi = f["AQI"].mean()
high_aqi_days = int((f["AQI"] > 200).sum())
avg_pm25 = f["PM2.5"].mean()
cities_count = f["City"].nunique()

c1,c2,c3,c4 = st.columns(4)
for col, title, value in [
    (c1,"Average AQI",f"{avg_aqi:.1f}"),
    (c2,"High-AQI Records (>200)",f"{high_aqi_days:,}"),
    (c3,"Average PM2.5",f"{avg_pm25:.1f}"),
    (c4,"Cities Covered",f"{cities_count}")
]:
    with col:
        st.markdown(f'<div class="kpi"><div class="small">{title}</div><h2>{value}</h2></div>', unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview","City Analysis","Time Trends","Pollutants","Data Quality"
])

with tab1:
    st.subheader("AQI Category Distribution")
    counts = f["AQI_Category"].value_counts().reindex(
        ["Good","Satisfactory","Moderate","Poor","Very Poor","Severe"], fill_value=0
    )
    fig, ax = plt.subplots()
    counts.plot.bar(ax=ax)
    ax.set_xlabel("AQI Category")
    ax.set_ylabel("Records")
    ax.tick_params(axis="x", rotation=30)
    st.pyplot(fig, clear_figure=True)

    st.subheader("Key observations")
    top_city = f.groupby("City")["AQI"].mean().sort_values(ascending=False)
    worst = top_city.index[0]
    best = top_city.index[-1]
    peak_month = f.assign(Month=f["Date"].dt.month).groupby("Month")["AQI"].mean().idxmax()
    st.info(
        f"Within the selected filters, **{worst}** has the highest average AQI "
        f"({top_city.iloc[0]:.1f}), while **{best}** has the lowest ({top_city.iloc[-1]:.1f}). "
        f"The highest average AQI month in the selection is month **{peak_month}**."
    )

with tab2:
    st.subheader("City Comparison")
    city = f.groupby("City").agg(
        Records=("AQI","count"),
        Average_AQI=("AQI","mean"),
        Median_AQI=("AQI","median"),
        Max_AQI=("AQI","max"),
        Average_PM25=("PM2.5","mean")
    ).reset_index().sort_values("Average_AQI", ascending=False)
    st.dataframe(city.style.format({"Average_AQI":"{:.1f}","Median_AQI":"{:.1f}","Max_AQI":"{:.1f}","Average_PM25":"{:.1f}"}), use_container_width=True)
    fig, ax = plt.subplots()
    city.sort_values("Average_AQI").plot.barh(x="City", y="Average_AQI", ax=ax, legend=False)
    ax.set_xlabel("Average AQI")
    ax.set_ylabel("City")
    st.pyplot(fig, clear_figure=True)

with tab3:
    st.subheader("Monthly and Annual Trends")
    monthly = f.assign(Month=f["Date"].dt.month).groupby("Month")["AQI"].mean()
    fig, ax = plt.subplots()
    ax.plot(monthly.index, monthly.values, marker="o")
    ax.set_xlabel("Month")
    ax.set_ylabel("Average AQI")
    ax.set_xticks(range(1,13))
    st.pyplot(fig, clear_figure=True)

    annual = f.assign(Year=f["Date"].dt.year).groupby("Year")["AQI"].mean()
    fig, ax = plt.subplots()
    ax.plot(annual.index, annual.values, marker="o")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average AQI")
    st.pyplot(fig, clear_figure=True)

with tab4:
    st.subheader("Estimated Pollutant Levels")
    pollutants = ["PM2.5","PM10","NO2","SO2","CO","O3"]
    p = f[pollutants].mean().sort_values(ascending=True)
    fig, ax = plt.subplots()
    p.plot.barh(ax=ax)
    ax.set_xlabel("Average Level (dataset units)")
    st.pyplot(fig, clear_figure=True)

    st.subheader("AQI vs Pollutants")
    corr = f[["AQI"] + pollutants].corr()["AQI"].sort_values(ascending=False).to_frame("Correlation with AQI")
    st.dataframe(corr.style.format("{:.3f}"), use_container_width=True)
    st.caption("Important: the supplied dataset README states that pollutant concentrations are mathematically estimated from AQI relationships, so these correlations should not be interpreted as independent causal evidence.")

with tab5:
    st.subheader("Data Quality Checks")
    numeric = ["AQI","PM2.5","PM10","NO2","SO2","CO","O3"]
    checks = pd.DataFrame({
        "Check": [
            "Rows after combining five city files",
            "Duplicate rows",
            "Missing AQI values after treatment",
            "Negative pollutant/AQI values",
            "Invalid dates",
            "Original missing AQI values"
        ],
        "Result": [
            len(f),
            int(f.duplicated().sum()),
            int(f["AQI"].isna().sum()),
            int((f[numeric] < 0).sum().sum()),
            int(f["Date"].isna().sum()),
            int(f["AQI_Missing_Original"].sum())
        ]
    })
    st.dataframe(checks, use_container_width=True)
    st.subheader("Data Preview")
    st.dataframe(f.head(100), use_container_width=True)
    st.download_button(
        "Download filtered data as CSV",
        f.to_csv(index=False).encode("utf-8"),
        "filtered_air_quality.csv",
        "text/csv"
    )

st.divider()
st.caption("Project by Satyam Pratap | Python • Pandas • Matplotlib • Streamlit")
