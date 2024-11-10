WITH source_neighbourhood AS (
    SELECT * FROM `dbt-icanooo.airbnb_euskadi.neighbourhoods_table_source`
)

SELECT
    row_number() over () as id,
    string_field_0 as neigbourhood_group,
    string_field_1 as neighbourhood
FROM
    source_neighbourhood