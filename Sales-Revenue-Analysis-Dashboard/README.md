# Sales & Revenue Analysis Dashboard

An interactive Streamlit dashboard for exploring sales and revenue data with KPI cards, monthly revenue trends, product/category/region analysis, filters, and CSV export.

## Features
- Load the bundled synthetic CSV dataset or upload a CSV/Excel file
- Filter by date range, region, and category
- Track total revenue, orders, units sold, and average order value
- Visualize monthly revenue, category performance, top products, and regional revenue share
- Inspect and download filtered records

## Dataset
The included `data/sales_data.csv` is synthetic and intended for educational use. It is not real company data. Uploaded files must contain these columns:
`Order_ID, Order_Date, Product, Category, Quantity, Unit_Price, Discount, Revenue, Region`

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```
Open the local URL shown in the terminal (usually http://localhost:8501).

## Run in Google Colab
```python
!pip install -r requirements.txt
!streamlit run app.py --server.port 8501
```
For an interactive browser-accessible app, use a Streamlit hosting service such as Streamlit Community Cloud after pushing this repository to GitHub.

## Project structure
```text
Sales-Revenue-Analysis-Dashboard/
├── data/
│   └── sales_data.csv
├── outputs/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
