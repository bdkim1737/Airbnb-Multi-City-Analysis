SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'raw_calendar' ORDER BY column_name;

DROP TABLE IF EXISTS calendar;

CREATE TABLE calendar AS
SELECT
    listing_id,
    city,
    date::DATE AS date,
    (available = 't') AS available,
    NULLIF(REPLACE(REPLACE(price, '$', ''), ',', ''), '')::NUMERIC AS price,
    NULLIF(REPLACE(REPLACE(adjusted_price, '$', ''), ',', ''), '')::NUMERIC AS adjusted_price,
    minimum_nights,
    maximum_nights
FROM raw_calendar;

SELECT column_name, data_type FROM information_schema.columns
WHERE table_name IN ('listings', 'calendar', 'reviews')
AND column_name IN ('id', 'listing_id');

SELECT COUNT(*) FROM calendar c
JOIN listings l ON c.listing_id = l.id
LIMIT 1;