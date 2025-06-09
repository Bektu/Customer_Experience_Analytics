# scripts/preprocess_reviews.py

import pandas as pd
import os
import re
from datetime import datetime

RAW_DATA_PATH = "../data/raw/all_banks_reviews_raw.csv"
CLEAN_DATA_DIR = "../data/clean/"
CLEAN_DATA_PATH = os.path.join(CLEAN_DATA_DIR, "all_banks_reviews_clean.csv")

def clean_text(text):
    """
    Basic cleaning for review text.

    Parameters:
        text (str): Raw review text.

    Returns:
        str: Cleaned review text.
    """
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-z\s]", "", text)  # Remove non-alphabetic characters
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra whitespace
    return text

def preprocess_reviews(input_path=RAW_DATA_PATH, output_path=CLEAN_DATA_PATH):
    """
    Load, clean, and save preprocessed review data.

    Parameters:
        input_path (str): Path to raw data CSV.
        output_path (str): Path to save clean data CSV.
    """
    print(f"[INFO] Loading raw reviews from {input_path}")
    df = pd.read_csv(input_path)

    # Drop missing or empty reviews
    df.dropna(subset=["review", "rating", "date", "bank"], inplace=True)
    df = df[df["review"].str.strip().astype(bool)]

    # Convert date to consistent format
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    # Clean text
    print("[INFO] Cleaning review text...")
    df["clean_review"] = df["review"].apply(clean_text)

    # Drop duplicates
    df.drop_duplicates(subset=["clean_review", "rating", "date", "bank"], inplace=True)

    # Save cleaned data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[INFO] Saved cleaned data with {len(df)} reviews to {output_path}")

def main():
    preprocess_reviews()

if __name__ == "__main__":
    main()
