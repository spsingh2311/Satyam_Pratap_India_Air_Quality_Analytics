# India Air Quality Analytics Dashboard

**Submitted by:** Satyam Pratap

## Project Overview
This project analyzes daily Air Quality Index (AQI) records for Bangalore, Chennai, Delhi, Hyderabad and Mumbai. The supplied dataset contains **12,042 combined records** covering **2018-01-01 to 2024-12-31**.

The project follows a real-world data analytics workflow:
1. Collect and load CSV data
2. Clean and validate the data
3. Handle the single missing AQI value transparently
4. Classify AQI into six analytical categories
5. Group and summarize city, time and pollutant data
6. Create charts
7. Generate observations and practical recommendations
8. Present the results in an interactive Streamlit dashboard

## Important Data Note
The dataset README says AQI values are sourced from CPCB and pollutant concentrations are mathematically estimated using AQI-to-pollutant relationships. Therefore, pollutant values are **estimated rather than direct independent monitoring measurements**. This project does not treat them as causal evidence.

## Main Findings from the Supplied Data
- Combined records: 12,042
- Average AQI: 107.58
- Maximum AQI: 494
- City with highest average AQI: Delhi (208.29)
- City with lowest average AQI: Bangalore (74.32)
- Highest-average month: 1
- Lowest-average month: 8

## Run
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Windows users can double-click `run_app.bat`.

## Project Files
- `app.py` - Streamlit dashboard
- `analysis.py` - reusable analysis/validation code
- `data/raw/` - original supplied city CSVs
- `data/india_air_quality_12042_rows.csv` - combined analysis dataset
- `report_images/` - generated charts
- `Project_Report.docx` - submission report
- `requirements.txt` - Python dependencies
