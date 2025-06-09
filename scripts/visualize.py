# scripts/visualize.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

def plot_sentiment_distribution(df, output_path=None):
    sns.countplot(data=df, x='sentiment_label', order=['POSITIVE', 'NEGATIVE'])
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    if output_path:
        plt.savefig(output_path)
    plt.show()

def plot_rating_distribution(df, output_path=None):
    sns.countplot(data=df, x='rating', order=sorted(df['rating'].unique()))
    plt.title('Rating Distribution')
    plt.xlabel('Rating (Stars)')
    plt.ylabel('Count')
    if output_path:
        plt.savefig(output_path)
    plt.show()

def plot_wordcloud(df, text_column='review', output_path=None):
    text = " ".join(df[text_column].dropna().tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(15,7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    if output_path:
        plt.savefig(output_path)
    plt.show()

if __name__ == "__main__":
    df = pd.read_csv('../data/processed/cbe_reviews_sentiment.csv')

    plot_sentiment_distribution(df)
    plot_rating_distribution(df)
    plot_wordcloud(df)
