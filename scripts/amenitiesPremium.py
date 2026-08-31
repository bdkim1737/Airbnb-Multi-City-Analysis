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

## regression

import statsmodels.api as sm

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[~df["price_outlier"] & df["price"].notna() & df["accommodates"].notna()].copy()

amenity_cols = [c for c in clean.columns if c.startswith("has_") or c in ("pets_allowed", "self_checkin")]

# room_type and city need to be dummy-coded since they're categories, not numbers
room_dummies = pd.get_dummies(clean["room_type"], prefix="room", drop_first=True)
city_dummies = pd.get_dummies(clean["city"], prefix="city", drop_first=True)

X = pd.concat([
    clean[amenity_cols].astype(int),
    clean[["accommodates"]],
    room_dummies,
    city_dummies,
], axis=1)
X = sm.add_constant(X)
y = clean["price"]

model = sm.OLS(y, X, missing="drop").fit()
print(model.summary())

print("\namenity coefficients only, sorted by effect size:")
coefs = model.params[amenity_cols].sort_values(ascending=False)
print(coefs)