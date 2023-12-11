""" This file stores the code used for Query 1."""
from typing import List, Dict
import pandas as pd
import webbrowser
from mapping.get_map import create_map 

def get_top_rated_restaurant_and_parking(
        postgresql_cursor,
        neo4j_session_object,
        mongo_client,
        cuisine: str):
    """
    :param postgresql_cursor: Cursor of the Postgresql Connection
    :param neo4j_session_object: Session object of the Neo4j Connection
    :param cuisine: Cuisine Selected by the user.

    :return Open a map in the browser
    """

    neo4j_query = f"""MATCH (restaurant:Restaurant)-[x:rating]->(c:Category {{id: '{cuisine}'}})
    RETURN restaurant, x.value as rating
    ORDER BY x.value desc
    LIMIT 1
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

        map = create_map(restaurant_output.get("longitude"), restaurant_output.get("latitude"))
        map.save("my_map.html")

        webbrowser.open("my_map.html")
