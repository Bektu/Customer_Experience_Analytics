# scripts/sentiment_analysis.py

import pandas as pd
import os
from transformers import pipeline
from script.preprocess import preprocess_reviews_df

CLEAN_DATA_PATH = "../data/clean/all_banks_reviews_clean.csv"
SENTIMENT_OUTPUT_PATH = "../data/processed/reviews_with_sentiment.csv"

def load_clean_data(path=CLEAN_DATA_PATH):
    """
    Load cleaned reviews CSV.

    Returns:
        pd.DataFrame: DataFrame containing cleaned reviews.
    """
    print(f"[INFO] Loading cleaned reviews from {path}")
    return pd.read_csv(path)

def run_sentiment_analysis(df, text_column="clean_review"):
    """
    Apply sentiment analysis to a DataFrame.

    Parameters:
        df (pd.DataFrame): DataFrame with cleaned reviews.
        text_column (str): Column name containing text for sentiment.

    Returns:
        pd.DataFrame: Original DataFrame with sentiment columns added.
    """
    print("[INFO] Initializing sentiment pipeline...")
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    print("[INFO] Running sentiment prediction...")
    sentiments = classifier(df[text_column].tolist(), truncation=True)

    df["sentiment_label"] = [s["label"] for s in sentiments]
    df["sentiment_score"] = [s["score"] for s in sentiments]

    return df

def save_with_sentiment(df, path=SENTIMENT_OUTPUT_PATH):
    """
    Save DataFrame with sentiment columns.

    Parameters:
        df (pd.DataFrame): DataFrame with sentiment results.
        path (str): Output CSV path.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"[INFO] Saved sentiment-enriched reviews to {path}")

def main():
    df = load_clean_data()
    df = run_sentiment_analysis(df)
    save_with_sentiment(df)

if __name__ == "__main__":
    main()
