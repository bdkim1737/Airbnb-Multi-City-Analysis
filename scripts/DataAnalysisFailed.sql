SELECT city, COUNT(*) FROM raw_listings GROUP BY city;
SELECT city, COUNT(*) FROM raw_calendar GROUP BY city;
SELECT city, COUNT(*) FROM raw_reviews GROUP BY city;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'raw_listings'
ORDER BY column_name;

SELECT id, city, price, room_type, neighbourhood_cleansed,
       neighbourhood_group_cleansed, review_scores_rating, host_is_superhost
FROM raw_listings
LIMIT 20;

SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE price IS NULL) AS null_price,
    COUNT(*) FILTER (WHERE review_scores_rating IS NULL) AS null_rating,
    COUNT(*) FILTER (WHERE review_scores_value IS NULL) AS null_value_score
FROM raw_listings;

DROP TABLE IF EXISTS listings;

CREATE TABLE listings AS
SELECT
    id,
    city,
    room_type,
    property_type,
    neighbourhood_cleansed,
    neighbourhood_group_cleansed,
    accommodates,
    bedrooms,
    beds,
    bathrooms,
    NULLIF(REPLACE(REPLACE(price, '$', ''), ',', ''), '')::NUMERIC AS price,
    (host_is_superhost = 't') AS host_is_superhost,
    host_response_rate,
    host_acceptance_rate,
    number_of_reviews,
    number_of_reviews_ltm,
    review_scores_rating,
    review_scores_accuracy,
    review_scores_cleanliness,
    review_scores_checkin,
    review_scores_communication,
    review_scores_location,
    review_scores_value,
    reviews_per_month,
    amenities,
    latitude,
    longitude
FROM raw_listings;

SELECT * FROM listings LIMIT 10;

SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'raw_calendar' ORDER BY column_name;

DROP TABLE IF EXISTS calendar;

CREATE TABLE calendar AS
SELECT
    listing_id,
    city,
    date::DATE AS date,
    (available = 't') AS available,
    minimum_nights,
    maximum_nights
FROM raw_calendar;

DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews AS
SELECT
    id AS review_id,
    listing_id,
    city,
    date::DATE AS review_date,
    reviewer_id,
    reviewer_name,
    comments
FROM raw_reviews;