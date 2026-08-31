# Airbnb Multi-City Analysis

What actually makes an Airbnb worth its price? To find out, I pulled listing, calendar, and review data for **Dallas, NYC, and Chicago** from Inside Airbnb.

## Questions I'm Exploring

1. Does a higher price point actually lead to higher guest satisfaction?
2. Which specific amenities justify a premium?
3. How much does location drive perceived value?
4. Which neighborhoods are statistically overpriced?
5. Which city offers travelers the most bang for their buck?
6. What makes a $300/night listing feel like it's actually worth it?
7. Are guests more sensitive to the price or the quality of reviews?
8. Does review sentiment predict pricing better than standard star ratings?

## Key Findings

**Price is a poor predictor of satisfaction.** Across all three cities, the correlation between price and guest ratings is statistically real (p < 0.001) but incredibly small (r = 0.06 to 0.11). Price only explains about 1% of the variation in guest happiness. You might get a slightly higher-rated stay by paying more, but not a meaningfully better one.

**Amenities that actually justify a premium: gym, washer, TV, hot tub, and AC.** A regression controlling for room type, city, and listing size (R² = 0.35) isolated each amenity's real effect. Gym access adds the biggest premium (+$68.76/night), followed by an in-unit washer (+$36.30), TV (+$34.10), hot tub (+$33.62), and AC (+$31.39) — all highly significant. Wifi, by contrast, added almost nothing (+$1.31, not statistically significant) — it's such a baseline expectation now that having it doesn't distinguish a listing. One genuine puzzle: kitchens showed up with a *negative* price association (-$88.61) even after controlling for room type. My working theory is that "Entire home/apt" listings without a full kitchen skew toward professionally-managed, hotel-like serviced apartments that charge a premium for amenities this model doesn't capture — a good candidate for a follow-up with `property_type` added as a control.

**Location is a real, statistically significant driver of perceived value** (ANOVA p < 0.0001 in all three cities) — and the pattern is consistent: NYC's most "overpriced" neighborhoods relative to what their listings' features justify are Tribeca (+$225/night), Greenwich Village, SoHo, and the Financial District; Chicago's Loop and Near North Side show the same thing. Meanwhile the best-value neighborhoods are almost entirely outer-borough spots most tourists have never heard of — Throgs Neck, Coney Island, Jamaica Estates. The takeaway: in famous neighborhoods, you're largely paying for the name, not for a measurably better stay.

**Dallas gives travelers the most value overall.** Guest ratings are nearly identical across all three cities (4.72–4.79), but price-per-person tells a different story: Dallas averages $54.88/person versus Chicago's $65.36 and NYC's $83.06 — over 50% more expensive in NYC for essentially the same satisfaction.

**At the $300/night price point, superhost status is the single biggest differentiator** between a listing that feels worth it and one that doesn't — 59% of "worth it" listings are superhosts versus just 35% of the rest, a much bigger gap than any individual amenity. Having an in-unit washer and simply offering more amenities overall also helps. Interestingly, having a gym at this price point is *not* associated with feeling worth it — a reminder that what earns a listing the right to charge more isn't always what makes guests happy once they're there.

**Guests are more sensitive to review quality than price** — but only mildly. Using actual booking rate (how often a listing's calendar shows as unavailable) as a real demand signal rather than stated preference, star rating (r = 0.079) and review sentiment (r = 0.072) both out-correlate price (r = -0.028) as predictors of demand. That said, all three correlations are weak, which is itself a finding: booking demand is probably driven mostly by factors this dataset doesn't capture directly, like neighborhood desirability or listing photos.

**Sentiment predicts price almost twice as well as star ratings do.** Regressing price on sentiment alone explains 1.27% of price variance versus just 0.66% for star rating alone — and combining both barely improves on sentiment by itself (1.29%). In other words, sentiment captures almost everything about guest experience that actually shows up in pricing, and star ratings add very little on top of it.

## The Stack

- **Python** — pandas, statsmodels, scipy, nltk (VADER sentiment), geopandas
- **Tableau** — final dashboard
- **PostgreSQL** — the project's starting point

## The Pipeline

My `scripts/` directory handles the heavy lifting, in run order:

- `CleanAirbnbData.py` — merges all three cities and cleans price/boolean formatting
- `parseAmenities.py` — converts the amenities text field into boolean flags and a total count
- `scoreSentiment.py` — runs VADER sentiment analysis on every review, rolled up per listing
- `combineNeighbourhoods.py` — merges geospatial neighborhood boundaries across cities
- `masterDataset.py` — joins everything together and calculates a city-relative value score
- `outliers.py` — flags (doesn't delete) unrealistically priced listings
- `priceSatisfaction.py` — Q1: price vs. guest satisfaction
- `amenitiesRegression.py` — Q2: which amenities actually justify a premium
- `locationValue.py` — Q3: does location drive value
- `overpricedNeighborhoods.py` — Q4: which neighborhoods are overpriced
- `cityValue.py` — Q5: which city gives the most value
- `Worth300.py` — Q6: what makes a $300/night listing feel worth it
- `priceSensitivity.py` — Q7: price vs. review sensitivity, using booking rate as a real demand signal
- `sentimentRating.py` — Q8: sentiment vs. star rating as a price predictor

Each script prints its own sanity checks (row counts, null rates, join match rates) so the process stays transparent rather than a black box.

## Data Sources

Data is sourced from [Inside Airbnb](http://insideairbnb.com/get-the-data/). Because files like the NYC calendar can exceed 700MB, I haven't included the full datasets in this repo — a small sample of the cleaned data is available in `data/sample/` instead. To reproduce this project, download the raw files into `DataRaw/<City>/` and run the pipeline scripts in order.

- **listings.csv** — one row per listing, with price, room type, amenities, host details, and review scores
- **calendar.csv** — daily availability and pricing status for every listing over a rolling year, used here as a demand proxy
- **reviews.csv** — every individual guest review and its date, used for the sentiment analysis
- **neighbourhoods.geojson** — the geographic boundary shapes for each city's neighborhoods, used to map listings to real neighborhood polygons

## A Note on My Process

This project actually began in Postgres with SQL since I wanted to showcase multiple skillsets. Mid-way through, however, I shifted the cleaning and analysis to Python to increase speed and keep the workflow unified. I think it's important to show that data science isn't always a straight line.

## Next Steps

- [ ] Build the Tableau dashboard
- [ ] Write the final summary of results

**Author:** Ben Kim
