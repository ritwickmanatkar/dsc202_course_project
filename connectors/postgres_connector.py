import psycopg2

from auth.connector_auth import (
    POSTGRES_DBNAME,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT
)

POSTGRESQL_CONNECTION = None


def get_postgresql_connection_object():
    """

    :return:
    """
    POSTGRESQL_CONNECTION = psycopg2.connect(
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    return POSTGRESQL_CONNECTION
