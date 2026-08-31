import pandas as pd
from scipy.stats import f_oneway

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[~df["price_outlier"] & df["value_score"].notna()]

print(f"using {len(clean)} listings with a valid value_score\n")

# does neighborhood actually explain differences in value_score, or is it
# basically random which neighborhood a good/bad deal shows up in?
for city in clean["city"].unique():
    sub = clean[clean["city"] == city]
    groups = [g["value_score"].values for _, g in sub.groupby("neighbourhood_cleansed") if len(g) >= 10]
    f_stat, p = f_oneway(*groups)
    print(f"{city}: ANOVA across {len(groups)} neighborhoods (min 10 listings each), F={f_stat:.2f}, p={p:.4f}")

print("\nbest value neighborhoods (top 5 per city, min 10 listings):")
for city in clean["city"].unique():
    sub = clean[clean["city"] == city]
    grouped = sub.groupby("neighbourhood_cleansed")["value_score"].agg(["mean", "count"])
    grouped = grouped[grouped["count"] >= 10].sort_values("mean", ascending=False)
    print(f"\n{city}:")
    print(grouped.head(5))

print("\nworst value neighborhoods (bottom 5 per city, min 10 listings):")
for city in clean["city"].unique():
    sub = clean[clean["city"] == city]
    grouped = sub.groupby("neighbourhood_cleansed")["value_score"].agg(["mean", "count"])
    grouped = grouped[grouped["count"] >= 10].sort_values("mean")
    print(f"\n{city}:")
    print(grouped.head(5))