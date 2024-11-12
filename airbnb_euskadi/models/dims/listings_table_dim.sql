{{
    config(
        materialized = 'view'
    )
}}

WITH source_listings AS (
    SELECT * FROM `dbt-icanooo.airbnb_euskadi.listings_table_source`
),
source_listings_cleansed as (
    SELECT
        safe_cast(id as int64) AS id,
        name as listing_name,
        host_id,
        host_name,
        neighbourhood,
        cast(latitude as float64) as latitude,
        cast(longitude as float64) as longitude,
        room_type,
        price,
        minimum_nights,
        license
    FROM source_listings
)

SELECT
    *
FROM source_listings_cleansed
WHERE id IS NOT NULL