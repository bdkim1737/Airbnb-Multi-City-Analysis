import pandas as pd
from scipy.stats import pearsonr

df = pd.read_csv("DataProcessed/master_listings.csv")

# drop outliers and anything without a rating or price - can't correlate against a blank
clean = df[~df["price_outlier"] & df["review_scores_rating"].notna() & df["price"].notna()]
print(f"using {len(clean)} listings after dropping outliers and unrated listings")

# overall correlation, all cities pooled
r, p = pearsonr(clean["price"], clean["review_scores_rating"])
print(f"\noverall correlation between price and rating: r={r:.3f}, p={p:.4f}")

# now break it out by city - pooling everything together can hide city-specific patterns
print("\nby city:")
for city in clean["city"].unique():
    sub = clean[clean["city"] == city]
    r, p = pearsonr(sub["price"], sub["review_scores_rating"])
    print(f"  {city}: r={r:.3f}, p={p:.4f}, n={len(sub)}")

# also worth checking price quartiles vs avg rating - correlation assumes
# a linear relationship, this checks if it's more like "good enough" plateaus
print("\navg rating by price quartile:")
clean["price_quartile"] = pd.qcut(clean["price"], 4, labels=["Q1 (cheapest)", "Q2", "Q3", "Q4 (priciest)"])
print(clean.groupby("price_quartile")["review_scores_rating"].mean())