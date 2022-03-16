import os
import geopandas as gpd
import folium
from folium import plugins
import matplotlib.pyplot as plt
import pandas as pd
import math

from geopy import distance
from cdp import append_pandas
from starbucks import go

COLOR_LIST = ['blue', 'red', 'violet']

def geo_df(lst):
    pd_dfs = append_pandas()
    rv_lst = []

    for i, df in enumerate(pd_dfs):
        gdf = convert_to_gdf(df, COLOR_LIST[i])
        rv_lst.append(gdf)
    #cafe_df = go()
    #gdf = convert_to_gdf(cafe_df)
    #rv_lst.append(gdf)

    return rv_lst

def convert_to_gdf(df, color):
    gdf = gpd.GeoDataFrame(df,
                geometry=gpd.points_from_xy(df['lat'], df['lon']))
    gdf['tooltips'] = gdf['name'] + '({})'.format(gdf['type'])
    gdf['color'] = color
    gdf = gdf.set_crs('EPSG:26916')
    return gdf

def distance_series(df, point):
    lat, long = point
    dist_series = df.apply(lambda x: distance.distance(
                        (x.latitude, x.longitude),
                        (lat, long)).miles, axis=1)
    return dist_series

def within_distance(point, library, pharmacy, starbucks, murals, walk_dist = 1):
    lib_dist = distance_series(library, point)
    pharm_dist = distance_series(pharmacy, point)
    sbucks_dist = distance_series(starbucks, point)
    murals_dist = distance_series(murals, point)
    
    lib_dist = lib_dist[lib_dist <= 1]
    pharm_dist = pharm_dist[pharm_dist <= 1]
    sbucks_dist = sbucks_dist[sbucks_dist <= 1]
    murals_dist = murals_dist[murals_dist <= 1]
    
    return lib_dist, pharm_dist, sbucks_dist, murals_dist

def compute_shannon_index(pt, lib, pharm, sbucks, murals):
    total = lib.shape[0] + pharm.shape[0] + sbucks.shape[0] + murals.shape[0]
    
    within_dist = within_distance(pt, lib, pharm, sbucks, murals)
    
    score = 0
    
    for amen in within_dist:
        prop = amen.shape[0]/total
        if prop == 0:
            continue
        score += -(prop * math.log(prop))
    if score == 0:
        return 'no amenities in the area'
    return score

def prepare_chlorpleth(df, column, description):
    bins = df[arg].quantile([0, 0.2, 0.4, 0.6, 0.8, 1])
    folium.Choropleth(
        geo_data=pdf,
        data=demo,
        columns=["GEOG", "BLACK"],
        key_on="feature.properties.pri_neigh",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name="% Black residents",
        name='demographic info',
        bins=demo_bins,
        reset=True,
    ).add_to(map)
    pass