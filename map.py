import geopandas as gpd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import pandas as pd

import map_util
import starbucks


def make_map_and_plot(geojson):
    map = initialize_map(geojson)
    
    print('are we getting here...?')

    dfs = map_util.geo_df() 
    
    keys = ['library', 'pharmacy', 'murals', 'starbucks']

    print('did we get here?')
    for i, df in enumerate(dfs):
        cluster_points(df, keys[i], map)

    folium.LayerControl().add_to(map)
    map.save('map.html')
    print('saved!')

def initialize_map(geojson):
    geojson_df = gpd.read_file(geojson)
    map = folium.Map(location = [41.8781, -87.5298], zoom_start=10)
    folium.GeoJson(geojson_df).add_to(map)
    return map

def cluster_points(df, key, map):

    color = {'pharmacy': 'red', 'library': 'blue',
            'starbucks': 'green', 'murals':'purple'}

    icon = {'pharmacy': 'heart', 'library': 'book',
            'starbucks': 'star', 'murals':'cloud'}

    cluster = plugins.MarkerCluster(name=key).add_to(map)
    for row in df.itertuples():
        folium.Marker(
        location = (row.latitude, row.longitude),
        popup = row.name,
        icon=folium.Icon(color=color[key], icon=icon[key])
        ).add_to(cluster)

if __name__ == '__main__':
    geojson_file = 'data/Boundaries - Neighborhoods.geojson'
    make_map_and_plot(geojson_file)