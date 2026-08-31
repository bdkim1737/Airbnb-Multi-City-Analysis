import geopandas as gpd
import pandas as pd
from pathlib import Path

raw_data = Path("DataRaw")
cities = ["Dallas", "NYC", "Chicago"]

gdfs = []
for city in cities:
    path = raw_data / city / "neighbourhoods.geojson"
    print(f"reading {path}")
    gdf = gpd.read_file(path)
    gdf["city"] = city
    gdfs.append(gdf)
    print(f"  {len(gdf)} neighbourhoods")

combined = pd.concat(gdfs, ignore_index=True)
combined = gpd.GeoDataFrame(combined, geometry="geometry")

print(f"\ntotal: {len(combined)} neighbourhoods across all cities")
print(combined.columns.tolist())

# save as one combined geojson - tableau can read this directly for a map
combined.to_file("DataProcessed/neighbourhoods_combined.geojson", driver="GeoJSON")
print("saved neighbourhoods_combined.geojson")

# quick check - do the neighbourhood names in here actually match
# neighbourhood_cleansed in the listings data? if not, joins in tableau
# won't work right
listings = pd.read_csv("DataProcessed/listings_with_amenities.csv")

for city in cities:
    geo_names = set(combined[combined["city"] == city]["neighbourhood"])
    listing_names = set(listings[listings["city"] == city]["neighbourhood_cleansed"])
    overlap = geo_names & listing_names
    print(f"\n{city}: {len(geo_names)} geojson names, {len(listing_names)} listing names, {len(overlap)} match")
    only_in_geo = geo_names - listing_names
    if only_in_geo:
        print(f"  in geojson but not listings (first 5): {list(only_in_geo)[:5]}")