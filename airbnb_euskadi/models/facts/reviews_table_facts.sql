WITH source_reviews AS (
    SELECT * FROM `dbt-icanooo.airbnb_euskadi.reviews_table_source`
)

SELECT
    listing_id,
    id,
    date as review_post_date,
    reviewer_id,
    reviewer_name,
    comments
FROM
    source_reviews