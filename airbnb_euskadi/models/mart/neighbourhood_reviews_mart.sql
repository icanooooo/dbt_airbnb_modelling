WITH reviews_with_neighbourhood AS (
    SELECT
        r.*,
        l.neighbourhood
    FROM {{ref('reviews_table_fct')}} AS r
    INNER JOIN {{ref('listings_table_dim')}} AS l
    ON r.listing_id = l.id
),
review_neighbourhood_full AS (
    SELECT
        r.comments,
        EXTRACT(MONTH FROM r.review_post_date) as review_month,
        EXTRACT(YEAR FROM r.review_post_date) as review_year,
        n.*
    FROM reviews_with_neighbourhood AS r
    INNER JOIN {{ref('neighbourhoods_table_dim')}} AS n
    ON r.neighbourhood = n.neighbourhood
)

SELECT
    neigbourhood_group,
    neighbourhood,
    review_month,
    review_year,
    count(*) AS count_of_reviews
FROM review_neighbourhood_full
GROUP BY 1,2,3,4
ORDER BY neigbourhood_group