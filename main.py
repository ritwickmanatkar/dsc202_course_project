from connectors.mongo_connector import get_mongo_connection
from connectors.postgres_connector import get_postgresql_connection_object
from queries.query1 import check_if_open_and_get_tips


if __name__ == '__main__':
    # Create connections to the data sources.
    postgresql_connection_object = get_postgresql_connection_object()
    postgresql_cursor = postgresql_connection_object.cursor()

    mongo_client = get_mongo_connection()
    mongodb_db = mongo_client['yelp_db']

    try:
        print('Query #1:')
        print(check_if_open_and_get_tips(
            postgresql_cursor=postgresql_cursor,
            mongo_client=mongodb_db,
            restaurant_name='Helena Avenue Bakery'
        ))
    except Exception as error:
        print(error)
    finally:
        if postgresql_cursor is not None:
            postgresql_cursor.close()
        if postgresql_connection_object is not None:
            postgresql_connection_object.close()
        if mongo_client is not None:
            mongo_client.close()
