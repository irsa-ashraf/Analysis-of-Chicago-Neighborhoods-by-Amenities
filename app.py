from dash import Dash, html
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, Output, Input
from dash_extensions.javascript import arrow_function, assign
import geopandas as gpd
import pandas as pd
import json
import cdp

from demographics import import_income, import_demographics
from dash.dependencies import Output, Input

# Get data
lib_dict, pharm_dict, mur_dict, cafe_dicts = cdp.get_data_dicts()

def cap(st):
    return st.title()

income = import_income()
income = income.loc[:,['neighbor', 'income_per_1000']]
income.columns = ['community','income_per_1000']

geojson_file = 'data/Boundaries - Community Areas (current).geojson'
comm_boundaries = gpd.read_file(geojson_file)
comm_boundaries['community'] = comm_boundaries.apply(lambda x: cap(x.community), axis = 1)
choro_boundaries = pd.merge(comm_boundaries, income, on='community', how='left')

classes = list(income['income_per_1000'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

# Create colorbar
ctg = ["{:.1f}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{:.1f}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")

# Geojson rendering
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

# Create geojson for chloropleth
geojson2 = dl.GeoJSON(data = json.loads(choro_boundaries.to_json()),
                     options=dict(style=style_handle),
                     zoomToBounds=True,
                     zoomToBoundsOnClick=True,
                     hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')), 
                     hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="income_per_1000"),
                     id="geojson")


# Create geojsons
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
                        dl.LayerGroup([geojson2]), name='community area, income', checked=True),
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
                    dl.TileLayer(), colorbar
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

