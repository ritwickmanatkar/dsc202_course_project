from typing import Dict

from bs4 import BeautifulSoup
import ast

DAY_OF_THE_WEEK_MAPPER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def alter_html(file: str, data: Dict) -> None:
    """ This file alters the generated html file.

    :param data: Data to enter into the file.
    :param file: File location

    :return: None
    """
    # data = {'business_id': 'IDtLPgUrqorrpqSLdfMhZQ', 'name': 'Helena Avenue Bakery', 'address': '131 Anacapa St, Ste C',
    #  'city': 'Santa Barbara', 'state': 'CA', 'postal_code': 93101, 'latitude': '34.4144445',
    #  'longitude': '-119.6906718', 'stars': '4', 'review_count': 389, 'is_open': 1,
    #  'attributes': '{\'RestaurantsTakeOut\': \'True\', \'NoiseLevel\': "u\'average\'", \'Caters\': \'True\', \'Ambience\': "{\'touristy\': False, \'hipster\': True, \'romantic\': False, \'divey\': False, \'intimate\': False, \'trendy\': True, \'upscale\': False, \'classy\': False, \'casual\': True}", \'RestaurantsReservations\': \'False\', \'BusinessAcceptsCreditCards\': \'True\', \'RestaurantsTableService\': \'False\', \'GoodForKids\': \'True\', \'RestaurantsPriceRange2\': \'2\', \'WheelchairAccessible\': \'True\', \'OutdoorSeating\': \'True\', \'RestaurantsDelivery\': \'None\', \'HasTV\': \'False\', \'RestaurantsAttire\': "\'casual\'", \'Alcohol\': "u\'none\'", \'GoodForMeal\': "{\'dessert\': False, \'latenight\': False, \'lunch\': True, \'dinner\': False, \'brunch\': True, \'breakfast\': True}", \'DogsAllowed\': \'True\', \'RestaurantsGoodForGroups\': \'True\', \'HappyHour\': \'False\', \'BusinessParking\': "{\'garage\': False, \'street\': True, \'validated\': False, \'lot\': False, \'valet\': False}", \'BikeParking\': \'True\', \'WiFi\': "u\'no\'"}',
    #  'categories': 'Food, Restaurants, Salad, Coffee & Tea, Breakfast & Brunch, Sandwiches, Bakeries',
    #  'hours': "{'Monday': '0:0-0:0', 'Tuesday': '8:0-14:0', 'Wednesday': '8:0-14:0', 'Thursday': '8:0-14:0', 'Friday': '8:0-14:0', 'Saturday': '8:0-14:0', 'Sunday': '8:0-14:0'}"}
    HTMLFile = open(file, "r")
    index = HTMLFile.read()
    soup = BeautifulSoup(index, "html.parser")

    new_div = soup.new_tag("div")

    for key, value in data.items():
        if key in ['stars', 'address', 'state', 'postal_code', 'review_count', 'is_open']:
            new_div.append(f"{key.upper()}: {value}")
            new_div.append(soup.new_tag("br"))
        if key == 'name':
            header = soup.new_tag("h1")
            header.append(value)
            new_div.append(header)
        if key == 'hours':
            if value is None:
                new_div.append(f"{key.upper()}: Timings not provided.")
                continue
            new_div.append(f"{key.upper()}:")
            restaurant_operating_hours = ast.literal_eval(value)
            times = soup.new_tag('ul', style="padding-left: 30px")
            for day in DAY_OF_THE_WEEK_MAPPER:
                li = soup.new_tag('li')
                li.append(f"{day}: {restaurant_operating_hours.get(day)}")
                times.append(li)
            new_div.append(times)

    soup.body.insert_before(new_div)

    with open(file, "w") as f:
        f.write(str(soup))


if __name__ == '__main__':
    alter_html('modifiedfile.html', {})
