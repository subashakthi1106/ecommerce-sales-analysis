# E-Commerce Sales Analysis

## Project Overview
This project analyzes an e-commerce sales dataset using Python and Pandas to identify sales patterns, product performance, customer payment preferences, and geographical sales distribution.

## Dataset
- Source: [Kaggle – E-Commerce Sales Dataset](https://www.kaggle.com/datasets/sharmajicoder/e-commerce-sales-dataset)
- Records: 10,000
- Columns: 21
- Period: January 1, 2026 – February 10, 2026

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib

## Work Performed
- Dataset inspection and data quality checks
- Missing value and duplicate checks
- Date conversion and preparation
- Sales calculation validation
- Daily sales analysis
- Category-wise sales analysis
- Top 10 product analysis
- State-wise and city-wise sales analysis
- Payment method analysis
- Discount range analysis
- Data visualization

## Key Findings
- Electronics generated the highest category sales.
- North Carolina recorded the highest state-wise sales.
- Lake Michael had the highest sales among the nine cities reviewed.
- COD had the highest order count.
- Orders in the 0–10% discount range had the highest average sales.
- The dataset contained no missing values or duplicate rows.
- The total sales calculation was validated against quantity, unit price, discount, and shipping cost.

## Project Outputs
The `analysis_output` folder contains:
- Daily sales report
- Category sales report
- Top 10 products report
- State and city sales reports
- Payment analysis
- Discount analysis
- Sales visualization charts

## How to Run
1. Install the required libraries:
   `pip install pandas numpy matplotlib`
2. Keep `amazon_sales_dataset.csv` in the project folder.
3. Run:
   `python sales_analysis.py`

## Conclusion
This project demonstrates the use of Python for data preparation, validation, exploratory analysis, business insights, and data visualization.