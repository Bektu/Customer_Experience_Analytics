# scripts/thematic_analysis.py

import pandas as pd
import os
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

CLEAN_DATA_PATH = "../data/clean/all_banks_reviews_clean.csv"

def load_clean_data(path=CLEAN_DATA_PATH):
    """
    Load cleaned reviews CSV.

    Returns:
        pd.DataFrame: DataFrame containing cleaned reviews.
    """
    print(f"[INFO] Loading cleaned reviews from {path}")
    return pd.read_csv(path)

def preprocess_text_for_lda(texts):
    """
    Preprocess text data for LDA (basic tokenization and filtering).

    Parameters:
        texts (list of str): List of cleaned review texts.

    Returns:
        list of str: Preprocessed text suitable for vectorization.
    """
    # Here you could add more preprocessing if needed
    processed = []
    for text in texts:
        # remove any non-alphabetic chars if needed (already cleaned in preprocess)
        tokens = re.findall(r'\b[a-z]{3,}\b', text.lower())
        processed.append(' '.join(tokens))
    return processed

def extract_themes(df, text_column='clean_review', n_topics=5, n_top_words=10):
    """
    Extract themes (topics) from reviews using LDA.

    Parameters:
        df (pd.DataFrame): DataFrame containing cleaned review texts.
        text_column (str): Column name with text to analyze.
        n_topics (int): Number of topics to extract.
        n_top_words (int): Number of words per topic to display.

    Returns:
        list of dict: Each dict contains 'topic' and 'words'.
    """
    print("[INFO] Preprocessing text for LDA...")
    texts = preprocess_text_for_lda(df[text_column].dropna().tolist())

    print("[INFO] Vectorizing text...")
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    dtm = vectorizer.fit_transform(texts)

    print(f"[INFO] Fitting LDA model with {n_topics} topics...")
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(dtm)

    feature_names = vectorizer.get_feature_names_out()
    themes = []
    for idx, topic in enumerate(lda.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
        themes.append({"topic": idx + 1, "words": top_words})

    return themes

def main():
    df = load_clean_data()
    themes = extract_themes(df)
    for theme in themes:
        print(f"Topic {theme['topic']}: {', '.join(theme['words'])}")

if __name__ == "__main__":
    main()
