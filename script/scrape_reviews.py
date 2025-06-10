# scripts/scrape_reviews.py

import os
import pandas as pd
from google_play_scraper import reviews, Sort

BANK_APPS = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "Dashen": "com.dashen.dashensuperapp",
}

RAW_DATA_DIR = "../data/raw/"

def fetch_reviews(app_id, bank_name, count=400):
    print(f"[INFO] Fetching reviews for {bank_name} ({app_id})...")
    result, _ = reviews(
        app_id,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=count
    )

    if not result:
        print(f"[WARNING] No reviews found for {bank_name} ({app_id}).")
        return pd.DataFrame()

    print(f"[DEBUG] Sample review keys: {list(result[0].keys())}")
    df = pd.DataFrame(result)
    df["bank"] = bank_name

    print(f"[DEBUG] DataFrame columns: {df.columns.tolist()}")

    expected_cols = ["userName", "content", "score", "at", "bank"]
    missing_cols = [col for col in expected_cols if col not in df.columns]

    if missing_cols:
        print(f"[ERROR] Missing expected columns for {bank_name}: {missing_cols}")
        # You can choose to handle missing columns differently
        # For now, return empty DataFrame to avoid errors
        return pd.DataFrame()

    return df[expected_cols].rename(columns={
        "content": "review",
        "score": "rating",
        "at": "date"
    })

def scrape_all_reviews():
    all_reviews = []
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)

    for bank, app_id in BANK_APPS.items():
        df = fetch_reviews(app_id, bank)
        if not df.empty:
            save_path = os.path.join(RAW_DATA_DIR, f"{bank.lower()}_reviews_raw.csv")
            df.to_csv(save_path, index=False)
            print(f"[INFO] Saved {len(df)} reviews to {save_path}")
            all_reviews.append(df)
        else:
            print(f"[WARNING] No reviews fetched for {bank}")

    if all_reviews:
        combined_df = pd.concat(all_reviews, ignore_index=True)
        combined_save_path = os.path.join(RAW_DATA_DIR, "combined_reviews_raw.csv")
        combined_df.to_csv(combined_save_path, index=False)
        print(f"[INFO] Combined dataset saved with {len(combined_df)} total reviews.")
        return combined_df
    else:
        print("[ERROR] No reviews fetched for any bank.")
        return pd.DataFrame()
