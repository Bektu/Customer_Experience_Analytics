# script/preprocess.py

import pandas as pd
import re

def preprocess_reviews_df(df):
    """
    Clean review texts in a DataFrame.
    Args:
        df (pd.DataFrame): Raw reviews DataFrame with 'review' column.
    Returns:
        pd.DataFrame: Cleaned DataFrame with 'clean_review' column added.
    """
    print("[INFO] Preprocessing reviews...")
    df = df.copy()

    # Drop rows with missing reviews
    df.dropna(subset=['review'], inplace=True)

    def clean_text(text):
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"[^A-Za-z0-9\s]", "", text)
        text = text.lower().strip()
        return text

    df["clean_review"] = df["review"].apply(clean_text)
    return df
