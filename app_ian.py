
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

from demographics import import_income, import_demographics

# import settings

from dash.dependencies import Output, Input

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
# Create colorbar.
ctg = ["{}+".format(cls, classes[i + 1]) for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
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
# Create geojson.
geojson = dl.GeoJSON(data = json.loads(choro_boundaries.to_json()),  # url to geojson file
                     options=dict(style=style_handle),  # how to style each polygon
                     zoomToBounds=True,  # when true, zooms to bounds when data changes (e.g. on load)
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. polygon) on click
                     hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),  # style applied on hover
                     hideout=dict(colorscale=colorscale, classes=classes, style=style, colorProp="income_per_1000"),
                     id="geojson")
# Create info control.
#info = html.Div(children=get_info(), id="info", className="info",
#                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})
# Create app.
app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div([dl.Map(children=[dl.TileLayer(), geojson, colorbar])],
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map")


@app.callback(Output("info", "children"), [Input("geojson", "hover_feature")])
def info_hover(feature):
    return get_info(feature)

if __name__ == '__main__':
    app.run_server()