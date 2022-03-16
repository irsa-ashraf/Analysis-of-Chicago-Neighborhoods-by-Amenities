from dash import Dash, html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, Output, Input
from dash_extensions.javascript import arrow_function, assign
import geopandas as gpd
import pandas as pd
import json
import cdp
import sys
import map_util as mu
import starbucks

from demographics import import_income, import_demographics
from dash.dependencies import Output, Input

# Get data
lib_dict, pharm_dict, mur_dict, cafe_dicts = cdp.get_data_dicts()


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


# Create geojsons for chloropleth
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


# Create geojsons for amenities
geojson_starb = dlx.dicts_to_geojson(cafe_dicts)
geojson_libs = dlx.dicts_to_geojson(lib_dict)
geojson_pharms = dlx.dicts_to_geojson(pharm_dict)
geojson_murals = dlx.dicts_to_geojson(mur_dict)


# Generate icons
# Credit to Github user pointhi for their icon images
draw_point = assign("""function(feature, latlng){
const point = L.icon({iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${feature.properties.color}.png`, iconSize: [20, 24]});
return L.marker(latlng, {icon: point});
}""")


# Create app.
app = Dash()
app.layout = html.Div(children=[
    html.H1(children="Chicago Amenities"),
    dl.Map(
        [
            dl.LayersControl(
                [
                    dl.Overlay(
                        dl.LayerGroup([choro_income]), name='Community Area, Income', checked=True),
                    dl.Overlay(
                        dl.LayerGroup([choro_demo]), name='Share of Black residents', checked=True),  
                    dl.Overlay(
                        dl.LayerGroup(children=[
                            dl.TileLayer(),
                            dl.GeoJSON(data=geojson_starb,
                            cluster=True,
                            options=dict(pointToLayer=draw_point),
                            zoomToBounds=True)]), name='starbucks', checked=True),
                    dl.Overlay(
                        dl.LayerGroup(children=[
                            dl.TileLayer(),
                            dl.GeoJSON(data=geojson_pharms,
                            cluster=True,
                            options=dict(pointToLayer=draw_point),
                            zoomToBounds=True)]), name='pharmacies', checked=True),
                    dl.Overlay(
                        dl.LayerGroup(children=[
                            dl.TileLayer(),
                            dl.GeoJSON(data=geojson_murals,
                            cluster=True,
                            options=dict(pointToLayer=draw_point),
                            zoomToBounds=True)]), name='murals', checked=True),
                    dl.Overlay(
                        dl.LayerGroup(children=[
                            dl.TileLayer(),
                            dl.GeoJSON(data=geojson_libs,
                            cluster=True,
                            options=dict(pointToLayer=draw_point),
                            zoomToBounds=True)]), name='libraries', checked=True)]),
                    dl.TileLayer(), colorbar_inc, colorbar_demo
                ],
        zoom=10,
        center=(41.8781, -87.5298),
    )],
    style={
        'width': '98%', 'height': '95vh', 'margin': "auto", "display": "block",
    }, id='map'
)


@app.callback(Output("info", "children"), [Input("geojson", "hover_feature")])
def info_hover(feature):
    return get_info(feature)


if __name__ == '__main__':
    app.run_server()

