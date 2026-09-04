import pandas as pd

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[~df["price_outlier"] & df["price"].notna() & df["review_scores_rating"].notna()]

print(clean["price"].quantile([0.25, 0.5, 0.75]))