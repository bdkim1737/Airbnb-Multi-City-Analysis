import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("DataProcessed/master_listings.csv")
clean = df[
    ~df["price_outlier"]
    & df["price"].notna()
    & df["review_scores_rating"].notna()
    & df["avg_sentiment"].notna()
].copy()

print(f"using {len(clean)} listings with price, rating, and sentiment\n")

# model 1: price predicted by star rating alone
X1 = sm.add_constant(clean[["review_scores_rating"]])
model1 = sm.OLS(clean["price"], X1).fit()
print(f"price ~ star rating alone:   R-squared = {model1.rsquared:.4f}")

# model 2: price predicted by sentiment alone
X2 = sm.add_constant(clean[["avg_sentiment"]])
model2 = sm.OLS(clean["price"], X2).fit()
print(f"price ~ sentiment alone:     R-squared = {model2.rsquared:.4f}")

# model 3: both together, to see if sentiment adds anything star rating doesn't already capture
X3 = sm.add_constant(clean[["review_scores_rating", "avg_sentiment"]])
model3 = sm.OLS(clean["price"], X3).fit()
print(f"price ~ both together:       R-squared = {model3.rsquared:.4f}")
print()
print(model3.summary())