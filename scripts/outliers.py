import pandas as pd

df = pd.read_csv("DataProcessed/master_listings.csv")

print("top 15 most expensive listings:")
top = df.nlargest(15, "price")[["listing_id", "city", "price", "room_type", "accommodates", "review_scores_rating", "number_of_reviews"]]
print(top.to_string(index=False))

print("\nprice percentiles:")
print(df["price"].quantile([0.5, 0.9, 0.95, 0.99, 0.999]))

print("\nhow many listings above $1000/night?")
print((df["price"] > 1000).sum())

print("\nhow many above $2000/night?")
print((df["price"] > 2000).sum())

cutoff = df["price"].quantile(0.99)
print(f"flagging anything above ${cutoff:.2f}/night as an outlier")

df["price_outlier"] = df["price"] > cutoff
print(f"{df['price_outlier'].sum()} listings flagged out of {len(df)}")

# also worth checking - are these outliers mostly the zero-review "vacation mode" listings?
outliers = df[df["price_outlier"]]
print(f"\nof the flagged outliers, {outliers['number_of_reviews'].eq(0).sum()} have zero reviews")

df.to_csv("DataProcessed/master_listings.csv", index=False)