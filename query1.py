import datetime
import ast

import pandas as pd
import pymongo

from connectors.mongo_connector import get_mongo_connection
from connectors.postgres_connector import get_postgresql_connection_object

DAY_OF_THE_WEEK_MAPPER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


if __name__ == "__main__":
    postgresql_connection_object = get_postgresql_connection_object()
    postgresql_cursor = postgresql_connection_object.cursor()

    mongo_client = get_mongo_connection()

    restaurant_name = 'Helena Avenue Bakery'
    try:
        query = f""" SELECT * FROM santa_barbara_restaurants WHERE name = '{restaurant_name}'; """
        postgresql_cursor.execute(query)
        result = postgresql_cursor.fetchall()

        column_names = [descriptor[0] for descriptor in postgresql_cursor.description]
        restaurant_info = pd.DataFrame(result, columns=column_names)

        open_now_status = False
        # Process opening hours
        time_now = datetime.datetime.now()
        current_day_of_the_week = DAY_OF_THE_WEEK_MAPPER[time_now.weekday()]
        current_hour = time_now.hour
        current_minutes = time_now.minute

        operating_hours = ast.literal_eval(restaurant_info.hours[0])
        if operating_hours is not None:
            if operating_hours.get(current_day_of_the_week) is not None:
                times = operating_hours.get(current_day_of_the_week)
                open_time = times.split('-')[0]
                close_time = times.split('-')[1]

                if open_time == close_time:
                    open_now_status = True
                elif int(open_time.split(':')[0]) < current_hour < int(close_time.split(':')[0]):
                    open_now_status = True
                elif int(open_time.split(':')[0]) == current_hour and int(open_time.split(':')[1]) <= current_minutes:
                    open_now_status = True
                elif int(close_time.split(':')[0]) == current_hour and int(close_time.split(':')[1]) >= current_minutes:
                    open_now_status = True

        if open_now_status:
            print(f"{restaurant_name} is open now !!!!!!")
            print(f"{restaurant_info}")
        else:
            print(f"{restaurant_name} is closed now :(")
            print(f"Operating hours are from {operating_hours.get(current_day_of_the_week)} on "
                  f"{current_day_of_the_week}'s")

        db = mongo_client['yelp_db']
        collection = db['santa_barbara_tips']
        query = {"business_id": restaurant_info.business_id[0]}
        result = collection.find(query).sort([('compliment_count', pymongo.DESCENDING), ('date', pymongo.DESCENDING)])
        for doc in result[:5]:
            print(doc.get('text'))
    except Exception as err:
        print(err)
    finally:
        if postgresql_cursor is not None:
            postgresql_cursor.close()
        if postgresql_connection_object is not None:
            postgresql_connection_object.close()
        if mongo_client is not None:
            mongo_client.close()
