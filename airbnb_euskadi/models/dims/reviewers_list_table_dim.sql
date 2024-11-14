{{
    config(
        materialized = 'view'
    )
}}

WITH reviewers as (
    SELECT
        *
    FROM `dbt-icanooo.airbnb_euskadi.reviews_table_fct`
)

SELECT
    DISTINCT reviewer_id as id,
    reviewer_name
FROM
    reviewers
ORDER BY
    id