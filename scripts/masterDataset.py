import pandas as pd

listings = pd.read_csv("DataProcessed/listings_with_amenities.csv")
sentiment = pd.read_csv("DataProcessed/listing_sentiment_scores.csv")

print(f"listings: {len(listings)} rows")
print(f"sentiment: {len(sentiment)} rows")

master = listings.merge(sentiment, on="listing_id", how="left")

print(f"master: {len(master)} rows after merge")
print(f"listings missing sentiment (no reviews): {master['avg_sentiment'].isna().sum()}")

# a couple derived columns that'll make the analysis questions easier later
master["price_per_person"] = master["price"] / master["accommodates"]

# value score - how good the reviews are relative to the price, within each city
# (z-score so dallas/nyc/chicago price scales don't distort it)
master["price_z"] = master.groupby("city")["price"].transform(lambda x: (x - x.mean()) / x.std())
master["rating_z"] = master.groupby("city")["review_scores_rating"].transform(lambda x: (x - x.mean()) / x.std())
master["value_score"] = master["rating_z"] - master["price_z"]

master.to_csv("DataProcessed/master_listings.csv", index=False)
print(master[["price", "review_scores_rating", "avg_sentiment", "value_score"]].describe())