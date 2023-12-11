""" This file stores the code used for Query 1."""
from typing import Dict
import datetime
import ast

import pandas as pd
import pymongo

from connectors.mongo_connector import get_mongo_connection
from connectors.postgres_connector import get_postgresql_connection_object

DAY_OF_THE_WEEK_MAPPER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def check_if_restaurant_is_open(operating_hours: Dict):
    """ This is a data specific function that check whether the restaurant is open or not given the operating hours and
    current timings.

    :param operating_hours: Dict containing the opening
    :return:
    """
    # Get current timings
    time_now = datetime.datetime.now()
    current_day_of_the_week = DAY_OF_THE_WEEK_MAPPER[time_now.weekday()]
    current_hour = time_now.hour
    current_minutes = time_now.minute

    # check if restaurant is open or not.
    if operating_hours is not None:
        if operating_hours.get(current_day_of_the_week) is not None:
            times = operating_hours.get(current_day_of_the_week)
            open_time = times.split('-')[0]
            close_time = times.split('-')[1]

            if open_time == close_time: # For 00:00 - 00:00 service
                return True
            elif int(open_time.split(':')[0]) < current_hour < int(close_time.split(':')[0]):
                return True
            elif int(open_time.split(':')[0]) == current_hour and int(open_time.split(':')[1]) <= current_minutes:
                return True
            elif int(close_time.split(':')[0]) == current_hour and int(close_time.split(':')[1]) >= current_minutes:
                return True

    return False


def check_if_open_and_get_tips(postgresql_cursor, mongo_client, restaurant_name:str):
    """ This function serves as the 1st query of our course project.

    NOTE:
        Is the 'X' restaurant open currently?
        What are the recommendations left by the users for that 'X' restaurant?
        ---> Utilizes: MongoDB database (for tips/recommendations) and Relational database (for Restaurant information
        and checking if its open)


    :param postgresql_cursor: Cursor of the Postgresql Connection
    :param mongo_client: MongoDB Connection client
    :param restaurant_name: Restaurant Name
    :return: json result as dict
    """
    # POSTGRESQL Execution
    postgresql_query = f""" SELECT * FROM santa_barbara_restaurants WHERE name = '{restaurant_name}'; """
    postgresql_cursor.execute(postgresql_query)
    postgresql_query_result = postgresql_cursor.fetchall()

    column_names = [descriptor[0] for descriptor in postgresql_cursor.description]
    restaurant_info = pd.DataFrame(postgresql_query_result, columns=column_names)

    # Get restaurant timings
    restaurant_operating_hours = ast.literal_eval(restaurant_info.hours[0])

    status = check_if_restaurant_is_open(restaurant_operating_hours)

    output = restaurant_info.to_dict('records')[0]
    output['status'] = status

    # MONGO DB Execution
    tips_collection = mongo_client['santa_barbara_tips']

    mongodb_query = {"business_id": restaurant_info.business_id[0]}
    mongodb_result = tips_collection.find(mongodb_query).sort(
        [
            ('compliment_count', pymongo.DESCENDING),
            ('date', pymongo.DESCENDING)
        ]
    )
    temp = []
    for document in mongodb_result:
        temp.append(document)
    output['reviews'] = temp

    return output

