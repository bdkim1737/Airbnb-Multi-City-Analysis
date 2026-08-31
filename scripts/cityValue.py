import pandas as pd
from scipy.stats import f_oneway

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[~df["price_outlier"] & df["value_score"].notna()]

print("value_score by city:")
print(clean.groupby("city")["value_score"].agg(["mean", "median", "std", "count"]))

groups = [g["value_score"].values for _, g in clean.groupby("city")]
f_stat, p = f_oneway(*groups)
print(f"\nANOVA across cities: F={f_stat:.2f}, p={p:.4f}")

# value_score is already z-scored within each city, so a "which city wins"
# comparison needs raw price/rating instead - value_score by design averages
# near 0 within each city and can't tell you which city is the best deal overall
print("\nraw price and rating by city (value_score can't answer this by itself):")
print(clean.groupby("city")[["price", "review_scores_rating"]].mean())

# price per person is a fairer cross-city comparison than raw price
print("\nprice per person by city:")
print(clean.groupby("city")["price_per_person"].mean())