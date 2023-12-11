import pandas as pd

from connectors.mongo_connector import get_mongo_connection


if __name__ == '__main__':
    mongo_client = get_mongo_connection()
    db = mongo_client['yelp_db']
    try:
        df = pd.read_json(r'../data/santa_barbara_photos.json')

        collection = db['santa_barbara_photos']

        collection.insert_many(df.to_dict('records'))

    except Exception as err:
        print(err)
    finally:
        mongo_client.close()
