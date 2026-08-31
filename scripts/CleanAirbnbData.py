import pandas as pd
from pathlib import Path

raw_data = Path("DataRaw")
output_dir = Path("DataProcessed")
output_dir.mkdir(parents=True, exist_ok=True)

cities = ["Dallas", "NYC", "Chicago"]  


def load_city_files(filename: str) -> pd.DataFrame:
    dfs = []
    for city in cities:
        path = raw_data / city / filename
        print(f"  Reading {path}")
        df = pd.read_csv(path, low_memory=False)
        df["city"] = city
        dfs.append(df)
        print(f"    -> {len(df):,} rows")
    combined = pd.concat(dfs, ignore_index=True)
    print(f"  Combined: {len(combined):,} rows\n")
    return combined


def clean_listings(df: pd.DataFrame) -> pd.DataFrame:
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(r"[$,]", "", regex=True)
        .replace("nan", pd.NA)
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["host_is_superhost"] = df["host_is_superhost"] == "t"

    keep_cols = [
        "id", "city", "room_type", "property_type",
        "neighbourhood_cleansed", "neighbourhood_group_cleansed",
        "accommodates", "bedrooms", "beds", "bathrooms",
        "price", "host_is_superhost",
        "host_response_rate", "host_acceptance_rate",
        "number_of_reviews", "number_of_reviews_ltm",
        "review_scores_rating", "review_scores_accuracy",
        "review_scores_cleanliness", "review_scores_checkin",
        "review_scores_communication", "review_scores_location",
        "review_scores_value", "reviews_per_month",
        "amenities", "latitude", "longitude",
    ]

    keep_cols = [c for c in keep_cols if c in df.columns]
    missing = set(["id", "city", "price", "review_scores_rating"]) - set(keep_cols)
    if missing:
        print(f"  WARNING: expected columns missing from listings: {missing}")

    df = df[keep_cols].rename(columns={"id": "listing_id"})
    print(f"  Final shape: {df.shape}\n")
    return df


def clean_calendar(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["available"] = df["available"] == "t"

    keep_cols = ["listing_id", "city", "date", "available",
                 "minimum_nights", "maximum_nights"]
    keep_cols = [c for c in keep_cols if c in df.columns]
    df = df[keep_cols]
    print(f"  Final shape: {df.shape}\n")
    return df


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    keep_cols = ["id", "listing_id", "city", "date",
                 "reviewer_id", "reviewer_name", "comments"]
    keep_cols = [c for c in keep_cols if c in df.columns]
    df = df[keep_cols].rename(columns={"id": "review_id", "date": "review_date"})
    print(f"  Final shape: {df.shape}\n")
    return df


def main():
    listings_raw = load_city_files("listings.csv")
    listings = clean_listings(listings_raw)
    listings.to_csv(output_dir / "listings_clean.csv", index=False)

    calendar_raw = load_city_files("calendar.csv")
    calendar = clean_calendar(calendar_raw)
    calendar.to_csv(output_dir / "calendar_clean.csv", index=False)

    reviews_raw = load_city_files("reviews.csv")
    reviews = clean_reviews(reviews_raw)
    reviews.to_csv(output_dir / "reviews_clean.csv", index=False)

    print("Listings per city:")
    print(listings["city"].value_counts())
    print(f"\nNull prices: {listings['price'].isna().sum():,} / {len(listings):,}")
    print(f"Null ratings: {listings['review_scores_rating'].isna().sum():,} / {len(listings):,}")

    joinable_calendar = calendar["listing_id"].isin(listings["listing_id"]).sum()
    joinable_reviews = reviews["listing_id"].isin(listings["listing_id"]).sum()
    print(f"\nCalendar rows matching a listing: {joinable_calendar:,} / {len(calendar):,}")
    print(f"Review rows matching a listing: {joinable_reviews:,} / {len(reviews):,}")


if __name__ == "__main__":
    main()