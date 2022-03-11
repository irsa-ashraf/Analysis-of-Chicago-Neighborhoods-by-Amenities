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

def geo_df():
    pd_dfs = append_pandas()
    rv_lst = []

    for df in pd_dfs:
        gdf = convert_to_gdf(df)
        rv_lst.append(gdf)
    cafe_df = go()
    gdf = convert_to_gdf(cafe_df)
    rv_lst.append(gdf)

    return rv_lst

def convert_to_gdf(df):
    gdf = gpd.GeoDataFrame(df,
                geometry=gpd.points_from_xy(df['latitude'], df['longitude']))
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
        score += -(prop * math.log(prop))
    
    return score