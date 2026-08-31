import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon", quiet=True)
sia = SentimentIntensityAnalyzer()

reviews = pd.read_csv("data/processed/reviews_clean.csv")
print(f"loaded {len(reviews)} reviews")

# some comments are blank/nan, vader just scores those as 0 which is fine
reviews["comments"] = reviews["comments"].fillna("")

def score(text):
    return sia.polarity_scores(text)["compound"]

reviews["sentiment"] = reviews["comments"].apply(score)
print(reviews["sentiment"].describe())

reviews.to_csv("data/processed/reviews_with_sentiment.csv", index=False)
print("saved reviews_with_sentiment.csv")

# roll up to listing level so we can join onto listings later
listing_sentiment = reviews.groupby("listing_id").agg(
    avg_sentiment=("sentiment", "mean"),
    review_count_check=("sentiment", "count")
).reset_index()

listing_sentiment.to_csv("data/processed/listing_sentiment_scores.csv", index=False)
print(f"saved listing_sentiment_scores.csv - {len(listing_sentiment)} listings with reviews")