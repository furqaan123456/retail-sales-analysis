# Retail Sales Analysis

**Question:** Where does the business make and lose money, and what drives sales over time?

## Tools
Python (pandas, NumPy), SQL, Excel (pivot tables on `retail_sales.csv`), Power BI (optional: import the CSV and rebuild the dashboard).

## Files
- `build_project.py`: generates the dataset, runs the pandas analysis, exports the dashboard
- `retail_sales.csv`: 6,000 orders, 2022 to 2025 (sample data)
- `queries.sql`: six business questions answered in SQL
- `dashboard.html`: interactive dashboard

## Key findings
- South is the top region, with 27% of sales.
- October to December brings about a third of annual sales.
- Sales grew about 43% from 2022 to 2025.
- Orders with a 30% discount lose money overall, while undiscounted orders are the main profit source.

## Recommendation
Cap discounts at 20%, and run seasonal stock and campaigns ahead of October.

## Next steps
Replace the sample data with a real dataset (for example Superstore from Kaggle), then add customer segmentation (RFM) and a sales forecast.
