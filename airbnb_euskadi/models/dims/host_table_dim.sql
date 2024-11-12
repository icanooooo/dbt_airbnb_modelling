{{
    config(
        materialized = 'view'
    )
}}

WITH source_listings AS (
    SELECT 
        safe_cast(host_id as int64) as host_id,
        host_name
    FROM {{ ref('listings_table_dim') }}
),
host_table_full as (
    SELECT
        DISTINCT(host_id) as id,
        host_name as name
    FROM source_listings
)

SELECT
    *
FROM host_table_full
WHERE id IS NOT NULL
ORDER BY id DESC