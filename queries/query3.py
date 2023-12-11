""" This file stores the code used for Query 3."""
from typing import List, Dict

import pandas as pd
import pymongo


def get_pictures_and_reviews_for_italian(
        postgresql_cursor,
        neo4j_session_object,
        mongo_client,
        cuisine: str
) -> List[Dict]:
    """ This function serves as the 3rd query of our course project.

    NOTE:
        Can you show me pictures and reviews of Italian restaurants in this city?
        ---> Utilizes: Graph+Relational database (for cuisine category connections)
        and MongoDB (for photos and reviews).

    :param postgresql_cursor: Cursor of the Postgresql Connection
    :param neo4j_session_object: Session object of the Neo4j Connection
    :param mongo_client: MongoDB Client object.
    :param cuisine: Cuisine Selected by the user.

    :return: Dict with information
    """
    neo4j_query = f"""MATCH (restaurant:Restaurant)-[x:rating]->(c:Category {{id: '{cuisine}'}})
    RETURN restaurant, x.value as rating
    ORDER BY x.value desc
    LIMIT 10
    """
    neo4j_result = neo4j_session_object.run(neo4j_query).data()

    output = []
    for restaurant_info in neo4j_result:
        postgresql_query = f""" 
        SELECT * FROM santa_barbara_restaurants WHERE business_id = '{restaurant_info.get('restaurant').get('id')}'; """
        postgresql_cursor.execute(postgresql_query)
        postgresql_query_result = postgresql_cursor.fetchall()

        column_names = [descriptor[0] for descriptor in postgresql_cursor.description]
        df = pd.DataFrame(postgresql_query_result, columns=column_names)
        restaurant_output = df.to_dict('records')[0]

        restaurant_output['weighted_rating'] = restaurant_info.get('rating')

        # Get Photos
        photos_collection = mongo_client['santa_barbara_photos']

        photos_query = {"business_id": restaurant_info.get('restaurant').get('id')}
        photos_result = photos_collection.find(photos_query).limit(5)
        photos = []
        for document in photos_result:
            photos.append(document)
        restaurant_output['photos'] = photos

        # Get Reviews
        reviews_collection = mongo_client['santa_barbara_reviews']

        reviews_query = {"business_id": restaurant_info.get('restaurant').get('id')}
        reviews_result = reviews_collection.find(reviews_query).sort(
            [
                ('useful', pymongo.DESCENDING),
                ('date', pymongo.DESCENDING)
            ]
        ).limit(10)
        reviews = []
        for document in reviews_result:
            reviews.append(document)
        restaurant_output['reviews'] = reviews

        output.append(restaurant_output)

    return output
