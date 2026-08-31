import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pathlib import Path

# Database connection
password = quote_plus("kim50253")
engine = create_engine(
    f"postgresql://postgres:{password}@localhost:5432/airbnb_analysis"
)

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "DataRaw"

cities = ["Dallas", "NYC", "Chicago"]

file_map = {
    "listings.csv": "raw_listings",
    "calendar.csv": "raw_calendar",
    "reviews.csv": "raw_reviews",
}

for filename, table_name in file_map.items():

    dfs = []

    for city in cities:
        path = DATA_DIR / city / filename

        print(f"Reading {path}")

        df = pd.read_csv(path, low_memory=False)
        df["city"] = city

        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)

    print(f"Writing {table_name} ({len(combined)} rows)")

    combined.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Successfully wrote {table_name}")

print("Done!")