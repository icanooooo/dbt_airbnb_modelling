from aws_helper import connect_to_redshift, redshift_query
from keys import redshift

connection = connect_to_redshift('sample_data_dev', redshift.user, redshift.password, redshift.host)

query = """
SELECT
    *
FROM
    tickit.category
limit = 5;
"""

result = redshift_query(connection, query)
print(result)

connection.close()

