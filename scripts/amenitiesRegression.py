import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[~df["price_outlier"] & df["price"].notna() & df["accommodates"].notna()].copy()

amenity_cols = [c for c in clean.columns if c.startswith("has_") or c in ("pets_allowed", "self_checkin")]

# room_type and city need to be dummy-coded since they're categories, not numbers
room_dummies = pd.get_dummies(clean["room_type"], prefix="room", drop_first=True).astype(int)
city_dummies = pd.get_dummies(clean["city"], prefix="city", drop_first=True).astype(int)

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