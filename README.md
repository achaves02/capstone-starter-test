# capstone-starter-test

## Sales dashboard

A Streamlit dashboard that reads `data/sales.csv` and provides filters, KPIs, charts, and a data download.

Run locally (macOS / zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app shows:
- Filters for date, region, category, and ship mode
- KPIs: total sales, orders, average order value
- Charts: sales over time, sales by region, top products, sales by category
- Table view and CSV download of filtered data