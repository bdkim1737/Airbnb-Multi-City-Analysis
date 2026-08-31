# Airbnb Multi-City Analysis

What actually makes an Airbnb worth its price? I pulled listings, calendar, and review data for **Dallas, NYC, and Chicago** from Inside Airbnb to find out — and to build something that touches SQL, Python, and Tableau end to end instead of just one of them.

## The questions I'm answering

1. Does a higher price actually lead to higher guest satisfaction?
2. What amenities justify a premium?
3. How much does location affect perceived value?
4. Which neighborhoods are overpriced?
5. Which city gives travelers the most value?
6. What makes a $300/night listing feel worth it?
7. Are guests more sensitive to price or to review quality?
8. Does review sentiment explain pricing better than star ratings?

## What I've found so far

**Price barely predicts satisfaction.** Across all three cities the correlation between price and guest rating is real (p < 0.001) but tiny — r = 0.06 to 0.11, meaning price explains roughly 1% of the variation in how happy guests are. Paying more gets you a slightly better-rated stay, not a meaningfully better one. Whatever actually drives satisfaction, it isn't the price tag.

**Naive amenity comparisons lie to you.** A straight average-price comparison said kitchens *lower* your price by ~17%. That's backwards — it's a confound. Most home listings have kitchens, so the "no kitchen" group is mostly hotel rooms, which charge more for reasons that have nothing to do with kitchens. Controlling for room type, city, and listing size in a regression is what actually isolates each amenity's real effect. (Full results landing here once the regression run is done.)

**A quarter of the data has no price or rating at all**, which turned out to be a real pattern, not a bug — mostly inactive or brand-new listings with zero bookings. And about 0.75% of listings are priced absurdly high ($10k+/night) with no reviews to match, consistent with hosts using extreme pricing to quietly delist without deactivating. Both got flagged rather than deleted, so the choice of whether to include them lives in each analysis, not baked into the dataset.

## Stack

- **Python** — pandas, statsmodels, scipy, nltk (VADER sentiment), geopandas
- **Tableau** — final dashboard
- **PostgreSQL** — where this started (see note below)

## Pipeline

```
scripts/
├── clean_airbnb_data.py        combines all 3 cities, fixes price/boolean formatting, drops dead columns
├── parse_amenities.py          amenities text -> boolean flags (has_wifi, has_pool, etc.) + count
├── score_sentiment.py          VADER sentiment on every review, rolled up to listing level
├── combine_neighbourhoods.py   merges neighborhood boundary shapes across cities
├── build_master_dataset.py     joins everything, adds price_per_person + a city-relative value_score
├── flag_outliers.py            flags (doesn't delete) listings priced above the 99th percentile
├── q1_price_vs_satisfaction.py
├── q2_amenities_premium.py
└── q2b_amenities_regression.py
```

Run them in that order. Each one prints its own sanity checks (row counts, null rates, join match rates) so you can see the pipeline actually working, not just trust that it did.

## Data

Pulled from [Inside Airbnb](http://insideairbnb.com/get-the-data/) — `listings.csv`, `calendar.csv`, `reviews.csv`, and `neighbourhoods.geojson` for each city.

The full processed files aren't in this repo — the NYC calendar file alone cleans in at ~700MB, well past what GitHub allows. `data/sample/` has a small slice of each cleaned file so you can see the actual schema without downloading anything. To run the full pipeline yourself: grab the source files from Inside Airbnb, drop them in `DataRaw/<City>/`, and run the scripts above in order.

## A quick note on process

This started as a Postgres + SQL project — you'll see some SQL in the early commit history. Partway through I moved the cleaning and analysis into Python for speed and to keep everything in one place. I'd rather show the real path a project like this actually takes than pretend it was a straight line.

## What's left

- [ ] Questions 3 through 8
- [ ] Tableau dashboard
- [ ] Final write-up of results

## Author

Ben Kim