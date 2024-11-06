import boto3
import psycopg2
import pandas as pd

def connect_to_redshift(db_rs, db_user, db_password, db_host):
    try:
        conn = psycopg2.connect(
            dbname= db_rs,
            user = db_user,
            password = db_password,
            host = db_host,
            port = '5439'
        )

        return conn
    except Exception as e:
        print(f"can't do it bruv: {e}")

def redshift_query(conn, query):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)

            results = cursor.fetchhall()
            columns = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(results, columns=columns)

            return df
    except Exception as e:
        print(f"can't do it bruv: {e}")