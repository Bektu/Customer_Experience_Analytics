import pandas as pd

def load_csv(filepath):
    return pd.read_csv(filepath)

def save_csv(df, filepath):
    df.to_csv(filepath, index=False)