# scripts/scrape_reviews.py

import pandas as pd
from google_play_scraper import Sort, reviews
from datetime import datetime
import os

BANK_APPS = {
    "CBE": "com.ethiopiasoftware.cbe",
    "BOA": "com.bankofabyssinia.boaapp.dev",
    "Dashen": "com.dashen.bankapp.dashenbank"
}

def fetch_reviews(app_id, bank_name, num_reviews=500):
    """
    Fetch reviews for a specific app from the Google Play Store.

    Parameters:
        app_id (str): The app's package ID on the Play Store.
        bank_name (str): The name of the bank (e.g., "CBE").
        num_reviews (int): Number of reviews to fetch.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped reviews.
    """
    print(f"[INFO] Fetching reviews for {bank_name} ({app_id})...")
    result, _ = reviews(
        app_id,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=num_reviews
    )

    data = []
    for r in result:
        data.append({
            "review": r["content"],
            "rating": r["score"],
            "date": r["at"].strftime("%Y-%m-%d"),
            "bank": bank_name,
            "source": "Google Play"
        })

    return pd.DataFrame(data)


def save_reviews(df, bank_name, out_dir="../data/raw/"):
    """
    Save the reviews DataFrame to CSV.

    Parameters:
        df (pd.DataFrame): DataFrame of reviews.
        bank_name (str): Name of the bank.
        out_dir (str): Directory to save the file.
    """
    os.makedirs(out_dir, exist_ok=True)
    file_path = os.path.join(out_dir, f"{bank_name.lower()}_reviews_raw.csv")
    df.to_csv(file_path, index=False)
    print(f"[INFO] Saved {len(df)} reviews to {file_path}")


def main():
    all_reviews = []

    for bank, app_id in BANK_APPS.items():
        df = fetch_reviews(app_id, bank)
        save_reviews(df, bank)
        all_reviews.append(df)

    combined = pd.concat(all_reviews, ignore_index=True)
    combined.to_csv("../data/raw/all_banks_reviews_raw.csv", index=False)
    print(f"[INFO] Combined dataset saved with {len(combined)} total reviews.")


if __name__ == "__main__":
    main()
