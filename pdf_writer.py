from typing import Dict

import ast
from PIL import Image

DAY_OF_THE_WEEK_MAPPER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
PHOTO_DIRECTORY_PATH = "/Users/ritwickmanatkar/Downloads/yelp_photos/photos/"


def pretty_print_given_information(restaurant_info: Dict) -> None:
    """ This function prints the given information in an organized manner.

    :param restaurant_info: Dictionary containing the results.
    :return: None
    """
    for key, value in restaurant_info.items():
        if key not in ['hours', 'photos', 'reviews', 'tips']:
            print(f"\033[1m{key.upper()}\033[0m : {value}")

        if key == 'hours':
            try:
                restaurant_operating_hours = ast.literal_eval(value)
                print(f"\033[1m{key.upper()}\033[0m :")
                for day in DAY_OF_THE_WEEK_MAPPER:
                    print(f"\t - \033[4m{day}\033[0m : {restaurant_operating_hours.get(day)}")
            except ValueError:
                print(f"\033[1m{key.upper()}\033[0m : {value}")

        if key == 'reviews':
            print('_' * 100)
            print('_' * 100)
            print(f"\033[1mReviews\033[0m :")
            print('_' * 100)
            for review in value:
                print(f"\t ---> \033[4m{review.get('user_id')}\033[0m ~ {review.get('date')} :")
                print(f"\t \t \033[4mStars\033[0m: {review.get('stars')} || \033[4mUseful\033[0m: {review.get('useful')}")
                text = review.get('text').replace('\n', '\n\t \t ')
                print(f"\t \t {text}")
                print('\t \t ' + '_' * 100)

        if key == 'tips':
            print('_' * 100)
            print('_' * 100)
            print(f"\033[1mTips\033[0m :")
            for tip in value:
                print(f"\t ---> \033[4m{tip.get('user_id')}\033[0m ~ {tip.get('date')} :")
                print(f"\t \t \033[ Compliment Count\033[0m: {tip.get('compliment_count')}")
                text = tip.get('text').replace('\n', '\n\t \t ')
                print(f"\t \t {text}")
                print('\t \t ' + '_' * 100)

        if key == 'photos':
            print('_' * 100)
            print('_' * 100)
            print(f"\033[1mPhotos\033[0m : {len(value)} photos")
            for photo in value:
                Image.open(f"{PHOTO_DIRECTORY_PATH}{photo.get('photo_id')}.jpg").show()

    print('_.' * 100)
    print('_.' * 100)
