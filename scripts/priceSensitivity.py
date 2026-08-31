import pandas as pd

print("loading calendar data - this file is big, might take a minute")
calendar = pd.read_csv("DataProcessed/calendar_clean.csv")
print(f"{len(calendar):,} calendar rows loaded")

# booking rate = fraction of days NOT available, as a proxy for demand.
# caveat: "not available" also includes days a host blocks off manually,
# not just actual bookings - worth a mention in the writeup, not a dealbreaker
booking_rate = calendar.groupby("listing_id")["available"].apply(lambda x: 1 - x.mean())
booking_rate = booking_rate.reset_index(name="booking_rate")
print(f"computed booking rate for {len(booking_rate)} listings")

listings = pd.read_csv("DataProcessed/master_listings.csv")
merged = listings.merge(booking_rate, on="listing_id", how="inner")
merged = merged[~merged["price_outlier"] & merged["price"].notna() & merged["review_scores_rating"].notna()]
print(f"{len(merged)} listings with price, rating, and booking data\n")

price_corr = merged["price"].corr(merged["booking_rate"])
rating_corr = merged["review_scores_rating"].corr(merged["booking_rate"])
sentiment_corr = merged["avg_sentiment"].corr(merged["booking_rate"])

print(f"correlation: price vs booking rate       = {price_corr:.3f}")
print(f"correlation: rating vs booking rate       = {rating_corr:.3f}")
print(f"correlation: sentiment vs booking rate    = {sentiment_corr:.3f}")

print("\nwhichever has the bigger absolute value is the stronger driver of actual demand")