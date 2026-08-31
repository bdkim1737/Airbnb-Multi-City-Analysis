import pandas as pd

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[~df["price_outlier"] & df["price"].notna()]

amenity_cols = [c for c in clean.columns if c.startswith("has_") or c == "pets_allowed" or c == "self_checkin"]
print(f"checking {len(amenity_cols)} amenities against price\n")

results = []
for col in amenity_cols:
    with_it = clean[clean[col]]["price"].mean()
    without_it = clean[~clean[col]]["price"].mean()
    diff = with_it - without_it
    pct_diff = (diff / without_it) * 100
    results.append((col, with_it, without_it, diff, pct_diff))

results_df = pd.DataFrame(results, columns=["amenity", "avg_price_with", "avg_price_without", "diff", "pct_diff"])
results_df = results_df.sort_values("diff", ascending=False)
print(results_df.to_string(index=False))