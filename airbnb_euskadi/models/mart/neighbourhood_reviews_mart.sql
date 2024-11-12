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
        n.*
    FROM reviews_with_neighbourhood AS r
    INNER JOIN {{ref('neighbourhoods_table_dim')}} AS n
    ON r.neighbourhood = n.neighbourhood
)

SELECT
    neigbourhood_group,
    neighbourhood,
    count(*) AS count_of_reviews
FROM review_neighbourhood_full
GROUP BY neighbourhood, neigbourhood_group
ORDER BY neigbourhood_group