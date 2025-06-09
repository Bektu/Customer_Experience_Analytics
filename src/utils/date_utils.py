import pandas as pd

def parse_dates(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column])
    return df

def normalize_date_to_day(df, date_column):
    df[date_column] = pd.to_datetime(df[date_column]).dt.date
    return df