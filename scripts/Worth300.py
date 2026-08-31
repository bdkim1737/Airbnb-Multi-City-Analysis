import pandas as pd

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[~df["price_outlier"] & df["price"].notna() & df["review_scores_rating"].notna()]

# "around $300" - use a band, not an exact match, since almost nothing is priced at exactly $300.00
band = clean[(clean["price"] >= 275) & (clean["price"] <= 325)]
print(f"{len(band)} listings priced $275-325/night\n")

# split that band into "felt worth it" (high rating) vs "didn't" (lower rating)
# using the band's own median rating as the cutoff, not an arbitrary number
cutoff = band["review_scores_rating"].median()
print(f"median rating in this price band: {cutoff}")

worth_it = band[band["review_scores_rating"] >= cutoff]
not_worth_it = band[band["review_scores_rating"] < cutoff]
print(f"'worth it' group: {len(worth_it)}, 'not worth it' group: {len(not_worth_it)}\n")

amenity_cols = [c for c in band.columns if c.startswith("has_") or c in ("pets_allowed", "self_checkin")]

print("amenity rates: worth-it group vs not-worth-it group")
for col in amenity_cols:
    worth_pct = worth_it[col].mean() * 100
    not_pct = not_worth_it[col].mean() * 100
    print(f"  {col:<20} worth-it: {worth_pct:5.1f}%   not-worth-it: {not_pct:5.1f}%   diff: {worth_pct - not_pct:+.1f}")

print("\nother characteristics compared:")
for col in ["accommodates", "bedrooms", "amenity_count", "avg_sentiment", "host_is_superhost"]:
    if col in band.columns:
        print(f"  {col}: worth-it={worth_it[col].mean():.2f}, not-worth-it={not_worth_it[col].mean():.2f}")