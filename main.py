from connectors.mongo_connector import get_mongo_connection
from connectors.postgres_connector import get_postgresql_connection_object
from connectors.neo4j_connector import get_neo4j_connection

from queries.query1 import check_if_open_and_get_tips
from queries.query2 import get_top_rated_restaurant_near_me
from queries.query3 import get_pictures_and_reviews_for_italian
from queries.query4 import get_top_rated_restaurant_and_parking
from pretty_printer import pretty_print_given_information

if __name__ == '__main__':
    # Create connections to the data sources.
    postgresql_connection_object = get_postgresql_connection_object()
    postgresql_cursor = postgresql_connection_object.cursor()

    mongo_client = get_mongo_connection()
    mongodb_db = mongo_client['yelp_db']

    neo4j_session_object = get_neo4j_connection()
    try:
        print('Query #1:')
        query1_result = check_if_open_and_get_tips(
            postgresql_cursor=postgresql_cursor,
            mongo_client=mongodb_db,
            restaurant_name='Helena Avenue Bakery'
        )
        pretty_print_given_information(query1_result)
        print('\n' * 5)

        print('Query #2:')
        query2_result = (
            get_top_rated_restaurant_near_me(
                postgresql_cursor=postgresql_cursor,
                neo4j_session_object=neo4j_session_object,
                restaurant_name='Helena Avenue Bakery'
            )
        )
        for result in query2_result:
            pretty_print_given_information(result)
            print('\n'*5)

        print('Query #3:')
        query3_result = (
            get_pictures_and_reviews_for_italian(
                postgresql_cursor=postgresql_cursor,
                neo4j_session_object=neo4j_session_object,
                mongo_client=mongodb_db,
                cuisine='Italian'
            )
        )
        for result in query3_result:
            pretty_print_given_information(result)
            print('\n'*5)

        print('Query #4:')
        query4_result = (
            get_top_rated_restaurant_and_parking(
                postgresql_cursor=postgresql_cursor,
                neo4j_session_object=neo4j_session_object,
                mongo_client=mongodb_db,
                cuisine='Japanese'
            )
        )

    except Exception as error:
        raise Exception(error)
    finally:
        if postgresql_cursor is not None:
            postgresql_cursor.close()
        if postgresql_connection_object is not None:
            postgresql_connection_object.close()
        if mongo_client is not None:
            mongo_client.close()
        if neo4j_session_object is not None:
            neo4j_session_object.close()
