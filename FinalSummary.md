# Airbnb Multi-City Analysis: Final Summary

## The Question

Does paying more for an Airbnb actually get you a better stay? I set out to answer that — and seven related questions — using listing, calendar, and review data for Dallas, NYC, and Chicago from Inside Airbnb. Below is what the data actually showed, question by question.

## 1. Does a higher price lead to higher guest satisfaction?

Barely. Across all three cities the correlation between price and guest rating is real (p < 0.001 everywhere) but weak — r = 0.082 in Dallas, 0.057 in NYC, 0.113 in Chicago. Price explains roughly 1% of the variation in how happy guests end up. Splitting listings into price quartiles tells the same story more intuitively: average rating climbs gently from 4.68 (cheapest quarter) to 4.79 (priciest quarter) — a real trend, but a small one.

![Rating climbing gently by price quartile](TableauVisuals/RatingPrice.png)

**Takeaway:** price tells you almost nothing about whether you'll enjoy your stay.

## 2. What amenities justify a premium?

A regression predicting price from all 14 tracked amenities, controlling for room type, city, and listing size (R² = 0.35), isolated real effects:

| Amenity | Price effect | Significant? |
|---|---|---|
| Gym | +$68.76 | Yes |
| Washer | +$36.30 | Yes |
| TV | +$34.10 | Yes |
| Hot tub | +$33.62 | Yes |
| AC | +$31.39 | Yes |
| Wifi | +$1.31 | No (p = 0.84) |
| Kitchen | **–$88.61** | Yes |

Wifi is so universally expected now that it commands no premium at all. The kitchen result is the interesting anomaly: even controlling for room type, listings with a kitchen are priced *lower*. My working theory is that "Entire home/apt" listings without a full kitchen skew toward professionally-managed, hotel-style serviced apartments — a segment charging premiums for things this model doesn't capture (concierge, brand, management quality). A natural follow-up would add `property_type` as an additional control to test that directly.

## 3. How much does location affect perceived value?

A lot, and it's statistically unambiguous. An ANOVA test on a city-relative value score (guest rating vs. price, standardized within each city) came back significant everywhere: Dallas F=6.70, NYC F=5.95, Chicago F=6.82, all p < 0.0001. Location isn't a minor factor in perceived value — it's one of the strongest.

## 4. Which neighborhoods are overpriced?

To answer this rigorously rather than just comparing raw averages, I built a second regression predicting price from listing features (bedrooms, accommodates, bathrooms, rating, room type, city) with R² = 0.379, then looked at where actual price consistently runs above what a listing's features justify.

**Most overpriced (NYC):** Tribeca (+$225/night), Greenwich Village (+$191), SoHo (+$177), Financial District (+$170), Theater District (+$134)
**Most overpriced (Chicago):** Loop (+$130), Near North Side (+$107), Lincoln Park (+$77)
**Best value (NYC):** Throgs Neck (–$130), Coney Island (–$125), Williamsbridge (–$123), Jamaica Estates (–$118)
**Best value (Chicago):** Brighton Park (–$132), West Garfield Park (–$128)

![Top 10 most overpriced neighborhoods](TableauVisuals/HighestPriceResid.png)
![Bottom 10 best-value neighborhoods](TableauVisuals/LowestPriceResid.png)

The pattern is consistent and tellable: in famous, tourist-heavy neighborhoods, guests are paying for the name, not for anything measurably better about the listing.

## 5. Which city gives travelers the most value?

Dallas, clearly. Guest ratings are nearly identical across all three cities (4.72–4.79 average — barely distinguishable), but price-per-person tells a very different story:

| City | Avg. price/person |
|---|---|
| Dallas | $54.88 |
| Chicago | $65.36 |
| NYC | $83.06 |

NYC guests pay over 50% more per person than Dallas guests for essentially the same satisfaction level.

![Price per person by city](TableauVisuals/PricePerPersonCity.png)
![City-level summary numbers](TableauVisuals/CityNumbers.png)

## 6. What makes a $300/night Airbnb feel worth it?

Looking at listings priced $275–325/night and splitting them into "felt worth it" (rating above the band's own median) versus "didn't," one factor stood out far above everything else: **host superhost status.** 59% of the "worth it" group were superhosts, versus only 35% of the rest — a 24-point gap, dwarfing any individual amenity. An in-unit washer (+11.5 percentage points) was the strongest single amenity signal, and total amenity count mattered too (43.3 vs. 38.6 average). Interestingly, having a gym was *negatively* associated with feeling worth it at this specific price point (-5.2 points) — a reminder that what lets a host charge more isn't always what makes guests happy once they're there.

## 7. Are guests more sensitive to price or review quality?

Using actual booking behavior (the fraction of a listing's calendar marked unavailable) as a real demand signal — rather than asking people what they say they prefer — star rating (r = 0.079) and review sentiment (r = 0.072) both out-predicted price (r = –0.028) as drivers of demand. All three correlations are weak in absolute terms, which is itself worth stating honestly: whatever mainly drives booking demand, this dataset doesn't fully capture it. But directionally, guests lean toward caring more about review quality than price when actually booking.

## 8. Does review sentiment explain pricing better than star ratings?

Yes, clearly. Regressing price on sentiment alone explained 1.27% of price variance; star rating alone explained only 0.66% — sentiment nearly doubles star rating's explanatory power. Combining both barely improved on sentiment alone (1.29%), meaning sentiment already captures almost everything about guest experience that shows up in price. Notably, star rating's effect was only marginally significant (p = 0.039) once sentiment was in the model, while sentiment's effect was overwhelming (p < 0.001).

![Price vs. rating relationship](TableauVisuals/RatingPrice.png)

## Data quality notes

A few decisions shaped this analysis and are worth stating plainly:

- **About 25% of listings had no price or rating** — mostly inactive or brand-new listings with no booking history. Kept in the dataset, excluded from analyses requiring those fields.
- **About 0.75% of listings (341) showed unrealistic prices** (some over $10,000/night), and 185 of those had zero reviews — consistent with hosts using extreme pricing to effectively delist without deactivating. Flagged rather than deleted.
- **VADER sentiment scoring is English-tuned** and scores non-English reviews as roughly neutral regardless of actual tone — a real blind spot given how international Airbnb's guest base is.
- **Several legacy columns** in the raw Inside Airbnb export (`host_verifications`, uncleaned `neighbourhood`, `calendar_updated`, etc.) were empty across all three cities and dropped during cleaning.

## Conclusion

The throughline across all eight questions: **price is a weak signal for almost everything that actually matters.** It barely predicts satisfaction, it's a worse predictor of guest experience than review sentiment, and its relationship to "value" depends far more on neighborhood reputation than on any measurable difference in what you're getting. What *does* predict a good stay: specific amenities (gym, washer, AC, TV, hot tub), host quality (superhost status, more than any single physical amenity at the $300 mark), and location choice — with the best deals sitting in solid, unglamorous neighborhoods rather than famous ones.

If I were advising a traveler with this data: skip the neighborhood everyone's heard of, look for a superhost, and weight the reviews more heavily than the price tag.

## What's next

- Add `property_type` as a control to resolve the kitchen pricing paradox
- Explore whether booking demand is better explained by factors not yet in this dataset (photos, listing age, search ranking position)
- Extend to additional cities to test whether the "famous neighborhood tax" pattern holds elsewhere

**Author:** Ben Kim
