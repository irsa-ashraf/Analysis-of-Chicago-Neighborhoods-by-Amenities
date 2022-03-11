import geopandas as gpd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import pandas as pd

import map_util

# initiliaze icon features for mapping

def make_map_and_plot(geojson):
    map = initialize_map(geojson)
    
    dfs = map.util.geo_df() 
    starbucks = dfs[1] # replace with a real function
    
    keys = ['library', 'pharmacy', 'murals']

    for i, df in enumerate(dfs):
        cluster_points(df, keys[i])
    cluster_points(starbucks, 'starbucks')

    return map

    folium.LayerControl().add_to(map)

def initialize_map(geojson):
    geojson_df = gpd.read_file(geojson)
    map = folium.Map(location = [41.8781, -87.5298], zoom_start=10)
    folium.GeoJson(geojson_df).add_to(map)
    return map

def cluster_points(df, key):

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