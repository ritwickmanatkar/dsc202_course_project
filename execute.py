import pandas as pd

from connectors.mongo_connector import get_mongo_connection
from connectors.postgres_connector import get_postgresql_connection_object


# Connect to MongoDB
def execute_mongo_query_reviews(business_ids):
    client = get_mongo_connection()
    db = client['yelp']
    collection = db['reviews']
    query = {"business_id": {"$in": business_ids}}
    result = collection.find(query)
    return result  # json


if __name__ == "__main__":
    pg_conn = get_postgresql_connection_object()
    pg_cursor = pg_conn.cursor()

    mongo_client = get_mongo_connection()
    try:
        query = """ SELECT * FROM santa_barbara_restaurants WHERE categories ilike '%American%'; """

        pg_cursor.execute(query)
        result = pg_cursor.fetchall()
        colnames = [desc[0] for desc in pg_cursor.description]
        # print(result)

        restaurants = pd.DataFrame(result, columns=colnames)
        print(restaurants)

        db = mongo_client['yelp_db']
        collection = db['santa_barbara_reviews']
        query = {"business_id": restaurants.business_id[0]}
        result = collection.find(query)
        for doc in result[:5]:
            print(doc.get('text'))
    except Exception as err:
        print(err)
    finally:
        if pg_cursor is not None:
            pg_cursor.close()
        if pg_conn is not None:
            pg_conn.close()
        if mongo_client is not None:
            mongo_client.close()
