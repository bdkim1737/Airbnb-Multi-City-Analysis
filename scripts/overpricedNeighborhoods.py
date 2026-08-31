import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[
    ~df["price_outlier"]
    & df["price"].notna()
    & df["accommodates"].notna()
    & df["review_scores_rating"].notna()
].copy()

print(f"using {len(clean)} listings\n")

# quick sanity check on that Port Morris outlier from Q3 before trusting neighborhood averages
port_morris = clean[clean["neighbourhood_cleansed"] == "Port Morris"]
print("Port Morris listings (checking if this is a few extreme outliers):")
print(port_morris[["price", "review_scores_rating", "value_score"]].sort_values("price"))
print()

# predict price from what the listing actually offers - if a neighborhood's
# real prices run way above what the model predicts, that's "overpriced"
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

print(f"model R-squared: {model.rsquared:.3f}\n")

# now look at where actual price runs consistently above what features justify
print("most overpriced neighborhoods (min 10 listings):")
for city in clean["city"].unique():
    sub = clean[clean["city"] == city]
    grouped = sub.groupby("neighbourhood_cleansed")["price_residual"].agg(["mean", "count"])
    grouped = grouped[grouped["count"] >= 10].sort_values("mean", ascending=False)
    print(f"\n{city}:")
    print(grouped.head(5))

print("\nbest bang-for-buck neighborhoods (most underpriced relative to features):")
for city in clean["city"].unique():
    sub = clean[clean["city"] == city]
    grouped = sub.groupby("neighbourhood_cleansed")["price_residual"].agg(["mean", "count"])
    grouped = grouped[grouped["count"] >= 10].sort_values("mean")
    print(f"\n{city}:")
    print(grouped.head(5))