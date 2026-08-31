# Airbnb Multi-City Analysis

What actually makes an Airbnb worth its price? To find out, I pulled listing, calendar, and review data for **Dallas, NYC, and Chicago** from Inside Airbnb.

## Questions I'm Exploring

1. Does a higher price point actually lead to higher guest satisfaction?
2. Which specific amenities justify a premium?
3. How much does location drive perceived value?
4. Which neighborhoods are statistically overpriced?
5. Which city offers travelers the most bang for their buck?
6. What makes a \$300/night listing feel like it's actually worth it?
7. Are guests more sensitive to the price or the quality of reviews?
8. Does review sentiment predict pricing better than standard star ratings?

## Key Findings So Far

**Price is a poor predictor of satisfaction.** Across all three cities, the correlation between price and guest ratings is statistically real (p < 0.001) but incredibly small (r = 0.06 to 0.11). This means price only explains about 1% of the variation in guest happiness. You might get a slightly higher-rated stay by paying more, but not a meaningfully better one. Whatever makes guests happy, it isn't the price tag.

**Simple amenity comparisons can be misleading.** At first glance, a straight average-price comparison suggested that having a kitchen *decreased* listing prices by ~17%. However, after digging deeper, most homes have kitchens, while the "no kitchen" group is largely made up of hotel rooms that charge higher rates for entirely different reasons. By using regression to control for room type, city, and size, I'm isolating the actual impact of each amenity. (I'll update the full results once the regression run finishes.)

**Data gaps tell their own story.** About a quarter of the listings had no price or rating data. While I thought this was a bug at first, it mostly represented inactive or brand-new listings with zero bookings. Additionally, roughly 0.75% of listings were priced at absurd levels (\$10k+/night) with no reviews, likely a tactic for hosts to "soft-delist" without deactivating. I’ve flagged these outliers rather than deleting them, keeping the analysis flexible.

## The Stack

- **Python** — pandas, statsmodels, scipy, nltk (VADER sentiment), geopandas
- **Tableau** — final dashboard
- **PostgreSQL** — the project's starting point

## The Pipeline

My `scripts/` directory handles the heavy lifting:
- `CleanAirbnbdata.py`: Merges cities and cleans formatting.
- `parseAmenities.py`: Converts text to boolean flags and counts.
- `scoreSentiment.py`: Runs VADER sentiment analysis on every review.
- `combineNeighbourhoods.py`: Merges geospatial boundary data.
- `masterDataset.py`: Joins all data and calculates value scores.
- `outliers.py`: Identifies extreme price points.
- `priceSatisfaction.py`, `amenitiesResgression.py`, etc.: Individual analysis scripts.

Each script outputs sanity checks (row counts, null rates, and join match rates) so the process is transparent.

## Data Sources

Data is sourced from [Inside Airbnb](http://insideairbnb.com/get-the-data/). Because files like the NYC calendar can exceed 700MB, I haven't included full datasets in this repo. You can find schema examples in `data/sample/`. To replicate this, download the raw files into `DataRaw/<City>/` and run the pipeline scripts in order.

- **listings.csv.gz** — Information about listings and numerical ratings
- **calendar.csv.gz** — 
- **reviews.csv.gz** — 
- **neighbourhoods.geojson** — 

## A Note on My Process

This project actually began in Postgres with SQL since I wanted to showcase multiple skillsets. Mid-way through, however, I shifted the cleaning and analysis to Python to increase speed and keep the workflow unified. I think it's important to show that data science isn't always a straight line.

## Next Steps

- [ ] Analyze Questions 3 through 8
- [ ] Build the Tableau dashboard
- [ ] Write the final summary of results

**Author:** Ben Kim
