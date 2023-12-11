from sqlalchemy import create_engine
import geopandas as gpd
import folium
from shapely.geometry import Polygon
from sqlalchemy import text


def create_map(longitude, latitude):

    engine = create_engine('postgresql+psycopg2://postgres:aseemaseem@localhost:5432/geodatabase_sample')
    con = engine.connect()

    bus_stop_path = "data/sb_bus_stops/bus_stop_point.shp"
    bus_stop_df = gpd.read_file(bus_stop_path)
    parking_path = "data/sb_parking/parking_polygon.shp"
    parking_df = gpd.read_file(parking_path)
    
    your_location = (longitude, latitude)

    query = text("""SELECT ST_AsText(ST_GeomFromWKB(decode(geometry, 'hex'))) FROM busstops
    WHERE ST_DWithin(geometry::geography, ST_MakePoint(:lon, :lat),500);""")

    params = {"lon": your_location[0], "lat": your_location[1]}
    query = query.bindparams(**params)

    r = con.execute(query)
    re = r.mappings().all()

    lst = []
    for i in range(0,len(re)):
        lst.append(re[i]['st_astext'])


    # List of points
    points = [(float(point.split()[0][6:]), float(point.split()[1][:-1])) for point in lst]

    # Create a map centered around the first point
    m = folium.Map(location=[points[0][1], points[0][0]], zoom_start=15)

    # Add markers for each point
    for point in points:
        folium.Marker(location=[point[1], point[0]], icon=folium.Icon(color = 'orange')).add_to(m)

    folium.Marker(location=[your_location[1], your_location[0]], popup='You are here',
                  icon=folium.Icon(color='red', icon='info-sign')).add_to(m)

    query = text("""SELECT ST_AsText(ST_GeomFromWKB(decode(geometry, 'hex'))) FROM parking
    WHERE ST_DWithin(geometry::geography, ST_MakePoint(:lon, :lat),500);""")

    params = {"lon": your_location[0], "lat": your_location[1]}
    query = query.bindparams(**params)

    r = con.execute(query)
    re = r.mappings().all()

    lst = []
    for i in range(0,len(re)):
        lst.append(re[i]['st_astext'])

    for polygon_str in lst:
        # Remove 'POLYGON((' and '))' from the string and split coordinates
        coordinates = polygon_str.replace('POLYGON((', '').replace('))', '').split(',')

        # Extract longitude and latitude from each coordinate pair
        polygon_coords = [[float(coord.split()[0]), float(coord.split()[1])] for coord in coordinates]

        # Create a Polygon object using Shapely
        polygon = Polygon(polygon_coords)

        # Add the polygon to the Folium map
        folium.GeoJson(polygon.__geo_interface__).add_to(m)

    # Display the map
    return m

