import psycopg2
from connectors.mongo_connector import get_mongo_connection
from execute_postgres import execute_postgres_query
from connectors.postgres_connector import get_postgresql_connection_object, get_postgresql_cursor_objectimport pymongo

# Execute the query in postgres
def execute_postgres_query(query): 
    pg_conn = get_postgresql_connection_object() 
    pg_cursor = get_postgresql_cursor_object()
    
    pg_cursor.execute(query)
    pg_conn.commit()
    result = pg_cursor.fetchall()
    return result # list

# Connect to MongoDB
def execute_mongo_query_reviews(bussiness_ids): 
    client = get_mongo_connection()
    db = client['yelp']
    collection = db['reviews']
    query = {"business_id": {"$in": business_ids}}
    result = collection.find(query)
    return result  # json

if __name__ == "__main__":
    
    # execute query
    query = """ SELECT * FROM santa_barbara_restaurants WHERE state = 'CA'; """ 
    result = execute_postgres_query(query, pg_cursor)

    print(table)
    execute_mongo_query_reviews(bussiness_ids) 
    for doc in result:
    print(doc)  
