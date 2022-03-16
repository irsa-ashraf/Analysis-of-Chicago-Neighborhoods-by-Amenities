
import os
from dash import Dash, html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, Output, Input
from dash_extensions.javascript import arrow_function, assign
import starbucks
import geopandas as gpd
import pandas as pd
import json

import map_util as mu
import starbucks

# import settings

from dash.dependencies import Output, Input

lib, pharm, murals = mu.geo_df()
sbucks = starbucks.starbucks_df()

# get choropleth data for income and demographics
income_choro, demo_choro, colors = mu.choropleth_data()
# customize colors for income data
bin_inc, colorscale_inc, bin_demo, colorscale_demo = colors
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

# create colorbars
ctg_demo = ["{:.1f}+".format(cls, bin_demo[i + 1]) for i, cls in
                        enumerate(bin_demo[:-1])] + ["{:.1f}+".format(bin_demo[-1])]
colorbar_demo = dlx.categorical_colorbar(categories=ctg_demo,
                                colorscale=colorscale_demo,
                                className = "Share of Black residents",
                                width = 300, height = 30, position = "bottomleft")
ctg_inc = ["{:.1f}+".format(cls, bin_inc[i + 1]) for i, cls in enumerate(bin_inc[:-1])] + ["{:.1f}+".format(bin_inc[-1])]
colorbar_inc = dlx.categorical_colorbar(categories=ctg_inc, colorscale=colorscale_inc,
                                className = "Per capita income in 1K$",
                                width = 300, height = 30, position = "bottomleft")
# Geojson rendering logic, must be JavaScript as it is executed in clientside.
style_handle = assign("""function(feature, context){
    const {classes, colorscale, style, colorProp} = context.props.hideout;  // get props from hideout
    const value = feature.properties[colorProp];  // get value the determines the color
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = colorscale[i];  // set the fill color according to the class
        }
    }
    return style;
}""")

# Create geojson for each choropleth
choro_income = dl.GeoJSON(data = json.loads(income_choro.to_json()),  # url to geojson file
                     options=dict(style=style_handle),  # how to style each polygon
                     zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                     hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),  # style applied on hover
                     hideout=dict(colorscale=colorscale_inc, classes=bin_inc, style=style, colorProp="income_per_1000"),
                     id="choro_income")
choro_demo = dl.GeoJSON(data = json.loads(demo_choro.to_json()),  # url to geojson file
                     options=dict(style=style_handle),  # how to style each polygon
                     zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                     hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),  # style applied on hover
                     hideout=dict(colorscale=colorscale_demo, classes=bin_demo, style=style, colorProp="share_BLACK"),
                     id="choro_demo")

# create info panel function
def get_info(si=None):
    header = [html.H4("Amenities in Chicago Community Areas Within 15 Minutes Walking Distance")]
    if not si:
        return header + [html.P("Click anywhere in Chicago to calculate"\
                        "the density and diversity of amenities within walking"\
                        "distance of the selected coordinates")]
    return header + [html.B("Shannon Index Score: {:.4f}".format(si)) , html.Br(),
                    "A score above 0.0273 indicates that "\
                    "there is at least one amenity from each category, or several from few.",
                    html.Sup("2")]

# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "left": "10px", "z-index": "1000"})


# Create app.
app = Dash()
app.layout = html.Div(dl.Map([
        dl.LayersControl([
            dl.Overlay(
                dl.LayerGroup([choro_income]), name='Income in 1K per capita', checked=True),
            dl.Overlay(
                dl.LayerGroup([choro_demo]), name='Share of Black residents', checked=True),                
        ]), 
        # add another layers control here
        dl.TileLayer(), colorbar_inc, colorbar_demo, info # add info at the end
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map")
)

# add mouse click feature
@app.callback(Output("info", "children"), [Input("map", "click_lat_lng")])
def info_click(click_lat_lng):
    si = mu.compute_shannon_index(click_lat_lng, lib, pharm, murals, sbucks)
    return get_info(si)

if __name__ == '__main__':
    app.run_server()