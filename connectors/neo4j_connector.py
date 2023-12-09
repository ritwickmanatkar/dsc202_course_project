from neo4j import GraphDatabase
from auth.connector_auth import neo4j_user, neo4j_password


def get_neo4j_connection():
    """ This function returns a neo4j session object."""
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(
        uri,
        auth=(neo4j_user, neo4j_password)
    )
    return driver.session()


if __name__ == '__main__':
    session = get_neo4j_connection()

    query = """
    MATCH (r1:Restaurant {id: "9L-MR0arflwFMF9szEBOOg"})-[rel:distance]->(r2:Restaurant)
    where rel.dist < 1
    RETURN  r2, rel
    order by rel.dist
    limit 10
    """

    result = session.run(query)
    print(result.data())
