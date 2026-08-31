import ast
import pandas as pd
from pathlib import Path
from collections import Counter

df = pd.read_csv("data/listings_clean.csv")
print(f"loaded {len(df)} listings")

# amenities column is a string that looks like a list, e.g. "['Wifi', 'Kitchen']"
# ast.literal_eval turns it back into an actual list
def parse_amenities(raw):
    if pd.isna(raw) or raw == "":
        return []
    try:
        return [str(a).strip() for a in ast.literal_eval(raw)]
    except:
        return []

df["amenities_list"] = df["amenities"].apply(parse_amenities)
df["amenity_count"] = df["amenities_list"].apply(len)

# check what's actually in there before hardcoding anything
all_amenities = Counter(a for lst in df["amenities_list"] for a in lst)
print("\ntop amenities:")
for name, count in all_amenities.most_common(30):
    print(f"{name} - {count} ({count/len(df)*100:.1f}%)")

# flags for the stuff that probably matters for pricing
# might need to tweak these once i see the real list above
flags = {
    "has_wifi": "wifi",
    "has_kitchen": "kitchen",
    "has_ac": "air conditioning",
    "has_heating": "heating",
    "has_washer": "washer",
    "has_dryer": "dryer",
    "has_parking": "free parking",
    "has_pool": "pool",
    "has_hot_tub": "hot tub",
    "has_gym": "gym",
    "has_workspace": "workspace",
    "has_tv": "tv",
    "pets_allowed": "pets allowed",
    "self_checkin": "self check-in",
}

for col, kw in flags.items():
    df[col] = df["amenities_list"].apply(lambda lst: any(kw in a.lower() for a in lst))
    print(f"{col}: {df[col].mean()*100:.1f}%")

df = df.drop(columns=["amenities", "amenities_list"])
df.to_csv("DataProcessed/listings_with_amenities.csv", index=False)
print(f"\nsaved, shape is {df.shape}")