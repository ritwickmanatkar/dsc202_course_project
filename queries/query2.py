""" This file stores the code used for Query 2."""
from typing import List, Dict
import pandas as pd

def get_top_rated_restaurant_near_me(
        postgresql_cursor,
        neo4j_session_object,
        restaurant_name: str):
    """
    :param postgresql_cursor: Cursor of the Postgresql Connection
    :param neo4j_session_object: Session object of the Neo4j Connection
    :param restaraunt_name: Restaraunt near which other other restaraunts are to be found
    :return list
    """

    postgresql_query = f""" SELECT * FROM santa_barbara_restaurants WHERE name = '{restaurant_name}'; """
    postgresql_cursor.execute(postgresql_query)
    postgresql_query_result = postgresql_cursor.fetchall()
    business_id = postgresql_query_result[0][0]

    neo4j_query = f"""MATCH (r1:Restaurant {{id: '{business_id}'}})-[r:distance]->(r2:Restaurant)
    WHERE r.dist < 0.1
    RETURN r2.id as id, r.dist
    ORDER BY r.dist
    """
    neo4j_result = neo4j_session_object.run(neo4j_query).data()

    output = []
    for restaurant_info in neo4j_result:
        postgresql_query = f""" SELECT name, address FROM santa_barbara_restaurants WHERE business_id = '{restaurant_info.get('id')}'; """
        postgresql_cursor.execute(postgresql_query)
        postgresql_query_result = postgresql_cursor.fetchall()

        column_names = [descriptor[0] for descriptor in postgresql_cursor.description]
        df = pd.DataFrame(postgresql_query_result, columns=column_names)
        output.append(df.to_dict('records')[0])

    return output


