
from dash import Dash, html
import dash_leaflet as dl
import dash_leaflet.express as dlx
import starbucks


cafe_dicts = starbucks.go()

app = Dash()
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        dl.GeoJSON(data=dlx.dicts_to_geojson(cafe_dicts), cluster=True),
        dl.GeoJSON(url='assets/leaflet_50k.pbf', format="geobuf", cluster=True, id="sc", zoomToBoundsOnClick=True,
                   superClusterOptions={"radius": 100}),
    ], center=(41.8781, -87.5298), zoom=10, style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
])


if __name__ == '__main__':
    app.run_server(debug=True)

