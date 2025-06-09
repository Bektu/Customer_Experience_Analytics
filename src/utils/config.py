import os

# File paths
RAW_NEWS_PATH = os.path.join("data", "raw", "news.csv")
RAW_STOCK_PATH = os.path.join("data", "raw", "stock.csv")
PROCESSED_DATA_PATH = os.path.join("data", "processed", "merged_data.csv")

# Columns
NEWS_DATE_COL = "date"
NEWS_HEADLINE_COL = "headline"
STOCK_DATE_COL = "Date"
STOCK_CLOSE_COL = "Close"