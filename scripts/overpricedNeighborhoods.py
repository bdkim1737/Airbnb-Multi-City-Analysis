import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[
    ~df["price_outlier"]
    & df["price"].notna()
    & df["accommodates"].notna()
    & df["review_scores_rating"].notna()
].copy()

print(f"using {len(clean)} listings")

room_dummies = pd.get_dummies(clean["room_type"], prefix="room", drop_first=True).astype(int)
city_dummies = pd.get_dummies(clean["city"], prefix="city", drop_first=True).astype(int)

X = pd.concat([
    clean[["accommodates", "bedrooms", "bathrooms", "review_scores_rating"]].fillna(0),
    room_dummies,
    city_dummies,
], axis=1)
X = sm.add_constant(X)
y = clean["price"]

model = sm.OLS(y, X, missing="drop").fit()
clean["predicted_price"] = model.predict(X)
clean["price_residual"] = clean["price"] - clean["predicted_price"]

print(f"model R-squared: {model.rsquared:.3f}")

# just the columns tableau actually needs to join and map this
out = clean[["listing_id", "city", "neighbourhood_cleansed", "price", "predicted_price", "price_residual"]]
out.to_csv("DataProcessed/listing_price_residuals.csv", index=False)
print(f"saved listing_price_residuals.csv, {len(out)} rows")

# also a neighborhood-level rollup, since that's what you'll actually color the map by
neighborhood_rollup = clean.groupby(["city", "neighbourhood_cleansed"]).agg(
    avg_price_residual=("price_residual", "mean"),
    listing_count=("price_residual", "count")
).reset_index()
neighborhood_rollup = neighborhood_rollup[neighborhood_rollup["listing_count"] >= 10]

neighborhood_rollup.to_csv("DataProcessed/neighborhood_price_residuals.csv", index=False)
print(f"saved neighborhood_price_residuals.csv, {len(neighborhood_rollup)} neighborhoods (min 10 listings each)")